#!/usr/bin/env python3
"""livedeck 정합성 검증 (DESIGN-PLAN.md 섹션 6).

사용법:
    python3 scripts/check_consistency.py <deck_dir>

검사 항목:
    1. 청중 index.html 의 data-slide 개수
    2. 발표자 view/index.html 의 SLIDES 항목 수
    3. 두 파일의 TOTAL_SLIDES 값
    4. data-slide 번호가 1부터 연속
    5. 채널명이 양쪽 모두 livedeck-sync
    6. 발표자 iframe src 가 ../index.html

위 다섯 가지가 모두 통과하면 종료 코드 0, 아니면 1.
"""
import re
import sys
from pathlib import Path


def fail(msg):
    print("  [FAIL] " + msg)


def ok(msg):
    print("  [OK] " + msg)


def check(deck_dir):
    deck = Path(deck_dir)
    audience = deck / "index.html"
    presenter = deck / "view" / "index.html"

    problems = 0

    if not audience.exists():
        fail("청중 뷰 없음: " + str(audience))
        return 1
    if not presenter.exists():
        fail("발표자 뷰 없음: " + str(presenter))
        return 1

    a_html = audience.read_text(encoding="utf-8")
    p_html = presenter.read_text(encoding="utf-8")

    # 1. data-slide 번호 수집
    a_nums = [int(x) for x in re.findall(r'data-slide="(\d+)"', a_html)]
    a_count = len(a_nums)

    # 2. 발표자 SLIDES 키 수집 (숫자 키)
    slides_keys = [int(x) for x in re.findall(r'"?(\d+)"?\s*:\s*\{\s*"?title', p_html)]
    p_count = len(slides_keys)

    # 3. TOTAL_SLIDES
    a_total = re.search(r'TOTAL_SLIDES\s*=\s*(\d+)', a_html)
    p_total = re.search(r'TOTAL_SLIDES\s*=\s*(\d+)', p_html)
    a_total = int(a_total.group(1)) if a_total else None
    p_total = int(p_total.group(1)) if p_total else None

    if a_count == p_count:
        ok("슬라이드 개수 일치 (청중 %d == 발표자 SLIDES %d)" % (a_count, p_count))
    else:
        fail("슬라이드 개수 불일치 (청중 %d != 발표자 SLIDES %d)" % (a_count, p_count))
        problems += 1

    if a_total == p_total == a_count and a_total is not None:
        ok("TOTAL_SLIDES 일치 (%s)" % a_total)
    else:
        fail("TOTAL_SLIDES 불일치 (청중 %s / 발표자 %s / data-slide %d)" % (a_total, p_total, a_count))
        problems += 1

    # 4. 1부터 연속
    if a_nums == list(range(1, a_count + 1)):
        ok("data-slide 1부터 연속")
    else:
        fail("data-slide 연속성 깨짐: %s" % a_nums)
        problems += 1

    # 5. 채널명
    a_chan = re.search(r"CHANNEL\s*=\s*'([^']+)'", a_html)
    p_chan = re.search(r"CHANNEL\s*=\s*'([^']+)'", p_html)
    a_chan = a_chan.group(1) if a_chan else None
    p_chan = p_chan.group(1) if p_chan else None
    if a_chan == p_chan == "livedeck-sync":
        ok("채널명 양쪽 livedeck-sync")
    else:
        fail("채널명 불일치 (청중 %s / 발표자 %s)" % (a_chan, p_chan))
        problems += 1

    # 6. iframe src
    src = re.search(r'<iframe[^>]*src="([^"]+)"', p_html)
    src = src.group(1) if src else None
    if src == "../index.html":
        ok("iframe src 가 ../index.html")
    else:
        fail("iframe src 가 ../index.html 아님: %s" % src)
        problems += 1

    print()
    if problems == 0:
        print("정합성 검증 통과 (슬라이드 %d장)" % a_count)
        return 0
    print("정합성 검증 실패 (%d건)" % problems)
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(check(sys.argv[1]))
