#!/usr/bin/env python3
"""Generate 3 IEEE / NeurIPS / Nature publication-grade pure-SVG figures for the Opening Report,
visually unified with the Midterm Report's editorial design system.
"""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Unified IEEE / NeurIPS / Nature Editorial Palette (identical to Midterm Report)
PALETTE = {
    "m3": "#2E5B88",
    "m3_light": "#6C9AC4",
    "m3_pale": "#DCE8F5",
    "m3_dark": "#1B3B5A",
    "e9": "#C95B3B",
    "e9_light": "#E5987E",
    "e9_pale": "#F9E6DF",
    "e9_dark": "#8A341C",
    "teal": "#2A8C82",
    "crimson": "#B8334A",
    "slate": "#1E293B",
    "muted": "#475569",
    "spine": "#334155",
    "grid": "#E2E8F0",
    "bg_panel": "#FAFBFD",
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


def add_panel_header(ax, letter: str, title: str, y_offset: float = 1.13):
    ax.text(
        0.0, y_offset, f"({letter})", transform=ax.transAxes,
        fontsize=10.5, fontweight="bold", color=PALETTE["slate"], va="bottom", ha="left",
    )
    ax.text(
        0.068, y_offset, title, transform=ax.transAxes,
        fontsize=10.2, fontweight="bold", color=PALETTE["slate"], va="bottom", ha="left",
    )


def _make_reg_strip(x0: float, y0: float, slot_w: float, slot_h: float, gap: float, colors: list, labels: list, txt_colors: list) -> str:
    out = []
    for i in range(16):
        rx = x0 + i * (slot_w + gap)
        out.append(f'<rect x="{rx:.1f}" y="{y0:.1f}" width="{slot_w:.1f}" height="{slot_h:.1f}" rx="2" fill="{colors[i]}" stroke="#FFFFFF" stroke-width="0.6"/>')
        out.append(f'<text x="{rx + slot_w/2:.1f}" y="{y0 + slot_h/2 + 3:.1f}" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="6.8" font-weight="700" fill="{txt_colors[i]}">{labels[i]}</text>')
    return "\n  ".join(out)


def _make_clk_wave(x0: float, y_hi: float, y_lo: float, cycles: int, step: float) -> str:
    pts = [f"M {x0:.1f} {y_lo:.1f}"]
    x = x0
    for _ in range(cycles):
        pts.append(f"L {x:.1f} {y_hi:.1f} L {x + step/2:.1f} {y_hi:.1f} L {x + step/2:.1f} {y_lo:.1f} L {x + step:.1f} {y_lo:.1f}")
        x += step
    return " ".join(pts)


def write_fig1_roadmap():
    """ISCA / IEEE MICRO / NeurIPS Hero Technical Roadmap (4-stage L->R with embedded micro-diagrams & 4 innovation anchors)."""
    m3_cols = (["#CBD5E1"]*4) + (["#2E5B88"]*8) + (["#94A3B8"]*4)
    m3_lbls = [f"r{i}" for i in range(12)] + ["ip", "sp", "lr", "pc"]
    m3_tcol = (["#334155"]*4) + (["#FFFFFF"]*8) + (["#FFFFFF"]*4)
    m3_reg_svg = _make_reg_strip(258, 179, 15.6, 17, 1.2, m3_cols, m3_lbls, m3_tcol)

    e9_cols = (["#E2E8F0"]*5) + (["#CBD5E1"]*3) + (["#C95B3B"]*2) + (["#E8A38C"]*6)
    e9_lbls = [f"x{i}" for i in range(16)]
    e9_tcol = (["#64748B"]*5) + (["#334155"]*3) + (["#FFFFFF"]*2) + (["#5A2010"]*6)
    e9_reg_svg = _make_reg_strip(258, 405, 15.6, 17, 1.2, e9_cols, e9_lbls, e9_tcol)

    clk_path = _make_clk_wave(622, 338, 350, 14, 13.5)
    retire_pulses = []
    for px in [649, 662.5, 676, 703, 716.5, 730, 757, 770.5, 784]:
        retire_pulses.append(f'<path d="M {px:.1f} 404 L {px:.1f} 391 L {px+5.2:.1f} 391 L {px+5.2:.1f} 404" fill="#FDE68A" stroke="#B45309" stroke-width="1.05"/>')
    retire_svg = "\n  ".join(retire_pulses)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 524" width="1080" height="524">
  <defs>
    <filter id="sh1" x="-2%" y="-2%" width="104%" height="106%">
      <feDropShadow dx="0" dy="1.0" stdDeviation="1.2" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
    <linearGradient id="gSlate1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E293B"/><stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="gBlue1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2E5B88"/><stop offset="100%" stop-color="#1D4063"/>
    </linearGradient>
    <linearGradient id="gTerra1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C95B3B"/><stop offset="100%" stop-color="#9A3B20"/>
    </linearGradient>
    <linearGradient id="gTeal1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2A8C82"/><stop offset="100%" stop-color="#1B665F"/>
    </linearGradient>
    <marker id="arrD1" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#475569"/>
    </marker>
    <marker id="arrB1" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2E5B88"/>
    </marker>
    <marker id="arrT1" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="8.5" markerHeight="8.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#C95B3B"/>
    </marker>
    <marker id="arrB1M" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2E5B88"/>
    </marker>
    <marker id="arrT1M" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#C95B3B"/>
    </marker>
    <marker id="arrMiniB1" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="5.5" markerHeight="5.5" markerUnits="userSpaceOnUse" orient="auto">
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

  <!-- Top 4-Stage Technical Architecture Banner -->
  <rect x="14"  y="12" width="206" height="30" rx="4" fill="url(#gSlate1)"/>
  <text x="117" y="31" text-anchor="middle" class="st-h">① 同源受控基准输入</text>
  <line x1="223" y1="27" x2="237.5" y2="27" stroke="#64748B" stroke-width="1.6" marker-end="url(#arrD1)"/>

  <rect x="245" y="12" width="295" height="30" rx="4" fill="url(#gSlate1)"/>
  <text x="392.5" y="31" text-anchor="middle" class="st-h">② 双架构编译移植与微架构对照</text>
  <line x1="543" y1="27" x2="557.5" y2="27" stroke="#64748B" stroke-width="1.6" marker-end="url(#arrD1)"/>

  <rect x="565" y="12" width="265" height="30" rx="4" fill="url(#gSlate1)"/>
  <text x="697.5" y="31" text-anchor="middle" class="st-h">③ 异构协同观测与标定</text>
  <line x1="833" y1="27" x2="847.5" y2="27" stroke="#64748B" stroke-width="1.6" marker-end="url(#arrD1)"/>

  <rect x="855" y="12" width="211" height="30" rx="4" fill="url(#gTeal1)"/>
  <text x="960.5" y="31" text-anchor="middle" class="st-h">④ 三粒度剥离与微架构归因</text>

  <!-- Stage 1 Column -->
  <g filter="url(#sh1)">
    <rect x="14" y="54" width="206" height="456" rx="4" fill="#FAFBFD" stroke="#CBD5E1" stroke-width="1.15"/>
  </g>
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

  <line x1="24" y1="261" x2="210" y2="261" stroke="#E2E8F0" stroke-width="1"/>
  <text x="117" y="278" text-anchor="middle" class="h-zh" font-size="10.4">四档编译优化谱系</text>

  <rect x="24" y="287" width="58" height="36" rx="3" fill="#F1F6FC" stroke="#B7CFE6" stroke-width="0.9"/>
  <text x="53" y="302" text-anchor="middle" class="mono" font-size="9.2" fill="#1D4063">-Os</text>
  <text x="53" y="315.5" text-anchor="middle" class="sub" font-size="8.0">体积最小</text>

  <rect x="88" y="287" width="58" height="36" rx="3" fill="#E6F0FA" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="117" y="302" text-anchor="middle" class="mono" font-size="9.2" fill="#1D4063">-O2</text>
  <text x="117" y="315.5" text-anchor="middle" class="sub" font-size="8.0">标准优化</text>

  <rect x="152" y="287" width="58" height="36" rx="3" fill="#DCE8F5" stroke="#6C9AC4" stroke-width="0.9"/>
  <text x="181" y="302" text-anchor="middle" class="mono" font-size="9.2" fill="#1D4063">-O3</text>
  <text x="181" y="315.5" text-anchor="middle" class="sub" font-size="8.0">激进内联</text>

  <rect x="24" y="329" width="186" height="34" rx="3" fill="#FDF3EF" stroke="#D98C73" stroke-width="0.95"/>
  <text x="117" y="343" text-anchor="middle" class="mono" font-size="8.6" fill="#8A341C">-O3 -funroll-loops</text>
  <text x="117" y="356" text-anchor="middle" class="sub" font-size="8.0" fill="#8A341C">激进循环展开</text>

  <line x1="24" y1="376" x2="210" y2="376" stroke="#E2E8F0" stroke-width="1"/>
  <text x="117" y="393" text-anchor="middle" class="h-zh" font-size="10.4">实验变量严格控制</text>

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

  <!-- Fan-Out Orthogonal Bus Connectors -->
  <path d="M 220 272 L 223.5 272 Q 228 272, 228 267.5 L 228 168.5 Q 228 164, 232.5 164 L 238 164" fill="none" stroke="#2E5B88" stroke-width="1.8" marker-end="url(#arrB1)"/>
  <path d="M 220 292 L 223.5 292 Q 228 292, 228 296.5 L 228 393.5 Q 228 398, 232.5 398 L 238 398" fill="none" stroke="#C95B3B" stroke-width="1.8" marker-end="url(#arrT1)"/>

  <!-- Stage 2 Top: Cortex-M3 -->
  <g filter="url(#sh1)">
    <rect x="245" y="54" width="295" height="218" rx="4" fill="#F6FAFE" stroke="#8FB5D9" stroke-width="1.2"/>
    <rect x="245" y="54" width="295" height="30" rx="4" fill="url(#gBlue1)"/>
    <rect x="245" y="76" width="295" height="8" fill="url(#gBlue1)"/>
  </g>
  <text x="392.5" y="73.5" text-anchor="middle" class="h-wh" font-size="11.5">路线 A · Arm Cortex-M3 / Thumb-2</text>

  <text x="258" y="100" class="h-zh" font-size="9.6" fill="#1D4063">三级哈佛流水线 · ARM GCC 13.2.1</text>
  <rect x="258" y="107" width="76" height="28" rx="4.5" fill="#FFFFFF" stroke="#2E5B88" stroke-width="1.15"/>
  <text x="296" y="124.5" text-anchor="middle" class="h-zh" font-size="9.8" fill="#1D4063">IF 取指</text>
  <line x1="334" y1="121" x2="348.2" y2="121" stroke="#2E5B88" stroke-width="1.35" marker-end="url(#arrB1M)"/>
  <rect x="354" y="107" width="76" height="28" rx="4.5" fill="#FFFFFF" stroke="#2E5B88" stroke-width="1.15"/>
  <text x="392" y="124.5" text-anchor="middle" class="h-zh" font-size="9.8" fill="#1D4063">ID 译码</text>
  <line x1="430" y1="121" x2="444.2" y2="121" stroke="#2E5B88" stroke-width="1.35" marker-end="url(#arrB1M)"/>
  <rect x="450" y="107" width="76" height="28" rx="4.5" fill="#2E5B88"/>
  <text x="488" y="124.5" text-anchor="middle" class="h-wh" font-size="9.8">EX 执行</text>

  <rect x="258" y="140" width="128" height="15" rx="3" fill="#DCE8F5"/>
  <text x="322" y="150.5" text-anchor="middle" class="mono" font-size="8" fill="#1D4063">I-Code Bus · 指令总线</text>
  <rect x="394" y="140" width="132" height="15" rx="3" fill="#DCE8F5"/>
  <text x="460" y="150.5" text-anchor="middle" class="mono" font-size="8" fill="#1D4063">D-Code / Sys · 数据总线</text>

  <text x="258" y="173" class="h-zh" font-size="9.6" fill="#1D4063">16×32b 通用寄存器文件</text>
  {m3_reg_svg}
  <path d="M 326 199 L 326 204 L 458 204 L 458 199" fill="none" stroke="#2E5B88" stroke-width="1.1"/>
  <text x="392" y="216" text-anchor="middle" class="h-zh" font-size="8.8" fill="#2E5B88">r4–r11：8 个被调保存寄存器 · 低栈溢出</text>

  <rect x="258" y="227" width="84" height="20" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="300" y="240" text-anchor="middle" class="b-zh" font-size="8.6">后自增寻址</text>
  <rect x="348" y="227" width="84" height="20" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="390" y="240" text-anchor="middle" class="b-zh" font-size="8.6">单指令乘加</text>
  <rect x="438" y="227" width="88" height="20" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="482" y="240" text-anchor="middle" class="b-zh" font-size="8.6">多寄存器压栈</text>
  <text x="392.5" y="263" text-anchor="middle" class="sub" font-size="8.6">-mcpu=cortex-m3 -mthumb · 裸机启动 + UART0</text>

  <!-- Stage 2 Bottom: XuanTie E902 -->
  <g filter="url(#sh1)">
    <rect x="245" y="286" width="295" height="224" rx="4" fill="#FDF7F4" stroke="#E0AC9A" stroke-width="1.2"/>
    <rect x="245" y="286" width="295" height="30" rx="4" fill="url(#gTerra1)"/>
    <rect x="245" y="308" width="295" height="8" fill="url(#gTerra1)"/>
  </g>
  <text x="392.5" y="305.5" text-anchor="middle" class="h-wh" font-size="11.5">路线 B · 玄铁 E902 / RV32EMC</text>

  <text x="258" y="332" class="h-zh" font-size="9.6" fill="#8A341C">两级顺序流水线 · RISC-V GCC 13.2.0</text>
  <rect x="258" y="339" width="90" height="28" rx="4.5" fill="#FFFFFF" stroke="#C95B3B" stroke-width="1.15"/>
  <text x="303" y="356.5" text-anchor="middle" class="h-zh" font-size="9.8" fill="#8A341C">IF 取指</text>
  <line x1="348" y1="353" x2="366.2" y2="353" stroke="#C95B3B" stroke-width="1.35" marker-end="url(#arrT1M)"/>
  <rect x="372" y="339" width="98" height="28" rx="4.5" fill="#C95B3B"/>
  <text x="421" y="356.5" text-anchor="middle" class="h-wh" font-size="9.8">EX/WB 执行</text>
  <rect x="476" y="341" width="52" height="24" rx="4" fill="#FEF2F2" stroke="#F87171" stroke-width="0.9"/>
  <text x="502" y="356" text-anchor="middle" class="h-zh" font-size="8.2" fill="#B91C1C">无 I-Cache</text>

  <rect x="258" y="372" width="270" height="15" rx="3" fill="#F9E6DF"/>
  <text x="393" y="382.5" text-anchor="middle" class="mono" font-size="8" fill="#8A341C">32-bit AMBA3 AHB-Lite 总线 · 顺序取指</text>

  <text x="258" y="399" class="h-zh" font-size="9.6" fill="#8A341C">16×32b 通用寄存器文件</text>
  {e9_reg_svg}
  <path d="M 393 425 L 393 430 L 424 430 L 424 425" fill="none" stroke="#B8334A" stroke-width="1.2"/>
  <text x="366" y="441" text-anchor="end" class="h-zh" font-size="8.2" fill="#B8334A">仅 x8, x9 保存</text>
  <line x1="370" y1="438" x2="391" y2="430" stroke="#B8334A" stroke-width="0.8"/>

  <path d="M 393 434 L 393 441 L 525 441 L 525 425" fill="none" stroke="#C95B3B" stroke-width="1.1"/>
  <text x="459" y="452" text-anchor="middle" class="h-zh" font-size="8.4" fill="#8A341C">x8–x15：3 位 RVC 压缩编码窗口</text>

  <rect x="258" y="463" width="84" height="20" rx="3" fill="#FFFFFF" stroke="#E0AC9A" stroke-width="0.9"/>
  <text x="300" y="476" text-anchor="middle" class="b-zh" font-size="8.6">Zicsr 规范适配</text>
  <rect x="348" y="463" width="86" height="20" rx="3" fill="#FFFFFF" stroke="#E0AC9A" stroke-width="0.9"/>
  <text x="391" y="476" text-anchor="middle" class="b-zh" font-size="8.6">.data 完整装载</text>
  <rect x="440" y="463" width="88" height="20" rx="3" fill="#FFFFFF" stroke="#E0AC9A" stroke-width="0.9"/>
  <text x="484" y="476" text-anchor="middle" class="b-zh" font-size="8.6">时钟使能完善</text>
  <text x="392.5" y="499" text-anchor="middle" class="sub" font-size="8.6">RV32EMC / ilp32e · 裸机启动 + RTL 仿真映像</text>

  <!-- Connectors Stage 2 -> Stage 3 -->
  <line x1="540" y1="164" x2="558" y2="164" stroke="#2E5B88" stroke-width="1.8" marker-end="url(#arrB1)"/>
  <line x1="540" y1="398" x2="558" y2="398" stroke="#C95B3B" stroke-width="1.8" marker-end="url(#arrT1)"/>

  <!-- Stage 3 Top: M3 Calibration -->
  <g filter="url(#sh1)">
    <rect x="565" y="54" width="265" height="218" rx="4" fill="#FAFBFD" stroke="#8FB5D9" stroke-width="1.15" stroke-dasharray="4,2"/>
  </g>
  <rect x="577" y="64" width="112" height="18" rx="3" fill="#2E5B88"/>
  <text x="633" y="76" text-anchor="middle" class="h-wh" font-size="8.8">QEMU 行为级仿真</text>
  <text x="818" y="76.5" text-anchor="end" class="mono" font-size="8.4" fill="#475569">mps2-an385</text>

  <rect x="577" y="88" width="241" height="106" rx="3.5" fill="#FFFFFF" stroke="#DCE4EE" stroke-width="1"/>
  <text x="697" y="102" text-anchor="middle" class="h-zh" font-size="9.2" fill="#1D4063">汇编闭环标定：500k × (subs + bne)</text>
  <line x1="612" y1="176" x2="796" y2="176" stroke="#475569" stroke-width="1"/>
  <line x1="612" y1="176" x2="612" y2="112" stroke="#475569" stroke-width="1"/>
  <line x1="612" y1="148" x2="796" y2="148" stroke="#E2E8F0" stroke-width="0.7" stroke-dasharray="2,2"/>
  <line x1="612" y1="122" x2="796" y2="122" stroke="#E2E8F0" stroke-width="0.7" stroke-dasharray="2,2"/>
  <line x1="612" y1="176" x2="758" y2="122" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="3,2"/>
  <circle cx="758" cy="122" r="3" fill="#64748B"/>
  <text x="750" y="121" text-anchor="end" class="sub" font-size="7.6">shift=1: 50,001</text>
  <line x1="612" y1="176" x2="758" y2="148" stroke="#2E5B88" stroke-width="2"/>
  <circle cx="758" cy="148" r="4" fill="#2E5B88" stroke="#FFFFFF" stroke-width="1.2"/>
  <rect x="692" y="156" width="112" height="16" rx="3" fill="#DCE8F5" stroke="#8FB5D9" stroke-width="0.7"/>
  <text x="748" y="167" text-anchor="middle" class="h-zh" font-size="8.0" fill="#1D4063">1 tick ≡ 40 指令</text>
  <text x="607" y="151" text-anchor="end" class="mono" font-size="7.4" fill="#2E5B88">25k</text>
  <text x="607" y="125" text-anchor="end" class="mono" font-size="7.4" fill="#64748B">50k</text>
  <text x="758" y="187" text-anchor="middle" class="mono" font-size="7.6" fill="#475569">10⁶ 动态指令</text>
  <text x="612" y="187" text-anchor="middle" class="mono" font-size="7.6" fill="#475569">0</text>

  <rect x="577" y="202" width="241" height="27" rx="3" fill="#EBF3FA" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="586" y="219" class="h-zh" font-size="9.0" fill="#1D4063">路径 A：≥10 s 长跑校验 · 半主机退出</text>
  <rect x="577" y="235" width="241" height="27" rx="3" fill="#FFFFFF" stroke="#8FB5D9" stroke-width="0.9"/>
  <text x="586" y="252" class="h-zh" font-size="9.0" fill="#334155">路径 B：-icount shift=0 动态指令估算</text>

  <!-- Stage 3 Bottom: E902 RTL Waveform -->
  <g filter="url(#sh1)">
    <rect x="565" y="286" width="265" height="224" rx="4" fill="#FAFBFD" stroke="#E0AC9A" stroke-width="1.15" stroke-dasharray="4,2"/>
  </g>
  <rect x="577" y="296" width="118" height="18" rx="3" fill="#C95B3B"/>
  <text x="636" y="308" text-anchor="middle" class="h-wh" font-size="8.8">RTL 周期精确仿真</text>
  <text x="818" y="308.5" text-anchor="end" class="mono" font-size="8.4" fill="#475569">Icarus 12.0</text>

  <rect x="577" y="320" width="241" height="134" rx="3.5" fill="#FFFFFF" stroke="#E9C3B5" stroke-width="1"/>
  <text x="697" y="333" text-anchor="middle" class="h-zh" font-size="9.2" fill="#8A341C">非侵入式退休指令监测时序波形</text>
  <text x="617" y="347" text-anchor="end" class="mono" font-size="7.6" fill="#475569">clk</text>
  <path d="{clk_path}" fill="none" stroke="#64748B" stroke-width="1.0"/>
  <text x="617" y="373" text-anchor="end" class="mono" font-size="7.6" fill="#2A8C82">win_en</text>
  <path d="M 622 377 L 642 377 L 642 362 L 792 362 L 792 377 L 811 377" fill="none" stroke="#2A8C82" stroke-width="1.5"/>
  <rect x="642" y="362" width="150" height="15" fill="#2A8C82" fill-opacity="0.10"/>
  <text x="717" y="372.5" text-anchor="middle" class="h-zh" font-size="7.8" fill="#175B54">外部地址触发监视窗口</text>
  <text x="617" y="401" text-anchor="end" class="mono" font-size="7.6" fill="#B45309">retire</text>
  <line x1="622" y1="404" x2="811" y2="404" stroke="#CBD5E1" stroke-width="0.9"/>
  {retire_svg}
  <text x="617" y="427" text-anchor="end" class="mono" font-size="7.6" fill="#C95B3B">MCYCLE</text>
  <rect x="653" y="416" width="128" height="14" rx="2.5" fill="#F9E6DF" stroke="#C95B3B" stroke-width="1.1"/>
  <text x="717" y="426" text-anchor="middle" class="mono" font-size="7.6" fill="#8A341C">64 位硬件周期计数器</text>
  <line x1="642" y1="377" x2="642" y2="444" stroke="#2A8C82" stroke-width="0.8" stroke-dasharray="2,2"/>
  <line x1="792" y1="377" x2="792" y2="444" stroke="#2A8C82" stroke-width="0.8" stroke-dasharray="2,2"/>
  <text x="717" y="445" text-anchor="middle" class="h-zh" font-size="8.0" fill="#175B54">双时钟差恒为 17–22 周期</text>

  <rect x="577" y="462" width="241" height="38" rx="4.5" fill="#FAEBE5" stroke="#C95B3B" stroke-width="0.9"/>
  <text x="697" y="478" text-anchor="middle" class="h-zh" font-size="8.9" fill="#8A341C">破解 MINSTRET 置零盲区</text>
  <text x="697" y="493" text-anchor="middle" class="mono" font-size="8.4" fill="#1E293B">实测 CPI = 窗口周期 / 退休指令数</text>

  <!-- Fan-In Orthogonal Bus Connectors -->
  <path d="M 830 164 L 833.5 164 Q 838 164, 838 168.5 L 838 261.5 Q 838 266, 842.5 266 L 848 266" fill="none" stroke="#2E5B88" stroke-width="1.8" marker-end="url(#arrB1)"/>
  <path d="M 830 398 L 833.5 398 Q 838 398, 838 393.5 L 838 298.5 Q 838 294, 842.5 294 L 848 294" fill="none" stroke="#C95B3B" stroke-width="1.8" marker-end="url(#arrT1)"/>

  <!-- Stage 4 Column -->
  <g filter="url(#sh1)">
    <rect x="855" y="54" width="211" height="456" rx="4" fill="#F4FAF9" stroke="#8AC5BE" stroke-width="1.2"/>
  </g>

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
  <text x="960.5" y="133.5" text-anchor="middle" class="sub" font-size="7.8">PERF + VALID 双种子语义等价</text>

  <rect x="866" y="148" width="189" height="122" rx="3.5" fill="#FFFFFF" stroke="#8AC5BE" stroke-width="1"/>
  <text x="960.5" y="165" text-anchor="middle" class="h-zh" font-size="10.2" fill="#175B54">三粒度无偏静态剥离</text>
  <rect x="876" y="173" width="169" height="86" rx="3" fill="#F1F5F9" stroke="#94A3B8" stroke-width="0.9"/>
  <text x="960.5" y="186.5" text-anchor="middle" class="sub" font-size="8.4">粒度① 整包 ELF 映像</text>
  <rect x="886" y="193" width="149" height="59" rx="3" fill="#DCE8F5" stroke="#6C9AC4" stroke-width="0.9"/>
  <text x="960.5" y="206.5" text-anchor="middle" class="h-zh" font-size="8.4" fill="#1D4063">粒度② 五核心算法 .o .text</text>
  <rect x="896" y="213" width="129" height="32" rx="2.5" fill="#2A8C82"/>
  <text x="960.5" y="227" text-anchor="middle" class="h-wh" font-size="8.4">粒度③ 纯 16b/32b 指令流</text>
  <text x="960.5" y="239" text-anchor="middle" font-family="Hiragino Sans GB, sans-serif" font-size="7.6" fill="#D1FAE5">剔除启动段与文字池</text>

  <rect x="866" y="280" width="189" height="132" rx="3.5" fill="#FFFFFF" stroke="#8AC5BE" stroke-width="1"/>
  <text x="960.5" y="297" text-anchor="middle" class="h-zh" font-size="10.2" fill="#175B54">微架构与汇编归因</text>
  <line x1="888" y1="382" x2="1042" y2="382" stroke="#475569" stroke-width="1"/>
  <line x1="888" y1="382" x2="888" y2="308" stroke="#475569" stroke-width="1"/>
  <polyline points="906,332 924,358 944,364 982,371" fill="none" stroke="#2E5B88" stroke-width="2"/>
  <circle cx="906" cy="332" r="2.8" fill="#2E5B88"/><circle cx="944" cy="364" r="2.8" fill="#2E5B88"/><circle cx="982" cy="371" r="2.8" fill="#2E5B88"/>
  <text x="896" y="379" class="h-zh" font-size="7.6" fill="#2E5B88">M3 占优前沿</text>
  <polyline points="918,315 936,348 960,354 1030,357" fill="none" stroke="#C95B3B" stroke-width="2"/>
  <rect x="915" y="312" width="5.5" height="5.5" fill="#C95B3B"/><rect x="957" y="351" width="5.5" height="5.5" fill="#C95B3B"/>
  <circle cx="1030" cy="357" r="4.2" fill="#B8334A" stroke="#FFFFFF" stroke-width="1"/>
  <text x="1002" y="344" text-anchor="middle" class="h-zh" font-size="7.6" fill="#B8334A">RVC 坍塌拐点</text>
  <text x="1002" y="333" text-anchor="middle" class="h-zh" font-size="7.6" fill="#B8334A">CPI 逆向抬升</text>
  <text x="965" y="396" text-anchor="middle" class="sub" font-size="8.0">代码体积 (KiB) →</text>
  <text x="960.5" y="407" text-anchor="middle" class="b-zh" font-size="8.2">矩阵/CRC 热点汇编拆解</text>

  <rect x="866" y="422" width="189" height="78" rx="3.5" fill="url(#gTeal1)"/>
  <text x="960.5" y="440.5" text-anchor="middle" class="h-wh" font-size="10.0">预期科研与工程产出</text>
  <text x="877" y="458.5" font-family="Hiragino Sans GB, sans-serif" font-size="8.5" fill="#E6FFFA">(1) 可复现双平台评测框架</text>
  <text x="877" y="474.5" font-family="Hiragino Sans GB, sans-serif" font-size="8.5" fill="#E6FFFA">(2) 全谱系性能与码流数据集</text>
  <text x="877" y="490.5" font-family="Hiragino Sans GB, sans-serif" font-size="8.5" fill="#E6FFFA">(3) 严守跨仿真层级推论边界</text>
</svg>
"""
    p = OUT_DIR / "fig1_tech_roadmap.svg"
    p.write_text(svg, encoding="utf-8")
    return p


def write_fig2_timing_arch():
    """ISCA / ISSCC Hardware Timing & Signal Instrumentation Schematic (Calibration Plot + 5-Track RTL Waveform)."""
    clk_wave = _make_clk_wave(596, 86, 98, 22, 16.5)
    # Discrete retire pulses inside active win_en (x=646..908)
    ret_svg = "\n  ".join([
        f'<path d="M {px:.1f} 254 L {px:.1f} 237 L {px+6.5:.1f} 237 L {px+6.5:.1f} 254" fill="#FDE68A" stroke="#B45309" stroke-width="1.15"/>'
        for px in [656, 672.5, 689, 722, 738.5, 755, 788, 804.5, 821, 854, 870.5, 887]
    ])

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 400" width="1040" height="400">
  <defs>
    <filter id="sh2" x="-2%" y="-2%" width="104%" height="106%">
      <feDropShadow dx="0" dy="1.0" stdDeviation="1.2" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
    <linearGradient id="gB2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2E5B88"/><stop offset="100%" stop-color="#1D4063"/>
    </linearGradient>
    <linearGradient id="gT2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C95B3B"/><stop offset="100%" stop-color="#9A3B20"/>
    </linearGradient>
    <marker id="arrB2" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="7.5" markerHeight="7.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2E5B88"/>
    </marker>
    <marker id="arrD2" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="7.5" markerHeight="7.5" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#475569"/>
    </marker>
    <marker id="arrG2" viewBox="0 0 10 10" refX="2.5" refY="5" markerWidth="5.2" markerHeight="5.2" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
      <path d="M 0 1.2 L 9.5 5 L 0 8.8 L 2.2 5 z" fill="#2A8C82"/>
    </marker>
    <style>
      .h-zh {{ font-family: "Hiragino Sans GB", "Heiti SC", "Helvetica Neue", sans-serif; font-weight: 700; fill: #1E293B; }}
      .h-wh {{ font-family: "Hiragino Sans GB", "Heiti SC", "Helvetica Neue", sans-serif; font-weight: 700; fill: #FFFFFF; }}
      .b-zh {{ font-family: "Hiragino Sans GB", "Helvetica Neue", sans-serif; fill: #334155; }}
      .sub  {{ font-family: "Hiragino Sans GB", "Helvetica Neue", sans-serif; fill: #64748B; }}
      .mono {{ font-family: "Menlo", "Helvetica Neue", monospace; font-weight: 700; }}
    </style>
  </defs>

  <rect x="0" y="0" width="1040" height="400" fill="#FFFFFF"/>

  <!-- ==================== LEFT PANEL (a): CORTEX-M3 DUAL-PATH & CALIBRATION ==================== -->
  <g filter="url(#sh2)">
    <rect x="16" y="14" width="490" height="372" rx="4" fill="#F6FAFE" stroke="#8FB5D9" stroke-width="1.2"/>
    <rect x="16" y="14" width="490" height="32" rx="4" fill="url(#gB2)"/>
    <rect x="16" y="38" width="490" height="8" fill="url(#gB2)"/>
  </g>
  <text x="261" y="34.5" text-anchor="middle" class="h-wh" font-size="12">(a) Arm Cortex-M3：64 位 SysTick 解耦双路径与汇编闭环标定</text>

  <!-- Top Hardware Counter Chain -->
  <rect x="32" y="58" width="136" height="48" rx="5.5" fill="#FFFFFF" stroke="#2E5B88" stroke-width="1.15"/>
  <text x="100" y="77" text-anchor="middle" class="h-zh" font-size="10.2" fill="#1D4063">24 位 SysTick</text>
  <text x="100" y="94" text-anchor="middle" class="mono" font-size="8.4" fill="#475569">25 MHz + 溢出中断</text>

  <line x1="168" y1="82" x2="185" y2="82" stroke="#2E5B88" stroke-width="1.45" marker-end="url(#arrB2)"/>

  <rect x="191" y="58" width="122" height="48" rx="5.5" fill="#DCE8F5" stroke="#2E5B88" stroke-width="1.15"/>
  <text x="252" y="77" text-anchor="middle" class="h-zh" font-size="10.2" fill="#1D4063">64 位单调时钟</text>
  <text x="252" y="94" text-anchor="middle" class="mono" font-size="8.4" fill="#1D4063">Δticks 差值采样</text>

  <!-- Two-Way Orthogonal Switch Branches -->
  <path d="M 313 74 L 321 74 Q 324 74, 324 72 Q 324 70, 327 70 L 339 70" fill="none" stroke="#475569" stroke-width="1.35" marker-end="url(#arrD2)"/>
  <path d="M 313 90 L 320 90 Q 324 90, 324 94 L 324 104 Q 324 108, 328 108 L 339 108" fill="none" stroke="#2E5B88" stroke-width="1.45" marker-end="url(#arrB2)"/>

  <rect x="345" y="54" width="146" height="32" rx="4.5" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
  <text x="418" y="68" text-anchor="middle" class="h-zh" font-size="8.8">路径 A：≥10 s 长跑合规</text>
  <text x="418" y="81" text-anchor="middle" class="sub" font-size="7.8">30k–40k 轮 · 半主机退出</text>

  <rect x="345" y="92" width="146" height="32" rx="4.5" fill="#2E5B88"/>
  <text x="418" y="106" text-anchor="middle" class="h-wh" font-size="8.8">路径 B：-icount 指令估算</text>
  <text x="418" y="119" text-anchor="middle" font-family="Hiragino Sans GB, sans-serif" font-size="7.8" fill="#DCE8F5">1 轮/20 轮 ≈ Δticks × 40</text>

  <!-- Embedded Full Linear Calibration Verification Graph -->
  <rect x="32" y="136" width="458" height="190" rx="6" fill="#FFFFFF" stroke="#BDD4EA" stroke-width="1"/>
  <text x="261" y="154" text-anchor="middle" class="h-zh" font-size="10.4" fill="#1D4063">汇编闭环标定验证曲线 · 500k × (subs + bne) = 10⁶ 指令</text>

  <!-- Plot Grid & Axes -->
  <line x1="94" y1="294" x2="456" y2="294" stroke="#334155" stroke-width="1.1"/>
  <line x1="94" y1="294" x2="94"  y2="168" stroke="#334155" stroke-width="1.1"/>
  <line x1="94" y1="252" x2="456" y2="252" stroke="#E2E8F0" stroke-width="0.8" stroke-dasharray="3,2"/>
  <line x1="94" y1="210" x2="456" y2="210" stroke="#E2E8F0" stroke-width="0.8" stroke-dasharray="3,2"/>
  <line x1="94" y1="176" x2="456" y2="176" stroke="#E2E8F0" stroke-width="0.8" stroke-dasharray="3,2"/>
  <line x1="252" y1="294" x2="252" y2="168" stroke="#E2E8F0" stroke-width="0.8" stroke-dasharray="3,2"/>
  <line x1="410" y1="294" x2="410" y2="168" stroke="#E2E8F0" stroke-width="0.8" stroke-dasharray="3,2"/>

  <!-- shift=1 line -->
  <line x1="94" y1="294" x2="410" y2="176" stroke="#64748B" stroke-width="1.7" stroke-dasharray="5,3"/>
  <circle cx="410" cy="176" r="4.5" fill="#64748B" stroke="#FFFFFF" stroke-width="1.3"/>
  <rect x="278" y="168" width="122" height="20" rx="4" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="339" y="181" text-anchor="middle" class="mono" font-size="8.2" fill="#334155">shift=1: 50,001 ticks</text>

  <!-- shift=0 primary line -->
  <line x1="94" y1="294" x2="410" y2="235" stroke="#2E5B88" stroke-width="2.5"/>
  <circle cx="252" cy="264.5" r="3.6" fill="#6C9AC4" stroke="#FFFFFF" stroke-width="1.1"/>
  <circle cx="410" cy="235" r="5.2" fill="#2E5B88" stroke="#FFFFFF" stroke-width="1.5"/>
  <rect x="248" y="264" width="196" height="22" rx="3" fill="#DCE8F5" stroke="#2E5B88" stroke-width="0.9"/>
  <text x="346" y="278" text-anchor="middle" class="h-zh" font-size="8.6" fill="#1D4063">shift=0: 25,000 → 1 tick ≡ 40 指令</text>

  <!-- Axis Ticks & Labels -->
  <text x="88" y="297" text-anchor="end" class="mono" font-size="8.2" fill="#475569">0</text>
  <text x="88" y="238" text-anchor="end" class="mono" font-size="8.2" fill="#2E5B88">25k</text>
  <text x="88" y="179" text-anchor="end" class="mono" font-size="8.2" fill="#64748B">50k</text>
  <text x="52" y="234" text-anchor="middle" class="h-zh" font-size="8.8" fill="#334155" transform="rotate(-90,52,234)">SysTick 差值 (ticks)</text>
  <text x="94"  y="309" text-anchor="middle" class="mono" font-size="8.2" fill="#475569">0</text>
  <text x="252" y="309" text-anchor="middle" class="mono" font-size="8.2" fill="#475569">0.5×10⁶</text>
  <text x="410" y="309" text-anchor="middle" class="mono" font-size="8.2" fill="#475569">1.0×10⁶ 动态指令</text>

  <!-- Bottom Boundary Callout -->
  <rect x="32" y="336" width="458" height="38" rx="5.5" fill="#EBF3FA" stroke="#8FB5D9" stroke-width="1"/>
  <text x="261" y="352" text-anchor="middle" class="h-zh" font-size="9.4" fill="#1D4063">口径界定：墙上时钟仅用于 ≥10 s 合规校验，跨平台比较采用标定动态指令数</text>
  <text x="261" y="367" text-anchor="middle" class="sub" font-size="8.6">1 轮与 20 轮 -icount 均值偏差 &lt; 0.02%，量化精度满足跨架构对比要求</text>

  <!-- ==================== RIGHT PANEL (b): E902 5-TRACK RTL SIGNAL TIMING ==================== -->
  <g filter="url(#sh2)">
    <rect x="524" y="14" width="500" height="372" rx="4" fill="#FDF7F4" stroke="#E0AC9A" stroke-width="1.2"/>
    <rect x="524" y="14" width="500" height="32" rx="4" fill="url(#gT2)"/>
    <rect x="524" y="38" width="500" height="8" fill="url(#gT2)"/>
  </g>
  <text x="774" y="34.5" text-anchor="middle" class="h-wh" font-size="12">(b) 玄铁 E902：周期精确 RTL 多信号时序与双时钟交叉互验</text>

  <!-- Signal Waveform Canvas -->
  <rect x="538" y="58" width="472" height="256" rx="6" fill="#FFFFFF" stroke="#E9C3B5" stroke-width="1"/>
  <text x="774" y="75" text-anchor="middle" class="h-zh" font-size="10.2" fill="#8A341C">RTL 顶层非侵入式硬件退休监视时序 · 100 MHz</text>

  <!-- Vertical Boundary Reference Guides -->
  <line x1="646" y1="84" x2="646" y2="298" stroke="#2A8C82" stroke-width="1.0" stroke-dasharray="3,2"/>
  <line x1="678" y1="184" x2="678" y2="298" stroke="#C95B3B" stroke-width="1.0" stroke-dasharray="3,2"/>
  <line x1="876" y1="184" x2="876" y2="298" stroke="#C95B3B" stroke-width="1.0" stroke-dasharray="3,2"/>
  <line x1="908" y1="84" x2="908" y2="298" stroke="#2A8C82" stroke-width="1.0" stroke-dasharray="3,2"/>

  <!-- Track 1: clk -->
  <text x="590" y="96" text-anchor="end" class="mono" font-size="8.4" fill="#334155">clk</text>
  <path d="{clk_wave}" fill="none" stroke="#64748B" stroke-width="1.05"/>

  <!-- Track 2: AHB trigger write -->
  <text x="590" y="131" text-anchor="end" class="mono" font-size="8.4" fill="#5C4D9A">AHB_wr</text>
  <line x1="596" y1="135" x2="960" y2="135" stroke="#CBD5E1" stroke-width="1"/>
  <rect x="633" y="117" width="26" height="18" rx="3" fill="#EDE9FE" stroke="#5C4D9A" stroke-width="1.1"/>
  <text x="646" y="129" text-anchor="middle" class="mono" font-size="7.6" fill="#4C1D95">Wr=1</text>
  <rect x="895" y="117" width="26" height="18" rx="3" fill="#EDE9FE" stroke="#5C4D9A" stroke-width="1.1"/>
  <text x="908" y="129" text-anchor="middle" class="mono" font-size="7.6" fill="#4C1D95">Wr=2</text>
  <text x="774" y="129" text-anchor="middle" class="sub" font-size="8.0">写监视触发地址 · 零硬件改动侵入</text>

  <!-- Track 3: win_en -->
  <text x="590" y="168" text-anchor="end" class="mono" font-size="8.4" fill="#2A8C82">win_en</text>
  <path d="M 596 173 L 646 173 L 646 153 L 908 153 L 908 173 L 960 173" fill="none" stroke="#2A8C82" stroke-width="1.8"/>
  <rect x="646" y="153" width="262" height="20" fill="#2A8C82" fill-opacity="0.11"/>
  <text x="777" y="166.5" text-anchor="middle" class="h-zh" font-size="8.6" fill="#175B54">监视窗口开启：同步累加窗口总周期与退休脉冲</text>

  <!-- Track 4: MCYCLE software window -->
  <text x="590" y="207" text-anchor="end" class="mono" font-size="8.4" fill="#C95B3B">MCYCLE</text>
  <line x1="596" y1="203" x2="678" y2="203" stroke="#E2E8F0" stroke-width="1.2"/>
  <line x1="876" y1="203" x2="960" y2="203" stroke="#E2E8F0" stroke-width="1.2"/>
  <rect x="678" y="192" width="198" height="22" rx="3.5" fill="#F9E6DF" stroke="#C95B3B" stroke-width="1.3"/>
  <text x="777" y="206.5" text-anchor="middle" class="h-zh" font-size="8.6" fill="#8A341C">软件 64 位 MCYCLE(0xB00) 读数窗口</text>

  <!-- Track 5: biu_pad_retire -->
  <text x="590" y="250" text-anchor="end" class="mono" font-size="8.4" fill="#B45309">retire</text>
  <line x1="596" y1="254" x2="960" y2="254" stroke="#CBD5E1" stroke-width="1"/>
  {ret_svg}
  <text x="965" y="248" class="h-zh" font-size="7.6" fill="#B45309">退休脉冲</text>

  <!-- Caliper Dimension Arrows showing δ1 + δ2 = 17-22 cycles -->
  <line x1="650.2" y1="274" x2="673.8" y2="274" stroke="#2A8C82" stroke-width="1.2" marker-start="url(#arrG2)" marker-end="url(#arrG2)"/>
  <text x="662" y="287" text-anchor="middle" class="mono" font-size="8.0" fill="#175B54">δ₁</text>
  <line x1="880.2" y1="274" x2="903.8" y2="274" stroke="#2A8C82" stroke-width="1.2" marker-start="url(#arrG2)" marker-end="url(#arrG2)"/>
  <text x="892" y="287" text-anchor="middle" class="mono" font-size="8.0" fill="#175B54">δ₂</text>
  <rect x="694" y="268" width="166" height="24" rx="3" fill="#E6F4F2" stroke="#8AC5BE" stroke-width="0.9"/>
  <text x="777" y="283.5" text-anchor="middle" class="h-zh" font-size="8.5" fill="#175B54">δ₁ + δ₂ 恒为 17–22 周期</text>
  <text x="777" y="306" text-anchor="middle" class="sub" font-size="8.2">对应起止边界“写标记—读 CSR”固定指令间隔</text>

  <!-- Bottom CPI Formula & MINSTRET Note -->
  <rect x="538" y="324" width="472" height="50" rx="5.5" fill="#FAEBE5" stroke="#C95B3B" stroke-width="1"/>
  <text x="774" y="343" text-anchor="middle" class="h-zh" font-size="9.6" fill="#8A341C">硬件核查：RTL 中 MINSTRET(0xB02) 固定置零 → 外部监视退休信号零侵入补全</text>
  <text x="774" y="363" text-anchor="middle" class="mono" font-size="9.4" fill="#1E293B">实测微架构 CPI = 监视窗口周期数 / 采样退休指令总数</text>
</svg>
"""
    p = OUT_DIR / "fig2_timing_architecture.svg"
    p.write_text(svg, encoding="utf-8")
    return p


def write_fig3_preliminary_svg():
    """IEEE / NeurIPS / Nature style 2-panel baseline comparison (dynamic insns + pure code density & 16b ratio)."""
    setup_pub_rc()

    opts = ["-Os", "-O2", "-O3", "-O3\n-funroll-loops"]
    m3_dyn = [365.840, 295.760, 281.520, 263.800]
    e9_dyn = [420.714, 318.606, 303.457, 295.724]

    data = {c["name"]: c for c in json.load(open(ROOT_DIR / "benchmark/results/elf_analysis.json"))}
    keys = ["Os", "O2", "O3", "O3_unroll"]
    m3_kib = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["bytes"] / 1024.0 for k in keys]
    e9_kib = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["bytes"] / 1024.0 for k in keys]
    m3_bytes = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["bytes"] for k in keys]
    e9_bytes = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["bytes"] for k in keys]
    m3_pct16 = [data[f"m3_{k}"]["disasm"]["coremark_funcs"]["pct_16b"] for k in keys]
    e9_pct16 = [data[f"e902_{k}"]["disasm"]["coremark_funcs"]["pct_16b"] for k in keys]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.05), dpi=200)
    plt.subplots_adjust(wspace=0.28, top=0.80, bottom=0.135, left=0.065, right=0.935)

    x = np.arange(len(opts)) * 1.22
    w = 0.39

    # ---------------- Panel (a): Dynamic Instructions with Delta Brackets ----------------
    ax1.grid(axis="y", zorder=0)
    ax1.bar(x - w/2, m3_dyn, w, color=PALETTE["m3"], edgecolor="#FFFFFF", linewidth=0.9, zorder=3,
            label="Arm Cortex-M3（QEMU -icount 估计）")
    ax1.bar(x + w/2, e9_dyn, w, color=PALETTE["e9"], edgecolor="#FFFFFF", linewidth=0.9, zorder=3,
            label="玄铁 E902（RTL 退休指令精确计数）")

    add_panel_header(ax1, "a", "每轮动态执行指令数对比", y_offset=1.135)
    ax1.set_ylabel("每轮动态指令数（千条 / 轮）", fontsize=9.5, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(opts, fontsize=9.0)
    ax1.set_ylim(0, 505)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(loc="upper left", bbox_to_anchor=(-0.01, 1.115), ncol=2, fontsize=7.5, columnspacing=0.9, handletextpad=0.4)

    for i in range(len(opts)):
        red = 100.0 * (m3_dyn[i] - e9_dyn[i]) / e9_dyn[i]
        ax1.text(x[i] - w/2, m3_dyn[i] - 18, f"{m3_dyn[i]:.1f}k", ha="center", va="top",
                 fontsize=7.3, color="#FFFFFF", fontweight="bold", zorder=5)
        ax1.text(x[i] + w/2, e9_dyn[i] - 18, f"{e9_dyn[i]:.1f}k", ha="center", va="top",
                 fontsize=7.3, color="#FFFFFF", fontweight="bold", zorder=5)
        y_top = e9_dyn[i] + 16
        ax1.plot([x[i] - w/2, x[i] - w/2, x[i] + w/2, x[i] + w/2],
                 [m3_dyn[i] + 6, y_top, y_top, e9_dyn[i] + 6],
                 color=PALETTE["muted"], linewidth=0.9, zorder=4)
        ax1.text(x[i], y_top + 6, f"M3 {red:.1f}%", ha="center", va="bottom",
                 fontsize=7.8, fontweight="bold", color=PALETTE["m3_dark"],
                 bbox=dict(boxstyle="round,pad=0.16", fc=PALETTE["m3_pale"], ec="none"))

    # ---------------- Panel (b): Pure Code Footprint (Bars) + 16-bit Ratio (Dual Axis Lines) ----------------
    ax2.grid(axis="y", zorder=0)
    # Soft rose highlight on -O3 -funroll-loops RVC collapse
    ax2.axvspan(x[3] - 0.50, x[3] + 0.50, color="#FEE2E2", alpha=0.42, zorder=1)

    ax2.bar(x - w/2, m3_kib, w, color=PALETTE["m3"], edgecolor="#FFFFFF", linewidth=0.9, alpha=0.88, zorder=3,
            label="M3 核心代码体积 (KiB)")
    ax2.bar(x + w/2, e9_kib, w, color=PALETTE["e9"], edgecolor="#FFFFFF", linewidth=0.9, alpha=0.88, zorder=3,
            label="E902 核心代码体积 (KiB)")

    for i in range(len(opts)):
        # Place byte label neatly above short bars or centered inside tall bars
        if m3_kib[i] > 6.5:
            ax2.text(x[i] - w/2, m3_kib[i] * 0.46, f"{m3_bytes[i]:,}\nB", ha="center", va="center",
                     fontsize=7.2, color="#FFFFFF", fontweight="bold", zorder=4)
        else:
            ax2.text(x[i] - w/2, m3_kib[i] + 0.32, f"{m3_bytes[i]:,} B", ha="center", va="bottom",
                     fontsize=6.9, color=PALETTE["m3_dark"], fontweight="bold", zorder=4)
        if e9_kib[i] > 6.5:
            ax2.text(x[i] + w/2, e9_kib[i] * 0.46, f"{e9_bytes[i]:,}\nB", ha="center", va="center",
                     fontsize=7.2, color="#FFFFFF", fontweight="bold", zorder=4)
        else:
            ax2.text(x[i] + w/2, e9_kib[i] + 0.32, f"{e9_bytes[i]:,} B", ha="center", va="bottom",
                     fontsize=6.9, color=PALETTE["e9_dark"], fontweight="bold", zorder=4)

    add_panel_header(ax2, "b", "CoreMark 核心函数纯指令体积与 16 位压缩占比", y_offset=1.135)
    ax2.set_ylabel("核心函数纯指令体积（KiB，不含文字池）", fontsize=9.5, fontweight="bold", color=PALETTE["slate"])
    ax2.set_xticks(x)
    ax2.set_xticklabels(opts, fontsize=9.0)
    ax2.set_ylim(0, 23.5)
    ax2.spines["top"].set_visible(False)

    ax2r = ax2.twinx()
    ax2r.plot(x, m3_pct16, color=PALETTE["m3_dark"], marker="o", linestyle="-", linewidth=2.0, markersize=6.4,
              markeredgecolor="#FFFFFF", markeredgewidth=1.1, zorder=6, label="M3 16 位占比 (%)")
    ax2r.plot(x, e9_pct16, color=PALETTE["crimson"], marker="s", linestyle="--", linewidth=2.0, markersize=6.2,
              markeredgecolor="#FFFFFF", markeredgewidth=1.1, zorder=7, label="E902 16 位占比 (%)")
    ax2r.set_ylabel("纯核心函数 16 位指令占比（%）", fontsize=9.5, fontweight="bold", color=PALETTE["crimson"])
    ax2r.set_ylim(8, 84)
    ax2r.spines["top"].set_visible(False)
    ax2r.spines["right"].set_color(PALETTE["crimson"])
    ax2r.tick_params(axis="y", colors=PALETTE["crimson"])

    pill = dict(boxstyle="round,pad=0.14", fc="#FFFFFF", ec="none", alpha=0.90)
    m3_off = [(0, 10), (0, 10), (0, -16), (0, 10)]
    e9_off = [(0, -16), (0, -16), (0, 10), (-36, 18)]
    for i in range(len(opts)):
        ax2r.annotate(f"{m3_pct16[i]:.1f}%", (x[i], m3_pct16[i]), textcoords="offset points", xytext=m3_off[i],
                      ha="center", fontsize=7.4, fontweight="bold", color=PALETTE["m3_dark"], bbox=pill, zorder=8)
        if i == 3:
            ax2r.annotate("42.6%\n(压缩坍塌)", (x[i], e9_pct16[i]), textcoords="offset points", xytext=(-44, 18),
                          ha="center", fontsize=7.4, fontweight="bold", color=PALETTE["crimson"],
                          bbox=dict(boxstyle="round,pad=0.18", fc="#FFF5F5", ec="#FCA5A5", lw=0.7),
                          arrowprops=dict(arrowstyle="->", color=PALETTE["crimson"], lw=1.0), zorder=8)
        else:
            ax2r.annotate(f"{e9_pct16[i]:.1f}%", (x[i], e9_pct16[i]), textcoords="offset points", xytext=e9_off[i],
                          ha="center", fontsize=7.4, fontweight="bold", color=PALETTE["crimson"], bbox=pill, zorder=8)

    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2r.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper left", bbox_to_anchor=(-0.02, 1.125), ncol=2, fontsize=7.3, columnspacing=0.8, handletextpad=0.35)

    p = OUT_DIR / "fig3_preliminary_results.svg"
    plt.savefig(p, format="svg")
    plt.close(fig)
    return p


if __name__ == "__main__":
    p1 = write_fig1_roadmap()
    p2 = write_fig2_timing_arch()
    p3 = write_fig3_preliminary_svg()
    print("Generated 3 IEEE/NeurIPS-grade Proposal SVGs:", p1, p2, p3)
