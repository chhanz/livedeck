---
# livedeck 기본 테마 토큰 (Vivid 라이트 — 컬러 강조형)
# 이 값을 LLM이 읽어 두 HTML 의 :root CSS 변수로 주입한다.
# 강조색을 바꾸려면 accent / accent-strong / accent-soft 세 값을 함께 고치면 전체 테마가 따라 바뀐다.
colors:
  canvas: "#ffffff"
  ink: "#0f172a"          # 제목·강조 텍스트 (slate-900)
  charcoal: "#334155"     # 본문 (slate-700)
  body: "#475569"         # 보조 본문 (slate-600)
  mute: "#94a3b8"         # 약한 텍스트·캡션 (slate-400)
  surface-soft: "#f8fafc" # 옅은 면 (slate-50)
  surface-card: "#ffffff" # 카드 바탕 (그림자/보더로 구분)
  surface-dark: "#0f172a" # 반전 면 (CLOSING / 발표자 무대)
  hairline: "#e2e8f0"     # 가는 선 (slate-200)
  hairline-strong: "#cbd5e1"
  on-dark: "#ffffff"
  # 강조색 (accent) — 기본 인디고 계열. 사용자 요청 시 이 세 값을 함께 바꾼다.
  accent: "#2563eb"       # 메인 강조 (blue-600)
  accent-strong: "#1d4ed8" # 진한 강조 (blue-700)
  accent-soft: "#eff6ff"  # 옅은 강조 배경 (blue-50)
  accent-ink: "#1e3a8a"   # 강조 배경 위 텍스트 (blue-900)
  # 시맨틱 컬러 — 콜아웃·배지·강조에 쓴다. soft 는 배경, 본색은 보더·아이콘·텍스트.
  info: "#0ea5e9"
  info-soft: "#f0f9ff"
  success: "#16a34a"
  success-soft: "#f0fdf4"
  warn: "#d97706"
  warn-soft: "#fffbeb"
  danger: "#dc2626"
  danger-soft: "#fef2f2"
  # 통계/카드 강조용 highlight (==mark== 인라인)
  mark-bg: "#fef08a"      # 노랑 하이라이트 (yellow-200)
rounded:
  sm: "8px"
  lg: "16px"
  xl: "22px"
  full: "9999px"
shadow:
  card: "0 1px 2px rgba(15,23,42,0.04), 0 8px 24px rgba(15,23,42,0.08)"
  card-hover: "0 2px 4px rgba(15,23,42,0.06), 0 16px 40px rgba(15,23,42,0.12)"
fonts:
  display: "'Noto Sans KR', 'Inter', 'Nunito', system-ui, sans-serif"
  body: "'Noto Sans KR', 'Inter', system-ui, sans-serif"
  code: "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
spacing:
  section: "88px"
---

# livedeck Design Tokens

> **테마 시스템이 도입되었습니다.** 룩(폰트·팔레트·시그니처 장식)은 이제 `themes/*.json` 프리셋이 결정한다(`themes/README.md` 참조). 이 문서는 그중 기본 테마 **`vivid`** 의 토큰 의미와 컬러 사용 규칙을 설명하는 레퍼런스다. 다른 테마(editorial/bold/orange)는 같은 토큰 이름을 자기 값으로 덮어쓴다. 토큰 *이름과 역할* 은 모든 테마 공통이므로 이 문서로 배우고, 실제 값은 각 테마 JSON 을 본다.

기본 테마 `vivid` 는 흰 캔버스 위에 강조색(accent)과 시맨틱 컬러(info/success/warn/danger)를 적극적으로 써서, 카드·통계·콜아웃·표 컴포넌트가 또렷하게 살아나게 한다.

## 원칙

