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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates"


def esc(s):
    return html.escape(str(s), quote=True)


def render_slide(slide):
    n = slide["id"]
    layout = slide.get("layout", "CONTENT")
    if layout not in {"COVER", "CONTENT", "SECTION", "CLOSING", "IMAGE"}:
        layout = "CONTENT"  # v2 신호는 CONTENT 폴백
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
        parts.append("<h1>%s</h1>" % esc(slide.get("title", "")))
        if slide.get("subtitle"):
            parts.append('<p class="subtitle">%s</p>' % esc(slide["subtitle"]))
    elif layout == "SECTION":
        parts.append('<div class="rule"></div>')
        parts.append("<h1>%s</h1>" % esc(slide.get("title", "")))
    elif layout == "CLOSING":
        parts.append("<h1>%s</h1>" % esc(slide.get("title", "")))
        if slide.get("subtitle"):
            parts.append('<p class="subtitle">%s</p>' % esc(slide["subtitle"]))
    elif layout == "IMAGE":
        variant = slide.get("variant", "right")
        if variant not in {"left", "right", "full"}:
            variant = "right"
        parts.append("<h2>%s</h2>" % esc(slide.get("title", "")))
        # full 은 본문(불릿)을 렌더하지 않는다. left/right 만 텍스트 영역을 둔다.
        if variant != "full":
            body = slide.get("body", [])
            if body:
                parts.append("<ul>")
                for item in body:
                    parts.append("<li>%s</li>" % esc(item))
                parts.append("</ul>")
        images = slide.get("images", [])
        parts.append('<div class="img-grid">')
        for img in images:
            parts.append("<figure>")
            parts.append('<img src="%s" alt="%s">' % (esc(img.get("src", "")), esc(img.get("caption", ""))))
            if img.get("caption"):
                parts.append("<figcaption>%s</figcaption>" % esc(img["caption"]))
            parts.append("</figure>")
        parts.append("</div>")
    else:  # CONTENT
        parts.append("<h2>%s</h2>" % esc(slide.get("title", "")))
        body = slide.get("body", [])
        if body:
            parts.append("<ul>")
            for item in body:
                parts.append("<li>%s</li>" % esc(item))
            parts.append("</ul>")
    parts.append("</section>")
    return "\n      ".join(parts)


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


def build(slides, out_dir, title, lang, footer):
    out = Path(out_dir)
    (out / "view").mkdir(parents=True, exist_ok=True)
    total = len(slides)

    pres_tpl = (TPL / "presentation.template.html").read_text(encoding="utf-8")
    scr_tpl = (TPL / "script.template.html").read_text(encoding="utf-8")

    slides_html = "\n    ".join(render_slide(s) for s in slides)
    footer_html = build_footer(footer)

    audience = (
        pres_tpl
        .replace("{{LANG}}", lang)
        .replace("{{TITLE}}", esc(title))
        .replace("{{TOTAL_SLIDES}}", str(total))
        .replace("{{SLIDES}}", slides_html)
        .replace("{{FOOTER}}", footer_html)
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
    )

    (out / "index.html").write_text(audience, encoding="utf-8")
    (out / "view" / "index.html").write_text(presenter, encoding="utf-8")
    print("생성: %s (슬라이드 %d장)" % (out, total))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides_json")
    ap.add_argument("out_dir")
    ap.add_argument("--title", default="Sample Deck")
    ap.add_argument("--lang", default="ko")
    args = ap.parse_args()

    data = json.loads(Path(args.slides_json).read_text(encoding="utf-8"))
    slides = data["slides"] if isinstance(data, dict) else data
    footer = data.get("footer") if isinstance(data, dict) else None
    build(slides, args.out_dir, args.title, args.lang, footer)


if __name__ == "__main__":
    main()
