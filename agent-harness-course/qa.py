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
            [ROOT / "COURSE.md", ROOT / "index.html"]
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
    check_basics()
    if issues:
        print(f"发现 {len(issues)} 个问题：")
        for i in issues:
            print(" -", i)
        sys.exit(1)
    print("QA 通过：quiz JSON、链接、基础结构全部正常")