- 흰 캔버스를 바탕으로, **강조색 1색 + 시맨틱 4색**을 컴포넌트 위계에 따라 쓴다. 같은 화면 안에서도 강조색·시맨틱색을 자유롭게 조합할 수 있다.
- 카드와 통계 블록은 **부드러운 그림자(`shadow.card`)와 라운드(`rounded.lg`/`xl`)**로 입체감을 준다. 미니멀 금지 규칙은 더 이상 적용하지 않는다.
- 강조색은 제목 옆 eyebrow, 섹션 룰, 활성 카드 보더, 통계 수치, 진행 바, 인라인 하이라이트에 쓴다.
- 시맨틱 컬러(info/success/warn/danger)는 콜아웃 박스와 배지에 쓴다. soft 색을 배경으로, 본색을 좌측 보더·아이콘·제목에 쓴다.
- 표(table)는 헤더 행에 강조색 옅은 배경(accent-soft)을, 행 구분에 hairline 을 쓴다.

## 컬러 사용 가이드

| 토큰 | 쓰임 |
|------|------|
| `accent` / `accent-strong` | 통계 수치, 섹션 룰, eyebrow, 활성 보더, 진행 바, 링크 |
| `accent-soft` / `accent-ink` | 강조 카드·표 헤더 배경 + 그 위 텍스트 |
| `info` (+`info-soft`) | 정보성 콜아웃 (참고·팁) |
| `success` (+`success-soft`) | 긍정 콜아웃 (장점·완료·권장) |
| `warn` (+`warn-soft`) | 주의 콜아웃 (제약·경고) |
| `danger` (+`danger-soft`) | 위험 콜아웃 (금지·오류·미지원) |
| `mark-bg` | 인라인 `==하이라이트==` 형광펜 배경 |

## 슬라이드 맥락 적용 (중요)

발표 슬라이드는 풀스크린 16:9(1920x1080) 캔버스다. 토큰 값(색/라운드/그림자/폰트)은 그대로 쓰되, 레이아웃은 슬라이드 맥락으로 짠다.

- 청중 슬라이드: 흰 캔버스 + 컬러 강조 컴포넌트. 한 슬라이드에 카드/통계/표/콜아웃 중 하나의 주(主) 컴포넌트를 둔다.
- 발표자 뷰: 라이트 톤으로 통일한다. 미리보기 iframe 을 감싸는 무대 영역만 `surface-dark`로 어둡게 둔다.
- `COVER`/`SECTION`/`CLOSING` 은 강조색 포인트(eyebrow·룰·반전 배경)를 주되 컴포넌트는 두지 않는다.

## 커스텀 방법

1. 위 front matter 토큰 값을 수정한다.
2. 생성 시 LLM 이 토큰을 읽어 두 HTML 의 `:root` 변수로 주입한다. (템플릿 `:root` 와 이 문서 값은 항상 일치시킨다.)

예: "강조를 초록으로" 요청이 오면 `accent`(#16a34a), `accent-strong`(#15803d), `accent-soft`(#f0fdf4), `accent-ink`(#14532d) 네 값을 함께 바꾼다.
예: "AWS 톤으로" 요청이 오면 `accent`(#FF9900), `accent-strong`(#EC7211), `accent-soft`(#FFF4E5), `accent-ink`(#7A4100), `ink`(#232F3E) 로 바꾼다.

## 폰트 / 이미지 전략

- 폰트: 시스템 폰트 스택을 우선한다. 웹폰트가 필요하면 Google Fonts CDN `<link>` + `font-display: swap` 으로 얹되, 오프라인에서도 시스템 폴백이 항상 동작하게 둔다.
- 이미지: `assets/` 폴더 상대경로 참조가 기본. 단일 파일 배포가 필요하면 작은 이미지에 한해 base64 인라인을 허용한다. 큰 이미지 인라인은 금지(HTML 비대).
- 아이콘: 카드(`CARDS`)·콜아웃(`CALLOUT`)의 `icon` 필드는 이모지 한 글자(예: "📦", "⚡", "🔒") 또는 짧은 텍스트를 받는다. 외부 아이콘 폰트는 v1 에서 쓰지 않는다.
