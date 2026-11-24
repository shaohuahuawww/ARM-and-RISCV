#!/usr/bin/env python3
"""Generate 4 IEEE / NeurIPS / Nature publication-grade pure-SVG figures for the Midterm Report."""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Unified IEEE / NeurIPS / Nature Editorial Visual System
# ---------------------------------------------------------------------------
PALETTE = {
    "m3": "#2E5B88",          # Deep editorial slate blue (Arm Cortex-M3)
    "m3_light": "#6C9AC4",    # Soft steel blue (16b / secondary)
    "m3_pale": "#DCE8F5",     # Tint
    "m3_dark": "#1B3B5A",
    "e9": "#C95B3B",          # Muted terracotta / vermilion (XuanTie E902)
    "e9_light": "#E5987E",    # Soft coral (2-iter / secondary)
    "e9_pale": "#F9E6DF",     # Tint
    "e9_dark": "#8A341C",
    "teal": "#2A8C82",        # Muted teal
    "indigo": "#5C4D9A",      # Royal muted indigo
    "ochre": "#C99738",       # Warm ochre
    "crimson": "#B8334A",     # Deep editorial crimson
    "slate": "#1E293B",       # Primary text
    "muted": "#475569",       # Secondary text
    "spine": "#334155",       # Axis spine
    "grid": "#E2E8F0",        # Hairline grid
    "bg_panel": "#FAFBFD",    # Ultra-subtle panel tint
}


def setup_pub_rc():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Hiragino Sans GB", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "svg.fonttype": "path",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": PALETTE["bg_panel"],
        "axes.edgecolor": PALETTE["spine"],
        "axes.linewidth": 0.85,
        "axes.labelcolor": PALETTE["slate"],
        "xtick.color": PALETTE["slate"],
        "ytick.color": PALETTE["slate"],
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.7,
        "grid.linestyle": "--",
        "legend.frameon": False,
    })


def add_panel_header(ax, letter: str, title: str, y_offset: float = 1.04):
    """Nature / NeurIPS / IEEE MICRO style top-left bold letter + clean subtitle."""
    ax.text(
        0.0, y_offset, f"({letter})", transform=ax.transAxes,
        fontsize=10.5, fontweight="bold", color=PALETTE["slate"], va="bottom", ha="left",
    )
    ax.text(
        0.068, y_offset, title, transform=ax.transAxes,
        fontsize=10.2, fontweight="bold", color=PALETTE["slate"], va="bottom", ha="left",
    )


def _make_reg_strip(x0: float, y0: float, slot_w: float, slot_h: float, gap: float, colors: list, labels: list, txt_colors: list) -> str:
    """Render a crisp 16-register hardware file strip in pure SVG."""
    out = []
    for i in range(16):
        rx = x0 + i * (slot_w + gap)
        out.append(f'<rect x="{rx:.1f}" y="{y0:.1f}" width="{slot_w:.1f}" height="{slot_h:.1f}" rx="2" fill="{colors[i]}" stroke="#FFFFFF" stroke-width="0.6"/>')
        out.append(f'<text x="{rx + slot_w/2:.1f}" y="{y0 + slot_h/2 + 3:.1f}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="6.8" font-weight="700" fill="{txt_colors[i]}">{labels[i]}</text>')
    return "\n  ".join(out)


def _make_clk_wave(x0: float, y_hi: float, y_lo: float, cycles: int, step: float) -> str:
    """Render crisp digital clock square wave path."""
    pts = [f"M {x0:.1f} {y_lo:.1f}"]
    x = x0
    for _ in range(cycles):
        pts.append(f"L {x:.1f} {y_hi:.1f} L {x + step/2:.1f} {y_hi:.1f} L {x + step/2:.1f} {y_lo:.1f} L {x + step:.1f} {y_lo:.1f}")
        x += step
    return " ".join(pts)


