#!/usr/bin/env python3
"""중간 표현(슬라이드 배열)에서 livedeck 두 HTML 을 생성한다.

스킬 본 흐름에서는 LLM 이 templates/ 의 PLACEHOLDER 를 직접 채운다.
이 스크립트는 그 채우기를 코드로 재현해 정합성 검증과 시연에 쓰는 참조 구현이다.

사용법:
    python3 scripts/build_deck.py <slides_json> <out_dir> [--title T] [--lang ko]

slides_json 예시는 examples/sample_slides.json 참조.
"""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates"
THEMES = ROOT / "themes"

LAYOUTS = {"COVER", "CONTENT", "SECTION", "CLOSING", "IMAGE",
           "STAT", "CARDS", "TABLE", "CALLOUT", "COMPARE", "TIMELINE", "CODE"}
TONES = {"info", "success", "warn", "danger", "accent"}


def esc(s):
    return html.escape(str(s), quote=True)


def inline(s):
    """인라인 강조 서식을 HTML 로 변환한다 (esc 후 안전한 태그만 복원).
       **굵게** -> <strong>, ==하이라이트== -> <mark>, `코드` -> <code>."""
    out = esc(s)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"==(.+?)==", r"<mark>\1</mark>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    return out


def li_list(items):
    """불릿 배열을 <ul> 로 렌더한다 (인라인 서식 허용). 빈 배열이면 빈 문자열."""
    if not items:
        return ""
    parts = ["<ul>"]
    for item in items:
        parts.append("<li>%s</li>" % inline(item))
    parts.append("</ul>")
    return "".join(parts)


def render_stat(slide, parts):
    """STAT: 큰 수치 카드 그리드. items: [{value, label, sub?, tone?}]"""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    parts.append('<div class="stat-grid">')
    for it in slide.get("items", []):
        tone = it.get("tone", "accent")
        tone = tone if tone in TONES else "accent"
        parts.append('<div class="stat" data-tone="%s">' % tone)
        parts.append('<div class="stat-value">%s</div>' % inline(it.get("value", "")))
        if it.get("label"):
            parts.append('<div class="stat-label">%s</div>' % inline(it["label"]))
        if it.get("sub"):
            parts.append('<div class="stat-sub">%s</div>' % inline(it["sub"]))
        parts.append("</div>")
    parts.append("</div>")


def render_cards(slide, parts):
    """CARDS: 카드 그리드. items: [{icon?, title, body?(str|list), tone?}]"""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    parts.append('<div class="card-grid">')
    for it in slide.get("items", []):
        tone = it.get("tone", "accent")
        tone = tone if tone in TONES else "accent"
        parts.append('<div class="card" data-tone="%s">' % tone)
        if it.get("icon"):
            parts.append('<div class="card-icon">%s</div>' % esc(it["icon"]))
        if it.get("title"):
            parts.append('<div class="card-title">%s</div>' % inline(it["title"]))
        body = it.get("body")
        if isinstance(body, list):
            parts.append('<div class="card-body">%s</div>' % li_list(body))
        elif body:
            parts.append('<div class="card-body"><p>%s</p></div>' % inline(body))
        parts.append("</div>")
    parts.append("</div>")


def render_table(slide, parts):
    """TABLE: 표. headers: [..], rows: [[..], ..]. 첫 열은 강조(th)."""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    headers = slide.get("headers", [])
    rows = slide.get("rows", [])
    parts.append('<div class="table-wrap"><table>')
    if headers:
        parts.append("<thead><tr>")
        for h in headers:
            parts.append("<th>%s</th>" % inline(h))
        parts.append("</tr></thead>")
    parts.append("<tbody>")
    for row in rows:
        parts.append("<tr>")
        for ci, cell in enumerate(row):
            tag = "th" if ci == 0 else "td"
            parts.append("<%s>%s</%s>" % (tag, inline(cell), tag))
        parts.append("</tr>")
    parts.append("</tbody></table></div>")


def render_callout(slide, parts):
    """CALLOUT: 강조 박스 + 보조 불릿. tone, icon?, heading?, body(str|list)."""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    tone = slide.get("tone", "info")
    tone = tone if tone in TONES else "info"
    parts.append('<div class="callout" data-tone="%s">' % tone)
    if slide.get("icon"):
        parts.append('<div class="callout-icon">%s</div>' % esc(slide["icon"]))
    parts.append('<div class="callout-text">')
    if slide.get("heading"):
        parts.append('<div class="callout-heading">%s</div>' % inline(slide["heading"]))
    body = slide.get("body")
    if isinstance(body, list):
        parts.append(li_list(body))
    elif body:
        parts.append("<p>%s</p>" % inline(body))
    parts.append("</div></div>")


def render_compare(slide, parts):
    """COMPARE: 좌우 2단 비교. left/right: {heading, tone?, body(list)}."""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    parts.append('<div class="compare-grid">')
    for side in ("left", "right"):
        col = slide.get(side) or {}
        tone = col.get("tone", "accent")
        tone = tone if tone in TONES else "accent"
        parts.append('<div class="compare-col" data-tone="%s">' % tone)
        if col.get("heading"):
            parts.append('<div class="compare-heading">%s</div>' % inline(col["heading"]))
        parts.append(li_list(col.get("body", [])))
        parts.append("</div>")
    parts.append("</div>")


