---
# livedeck 기본 테마 토큰 (Ollama 모노크롬 라이트)
# 이 값을 LLM이 읽어 두 HTML 의 :root CSS 변수로 주입한다.
# 강조색을 바꾸려면 primary 값만 고치면 전체 테마가 따라 바뀐다.
colors:
  canvas: "#ffffff"
  primary: "#000000"
  ink: "#000000"
  charcoal: "#525252"
  body: "#737373"
  mute: "#a3a3a3"
  surface-soft: "#fafafa"
  surface-dark: "#171717"
  hairline: "#e5e5e5"
  hairline-strong: "#d4d4d4"
  on-dark: "#ffffff"
rounded:
  lg: "12px"
  full: "9999px"
fonts:
  display: "'Noto Sans KR', 'Nunito', 'Inter', system-ui, sans-serif"
  body: "'Noto Sans KR', 'Inter', system-ui, sans-serif"
  code: "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
spacing:
  section: "88px"
---

# livedeck Design Tokens

기본 테마는 Ollama 모노크롬 라이트 톤이다. 출처 토큰은 `/tmp/ollama-design.md`(개발용)이며, 이 문서가 livedeck의 단일 기본값이다.

## 원칙

- 그라데이션과 그림자를 쓰지 않는다. 캔버스는 순백, 텍스트는 검정과 회색.
- 브랜드색은 검정 하나. 한 화면에 검정 pill은 하나만 둔다.
- pill 은 `rounded.full`(9999px), 카드는 `rounded.lg`(12px). 그 외 라운드는 쓰지 않는다.
- 카드는 1px 헤어라인 또는 `surface-dark` 반전 중 하나로만 구분한다.

## 슬라이드 맥락 적용 (중요)

Ollama 원본은 720px 리딩 컬럼이지만, 발표 슬라이드는 풀스크린 16:9(1920x1080) 캔버스다. 따라서 토큰 값(색/라운드/폰트)은 그대로 쓰되, 레이아웃은 슬라이드 맥락으로 다시 짠다.

- 청중 슬라이드: 흰 캔버스 + 검정 텍스트 + 최소 헤어라인. 섹션 라벨과 강조에만 포인트를 준다.
- 발표자 뷰: 라이트 톤으로 통일한다. 단 미리보기 iframe 을 감싸는 무대 영역만 `surface-dark`로 어둡게 허용한다.
- `CLOSING` 슬라이드는 시스템에서 한 번 허용하는 반전 surface(`surface-dark`)를 쓴다.

## 커스텀 방법

1. 위 front matter 토큰 값을 수정한다.
2. 필요하면 `npx @google/design.md lint DESIGN.md`로 대비/참조를 검증한다.
3. 생성 시 LLM 이 토큰을 읽어 두 HTML 의 `:root` 변수로 주입한다.

예: "강조를 파란색으로" 요청이 오면 `primary` 값만 바꾸면 두 뷰 전체가 따라 바뀐다.

## 폰트 / 이미지 전략 (v1)

- 폰트: 시스템 폰트 스택을 우선한다. 웹폰트가 필요하면 Google Fonts CDN `<link>` + `font-display: swap` 으로 얹되, 오프라인에서도 시스템 폴백이 항상 동작하게 둔다. (번들은 v2.)
- 이미지: `assets/` 폴더 상대경로 참조가 기본. 단일 파일 배포가 필요하면 작은 이미지에 한해 base64 인라인을 허용한다. 큰 이미지 인라인은 금지(HTML 비대).
