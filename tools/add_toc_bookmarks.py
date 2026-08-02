#!/usr/bin/env python3
"""给成书 PDF 补书签目录（PDF outline / bookmarks）。

背景：issue #2「如果生成的PDF能够有目录就好了」。
书内正文第 2-3 页有印刷版目录，但 PDF 文件本身没有大纲书签，
阅读器侧边栏是空的，长文档跳转很费劲。

做法：扫描每一页的首行，找到 §01–§21 各节的起始页（自动定位，
不写死页码，换版本重跑即可），再按 Part 分组写入两级书签。
节标题用书内目录页的原文（提取文本有断字，不能直接用）。

用法：
    pip install pypdf
    python3 tools/add_toc_bookmarks.py            # 处理仓库根目录两本 PDF，原地覆盖
    python3 tools/add_toc_bookmarks.py 某本.pdf   # 只处理指定文件
"""

import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

REPO_ROOT = Path(__file__).resolve().parent.parent

# 每本书：文件名 -> (封面/目录条目文案, Part 列表)
# Part: (Part 标题, {节号: 节标题})
BOOKS = {
    "Hermes-Agent橙皮书2.0-v260607.pdf": (
        ("封面", "目录"),
        [
            ("Part 1: 这是什么", {
                1: "§01 先认识 Hermes：一个会自己长本事的 Agent",
                2: "§02 60 秒全景：一个大脑，很多张脸",
                3: "§03 Nous 为什么做这件事",
            }),
            ("Part 2: 缰绳会自己长", {
                4: "§04 造、修、续：自改进的三台引擎",
                5: "§05 Curator：给自进化装刹车",
                6: "§06 最该学的是「不要学」",
            }),
            ("Part 3: 它怎么记住你", {
                7: "§07 三层记忆：从金鱼到老友",
                8: "§08 会话搜索：把不该用 LLM 的活要回来",
                9: "§09 Skill 系统与开放标准红利",
                10: "§10 一个 agent 指挥一群 agent",
            }),
            ("Part 4: 连接一切", {
                11: "§11 64 个工具与按需暴露",
                12: "§12 MCP 的两个方向",
                13: "§13 23 个平台与会自生长的 Gateway",
                14: "§14 三种和它说话的姿势",
            }),
            ("Part 5: 多 Agent 与编排", {
                15: "§15 从 delegate_task 到 Kanban 平台",
                16: "§16 笨内核 + 用户空间装饰",
                17: "§17 八种协作模式与按卡片控成本",
            }),
            ("Part 6: 部署、安全与边界", {
                18: "§18 部署：从发命令到发安装包",
                19: "§19 唯一的边界是操作系统",
                20: "§20 Promptware 防御与可观测性",
                21: "§21 自改进 Agent 能走多远",
            }),
        ],
    ),
    "Hermes-Agent-The-Complete-Guide-v260607.pdf": (
        ("Cover", "Contents"),
        [
            ("Part 1: What This Is", {
                1: "§01 Meet Hermes: An Agent That Grows Its Own Skills",
                2: "§02 60-Second Overview: One Brain, Many Faces",
                3: "§03 Why Nous Built This",
            }),
            ("Part 2: The Reins Grow by Themselves", {
                4: "§04 Build, Repair, Continue: Three Engines of Self-Improvement",
                5: "§05 Curator: Brakes for Self-Evolution",
                6: "§06 The Most Important Lesson Is What Not to Learn",
            }),
            ("Part 3: How It Remembers You", {
                7: "§07 Three Layers of Memory: From Goldfish to Old Friend",
                8: "§08 Session Search: Taking Back the Work LLMs Should Not Do",
                9: "§09 The Skill System and the Open-Standard Dividend",
                10: "§10 One Agent Commanding a Swarm of Agents",
            }),
            ("Part 4: Connecting Everything", {
                11: "§11 64 Tools and Exposure on Demand",
                12: "§12 MCP in Two Directions",
                13: "§13 23 Platforms and a Self-Growing Gateway",
                14: "§14 Three Ways to Talk to It",
            }),
            ("Part 5: Multi-Agent & Orchestration", {
                15: "§15 From delegate_task to a Kanban Platform",
                16: "§16 Dumb Core, Userspace Decoration",
                17: "§17 Eight Collaboration Patterns and Per-Card Cost Control",
            }),
            ("Part 6: Deployment, Security & Limits", {
                18: "§18 Deploy: From Sending Commands to Sending Installers",
                19: "§19 The Only Boundary Is the Operating System",
                20: "§20 Promptware Defense and Observability",
                21: "§21 How Far Can a Self-Improving Agent Go",
            }),
        ],
    ),
}

SECTION_RE = re.compile(r"§\s*(\d{2})")


def find_section_pages(reader: PdfReader) -> dict[int, int]:
    """扫描每页首行，返回 {节号: 0-based 页码}。只认每节第一次出现。"""
    pages: dict[int, int] = {}
    for i, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        first_line = text.split("\n", 1)[0]
        m = SECTION_RE.match(first_line)
        if m:
            num = int(m.group(1))
            pages.setdefault(num, i)
    return pages


def add_bookmarks(pdf_path: Path) -> None:
    (cover_label, toc_label), parts = BOOKS[pdf_path.name]
    reader = PdfReader(pdf_path)
    section_pages = find_section_pages(reader)

    expected = {n for _, secs in parts for n in secs}
    missing = sorted(expected - set(section_pages))
    if missing:
        raise SystemExit(f"{pdf_path.name}: 定位不到这些节的起始页：{missing}，中止。")

    writer = PdfWriter(clone_from=reader)
    writer.add_outline_item(cover_label, 0)
    writer.add_outline_item(toc_label, 1)
    for part_title, secs in parts:
        first_page = section_pages[min(secs)]
        parent = writer.add_outline_item(part_title, first_page)
        for num in sorted(secs):
            writer.add_outline_item(secs[num], section_pages[num], parent=parent)

    tmp = pdf_path.with_suffix(".tmp.pdf")
    with open(tmp, "wb") as f:
        writer.write(f)
    tmp.replace(pdf_path)
    print(f"{pdf_path.name}: 写入 2 + {len(parts)} + {len(expected)} 条书签，"
          f"§01 在第 {section_pages[1] + 1} 页。")


def main() -> None:
    targets = [Path(p) for p in sys.argv[1:]] or [REPO_ROOT / name for name in BOOKS]
    for path in targets:
        if path.name not in BOOKS:
            raise SystemExit(f"不认识 {path.name}，本脚本只处理：{', '.join(BOOKS)}")
        add_bookmarks(path)


if __name__ == "__main__":
    main()