def render_timeline(slide, parts):
    """TIMELINE: 가로 단계. steps: [{label?, title, body?(str|list), tone?}].
       각 단계는 번호 노드 + 세로 카드(제목/본문). 연결선은 CSS 가 그린다."""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    parts.append('<div class="timeline">')
    for i, st in enumerate(slide.get("steps", []), 1):
        tone = st.get("tone", "accent")
        tone = tone if tone in TONES else "accent"
        parts.append('<div class="tl-step" data-tone="%s">' % tone)
        parts.append('<div class="tl-node">%d</div>' % i)
        parts.append('<div class="tl-card">')
        if st.get("label"):
            parts.append('<div class="tl-label">%s</div>' % inline(st["label"]))
        parts.append('<div class="tl-title">%s</div>' % inline(st.get("title", "")))
        body = st.get("body")
        if isinstance(body, list):
            parts.append(li_list(body))
        elif body:
            parts.append('<p class="tl-body">%s</p>' % inline(body))
        parts.append("</div></div>")
    parts.append("</div>")


def render_code(slide, parts):
    """CODE: 어두운 코드 블록. lines: [..] 또는 code: "여러 줄 문자열".
       intro(선택) 한 줄 설명. 줄별로 렌더하여 들여쓰기를 보존한다."""
    parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
    if slide.get("intro"):
        parts.append('<p class="code-intro">%s</p>' % inline(slide["intro"]))
    lines = slide.get("lines")
    if lines is None:
        code = slide.get("code", "")
        lines = code.split("\n") if code else []
    parts.append('<div class="code-block"><pre>')
    for ln in lines:
        # 코드는 인라인 서식을 적용하지 않고 그대로 이스케이프 (들여쓰기·기호 보존)
        parts.append('<span class="code-line">%s</span>' % esc(ln) if ln != "" else '<span class="code-line"> </span>')
    parts.append("</pre></div>")


def render_slide(slide):
    n = slide["id"]
    layout = slide.get("layout", "CONTENT")
    if layout not in LAYOUTS:
        layout = "CONTENT"  # 미지원 신호는 CONTENT 폴백
    open_tag = '<section class="slide" id="slide-%d" data-slide="%d" data-layout="%s"' % (n, n, layout)
    if layout == "IMAGE":
        variant = slide.get("variant", "right")
        if variant not in {"left", "right", "full"}:
            variant = "right"  # 미지정/미지원 variant 는 right 폴백
        open_tag += ' data-variant="%s"' % variant
    open_tag += ">"
    parts = [open_tag]
    if layout == "COVER":
        if slide.get("section"):
            parts.append('<div class="eyebrow">%s</div>' % esc(slide["section"]))
        parts.append("<h1>%s</h1>" % inline(slide.get("title", "")))
        if slide.get("subtitle"):
            parts.append('<p class="subtitle">%s</p>' % inline(slide["subtitle"]))
    elif layout == "SECTION":
        parts.append('<div class="rule"></div>')
        if slide.get("section"):
            parts.append('<div class="eyebrow">%s</div>' % esc(slide["section"]))
        parts.append("<h1>%s</h1>" % inline(slide.get("title", "")))
    elif layout == "CLOSING":
        parts.append("<h1>%s</h1>" % inline(slide.get("title", "")))
        if slide.get("subtitle"):
            parts.append('<p class="subtitle">%s</p>' % inline(slide["subtitle"]))
    elif layout == "IMAGE":
        variant = slide.get("variant", "right")
        if variant not in {"left", "right", "full"}:
            variant = "right"
        parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
        # full 은 본문(불릿)을 렌더하지 않는다. left/right 만 텍스트 영역을 둔다.
        if variant != "full":
            parts.append(li_list(slide.get("body", [])))
        images = slide.get("images", [])
        parts.append('<div class="img-grid">')
        for img in images:
            parts.append("<figure>")
            parts.append('<img src="%s" alt="%s">' % (esc(img.get("src", "")), esc(img.get("caption", ""))))
            if img.get("caption"):
                parts.append("<figcaption>%s</figcaption>" % inline(img["caption"]))
            parts.append("</figure>")
        parts.append("</div>")
    elif layout == "STAT":
        render_stat(slide, parts)
    elif layout == "CARDS":
        render_cards(slide, parts)
    elif layout == "TABLE":
        render_table(slide, parts)
    elif layout == "CALLOUT":
        render_callout(slide, parts)
    elif layout == "COMPARE":
        render_compare(slide, parts)
    elif layout == "TIMELINE":
        render_timeline(slide, parts)
    elif layout == "CODE":
        render_code(slide, parts)
    else:  # CONTENT
        parts.append("<h2>%s</h2>" % inline(slide.get("title", "")))
        parts.append(li_list(slide.get("body", [])))
    parts.append("</section>")
    return "\n      ".join(parts)


