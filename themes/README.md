# livedeck 테마(프리셋) 시스템

하나의 강한 디자인 시스템을 골라 덱 전체를 그 시각 언어로 통일한다. (frontend-slides 의 "테마로 룩을 결정" 철학을 livedeck 의 듀얼 뷰 구조에 흡수.) 각 테마는 `themes/<name>.json` 파일 하나로 정의되고, `build_deck.py` 가 청중·발표자 템플릿의 `{{THEME_*}}` 자리에 주입한다.

## 기본 테마 4종

| 테마 | display 폰트 | 팔레트 | 시그니처 | 적합 |
|------|-------------|--------|----------|------|
| **vivid** | Plus Jakarta Sans (800) | 흰 캔버스 + 인디고 + 시맨틱 4색 | 그림자·라운드 카드, 컬러 통계 | 범용 비즈니스·기술, 정보 밀도 높은 덱 |
| **editorial** | Fraunces (세리프, opsz) | 오트밀 크림 + 포레스트 그린 | 상단 헤어라인 chrome, 그림자 없음, 종이 질감 | 문화/브랜드/고급, 사색적 키노트 |
| **bold** | Archivo Black | 흰 + 토마토 레드 + 검정 | 3px 검정 보더, 8px 하드 오프셋 그림자, 사각 모서리, 검정 pill eyebrow | 매니페스토, 피칭, 스타트업, 강한 인상 |
| **orange** | Inter (800) | 네이비(#232f3e) + 오렌지(#ec7211) | 네이비 표 헤더, 오렌지 강조 | 격식 있는 기술·기업 발표 |

## 테마 선택 가이드

발표 성격을 테마에 매칭한다. 사용자가 지정하지 않으면 콘텐츠 톤으로 추론하되, 갈리면 사용자에게 묻는다.

- 격식·기술·정보 밀도 높음 → `vivid` 또는 `orange`
- 문화·예술·에세이·고급 브랜드·차분함 → `editorial`
- 강한 주장·피칭·도발적·자신감 → `bold`
- 네이비+오렌지 색감·기업/기술 톤 → `orange`

## 테마 JSON 스키마

```json
{
  "name": "editorial",
  "label": "Editorial — 매거진 세리프형",
  "description": "한 줄 설명 (선택 가이드용)",
  "stage_bg": "#1a1a17",
  "fonts": "<link ...>  (Google Fonts CDN, head 에 주입)",
  "vars": { "--canvas": "#efe7d4", "--accent": "#2e4a2a", ... },
  "css": ".slide .eyebrow { ... }  /* 시그니처 장식 CSS */"
}
```

- **vars**: `:root` 에 주입되는 CSS 변수. 템플릿의 베이스 토큰을 덮어쓴다. 필요한 것만 적으면 된다(나머지는 베이스 유지).
- **fonts**: `<link>` 태그(들). 시스템 폴백을 항상 var 스택 뒤에 두어 오프라인에서도 깨지지 않게 한다.
- **css**: 테마 고유의 시그니처 장식. 템플릿 맨 끝(`{{THEME_CSS}}`)에 들어가므로 컴포넌트 CSS를 덮어쓸 수 있다.
- **stage_bg**: 레터박스 여백(스테이지 바깥) 색.

## 덮어쓸 수 있는 주요 토큰

색: `--canvas --ink --charcoal --body --mute --surface-soft --surface-card --surface-dark --hairline --hairline-strong --accent --accent-strong --accent-soft --accent-ink --info(-soft) --success(-soft) --warn(-soft) --danger(-soft) --mark-bg`

형태/그림자: `--rounded-sm --rounded-lg --rounded-xl --rounded-full --shadow-card --card-border --card-accent-edge`

타이포: `--font-display --font-body --font-code --track-display --track-h2 --eyebrow-track --weight-display --weight-h2`

레이아웃: `--pad-y --pad-x` (1920×1080 기준 px)

## 새 테마 만들기

1. `themes/<name>.json` 작성 (위 스키마).
2. display 폰트는 개성 있는 것을 고른다 — Inter/Roboto/Arial 같은 "AI slop" 폰트는 display 로 쓰지 않는다. 큰 제목에는 음수 자간(`--track-display: -0.02 ~ -0.04em`)으로 덩어리감을 준다.
3. 팔레트는 3~5색으로 절제한다. 강조색 1색 + 시맨틱 보조. 부차 위계는 새 색보다 같은 색의 opacity 변형이 깔끔하다.
4. 시그니처 장식 1개를 `css` 에 정한다(배경 텍스처/상단 chrome/하드 그림자/회전 등) — 그 테마를 한눈에 알아보게 하는 무기.
5. `build_deck.py ... --theme <name>` 로 빌드하고 브라우저에서 확인.

## 고정 스테이지 원칙 (모든 테마 공통)

모든 슬라이드는 1920×1080 px 캔버스에 그려지고 JS 가 통째 scale 한다. 테마 CSS에서 슬라이드 내부 치수는 vh/vw 가 아니라 **px** 로 적는다(1920 폭 기준). 리플로우 금지 — 화면이 작아도 레터박스만 생긴다.
