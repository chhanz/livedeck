# Slide Components (청중 뷰)

청중용 `index.html` 슬라이드의 HTML 골격과 컴포넌트. 실제 뼈대는 `templates/presentation.template.html`에 있다. 이 문서는 슬라이드별 마크업을 어떻게 채우는지 설명한다.

## 슬라이드 공통 골격

각 슬라이드는 `data-slide`(1부터 연속)와 `data-layout`을 갖는다. 채널/동기화 로직은 템플릿에 고정돼 있으므로 건드리지 않는다.

```html
<section class="slide" id="slide-1" data-slide="1" data-layout="COVER">
  ...
</section>
```

## 레이아웃별 마크업

### COVER
```html
<section class="slide" id="slide-1" data-slide="1" data-layout="COVER">
  <div class="eyebrow">발표 주제</div>
  <h1>발표 제목</h1>
  <p class="subtitle">한 줄 부제</p>
</section>
```

### CONTENT
```html
<section class="slide" id="slide-2" data-slide="2" data-layout="CONTENT">
  <h2>슬라이드 제목</h2>
  <ul>
    <li>핵심 포인트 1</li>
    <li>핵심 포인트 2</li>
    <li>핵심 포인트 3</li>
  </ul>
</section>
```

### SECTION
```html
<section class="slide" id="slide-3" data-slide="3" data-layout="SECTION">
  <div class="rule"></div>
  <h1>새 챕터 제목</h1>
</section>
```

### CLOSING
```html
<section class="slide" id="slide-4" data-slide="4" data-layout="CLOSING">
  <h1>감사합니다</h1>
  <p class="subtitle">you@example.com</p>
</section>
```

## 규칙

- `data-slide` 번호는 1부터 빈틈없이 연속이어야 한다.
- 슬라이드 개수는 발표자 뷰의 `SLIDES` 항목 수, `TOTAL_SLIDES` 값과 정확히 일치해야 한다 (정합성 검증 대상).
- 불릿은 3~5개를 권장한다. 그 이상이면 슬라이드를 나눈다.
- 이미지는 `assets/` 상대경로 참조를 기본으로 한다. 작은 이미지에 한해 base64 인라인을 허용한다.
