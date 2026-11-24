#!/usr/bin/env python3
"""Analyze ELF sections, per-object code/rodata breakdown, and instruction width mix (16-bit vs 32-bit)
for Arm Cortex-M3 (Thumb-2) and XuanTie E902 (RV32EMC) CoreMark binaries.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path


COREMARK_FUNCS = {
    "iterate",
    "core_list_find",
    "core_list_reverse",
    "core_list_remove",
    "core_list_undo_remove",
    "core_list_insert_new",
    "core_list_mergesort",
    "core_bench_list",
    "core_list_init",
    "core_bench_matrix",
    "core_init_matrix",
    "matrix_test",
    "matrix_sum",
    "matrix_mul_const",
    "matrix_mul_vect",
    "matrix_mul_matrix",
    "matrix_mul_matrix_bitextract",
    "matrix_add_const",
    "core_bench_state",
    "core_init_state",
    "core_state_transition",
    "crcu8",
    "crc16",
    "crcu16",
    "crcu32",
    "calc_func",
    "check_data_types",
    "cmp_complex",
    "cmp_idx",
    "ee_isdigit",
    "main",
}

COREMARK_OBJS = [
    "core_main.o",
    "core_list_join.o",
    "core_matrix.o",
    "core_state.o",
    "core_util.o",
]

ALL_OBJS = COREMARK_OBJS + [
    "core_portme.o",
    "ee_printf.o",
    "cvt.o",
    "startup.o",
    "crt0.o",
    "mem_stubs.o",
]


def run_cmd(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, errors="replace")


def parse_sections(readelf_bin: str, elf_path: Path, alloc_only: bool = True) -> dict:
    out = run_cmd([readelf_bin, "-S", "-W", str(elf_path)])
    sections = {}
    pat = re.compile(
        r"^\s*\[\s*\d+\]\s+(\S+)\s+(\S+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+\S+\s+(\S*)"
    )
    for line in out.splitlines():
        m = pat.match(line)
        if not m:
            continue
        name, stype, addr, off, size_hex, flags = m.groups()
        if alloc_only and "A" not in flags:
            continue
        sections[name] = {
            "type": stype,
            "addr": int(addr, 16),
            "size": int(size_hex, 16),
            "flags": flags,
        }
    return sections


def parse_object_breakdown(readelf_bin: str, obj_path: Path) -> dict:
    secs = parse_sections(readelf_bin, obj_path, alloc_only=True)
    text_b = 0
    rodata_b = 0
    data_b = 0
    bss_b = 0
    for name, info in secs.items():
        sz = info["size"]
        if sz == 0:
            continue
        if info["type"] == "NOBITS":
            bss_b += sz
        elif name.startswith(".text"):
            text_b += sz
        elif name.startswith(".rodata") or name.startswith(".srodata"):
            rodata_b += sz
        elif name.startswith(".data") or name.startswith(".sdata"):
            data_b += sz
        elif "X" in info["flags"]:
            text_b += sz
        elif "W" in info["flags"]:
            data_b += sz
        else:
            rodata_b += sz
    return {"text": text_b, "rodata": rodata_b, "data": data_b, "bss": bss_b}


def parse_size_summary(size_bin: str, elf_path: Path) -> dict:
    out = run_cmd([size_bin, str(elf_path)])
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if len(lines) >= 2:
        parts = lines[1].split()
        if len(parts) >= 4:
            return {
                "text": int(parts[0]),
                "data": int(parts[1]),
                "bss": int(parts[2]),
                "dec": int(parts[3]),
            }
    return {}


def parse_disassembly(objdump_bin: str, elf_path: Path, arch: str) -> dict:
    args = [objdump_bin, "-d", str(elf_path)]
    if arch == "e902":
        args = [objdump_bin, "-d", "-Mnumeric", str(elf_path)]
    out = run_cmd(args)

    func_pat = re.compile(r"^[0-9a-fA-F]+\s+<([^>]+)>:\s*$")
    arm_insn_pat = re.compile(r"^\s*[0-9a-fA-F]+:\s+([0-9a-fA-F]{4})(?:\s+([0-9a-fA-F]{4}))?\s+(.+)$")
    arm_word_pat = re.compile(r"^\s*[0-9a-fA-F]+:\s+([0-9a-fA-F]{2,8})\s+(\.\S+.*)$")
    rv_insn_pat = re.compile(r"^\s*[0-9a-fA-F]+:\s+([0-9a-fA-F]{4,8})\s+(.+)$")

    total = {"16b": 0, "32b": 0, "bytes": 0, "literal_items": 0, "literal_bytes": 0}
    core = {"16b": 0, "32b": 0, "bytes": 0}
    per_func = {}

    cur_func = None
    for line in out.splitlines():
        fm = func_pat.match(line)
        if fm:
            cur_func = fm.group(1)
            per_func.setdefault(cur_func, {"16b": 0, "32b": 0, "bytes": 0})
            continue

        if arch == "m3":
            wm = arm_word_pat.match(line)
            if wm:
                hexw, _ = wm.groups()
                total["literal_items"] += 1
                total["literal_bytes"] += len(hexw) // 2
                continue
            im = arm_insn_pat.match(line)
            if not im:
                continue
            w1, w2, asm = im.groups()
            if asm.strip().startswith("."):
                total["literal_items"] += 1
                total["literal_bytes"] += 4 if w2 else 2
                continue
            width = 4 if w2 is not None else 2
        else:
            im = rv_insn_pat.match(line)
            if not im:
                continue
            hexword, asm = im.groups()
            if asm.strip().startswith("."):
                total["literal_items"] += 1
                total["literal_bytes"] += len(hexword) // 2
                continue
            width = 4 if len(hexword) == 8 else 2

        key = "32b" if width == 4 else "16b"
        total[key] += 1
        total["bytes"] += width
        if cur_func is not None:
            per_func[cur_func][key] += 1
            per_func[cur_func]["bytes"] += width
            base_func = cur_func.split(".")[0]
            if base_func in COREMARK_FUNCS:
                core[key] += 1
                core["bytes"] += width

    def finalize(d: dict) -> dict:
        cnt = d["16b"] + d["32b"]
        out_d = dict(d)
        out_d["total_insns"] = cnt
        out_d["pct_16b"] = round((100.0 * d["16b"] / cnt), 2) if cnt else 0.0
        out_d["avg_insn_bytes"] = round((d["bytes"] / cnt), 3) if cnt else 0.0
        return out_d

    return {
        "total": finalize(total),
        "coremark_funcs": finalize(core),
        "functions": {
            k: finalize(v)
            for k, v in sorted(per_func.items())
            if v["16b"] + v["32b"] > 0
        },
    }


def analyze_case(name: str, arch: str, elf_path: Path) -> dict:
    prefix = "arm-none-eabi" if arch == "m3" else "riscv64-unknown-elf"
    build_dir = elf_path.parent
    size_summary = parse_size_summary(f"{prefix}-size", elf_path)
    sections = parse_sections(f"{prefix}-readelf", elf_path)
    disasm = parse_disassembly(f"{prefix}-objdump", elf_path, arch)

    objects = {}
    core_sum = {"text": 0, "rodata": 0, "data": 0, "bss": 0}
    for obj_name in ALL_OBJS:
        op = build_dir / obj_name
        if op.exists():
            bd = parse_object_breakdown(f"{prefix}-readelf", op)
            objects[obj_name] = bd
            if obj_name in COREMARK_OBJS:
                for k in core_sum:
                    core_sum[k] += bd[k]

    return {
        "name": name,
        "arch": arch,
        "elf": str(elf_path),
        "size": size_summary,
        "core_objects_sum": core_sum,
        "objects": objects,
        "sections": sections,
        "disasm": disasm,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-root", default="/work/benchmark", help="Benchmark root containing m3/ and e902/")
    parser.add_argument("--out", required=True, help="Output JSON path")
    args = parser.parse_args()

    root = Path(args.work_root)
    cases = [
        ("m3_O2", "m3", root / "m3/build_O2_ic1/coremark_m3.elf"),
        ("m3_O3", "m3", root / "m3/build_O3_ic1/coremark_m3.elf"),
        ("m3_O3_unroll", "m3", root / "m3/build_O3_unroll_ic1/coremark_m3.elf"),
        ("m3_Os", "m3", root / "m3/build_Os_ic1/coremark_m3.elf"),
        ("e902_O2", "e902", root / "e902/build_O2_it1/coremark_e902.elf"),
        ("e902_O3", "e902", root / "e902/build_O3_it1/coremark_e902.elf"),
        ("e902_O3_unroll", "e902", root / "e902/build_O3_unroll_it1/coremark_e902.elf"),
        ("e902_Os", "e902", root / "e902/build_Os_it1/coremark_e902.elf"),
    ]

    results = []
    for name, arch, elf in cases:
        if elf.exists():
            results.append(analyze_case(name, arch, elf))
        else:
            results.append({"name": name, "arch": arch, "elf": str(elf), "missing": True})

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))
    print(f"Wrote {len(results)} case analyses to {out_path}")


if __name__ == "__main__":
    main()
