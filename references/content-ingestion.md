# Content Ingestion

자연어 텍스트나 마크다운을 받아 슬라이드 배열로 구조화하는 규칙. 무거운 파서(docx/pdf/pptx/URL/이미지) 없이, LLM 이 입력을 읽고 직접 중간 표현을 만든다.

## 지원 입력

| 입력 | 처리 |
|------|------|
| 자연어 텍스트 | LLM이 주제/흐름을 분석해 슬라이드 배열로 직접 구조화한다. |
| 마크다운 (.md) | 헤딩을 슬라이드 경계로, 본문/리스트를 슬라이드 콘텐츠로 매핑한다. |

## 마크다운 매핑 규칙

- 첫 `# H1` -> 첫 슬라이드의 `COVER` 제목 (덱 표지).
- 이후 `# H1` -> 새 `SECTION` 슬라이드 (구간 구분, title 만).
- `## H2` -> 새 `CONTENT` 슬라이드의 제목.
- 불릿 리스트 -> 슬라이드 불릿 (한눈에 들어오는 분량, 넘치면 슬라이드 분할).
- 마지막 마무리/감사/Q&A 성격의 헤딩 -> `CLOSING` 슬라이드.
- 인용/짧은 한 문장 강조 등 전용 레이아웃이 없는 신호 -> `CONTENT`로 폴백.

레이아웃 선택 기준의 단일 출처는 `layouts.md`다. 입력 신호 -> 레이아웃 판정은 `layouts.md`의 `## 6. 자동 매핑 규칙`을 따른다 (여기서 중복 서술하지 않는다).

## 중간 표현 (LLM 내부 작업용, 파일로 저장하지 않음)

```
slides = [
  { id: 1, layout: "COVER",   section: "Opening", title: "...", subtitle: "...", script: "...", ref: "" },
  { id: 2, layout: "SECTION", title: "...", script: "...", ref: "" },
  { id: 3, layout: "CONTENT", title: "...", body: ["...", "..."], script: "...", ref: "" },
  { id: 4, layout: "CLOSING", title: "...", subtitle: "...", script: "...", ref: "" }
]
```

레이아웃별로 화면에 쓰이는 필드는 다르다 (출처: `build_deck.py` render_slide, `layouts.md`):

| layout | 사용 필드 |
|--------|-----------|
| COVER | section(eyebrow) / title / subtitle |
| SECTION | section(eyebrow, 선택) / title |
| CONTENT | title / body(불릿) |
| IMAGE | title / variant / body / images[{src,caption}] |
| STAT | title / items[{value, label, sub?, tone?}] |
| CARDS | title / items[{icon?, title, body(str\|list)?, tone?}] |
| TABLE | title / headers[] / rows[[]] (각 행 첫 셀은 강조) |
| CALLOUT | title / tone / icon? / heading? / body(str\|list) |
| COMPARE | title / left{heading,tone?,body[]} / right{...} |
| TIMELINE | title / steps[{label?, title, body(str\|list)?, tone?}] |
| CODE | title / intro? / lines[] (또는 code 문자열) |
| CLOSING | title / subtitle |

모든 텍스트 필드는 인라인 서식을 받는다: `**굵게**` / `==하이라이트==` / `` `코드` ``. tone 값: accent/info/success/warn/danger.

- `id`는 1부터 연속.
- `script`/`ref`는 모든 레이아웃에서 발표자 뷰로만 전달된다 (청중 화면 비표시).
- 화면에 안 쓰는 필드는 빈 값(`""`/`[]`)으로 두거나 생략한다. 원본에 없는 값을 지어내지 않는다.
- 이 배열에서 청중 슬라이드 마크업과 발표자 `SLIDES` 객체를 동시에 생성한다.
- 따라서 슬라이드 개수가 양쪽에서 자동으로 일치한다 (정합성 검증으로 재확인).

## 인제스천 워크플로

LLM이 입력을 받았을 때 따르는 순서:

1. **주제 분해** - 입력을 읽고 표지 / 구간 / 본문 / 마무리로 흐름을 나눈다.
2. **레이아웃 배정** - 각 조각에 `layouts.md`의 자동 매핑 규칙으로 layout을 정한다. 표/수치/대조/경고는 전용 레이아웃(TABLE/STAT/COMPARE/CALLOUT)으로 살린다.
3. **필드 채우기** - 레이아웃별 필드만 채운다. 텍스트에는 인라인 강조(`**굵게**`/`==하이라이트==`/`` `코드` ``)를 적극 쓴다. 없는 정보는 비워 둔다.
4. **대본 작성** - 아래 "대본 생성" 규칙으로 각 슬라이드 `script`를 쓴다.
5. **테마 선택** - 발표 성격에 맞는 테마를 고른다(`themes/README.md`). slides.json 최상위 `"theme"` 키에 넣거나 빌드 시 `--theme` 로 전달.
6. **self-check** - id 연속성, 레이아웃별 필드 정합, 빈 슬라이드 여부를 점검한다. 빌드 후 `check_consistency.py`로 재확인한다.

## 대본 생성

각 슬라이드의 `script`는 구어체 한국어(기본)로 작성한다. 슬라이드에 적힌 불릿을 그대로 읽지 말고, 말로 풀어 설명하는 문장으로 쓴다. 강조/행동/멈춤 서식은 `presenter-view-template.md`를 따른다.
