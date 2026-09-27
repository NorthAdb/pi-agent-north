"""课程 QA：① 每课 data-quiz JSON 合法性；② 全站相对链接完整性；③ 测验选项长度平衡。
用法：python qa.py （在 agent-harness-course/ 下运行）"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
issues = []


def check_quizzes():
    for lesson in sorted((ROOT / "lessons").glob("0*.html")):
        html = lesson.read_text(encoding="utf-8")
        for m in re.finditer(r"data-quiz='([^']*)'", html, re.S):
            try:
                data = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                issues.append(f"[quiz-json] {lesson.name}: JSON 解析失败 {e}")
                continue
            for i, item in enumerate(data.get("items", [])):
                opts = item.get("options", [])
                ans = item.get("answer")
                if not (0 <= ans < len(opts)):
                    issues.append(f"[quiz-answer] {lesson.name} Q{i+1}: answer={ans} 越界")
                if len(set(map(str, opts))) != len(opts):
                    issues.append(f"[quiz-dup] {lesson.name} Q{i+1}: 选项重复")
                # 平衡性：正确答案不应是唯一显著最长项
                lens = [len(str(o)) for o in opts]
                if lens[ans] == max(lens) and lens[ans] - sorted(lens)[-2] > 8:
                    issues.append(f"[quiz-balance] {lesson.name} Q{i+1}: 正确答案比次长项长 "
                                  f"{lens[ans] - sorted(lens)[-2]} 字符（可能提示性）")


def check_links():
    pages = list((ROOT / "lessons").glob("0*.html")) + \
            list((ROOT / "reference").glob("*.html")) + \
            [ROOT / "COURSE.md", ROOT / "index.html", ROOT / "diagrams.html"]
    for page in pages:
        base = page.parent
        text = page.read_text(encoding="utf-8")
        for m in re.finditer(r'(?:href|src)="([^"]+)"', text):
            url = m.group(1)
            if url.startswith(("http", "#", "mailto:", "data:")):
                continue
            target = (base / url.split("#")[0]).resolve()
            if not url.split("#")[0]:
                continue
            if not target.exists():
                issues.append(f"[broken-link] {page.name}: {url}")


def check_nav():
    """课程导航一致性：每课的上一课/下一课必须与课程顺序吻合。"""
    order = ["0001-why-llm-is-not-agent", "0002-agent-loop", "0003-tool-calling",
             "0004-context-assembly", "0005-session-tree", "0006-compaction",
             "0007-skills", "0008-extensions", "0009-capability-boundary",
             "0010-interfaces", "0011-full-runtime", "0012-generic-harness",
             "0013-comparison", "0014-mental-model"]
    for i, slug in enumerate(order):
        p = ROOT / "lessons" / f"{slug}.html"
        html = p.read_text(encoding="utf-8")
        prev = "../COURSE.md" if i == 0 else f"{order[i - 1]}.html"
        nxt = ("../reference/minimal-harness.html" if i == len(order) - 1
               else f"{order[i + 1]}.html")
        if f'href="{prev}"' not in html:
            issues.append(f"[nav] {slug}: 上一课应为 {prev}")
        if f'href="{nxt}"' not in html:
            issues.append(f"[nav] {slug}: 下一课应为 {nxt}")


def check_lesson_diagram():
    """课图交叉引用：有图的课必须恰好嵌入自己的那张图；0013 例外（表驱动无图）。"""
    mapping = {"0001-why-llm-is-not-agent": "01-harness-overview",
               "0002-agent-loop": "02-agent-loop", "0003-tool-calling": "03-tool-calling",
               "0004-context-assembly": "04-context-assembly",
               "0005-session-tree": "05-session-tree", "0006-compaction": "06-compaction",
               "0007-skills": "07-skills", "0008-extensions": "08-extensions",
               "0009-capability-boundary": "09-capability-boundary",
               "0010-interfaces": "10-interfaces", "0011-full-runtime": "11-full-runtime",
               "0012-generic-harness": "12-generic-harness",
               "0014-mental-model": "13-mental-model"}
    for slug, diagram in mapping.items():
        html = (ROOT / "lessons" / f"{slug}.html").read_text(encoding="utf-8")
        expected = f"diagrams/{diagram}.html"
        if html.count(f'src="{expected}"') != 1:
            issues.append(f"[lesson-diagram] {slug}: 应恰好嵌入一次 {expected}")
        if f'href="{expected}"' not in html:
            issues.append(f"[lesson-diagram] {slug}: 缺少全屏打开链接 {expected}")
    no_diagram = "0013-comparison"
    html = (ROOT / "lessons" / f"{no_diagram}.html").read_text(encoding="utf-8")
    if "figure.diagram" in html:
        issues.append(f"[lesson-diagram] {no_diagram}: 表驱动课不应嵌图")


def check_basics():
    for lesson in sorted((ROOT / "lessons").glob("0*.html")):
        html = lesson.read_text(encoding="utf-8")
        if "course.css" not in html:
            issues.append(f"[style] {lesson.name}: 未引用 course.css")
        if 'data-quiz' in html and "quiz.js" not in html:
            issues.append(f"[quiz-js] {lesson.name}: 有测验但未引入 quiz.js")
        if "</html>" not in html:
            issues.append(f"[html] {lesson.name}: 未闭合")


if __name__ == "__main__":
    check_quizzes()
    check_links()
    check_nav()
    check_lesson_diagram()
    check_basics()
    if issues:
        print(f"发现 {len(issues)} 个问题：")
        for i in issues:
            print(" -", i)
        sys.exit(1)
    print("QA 通过：quiz JSON、链接、基础结构全部正常")