def write_fig1_system_framework():
    """ISCA / IEEE MICRO / NeurIPS Hero Architecture Figure (4-stage L->R with embedded hardware micro-diagrams)."""
    # Build 16-register strips for Cortex-M3 (r4-r11 = 8 callee-saved) vs E902 ilp32e (x8-x9 = 2 callee-saved)
    m3_cols = (["#CBD5E1"]*4) + (["#2E5B88"]*8) + (["#94A3B8"]*4)
    m3_lbls = [f"r{i}" for i in range(12)] + ["ip", "sp", "lr", "pc"]
    m3_tcol = (["#334155"]*4) + (["#FFFFFF"]*8) + (["#FFFFFF"]*4)
    m3_reg_svg = _make_reg_strip(258, 179, 15.6, 17, 1.2, m3_cols, m3_lbls, m3_tcol)

    e9_cols = (["#E2E8F0"]*5) + (["#CBD5E1"]*3) + (["#C95B3B"]*2) + (["#E8A38C"]*6)
    e9_lbls = [f"x{i}" for i in range(16)]
    e9_tcol = (["#64748B"]*5) + (["#334155"]*3) + (["#FFFFFF"]*2) + (["#5A2010"]*6)
    e9_reg_svg = _make_reg_strip(258, 405, 15.6, 17, 1.2, e9_cols, e9_lbls, e9_tcol)

    clk_path = _make_clk_wave(622, 338, 350, 14, 13.5)

    # Discrete retire pulses inside active window (x=642..792)
    retire_pulses = []
    for px in [649, 662.5, 676, 703, 716.5, 730, 757, 770.5, 784]:
        retire_pulses.append(f'<path d="M {px:.1f} 404 L {px:.1f} 391 L {px+5.2:.1f} 391 L {px+5.2:.1f} 404" fill="#FDE68A" stroke="#B45309" stroke-width="1.05"/>')
    retire_svg = "\n  ".join(retire_pulses)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 524" width="1080" height="524">
  <defs>
    <filter id="sh" x="-2%" y="-2%" width="104%" height="106%">
      <feDropShadow dx="0" dy="1.0" stdDeviation="1.2" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
    <linearGradient id="gSlate" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E293B"/><stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="gBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2E5B88"/><stop offset="100%" stop-color="#1D4063"/>
    </linearGradient>
    <linearGradient id="gTerra" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C95B3B"/><stop offset="100%" stop-color="#9A3B20"/>
    </linearGradient>
    <linearGradient id="gTeal" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2A8C82"/><stop offset="100%" stop-color="#1B665F"/>
    </linearGradient>
    <marker id="arrDark" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#475569"/>
    </marker>
    <marker id="arrBlue" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2E5B88"/>
    </marker>
    <marker id="arrTerra" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#C95B3B"/>
    </marker>
    <marker id="arrBlueM" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2E5B88"/>
    </marker>
    <marker id="arrTerraM" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#C95B3B"/>
    </marker>
    <marker id="arrMiniB" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="5.5" markerHeight="5.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2E5B88"/>
    </marker>
    <style>
      .st-h  {{ font-family: "Hiragino Sans GB", "Heiti SC", "Helvetica Neue", sans-serif; font-weight: 700; font-size: 11.2px; fill: #FFFFFF; }}
      .h-zh  {{ font-family: "Hiragino Sans GB", "Heiti SC", "Helvetica Neue", sans-serif; font-weight: 700; fill: #1E293B; }}
      .h-wh  {{ font-family: "Hiragino Sans GB", "Heiti SC", "Helvetica Neue", sans-serif; font-weight: 700; fill: #FFFFFF; }}
      .b-zh  {{ font-family: "Hiragino Sans GB", "Helvetica Neue", sans-serif; fill: #334155; }}
      .sub   {{ font-family: "Hiragino Sans GB", "Helvetica Neue", sans-serif; fill: #64748B; }}
      .mono  {{ font-family: "Menlo", "Helvetica Neue", monospace; font-weight: 700; }}
    </style>
  </defs>

  <rect x="0" y="0" width="1080" height="524" fill="#FFFFFF"/>

  <!-- ==================== TOP 4-STAGE TECHNICAL ARCHITECTURE BAR ==================== -->
  <rect x="14"  y="12" width="206" height="30" rx="4" fill="url(#gSlate)"/>
  <text x="117" y="31" text-anchor="middle" class="st-h">① 同源受控基准输入</text>
  <line x1="223" y1="27" x2="237.5" y2="27" stroke="#64748B" stroke-width="1.6" marker-end="url(#arrDark)"/>

  <rect x="245" y="12" width="295" height="30" rx="4" fill="url(#gSlate)"/>
  <text x="392.5" y="31" text-anchor="middle" class="st-h">② 双架构流水线与寄存器微架构</text>
  <line x1="543" y1="27" x2="557.5" y2="27" stroke="#64748B" stroke-width="1.6" marker-end="url(#arrDark)"/>

  <rect x="565" y="12" width="265" height="30" rx="4" fill="url(#gSlate)"/>
  <text x="697.5" y="31" text-anchor="middle" class="st-h">③ 异构协同观测与波形互验</text>
  <line x1="833" y1="27" x2="847.5" y2="27" stroke="#64748B" stroke-width="1.6" marker-end="url(#arrDark)"/>

  <rect x="855" y="12" width="211" height="30" rx="4" fill="url(#gTeal)"/>
  <text x="960.5" y="31" text-anchor="middle" class="st-h">④ 三粒度归因与协同优化</text>

  <!-- ==================== STAGE 1: CONTROLLED BENCHMARK INPUT ==================== -->
  <g filter="url(#sh)">
    <rect x="14" y="54" width="206" height="456" rx="4" fill="#FAFBFD" stroke="#CBD5E1" stroke-width="1.15"/>
  </g>

  <!-- 1A: CoreMark v1.0 5 Source Modules & Microarchitectural Stress Table -->
  <text x="117" y="74" text-anchor="middle" class="h-zh" font-size="10.4">CoreMark v1.0 基准源码</text>

  <rect x="24" y="83" width="186" height="30" rx="2.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="0.9"/>
  <rect x="24" y="83" width="3.2" height="30" rx="1" fill="#2E5B88"/>
  <text x="34" y="95.5" class="mono" font-size="8.3" fill="#1D4063">core_list_join.c</text>
  <text x="34" y="107.5" class="sub" font-size="7.9">链表查找/归并 · 指针追逐与分支</text>

  <rect x="24" y="117" width="186" height="30" rx="2.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="0.9"/>
  <rect x="24" y="117" width="3.2" height="30" rx="1" fill="#2E5B88"/>
  <text x="34" y="129.5" class="mono" font-size="8.3" fill="#1D4063">core_matrix.c</text>
  <text x="34" y="141.5" class="sub" font-size="7.9">整数矩阵乘加 · 乘加与步进访存</text>

  <rect x="24" y="151" width="186" height="30" rx="2.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="0.9"/>
  <rect x="24" y="151" width="3.2" height="30" rx="1" fill="#2A8C82"/>
  <text x="34" y="163.5" class="mono" font-size="8.3" fill="#175B54">core_state.c</text>
  <text x="34" y="175.5" class="sub" font-size="7.9">有限状态机 · 多路跳转控制流</text>

  <rect x="24" y="185" width="186" height="30" rx="2.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="0.9"/>
  <rect x="24" y="185" width="3.2" height="30" rx="1" fill="#C95B3B"/>
  <text x="34" y="197.5" class="mono" font-size="8.3" fill="#8A341C">core_util.c</text>
  <text x="34" y="209.5" class="sub" font-size="7.9">16 位 CRC 校验 · 位移与异或</text>

  <rect x="24" y="219" width="186" height="30" rx="2.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="0.9"/>
  <rect x="24" y="219" width="3.2" height="30" rx="1" fill="#475569"/>
  <text x="34" y="231.5" class="mono" font-size="8.3" fill="#334155">core_main.c</text>
  <text x="34" y="243.5" class="sub" font-size="7.9">迭代驱动 · 四重校验和聚合</text>

  <!-- 1B: 4-Tier Compilation Flag Matrix (Flat Technical Cells, Zero Fake Bars) -->
  <line x1="24" y1="261" x2="210" y2="261" stroke="#E2E8F0" stroke-width="1"/>
  <text x="117" y="278" text-anchor="middle" class="h-zh" font-size="10.4">四档编译优化矩阵</text>

  <rect x="24" y="287" width="58" height="36" rx="3" fill="#F1F6FC" stroke="#B7CFE6" stroke-width="0.9"/>
  <text x="53" y="302" text-anchor="middle" class="mono" font-size="9.2" fill="#1D4063">-Os</text>
  <text x="53" y="315.5" text-anchor="middle" class="sub" font-size="8.0">体积优先</text>

  <rect x="88" y="287" width="58" height="36" rx="3" fill="#E6F0FA" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="117" y="302" text-anchor="middle" class="mono" font-size="9.2" fill="#1D4063">-O2</text>
  <text x="117" y="315.5" text-anchor="middle" class="sub" font-size="8.0">均衡标准</text>

  <rect x="152" y="287" width="58" height="36" rx="3" fill="#DCE8F5" stroke="#6C9AC4" stroke-width="0.9"/>
  <text x="181" y="302" text-anchor="middle" class="mono" font-size="9.2" fill="#1D4063">-O3</text>
  <text x="181" y="315.5" text-anchor="middle" class="sub" font-size="8.0">激进内联</text>

  <rect x="24" y="329" width="186" height="34" rx="3" fill="#FDF3EF" stroke="#D98C73" stroke-width="0.95"/>
  <text x="117" y="343" text-anchor="middle" class="mono" font-size="8.6" fill="#8A341C">-O3 -funroll-loops</text>
  <text x="117" y="356" text-anchor="middle" class="sub" font-size="8.0" fill="#8A341C">激进循环展开</text>

  <!-- 1C: Controlled Experiment Invariants Table -->
  <line x1="24" y1="376" x2="210" y2="376" stroke="#E2E8F0" stroke-width="1"/>
  <text x="117" y="393" text-anchor="middle" class="h-zh" font-size="10.4">受控实验变量约束</text>

  <rect x="24" y="402" width="186" height="96" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.95"/>
  <line x1="24" y1="434" x2="210" y2="434" stroke="#E2E8F0" stroke-width="0.8"/>
  <line x1="24" y1="466" x2="210" y2="466" stroke="#E2E8F0" stroke-width="0.8"/>
  <line x1="78" y1="402" x2="78" y2="498" stroke="#E2E8F0" stroke-width="0.8"/>

  <text x="51" y="421" text-anchor="middle" class="sub" font-size="8.4">编译器</text>
  <text x="144" y="421" text-anchor="middle" class="mono" font-size="8.2" fill="#1E293B">GCC 13.2 (ARM/RV)</text>

  <text x="51" y="453" text-anchor="middle" class="sub" font-size="8.4">数制/栈</text>
  <text x="144" y="453" text-anchor="middle" class="mono" font-size="8.0" fill="#1E293B">FLOAT=0 · STACK</text>

  <text x="51" y="485" text-anchor="middle" class="sub" font-size="8.4">数据集</text>
  <text x="144" y="485" text-anchor="middle" class="b-zh" font-size="8.4" fill="#1E293B">性能 / 验证双种子</text>

  <!-- ==================== FAN-OUT ORTHOGONAL BUS CONNECTORS (Stage 1 -> Stage 2) ==================== -->
  <path d="M 220 272 L 223.5 272 Q 228 272, 228 267.5 L 228 168.5 Q 228 164, 232.5 164 L 238 164" fill="none" stroke="#2E5B88" stroke-width="1.8" marker-end="url(#arrBlue)"/>
  <path d="M 220 292 L 223.5 292 Q 228 292, 228 296.5 L 228 393.5 Q 228 398, 232.5 398 L 238 398" fill="none" stroke="#C95B3B" stroke-width="1.8" marker-end="url(#arrTerra)"/>

  <!-- ==================== STAGE 2 TOP: ARM CORTEX-M3 MICROARCHITECTURE ==================== -->
  <g filter="url(#sh)">
    <rect x="245" y="54" width="295" height="218" rx="4" fill="#F6FAFE" stroke="#8FB5D9" stroke-width="1.2"/>
    <rect x="245" y="54" width="295" height="30" rx="4" fill="url(#gBlue)"/>
    <rect x="245" y="76" width="295" height="8" fill="url(#gBlue)"/>
  </g>
  <text x="392.5" y="73.5" text-anchor="middle" class="h-wh" font-size="11.5">Arm Cortex-M3 · ARMv7-M / Thumb-2</text>

  <!-- Drawn 3-Stage Harvard Pipeline -->
  <text x="258" y="100" class="h-zh" font-size="9.6" fill="#1D4063">三级哈佛流水线</text>
  <rect x="258" y="107" width="76" height="28" rx="4.5" fill="#FFFFFF" stroke="#2E5B88" stroke-width="1.15"/>
  <text x="296" y="124.5" text-anchor="middle" class="h-zh" font-size="9.8" fill="#1D4063">IF 取指</text>
  <line x1="334" y1="121" x2="348.2" y2="121" stroke="#2E5B88" stroke-width="1.35" marker-end="url(#arrBlueM)"/>

  <rect x="354" y="107" width="76" height="28" rx="4.5" fill="#FFFFFF" stroke="#2E5B88" stroke-width="1.15"/>
  <text x="392" y="124.5" text-anchor="middle" class="h-zh" font-size="9.8" fill="#1D4063">ID 译码</text>
  <line x1="430" y1="121" x2="444.2" y2="121" stroke="#2E5B88" stroke-width="1.35" marker-end="url(#arrBlueM)"/>

  <rect x="450" y="107" width="76" height="28" rx="4.5" fill="#2E5B88"/>
  <text x="488" y="124.5" text-anchor="middle" class="h-wh" font-size="9.8">EX 执行</text>

  <!-- Dual Harvard Bus Indicators -->
  <rect x="258" y="140" width="128" height="15" rx="3" fill="#DCE8F5"/>
  <text x="322" y="150.5" text-anchor="middle" class="mono" font-size="8" fill="#1D4063">I-Code Bus · 指令总线</text>
  <rect x="394" y="140" width="132" height="15" rx="3" fill="#DCE8F5"/>
  <text x="460" y="150.5" text-anchor="middle" class="mono" font-size="8" fill="#1D4063">D-Code / Sys · 数据总线</text>

  <!-- Drawn 16-Register Heatmap Strip (M3) -->
  <text x="258" y="173" class="h-zh" font-size="9.6" fill="#1D4063">16×32b 通用寄存器文件</text>
  {m3_reg_svg}
  <!-- Bracket under r4-r11 -->
  <path d="M 326 199 L 326 204 L 458 204 L 458 199" fill="none" stroke="#2E5B88" stroke-width="1.1"/>
  <text x="392" y="216" text-anchor="middle" class="h-zh" font-size="8.8" fill="#2E5B88">r4–r11：8 个被调保存寄存器 · 低溢出</text>

  <!-- ISA Feature Chips -->
  <rect x="258" y="227" width="84" height="20" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="300" y="240" text-anchor="middle" class="b-zh" font-size="8.6">后自增 ldrsh</text>
  <rect x="348" y="227" width="84" height="20" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="390" y="240" text-anchor="middle" class="b-zh" font-size="8.6">单指令乘加 mla</text>
  <rect x="438" y="227" width="88" height="20" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="482" y="240" text-anchor="middle" class="b-zh" font-size="8.6">批量 stmdb/ldm</text>
  <text x="392.5" y="263" text-anchor="middle" class="sub" font-size="8.6">ELF32 ARM EABI5 · 16b/32b 高密度混编</text>

  <!-- ==================== STAGE 2 BOTTOM: XUANTIE E902 MICROARCHITECTURE ==================== -->
  <g filter="url(#sh)">
    <rect x="245" y="286" width="295" height="224" rx="4" fill="#FDF7F4" stroke="#E0AC9A" stroke-width="1.2"/>
    <rect x="245" y="286" width="295" height="30" rx="4" fill="url(#gTerra)"/>
    <rect x="245" y="308" width="295" height="8" fill="url(#gTerra)"/>
  </g>
  <text x="392.5" y="305.5" text-anchor="middle" class="h-wh" font-size="11.5">玄铁 E902 · RV32EMC / ilp32e</text>

  <!-- Drawn 2-Stage In-Order Pipeline -->
  <text x="258" y="332" class="h-zh" font-size="9.6" fill="#8A341C">两级顺序流水线</text>
  <rect x="258" y="339" width="90" height="28" rx="4.5" fill="#FFFFFF" stroke="#C95B3B" stroke-width="1.15"/>
  <text x="303" y="356.5" text-anchor="middle" class="h-zh" font-size="9.8" fill="#8A341C">IF 取指</text>
  <line x1="348" y1="353" x2="366.2" y2="353" stroke="#C95B3B" stroke-width="1.35" marker-end="url(#arrTerraM)"/>

  <rect x="372" y="339" width="98" height="28" rx="4.5" fill="#C95B3B"/>
  <text x="421" y="356.5" text-anchor="middle" class="h-wh" font-size="9.8">EX/WB 执行</text>

  <rect x="476" y="341" width="52" height="24" rx="4" fill="#FEF2F2" stroke="#F87171" stroke-width="0.9"/>
  <text x="502" y="356" text-anchor="middle" class="h-zh" font-size="8.2" fill="#B91C1C">无 I-Cache</text>

  <!-- Single AHB-Lite Bus -->
  <rect x="258" y="372" width="270" height="15" rx="3" fill="#F9E6DF"/>
  <text x="393" y="382.5" text-anchor="middle" class="mono" font-size="8" fill="#8A341C">32-bit AMBA3 AHB-Lite Bus · 单总线顺序取指</text>

  <!-- Drawn 16-Register Heatmap Strip (E902 ilp32e) -->
  <text x="258" y="399" class="h-zh" font-size="9.6" fill="#8A341C">16×32b 通用寄存器文件</text>
  {e9_reg_svg}
  <!-- Two Brackets: x8-x9 callee-saved + x8-x15 RVC window -->
  <path d="M 393 425 L 393 430 L 424 430 L 424 425" fill="none" stroke="#B8334A" stroke-width="1.2"/>
  <text x="366" y="441" text-anchor="end" class="h-zh" font-size="8.2" fill="#B8334A">仅 x8, x9 保存</text>
  <line x1="370" y1="438" x2="391" y2="430" stroke="#B8334A" stroke-width="0.8"/>

  <path d="M 393 434 L 393 441 L 525 441 L 525 425" fill="none" stroke="#C95B3B" stroke-width="1.1"/>
  <text x="459" y="452" text-anchor="middle" class="h-zh" font-size="8.4" fill="#8A341C">x8–x15：3 位 RVC 压缩编码域</text>

  <!-- ISA Feature Chips -->
  <rect x="258" y="463" width="84" height="20" rx="3" fill="#FFFFFF" stroke="#E0AC9A" stroke-width="0.9"/>
  <text x="300" y="476" text-anchor="middle" class="b-zh" font-size="8.6">bne 融合分支</text>
  <rect x="348" y="463" width="86" height="20" rx="3" fill="#FFFFFF" stroke="#E0AC9A" stroke-width="0.9"/>
  <text x="391" y="476" text-anchor="middle" class="b-zh" font-size="8.6">mul+add 拆分</text>
  <rect x="440" y="463" width="88" height="20" rx="3" fill="#FFFFFF" stroke="#E0AC9A" stroke-width="0.9"/>
  <text x="484" y="476" text-anchor="middle" class="b-zh" font-size="8.6">32 B 栈帧溢出</text>
  <text x="392.5" y="499" text-anchor="middle" class="sub" font-size="8.6">ELF32 RISC-V (RVC/RVE) · Zicsr/Zifencei</text>

  <!-- ==================== CONNECTORS (Stage 2 -> Stage 3) ==================== -->
  <line x1="540" y1="164" x2="558" y2="164" stroke="#2E5B88" stroke-width="1.8" marker-end="url(#arrBlue)"/>
  <line x1="540" y1="398" x2="558" y2="398" stroke="#C95B3B" stroke-width="1.8" marker-end="url(#arrTerra)"/>

  <!-- ==================== STAGE 3 TOP: CORTEX-M3 CALIBRATION & DUAL-PATH ==================== -->
  <g filter="url(#sh)">
    <rect x="565" y="54" width="265" height="218" rx="4" fill="#FAFBFD" stroke="#8FB5D9" stroke-width="1.15" stroke-dasharray="4,2"/>
  </g>
  <rect x="577" y="64" width="112" height="18" rx="3" fill="#2E5B88"/>
  <text x="633" y="76" text-anchor="middle" class="h-wh" font-size="8.8">QEMU 行为级仿真边界</text>
  <text x="818" y="76.5" text-anchor="end" class="mono" font-size="8.4" fill="#475569">mps2-an385</text>

  <!-- Mini Linear Calibration Plot inside Card -->
  <rect x="577" y="88" width="241" height="106" rx="3.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="1"/>
  <text x="697" y="102" text-anchor="middle" class="h-zh" font-size="9.2" fill="#1D4063">汇编闭环标定：500k × (subs + bne)</text>
  <!-- Axes -->
  <line x1="612" y1="176" x2="796" y2="176" stroke="#475569" stroke-width="1"/>
  <line x1="612" y1="176" x2="612" y2="112" stroke="#475569" stroke-width="1"/>
  <line x1="612" y1="148" x2="796" y2="148" stroke="#E2E8F0" stroke-width="0.7" stroke-dasharray="2,2"/>
  <line x1="612" y1="122" x2="796" y2="122" stroke="#E2E8F0" stroke-width="0.7" stroke-dasharray="2,2"/>
  <!-- shift=1 dashed upper line -->
  <line x1="612" y1="176" x2="758" y2="122" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="3,2"/>
  <circle cx="758" cy="122" r="3" fill="#64748B"/>
  <text x="750" y="121" text-anchor="end" class="sub" font-size="7.6">shift=1: 50,001</text>
  <!-- shift=0 primary calibration line -->
  <line x1="612" y1="176" x2="758" y2="148" stroke="#2E5B88" stroke-width="2"/>
  <circle cx="758" cy="148" r="4" fill="#2E5B88" stroke="#FFFFFF" stroke-width="1.2"/>
  <!-- Slope Callout -->
  <rect x="692" y="156" width="112" height="16" rx="3" fill="#DCE8F5" stroke="#8FB5D9" stroke-width="0.7"/>
  <text x="748" y="167" text-anchor="middle" class="h-zh" font-size="8.0" fill="#1D4063">1 tick ≡ 40 指令</text>
  <text x="607" y="151" text-anchor="end" class="mono" font-size="7.4" fill="#2E5B88">25k</text>
  <text x="607" y="125" text-anchor="end" class="mono" font-size="7.4" fill="#64748B">50k</text>
  <text x="758" y="187" text-anchor="middle" class="mono" font-size="7.6" fill="#475569">10⁶ 动态指令</text>
  <text x="612" y="187" text-anchor="middle" class="mono" font-size="7.6" fill="#475569">0</text>

  <!-- Two Decoupled Paths Blocks -->
  <rect x="577" y="202" width="241" height="27" rx="3" fill="#EBF3FA" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="586" y="219" class="h-zh" font-size="9.0" fill="#1D4063">路径 A：≥10 s 长跑合规 · 30k–40k 轮</text>

  <rect x="577" y="235" width="241" height="27" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="586" y="252" class="h-zh" font-size="9.0" fill="#334155">路径 B：-icount 估值 · 1/20 轮偏差 &lt;0.02%</text>

  <!-- ==================== STAGE 3 BOTTOM: E902 RTL DIGITAL WAVEFORM MONITOR ==================== -->
  <g filter="url(#sh)">
    <rect x="565" y="286" width="265" height="224" rx="4" fill="#FAFBFD" stroke="#E0AC9A" stroke-width="1.15" stroke-dasharray="4,2"/>
  </g>
  <rect x="577" y="296" width="118" height="18" rx="3" fill="#C95B3B"/>
  <text x="636" y="308" text-anchor="middle" class="h-wh" font-size="8.8">RTL 周期精确硬件边界</text>
  <text x="818" y="308.5" text-anchor="end" class="mono" font-size="8.4" fill="#475569">Icarus 12.0</text>

  <!-- Drawn 4-Track Digital Logic Waveform Box -->
  <rect x="577" y="320" width="241" height="134" rx="3.5" fill="#FFFFFF" stroke="#E9C3B5" stroke-width="1"/>
  <text x="697" y="333" text-anchor="middle" class="h-zh" font-size="9.2" fill="#8A341C">总线地址触发非侵入退休监测时序</text>

  <!-- Track 1: clk -->
  <text x="617" y="347" text-anchor="end" class="mono" font-size="7.6" fill="#475569">clk</text>
  <path d="{clk_path}" fill="none" stroke="#64748B" stroke-width="1.0"/>

  <!-- Track 2: win_en -->
  <text x="617" y="373" text-anchor="end" class="mono" font-size="7.6" fill="#2A8C82">win_en</text>
  <path d="M 622 377 L 642 377 L 642 362 L 792 362 L 792 377 L 811 377" fill="none" stroke="#2A8C82" stroke-width="1.5"/>
  <rect x="642" y="362" width="150" height="15" fill="#2A8C82" fill-opacity="0.10"/>
  <text x="717" y="372.5" text-anchor="middle" class="h-zh" font-size="7.8" fill="#175B54">非侵入硬件监视窗口开启</text>

  <!-- Track 3: retire pulses -->
  <text x="617" y="401" text-anchor="end" class="mono" font-size="7.6" fill="#B45309">retire</text>
  <line x1="622" y1="404" x2="811" y2="404" stroke="#CBD5E1" stroke-width="0.9"/>
  {retire_svg}

  <!-- Track 4: MCYCLE bar with 17-22 cyc caliper -->
  <text x="617" y="427" text-anchor="end" class="mono" font-size="7.6" fill="#C95B3B">MCYCLE</text>
  <rect x="653" y="416" width="128" height="14" rx="2.5" fill="#F9E6DF" stroke="#C95B3B" stroke-width="1.1"/>
  <text x="717" y="426" text-anchor="middle" class="mono" font-size="7.6" fill="#8A341C">软件 64 位周期读数</text>
  <!-- Boundary delta markers -->
  <line x1="642" y1="377" x2="642" y2="444" stroke="#2A8C82" stroke-width="0.8" stroke-dasharray="2,2"/>
  <line x1="792" y1="377" x2="792" y2="444" stroke="#2A8C82" stroke-width="0.8" stroke-dasharray="2,2"/>
  <text x="717" y="445" text-anchor="middle" class="h-zh" font-size="8.0" fill="#175B54">双时钟边界差恒为 17–22 周期</text>

  <!-- MINSTRET Bypass Pill -->
  <rect x="577" y="462" width="241" height="38" rx="4.5" fill="#FAEBE5" stroke="#C95B3B" stroke-width="0.9"/>
  <text x="697" y="478" text-anchor="middle" class="h-zh" font-size="8.9" fill="#8A341C">MINSTRET ≡ 0 → 外部采样退休脉冲</text>
  <text x="697" y="493" text-anchor="middle" class="mono" font-size="8.4" fill="#1E293B">实测 CPI = 窗口周期 / 退休指令数</text>

  <!-- ==================== FAN-IN ORTHOGONAL BUS CONNECTORS (Stage 3 -> Stage 4) ==================== -->
  <path d="M 830 164 L 833.5 164 Q 838 164, 838 168.5 L 838 261.5 Q 838 266, 842.5 266 L 848 266" fill="none" stroke="#2E5B88" stroke-width="1.8" marker-end="url(#arrBlue)"/>
  <path d="M 830 398 L 833.5 398 Q 838 398, 838 393.5 L 838 298.5 Q 838 294, 842.5 294 L 848 294" fill="none" stroke="#C95B3B" stroke-width="1.8" marker-end="url(#arrTerra)"/>

  <!-- ==================== STAGE 4: MULTI-DIMENSIONAL ATTRIBUTION ==================== -->
  <g filter="url(#sh)">
    <rect x="855" y="54" width="211" height="456" rx="4" fill="#F4FAF9" stroke="#8AC5BE" stroke-width="1.2"/>
  </g>

  <!-- 4A: Bit-Exact CRC Equivalence Register Table (Zero Decorative Shield Icons) -->
  <rect x="866" y="66" width="189" height="72" rx="3.5" fill="#FFFFFF" stroke="#8AC5BE" stroke-width="1"/>
  <rect x="866" y="66" width="189" height="19" rx="3.5" fill="#E6F4F2"/>
  <rect x="866" y="80" width="189" height="5" fill="#E6F4F2"/>
  <line x1="866" y1="85" x2="1055" y2="85" stroke="#B7DDD8" stroke-width="0.8"/>
  <text x="960.5" y="79" text-anchor="middle" class="h-zh" font-size="8.6" fill="#175B54">四重 CRC 等价核验 · M3 ≡ E902</text>

  <rect x="873" y="90" width="84" height="15" rx="2" fill="#F8FAFC" stroke="#DCE4EE" stroke-width="0.7"/>
  <text x="915" y="100.5" text-anchor="middle" class="mono" font-size="7.6" fill="#334155">list: 0xe9f5</text>
  <rect x="964" y="90" width="84" height="15" rx="2" fill="#F8FAFC" stroke="#DCE4EE" stroke-width="0.7"/>
  <text x="1006" y="100.5" text-anchor="middle" class="mono" font-size="7.6" fill="#334155">mat : 0x1fd7</text>
  <rect x="873" y="108" width="84" height="15" rx="2" fill="#F8FAFC" stroke="#DCE4EE" stroke-width="0.7"/>
  <text x="915" y="118.5" text-anchor="middle" class="mono" font-size="7.6" fill="#334155">stat: 0x8e3a</text>
  <rect x="964" y="108" width="84" height="15" rx="2" fill="#F8FAFC" stroke="#DCE4EE" stroke-width="0.7"/>
  <text x="1006" y="118.5" text-anchor="middle" class="mono" font-size="7.6" fill="#175B54">fin : 0xe714</text>
  <text x="960.5" y="133.5" text-anchor="middle" class="sub" font-size="7.8">1→2 轮同步：0xe714 → 0x72be</text>

  <!-- 4B: 3-Granularity Nested Layer Diagram -->
  <rect x="866" y="148" width="189" height="122" rx="3.5" fill="#FFFFFF" stroke="#8AC5BE" stroke-width="1"/>
  <text x="960.5" y="165" text-anchor="middle" class="h-zh" font-size="10.2" fill="#175B54">三粒度无偏静态剥离</text>
  <!-- Nested Layer 1 -->
  <rect x="876" y="173" width="169" height="86" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="0.9"/>
  <text x="960.5" y="186.5" text-anchor="middle" class="sub" font-size="8.4">粒度① 整包 ELF 映像</text>
  <!-- Nested Layer 2 -->
  <rect x="886" y="193" width="149" height="59" rx="3" fill="#DCE8F5" stroke="#6C9AC4" stroke-width="0.9"/>
  <text x="960.5" y="206.5" text-anchor="middle" class="h-zh" font-size="8.4" fill="#1D4063">粒度② 五核心算法 .o .text</text>
  <!-- Nested Layer 3 -->
  <rect x="896" y="213" width="129" height="32" rx="2.5" fill="#2A8C82"/>
  <text x="960.5" y="227" text-anchor="middle" class="h-wh" font-size="8.4">粒度③ 纯 16b/32b 指令流</text>
  <text x="960.5" y="239" text-anchor="middle" font-family="Hiragino Sans GB, sans-serif" font-size="7.6" fill="#D1FAE5">剔除启动段与数据文字池</text>

  <!-- 4C: Mini Pareto Sparkline -->
  <rect x="866" y="280" width="189" height="132" rx="3.5" fill="#FFFFFF" stroke="#8AC5BE" stroke-width="1"/>
  <text x="960.5" y="297" text-anchor="middle" class="h-zh" font-size="10.2" fill="#175B54">帕累托前沿与热点归因</text>
  <!-- Mini Axes -->
  <line x1="888" y1="382" x2="1042" y2="382" stroke="#475569" stroke-width="1"/>
  <line x1="888" y1="382" x2="888" y2="308" stroke="#475569" stroke-width="1"/>
  <!-- Mini M3 Pareto curve -->
  <polyline points="906,332 924,358 944,364 982,371" fill="none" stroke="#2E5B88" stroke-width="2"/>
  <circle cx="906" cy="332" r="2.8" fill="#2E5B88"/>
  <circle cx="944" cy="364" r="2.8" fill="#2E5B88"/>
  <circle cx="982" cy="371" r="2.8" fill="#2E5B88"/>
  <text x="896" y="379" class="h-zh" font-size="7.6" fill="#2E5B88">M3 占优前沿</text>
  <!-- Mini E902 curve with red cliff dot -->
  <polyline points="918,315 936,348 960,354 1030,357" fill="none" stroke="#C95B3B" stroke-width="2"/>
  <rect x="915" y="312" width="5.5" height="5.5" fill="#C95B3B"/>
  <rect x="957" y="351" width="5.5" height="5.5" fill="#C95B3B"/>
  <circle cx="1030" cy="357" r="4.2" fill="#B8334A" stroke="#FFFFFF" stroke-width="1"/>
  <text x="1002" y="344" text-anchor="middle" class="h-zh" font-size="7.6" fill="#B8334A">RVC 42.6%</text>
  <text x="1002" y="333" text-anchor="middle" class="h-zh" font-size="7.6" fill="#B8334A">CPI→1.4846</text>
  <text x="965" y="396" text-anchor="middle" class="sub" font-size="8.0">代码体积 (KiB) →</text>
  <text x="960.5" y="407" text-anchor="middle" class="b-zh" font-size="8.2">矩阵内循环 6 vs 7 条逐行归因</text>

  <!-- 4D: Co-Design Implications -->
  <rect x="866" y="422" width="189" height="78" rx="3.5" fill="url(#gTeal)"/>
  <text x="960.5" y="440.5" text-anchor="middle" class="h-wh" font-size="10.0">国产 RISC-V 协同优化启示</text>
  <text x="877" y="458.5" font-family="Hiragino Sans GB, sans-serif" font-size="8.5" fill="#E6FFFA">(1) 优选 -O2/-O3 · 慎用循环展开</text>
  <text x="877" y="474.5" font-family="Hiragino Sans GB, sans-serif" font-size="8.5" fill="#E6FFFA">(2) 强化 x8–x15 窗口寄存器分配</text>
  <text x="877" y="490.5" font-family="Hiragino Sans GB, sans-serif" font-size="8.5" fill="#E6FFFA">(3) 引入 Zcb / Zcmp 压缩扩展</text>
</svg>
"""
    p = OUT_DIR / "fig1_system_framework.svg"
    p.write_text(svg, encoding="utf-8")
    return p


def write_fig2_dynamic_cpi_svg():
    """IEEE MICRO / NeurIPS style 2-panel dynamic efficiency & E902 multi-iter CPI sensitivity figure."""
    setup_pub_rc()

    opts = ["-Os", "-O2", "-O3", "-O3\n-funroll-loops"]
    m3_dyn = [365.840, 295.760, 281.520, 263.800]   # thousands (1-iter)
    m3_20  = [365.848, 295.760, 281.482, 263.812]   # thousands (20-iter mean)
    e9_dyn = [420.714, 318.606, 303.457, 295.724]   # thousands

    e9_cyc1 = [628.383, 461.045, 436.516, 439.008]
    e9_cyc2 = [np.nan,  463.694, 442.326, 439.015]
    e9_cpi1 = [1.4937, 1.4471, 1.4385, 1.4846]
    e9_cpi2 = [np.nan, 1.4553, 1.4576, 1.4846]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.05), dpi=200)
    plt.subplots_adjust(wspace=0.28, top=0.80, bottom=0.135, left=0.065, right=0.935)

    x = np.arange(len(opts)) * 1.22
    w = 0.39

    # ---------------- Panel (a): Dynamic Instructions with Delta Brackets ----------------
    ax1.grid(axis="y", zorder=0)
    b1 = ax1.bar(x - w/2, m3_dyn, w, color=PALETTE["m3"], edgecolor="#FFFFFF", linewidth=0.9, zorder=3,
                 label="Arm Cortex-M3（QEMU -icount 估计）")
    b2 = ax1.bar(x + w/2, e9_dyn, w, color=PALETTE["e9"], edgecolor="#FFFFFF", linewidth=0.9, zorder=3,
                 label="玄铁 E902（RTL 退休指令精确计数）")
    ax1.scatter(x - w/2, m3_20, marker="D", s=16, facecolor="#FFFFFF", edgecolor=PALETTE["m3_dark"],
                linewidth=1.1, zorder=5, label="M3 20 轮均值校验点")

    add_panel_header(ax1, "a", "每轮动态执行指令数对比", y_offset=1.135)
    ax1.set_ylabel("每轮动态指令数（千条 / 轮）", fontsize=9.5, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(opts, fontsize=9.0)
    ax1.set_ylim(0, 505)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", bbox_to_anchor=(-0.01, 1.125), ncol=2, fontsize=7.5, columnspacing=0.9, handletextpad=0.4)

    # Editorial delta brackets above each pair
    for i in range(len(opts)):
        red = 100.0 * (m3_dyn[i] - e9_dyn[i]) / e9_dyn[i]
        # Value labels neatly inside top or just above bar
        ax1.text(x[i] - w/2, m3_dyn[i] - 18, f"{m3_dyn[i]:.1f}k", ha="center", va="top",
                 fontsize=7.3, color="#FFFFFF", fontweight="bold", zorder=6)
        ax1.text(x[i] + w/2, e9_dyn[i] - 18, f"{e9_dyn[i]:.1f}k", ha="center", va="top",
                 fontsize=7.3, color="#FFFFFF", fontweight="bold", zorder=6)
        # Bracket connecting M3 top and E902 top
        y_top = e9_dyn[i] + 16
        ax1.plot([x[i] - w/2, x[i] - w/2, x[i] + w/2, x[i] + w/2],
                 [m3_dyn[i] + 6, y_top, y_top, e9_dyn[i] + 6],
                 color=PALETTE["muted"], linewidth=0.9, zorder=4)
        ax1.text(x[i], y_top + 6, f"M3 {red:.1f}%", ha="center", va="bottom",
                 fontsize=7.8, fontweight="bold", color=PALETTE["m3_dark"],
                 bbox=dict(boxstyle="round,pad=0.16", fc=PALETTE["m3_pale"], ec="none"))

    # ---------------- Panel (b): E902 RTL Cycles (1 vs 2 iter) + Shaded Plateau + CPI ----------------
    ax2.grid(axis="y", zorder=0)
    # Shaded ±0.8% cycle plateau region spanning -O3 and -O3 -funroll-loops
    ax2.axvspan(x[2] - 0.50, x[3] + 0.50, color="#FEF3C7", alpha=0.42, zorder=1)
    ax2.text((x[2] + x[3]) / 2, 858, "周期窄幅平台区（±0.8%）\n指令降 2.55% 被 CPI 抬升抵消",
             ha="center", va="top", fontsize=7.3, color="#92400E", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.22", fc="#FFFBEB", ec="#F59E0B", lw=0.7), zorder=4)

    ax2.bar(x - w/2, e9_cyc1, w, color=PALETTE["e9"], edgecolor="#FFFFFF", linewidth=0.9, alpha=0.86, zorder=3,
            label="E902 周期/轮（1 轮）")
    c2_vals = [0 if np.isnan(v) else v for v in e9_cyc2]
    ax2.bar(x + w/2, c2_vals, w, color=PALETTE["e9_light"], edgecolor="#FFFFFF", linewidth=0.9, hatch="///", alpha=0.90, zorder=3,
            label="E902 均值周期/轮（2 轮）")

    for i in range(len(opts)):
        ax2.text(x[i] - w/2, e9_cyc1[i] - 24, f"{e9_cyc1[i]:.1f}k", ha="center", va="top",
                 fontsize=7.1, color="#FFFFFF", fontweight="bold", zorder=4)
        if not np.isnan(e9_cyc2[i]):
            ax2.text(x[i] + w/2, e9_cyc2[i] - 24, f"{e9_cyc2[i]:.1f}k", ha="center", va="top",
                     fontsize=7.1, color="#5A2010", fontweight="bold", zorder=4)

    add_panel_header(ax2, "b", "玄铁 E902 硬件周期与实测 CPI 演化（1 轮 vs 2 轮）", y_offset=1.135)
    ax2.set_ylabel("核心硬件周期数（千周期 / 轮）", fontsize=9.5, fontweight="bold", color=PALETTE["e9_dark"])
    ax2.set_xticks(x)
    ax2.set_xticklabels(opts, fontsize=9.0)
    ax2.set_ylim(0, 895)
    ax2.spines["top"].set_visible(False)

    ax2r = ax2.twinx()
    ax2r.plot(x, e9_cpi1, color=PALETTE["crimson"], marker="o", linewidth=2.2, markersize=6.8,
              markeredgecolor="#FFFFFF", markeredgewidth=1.2, zorder=6, label="实测 CPI（1 轮）")
    ax2r.plot(x[1:], e9_cpi2[1:], color=PALETTE["indigo"], marker="s", linestyle="--", linewidth=1.9, markersize=6.2,
              markeredgecolor="#FFFFFF", markeredgewidth=1.1, zorder=7, label="实测 CPI（2 轮）")
    ax2r.set_ylabel("玄铁 E902 实测硬件 CPI", fontsize=9.5, fontweight="bold", color=PALETTE["crimson"])
    ax2r.set_ylim(1.23, 1.57)
    ax2r.spines["top"].set_visible(False)
    ax2r.spines["right"].set_color(PALETTE["crimson"])
    ax2r.tick_params(axis="y", colors=PALETTE["crimson"])

    pill = dict(boxstyle="round,pad=0.14", fc="#FFFFFF", ec="none", alpha=0.88)
    # CPI labels carefully positioned without colliding with bars or shaded box
    ax2r.annotate("1.4937", (x[0], e9_cpi1[0]), textcoords="offset points", xytext=(0, 10),
                  ha="center", fontsize=7.6, fontweight="bold", color=PALETTE["crimson"], bbox=pill, zorder=8)
    ax2r.annotate("1.4471", (x[1], e9_cpi1[1]), textcoords="offset points", xytext=(0, -16),
                  ha="center", fontsize=7.6, fontweight="bold", color=PALETTE["crimson"], bbox=pill, zorder=8)
    ax2r.annotate("1.4385", (x[2], e9_cpi1[2]), textcoords="offset points", xytext=(0, -16),
                  ha="center", fontsize=7.6, fontweight="bold", color=PALETTE["crimson"], bbox=pill, zorder=8)
    ax2r.annotate("1.4846\n(CPI 跃升)", (x[3], e9_cpi1[3]), textcoords="offset points", xytext=(0, -25),
                  ha="center", fontsize=7.5, fontweight="bold", color=PALETTE["crimson"], bbox=pill, zorder=8)
    ax2r.annotate("1.4553", (x[1], e9_cpi2[1]), textcoords="offset points", xytext=(0, 10),
                  ha="center", fontsize=7.4, fontweight="bold", color=PALETTE["indigo"], bbox=pill, zorder=8)
    ax2r.annotate("1.4576", (x[2], e9_cpi2[2]), textcoords="offset points", xytext=(0, 10),
                  ha="center", fontsize=7.4, fontweight="bold", color=PALETTE["indigo"], bbox=pill, zorder=8)

    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2r.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper left", bbox_to_anchor=(-0.02, 1.125), ncol=2, fontsize=7.3, columnspacing=0.8, handletextpad=0.4)

    p = OUT_DIR / "fig2_dynamic_cpi_analysis.svg"
    plt.savefig(p, format="svg")
    plt.close(fig)
    return p


def write_fig3_code_density_modules_svg():
    """IEEE / NeurIPS style 2-panel module breakdown + RVC compression cliff analysis."""
    setup_pub_rc()
    data = {c["name"]: c for c in json.load(open(ROOT_DIR / "benchmark/results/elf_analysis.json"))}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.05), dpi=200)
    plt.subplots_adjust(wspace=0.28, top=0.80, bottom=0.135, left=0.065, right=0.935)

    # ---------------- Panel (a): Stacked 5 Core Modules (.text) ----------------
    configs = ["m3_O2", "e902_O2", "m3_O3_unroll", "e902_O3_unroll"]
    cfg_labels = ["Arm M3\n(-O2)", "玄铁 E902\n(-O2)", "Arm M3\n(-O3+unroll)", "玄铁 E902\n(-O3+unroll)"]
    # Paul Tol / Nature muted categorical palette
    mods = [
        ("core_matrix.o",    "core_matrix (矩阵)",  "#2E5B88"),
        ("core_list_join.o", "core_list_join (链表)", "#2A8C82"),
        ("core_main.o",      "core_main (主控)",    "#C95B3B"),
        ("core_state.o",     "core_state (状态机)",  "#6D5B97"),
        ("core_util.o",      "core_util (CRC/工具)", "#C99738"),
    ]
    ax1.grid(axis="y", zorder=0)
    x1 = np.arange(len(configs))
    bottoms = np.zeros(len(configs))
    for mod_key, mod_lbl, col in mods:
        vals = np.array([data[c]["objects"][mod_key]["text"] / 1024.0 for c in configs])
        ax1.bar(x1, vals, width=0.50, bottom=bottoms, label=mod_lbl, color=col, edgecolor="#FFFFFF", linewidth=0.8, zorder=3)
        if mod_key == "core_matrix.o":
            for j, v in enumerate(vals):
                if v > 3.5:
                    ax1.text(x1[j], bottoms[j] + v / 2, f"矩阵模块\n{data[configs[j]]['objects'][mod_key]['text']:,} B",
                             ha="center", va="center", fontsize=7.5, color="#FFFFFF", fontweight="bold", zorder=4)
        bottoms += vals

    # Totals + E902/M3 overhead callouts
    for j, c in enumerate(configs):
        tot = data[c]["core_objects_sum"]["text"]
        extra = ""
        if j == 1:
            extra = "\n(+33.5%)"
        elif j == 3:
            extra = "\n(+49.5%)"
        col_txt = PALETTE["e9_dark"] if j in (1, 3) else PALETTE["m3_dark"]
        ax1.text(x1[j], bottoms[j] + 0.35, f"{tot:,} B{extra}", ha="center", va="bottom",
                 fontsize=7.8, fontweight="bold", color=col_txt, zorder=5)

    add_panel_header(ax1, "a", "CoreMark 五大核心算法模块体积拆解（链接前 .text）", y_offset=1.135)
    ax1.set_ylabel("核心模块代码段累计体积（KiB）", fontsize=9.5, fontweight="bold")
    ax1.set_xticks(x1)
    ax1.set_xticklabels(cfg_labels, fontsize=8.8)
    ax1.set_ylim(0, 23.8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", bbox_to_anchor=(-0.01, 1.125), ncol=3, fontsize=7.2, columnspacing=0.7, handletextpad=0.35)

    # ---------------- Panel (b): 16-bit Ratio & Avg Width with Shaded Collapse Zone ----------------
    opts = ["-Os", "-O2", "-O3", "-O3\n-funroll-loops"]
    keys = ["Os", "O2", "O3", "O3_unroll"]
    m3_pct = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["pct_16b"] for k in keys]
    e9_pct = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["pct_16b"] for k in keys]
    m3_avg = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["avg_insn_bytes"] for k in keys]
    e9_avg = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["avg_insn_bytes"] for k in keys]

    x2 = np.arange(len(opts))
    ax2.grid(axis="y", zorder=0)
    # Soft rose highlight for the RVC collapse transition (-O3 -> -O3 -funroll-loops)
    ax2.axvspan(x2[2] + 0.08, x2[3] + 0.34, color="#FEE2E2", alpha=0.45, zorder=1)
    ax2.text((x2[2] + x2[3]) / 2 + 0.14, 77.6, "RVC 压缩率坍塌区\n(-25.17 pp)", ha="center", va="top",
             fontsize=7.4, fontweight="bold", color=PALETTE["crimson"],
             bbox=dict(boxstyle="round,pad=0.20", fc="#FFF5F5", ec="#F87171", lw=0.7), zorder=4)

    ax2.plot(x2, m3_pct, color=PALETTE["m3"], marker="o", linewidth=2.3, markersize=6.8,
             markeredgecolor="#FFFFFF", markeredgewidth=1.2, zorder=5, label="M3 16 位占比 (%)")
    ax2.plot(x2, e9_pct, color=PALETTE["e9"], marker="s", linewidth=2.3, markersize=6.8,
             markeredgecolor="#FFFFFF", markeredgewidth=1.2, zorder=6, label="E902 16 位占比 (%)")

    add_panel_header(ax2, "b", "全优化谱系 16 位压缩指令占比与平均指令宽度", y_offset=1.135)
    ax2.set_ylabel("纯核心函数 16 位指令占比（%）", fontsize=9.5, fontweight="bold", color=PALETTE["slate"])
    ax2.set_xticks(x2)
    ax2.set_xticklabels(opts, fontsize=9.0)
    ax2.set_ylim(34, 81)
    ax2.set_xlim(-0.32, 3.40)
    ax2.spines["top"].set_visible(False)

    pill = dict(boxstyle="round,pad=0.13", fc="#FFFFFF", ec="none", alpha=0.86)
    m3_off = [(0, 9), (0, 9), (-10, -15), (0, 9)]
    e9_off = [(0, -15), (0, -15), (-8, 9), (0, -16)]
    for i in range(len(opts)):
        ax2.annotate(f"{m3_pct[i]:.2f}%", (x2[i], m3_pct[i]), textcoords="offset points", xytext=m3_off[i],
                     ha="center", fontsize=7.5, fontweight="bold", color=PALETTE["m3_dark"], bbox=pill, zorder=7)
        ax2.annotate(f"{e9_pct[i]:.2f}%", (x2[i], e9_pct[i]), textcoords="offset points", xytext=e9_off[i],
                     ha="center", fontsize=7.5, fontweight="bold", color=PALETTE["e9_dark"], bbox=pill, zorder=7)

    ax2r = ax2.twinx()
    ax2r.plot(x2, m3_avg, color=PALETTE["m3_light"], marker="^", linestyle="--", linewidth=1.7, markersize=5.8,
              markeredgecolor="#FFFFFF", markeredgewidth=0.9, zorder=4, label="M3 平均宽度 (B)")
    ax2r.plot(x2, e9_avg, color=PALETTE["crimson"], marker="D", linestyle="--", linewidth=1.7, markersize=5.4,
              markeredgecolor="#FFFFFF", markeredgewidth=0.9, zorder=5, label="E902 平均宽度 (B)")
    ax2r.set_ylabel("平均单指令字节数（B / 条）", fontsize=9.5, fontweight="bold", color=PALETTE["crimson"])
    ax2r.set_ylim(2.40, 3.40)
    ax2r.spines["top"].set_visible(False)
    ax2r.spines["right"].set_color(PALETTE["crimson"])
    ax2r.tick_params(axis="y", colors=PALETTE["crimson"])

    ax2r.annotate("3.148 B", (x2[3], e9_avg[3]), textcoords="offset points", xytext=(-30, 5),
                  ha="center", fontsize=7.6, fontweight="bold", color=PALETTE["crimson"], bbox=pill, zorder=8)
    ax2r.annotate("2.772 B", (x2[3], m3_avg[3]), textcoords="offset points", xytext=(-2, 10),
                  ha="center", fontsize=7.4, fontweight="bold", color=PALETTE["m3"], bbox=pill, zorder=8)

    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2r.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper left", bbox_to_anchor=(-0.02, 1.125), ncol=2, fontsize=7.3, columnspacing=0.8, handletextpad=0.35)

    p = OUT_DIR / "fig3_code_density_modules.svg"
    plt.savefig(p, format="svg")
    plt.close(fig)
    return p


def write_fig4_pareto_hotspot_svg():
    """Crown-jewel NeurIPS / ISCA figure: (a) Code-Size vs Dynamic-Insn Pareto Trajectory; (b) Hotspot 16b/32b Breakdown."""
    setup_pub_rc()
    data = {c["name"]: c for c in json.load(open(ROOT_DIR / "benchmark/results/elf_analysis.json"))}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.05), dpi=200)
    plt.subplots_adjust(wspace=0.34, top=0.80, bottom=0.135, left=0.068, right=0.965)

    # ---------------- Panel (a): Pareto Trajectory (Pure Code Footprint vs Dynamic Insns) ----------------
    keys = ["Os", "O2", "O3", "O3_unroll"]
    tags = ["-Os", "-O2", "-O3", "-O3+unroll"]
    m3_x = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["bytes"] / 1024.0 for k in keys]
    e9_x = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["bytes"] / 1024.0 for k in keys]
    m3_y = [365.840, 295.760, 281.520, 263.800]
    e9_y = [420.714, 318.606, 303.457, 295.724]
    m3_p = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["pct_16b"] for k in keys]
    e9_p = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["pct_16b"] for k in keys]

    ax1.grid(True, zorder=0)
    # Soft optimal direction hint cleanly tucked into lower-left open corner
    ax1.annotate("帕累托更优方向\n更小体积 · 更少指令", xy=(2.15, 238), xytext=(5.55, 240),
                 arrowprops=dict(arrowstyle="->", color=PALETTE["teal"], lw=1.6, connectionstyle="arc3,rad=0.08"),
                 fontsize=7.4, fontweight="bold", color=PALETTE["teal"], ha="center", va="center",
                 bbox=dict(boxstyle="round,pad=0.20", fc="#F0FDFA", ec="#5EEAD4", lw=0.7), zorder=4)

    # Draw trajectory lines with directional mid-arrows
    ax1.plot(m3_x, m3_y, color=PALETTE["m3"], linewidth=2.1, alpha=0.88, zorder=3, label="Arm Cortex-M3（Thumb-2 帕累托前沿）")
    ax1.plot(e9_x, e9_y, color=PALETTE["e9"], linewidth=2.1, alpha=0.88, zorder=3, label="玄铁 E902（RV32EMC 演进轨迹）")

    for xs, ys, col in [(m3_x, m3_y, PALETTE["m3"]), (e9_x, e9_y, PALETTE["e9"])]:
        for i in range(len(xs) - 1):
            mx = xs[i] + 0.56 * (xs[i+1] - xs[i])
            my = ys[i] + 0.56 * (ys[i+1] - ys[i])
            ax1.annotate("", xy=(mx, my), xytext=(xs[i], ys[i]),
                         arrowprops=dict(arrowstyle="-|>", color=col, lw=0, mutation_scale=11), zorder=4)

    # Bubble markers (size encodes 16-bit compression ratio!)
    m3_sz = [45 + (p - 35) * 2.4 for p in m3_p]
    e9_sz = [45 + (p - 35) * 2.4 for p in e9_p]
    ax1.scatter(m3_x, m3_y, s=m3_sz, color=PALETTE["m3"], edgecolor="#FFFFFF", linewidth=1.4, zorder=5)
    ax1.scatter(e9_x, e9_y, s=e9_sz, color=PALETTE["e9"], edgecolor="#FFFFFF", linewidth=1.4, marker="s", zorder=5)

    # Carefully placed non-overlapping optimization point labels
    m3_specs = [
        (0, 12, "center", "bottom"),    # -Os cleanly above dot in wide open space
        (-10, -10, "right", "top"),     # -O2 cleanly lower-left inside panel
        (0, -13, "center", "top"),      # -O3 cleanly below (above optimal box at y=240!)
        (16, -12, "center", "top"),     # -O3+unroll cleanly below-right
    ]
    e9_specs = [
        (12, 0, "left", "center"),      # -Os cleanly right of square
        (10, 6, "left", "bottom"),      # -O2 cleanly upper-right
        (8, 10, "left", "bottom"),      # -O3 cleanly upper-right
        (-4, 12, "center", "bottom"),   # -O3+unroll cleanly above
    ]
    for i, t in enumerate(tags):
        dx, dy, ha, va = m3_specs[i]
        ax1.annotate(f"{t}\n({m3_p[i]:.0f}% 16b)", (m3_x[i], m3_y[i]), textcoords="offset points",
                     xytext=(dx, dy), ha=ha, va=va,
                     fontsize=7.1, fontweight="bold", color=PALETTE["m3_dark"], zorder=6)
        dx, dy, ha, va = e9_specs[i]
        ax1.annotate(f"{t}\n({e9_p[i]:.0f}% 16b)", (e9_x[i], e9_y[i]), textcoords="offset points",
                     xytext=(dx, dy), ha=ha, va=va,
                     fontsize=7.1, fontweight="bold", color=PALETTE["e9_dark"], zorder=6)

    # Callout highlighting E902 diminishing returns on -O3 -> -O3+unroll
    ax1.annotate("体积 +87%，指令仅降 2.55%\n边际收益显著递减",
                 xy=(11.3, 299.5), xytext=(11.5, 372),
                 arrowprops=dict(arrowstyle="->", color=PALETTE["crimson"], lw=1.2, connectionstyle="arc3,rad=-0.15"),
                 fontsize=7.4, fontweight="bold", color=PALETTE["crimson"], ha="center",
                 bbox=dict(boxstyle="round,pad=0.22", fc="#FFF5F5", ec="#FCA5A5", lw=0.7), zorder=6)

    add_panel_header(ax1, "a", "性能–代码体积帕累托演进轨迹（点径表征 16 位压缩比）", y_offset=1.135)
    ax1.set_xlabel("CoreMark 纯核心算法指令体积（KiB，不含文字池）", fontsize=9.2, fontweight="bold")
    ax1.set_ylabel("每轮动态执行指令数（千条 / 轮）", fontsize=9.2, fontweight="bold")
    ax1.set_xlim(1.3, 16.5)
    ax1.set_ylim(218, 452)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", bbox_to_anchor=(-0.01, 1.125), ncol=1, fontsize=7.5, handletextpad=0.4)

    # ---------------- Panel (b): Hotspot Function 16b vs 32b Composition (Horizontal Paired Stacked Bars) ----------------
    hotspots = [
        ("matrix_mul_matrix\n(-O2)",     "m3_O2",       "e902_O2",       "matrix_mul_matrix"),
        ("core_list_mergesort\n(-O2)",   "m3_O2",       "e902_O2",       "core_list_mergesort"),
        ("core_state_transition\n(-O2)", "m3_O2",       "e902_O2",       "core_state_transition"),
        ("crc16\n(-O3)",                 "m3_O3",       "e902_O3",       "crc16"),
        ("crc16\n(-O3+unroll)",          "m3_O3_unroll","e902_O3_unroll","crc16"),
    ]
    y = np.arange(len(hotspots))[::-1]
    h = 0.34
    ax2.grid(axis="x", zorder=0)

    for idx, (lbl, m3_cfg, e9_cfg, fn) in enumerate(hotspots):
        fm = data[m3_cfg]["disasm"]["functions"][fn]
        fe = data[e9_cfg]["disasm"]["functions"][fn]
        ym = y[idx] + h/2 + 0.02
        ye = y[idx] - h/2 - 0.02

        # M3: 16b dark steel blue + 32b pale steel blue
        ax2.barh(ym, fm["16b"], height=h, color=PALETTE["m3"], edgecolor="#FFFFFF", linewidth=0.7, zorder=3,
                 label="M3 16 位指令" if idx == 0 else None)
        ax2.barh(ym, fm["32b"], left=fm["16b"], height=h, color=PALETTE["m3_light"], edgecolor="#FFFFFF", linewidth=0.7, zorder=3,
                 label="M3 32 位指令" if idx == 0 else None)
        ax2.text(fm["total_insns"] + 3.5, ym, f"{fm['total_insns']} 条 ({fm['pct_16b']:.1f}% 16b)",
                 va="center", ha="left", fontsize=7.1, color=PALETTE["m3_dark"], fontweight="bold")

        # E902: 16b deep terracotta + 32b pale coral
        ax2.barh(ye, fe["16b"], height=h, color=PALETTE["e9"], edgecolor="#FFFFFF", linewidth=0.7, zorder=3,
                 label="E902 16 位指令" if idx == 0 else None)
        ax2.barh(ye, fe["32b"], left=fe["16b"], height=h, color=PALETTE["e9_light"], edgecolor="#FFFFFF", linewidth=0.7, zorder=3,
                 label="E902 32 位指令" if idx == 0 else None)
        txt_col = PALETTE["crimson"] if (fn == "crc16" and "unroll" in e9_cfg) else PALETTE["e9_dark"]
        ax2.text(fe["total_insns"] + 3.5, ye, f"{fe['total_insns']} 条 ({fe['pct_16b']:.1f}% 16b)",
                 va="center", ha="left", fontsize=7.1, color=txt_col, fontweight="bold")

    # Highlight box around crc16 -O3+unroll extreme collapse
    ax2.axhspan(y[4] - 0.45, y[4] + 0.45, color="#FEE2E2", alpha=0.38, zorder=1)

    add_panel_header(ax2, "b", "典型热点函数 16 位 / 32 位静态指令构成剖析", y_offset=1.135)
    ax2.set_xlabel("热点函数静态指令总条数（16 位压缩 + 32 位常规）", fontsize=9.2, fontweight="bold")
    ax2.set_yticks(y)
    ax2.set_yticklabels([item[0] for item in hotspots], fontsize=8.1)
    ax2.set_xlim(0, 280)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="upper left", bbox_to_anchor=(-0.02, 1.125), ncol=2, fontsize=7.2, columnspacing=0.8, handletextpad=0.35)

    p = OUT_DIR / "fig4_pareto_hotspot.svg"
    plt.savefig(p, format="svg")
    plt.close(fig)
    return p


if __name__ == "__main__":
    p1 = write_fig1_system_framework()
    p2 = write_fig2_dynamic_cpi_svg()
    p3 = write_fig3_code_density_modules_svg()
    p4 = write_fig4_pareto_hotspot_svg()
    print("Generated 4 IEEE/NeurIPS-grade SVGs:", p1, p2, p3, p4)