def load_theme(name):
    """themes/<name>.json 을 읽어 (vars_css, fonts_html, css, stage_bg) 를 만든다.
       이름이 없거나 파일이 없으면 베이스 토큰만 쓰는 빈 테마로 폴백한다."""
    empty = {"vars": "", "fonts": "", "css": "", "stage_bg": "", "assets": []}
    if not name:
        return empty
    path = THEMES / ("%s.json" % name)
    if not path.exists():
        print("경고: 테마 '%s' 없음 → 기본 토큰 사용" % name)
        return empty
    data = json.loads(path.read_text(encoding="utf-8"))
    decls = "".join("      %s: %s;\n" % (k, v) for k, v in data.get("vars", {}).items())
    stage_bg = data.get("stage_bg", "")
    if stage_bg:
        decls += "      --stage-bg: %s;\n" % stage_bg
    vars_css = ":root {\n%s    }" % decls if decls else ""
    return {
        "vars": vars_css, "fonts": data.get("fonts", ""), "css": data.get("css", ""),
        "stage_bg": stage_bg, "name": data.get("name", name),
        "assets": data.get("assets", []),  # themes/ 기준 상대경로 목록
    }


def copy_theme_assets(th, out):
    """테마가 선언한 에셋을 <out_dir>/assets/ 로 복사한다. HTML 에선 assets/<파일명> 로 참조."""
    assets = th.get("assets") or []
    if not assets:
        return
    import shutil
    dst_dir = out / "assets"
    dst_dir.mkdir(parents=True, exist_ok=True)
    for rel in assets:
        src = THEMES / rel
        if src.exists():
            shutil.copy(src, dst_dir / src.name)
        else:
            print("경고: 테마 에셋 없음 → %s" % src)


def build_footer(footer):
    if not footer or not footer.get("enabled"):
        return ""
    left = esc(footer["copyright"]) if footer.get("copyright") else ""
    center = "<span class=\"page\"></span>" if footer.get("page_number") else ""
    right = ('<img src="%s" alt="logo">' % esc(footer["logo_path"])) if footer.get("logo_path") else ""
    return (
        '<div class="deck-footer">'
        '<span class="left">%s</span>'
        '<span class="center">%s</span>'
        '<span class="right">%s</span>'
        "</div>" % (left, center, right)
    )


def build(slides, out_dir, title, lang, footer, theme="vivid"):
    out = Path(out_dir)
    (out / "view").mkdir(parents=True, exist_ok=True)
    total = len(slides)

    pres_tpl = (TPL / "presentation.template.html").read_text(encoding="utf-8")
    scr_tpl = (TPL / "script.template.html").read_text(encoding="utf-8")

    slides_html = "\n    ".join(render_slide(s) for s in slides)
    footer_html = build_footer(footer)
    th = load_theme(theme)

    audience = (
        pres_tpl
        .replace("{{LANG}}", lang)
        .replace("{{TITLE}}", esc(title))
        .replace("{{TOTAL_SLIDES}}", str(total))
        .replace("{{SLIDES}}", slides_html)
        .replace("{{FOOTER}}", footer_html)
        .replace("{{THEME_FONTS}}", th["fonts"])
        .replace("{{THEME_VARS}}", th["vars"])
        .replace("{{THEME_CSS}}", th["css"])
        .replace("{{THEME}}", th.get("name", theme or ""))
    )

    script_data = {}
    for s in slides:
        script_data[s["id"]] = {
            "title": s.get("title", ""),
            "script": s.get("script", ""),
            "ref": s.get("ref", ""),
        }
    presenter = (
        scr_tpl
        .replace("{{LANG}}", lang)
        .replace("{{TITLE}}", esc(title))
        .replace("{{TOTAL_SLIDES}}", str(total))
        .replace("{{SCRIPT_DATA}}", json.dumps(script_data, ensure_ascii=False))
        .replace("{{THEME_FONTS}}", th["fonts"])
        .replace("{{THEME_VARS}}", th["vars"])
    )

    (out / "index.html").write_text(audience, encoding="utf-8")
    (out / "view" / "index.html").write_text(presenter, encoding="utf-8")
    copy_theme_assets(th, out)
    print("생성: %s (슬라이드 %d장, 테마 %s)" % (out, total, theme))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides_json")
    ap.add_argument("out_dir")
    ap.add_argument("--title", default="Sample Deck")
    ap.add_argument("--lang", default="ko")
    ap.add_argument("--theme", default="vivid", help="themes/ 의 테마 이름 (vivid/editorial/bold/orange)")
    args = ap.parse_args()

    data = json.loads(Path(args.slides_json).read_text(encoding="utf-8"))
    slides = data["slides"] if isinstance(data, dict) else data
    footer = data.get("footer") if isinstance(data, dict) else None
    # slides.json 의 최상위 "theme" 키가 있으면 CLI 기본값을 덮어쓴다 (CLI 명시 시 CLI 우선은 사용자가 직접 판단).
    theme = args.theme
    if isinstance(data, dict) and data.get("theme"):
        theme = data["theme"]
    build(slides, args.out_dir, args.title, args.lang, footer, theme)


if __name__ == "__main__":
    main()
