# Presenter View (발표자 뷰)

발표자용 `view/index.html`의 구조와 대본 작성법. 실제 뼈대는 `templates/script.template.html`에 있다.

## 레이아웃 (v1)

- 좌측 75%: 청중 뷰 iframe 미리보기 (어두운 무대 배경). 하단에 다음 슬라이드 미리보기 한 줄.
- 우측 25%: 대본 패널. 상단 카운터 + 경과 타이머, 본문 대본, 하단 컨트롤(이전/다음, 글자 크기, 타이머 리셋).

## iframe 경로 계약

iframe `src`는 항상 `../index.html`로 고정한다. 발표자 뷰가 `/view`에 있고 청중 뷰가 `/`(루트의 `index.html`)에 있으므로 same-origin 상대경로로 청중 뷰를 로드한다. 도메인에 독립적이다.

## 대본 데이터 주입

`SLIDES`는 슬라이드 번호를 키로 갖는 객체다. 생성 시 `{{SCRIPT_DATA}}` 자리에 JSON으로 주입한다.

```js
var SLIDES = {
  1: { title: "표지", script: "...", ref: "" },
  2: { title: "본론 제목", script: "...", ref: "참고: ..." }
};
```

- `title`: 다음 슬라이드 미리보기에 쓰인다.
- `script`: 대본 본문(HTML 허용). 아래 서식 클래스를 쓸 수 있다.
- `ref`: 참고/출처(선택).

## 대본 서식

| 의미 | 마크업 |
|------|--------|
| 강조 | `<span class="emphasis">...</span>` |
| 행동 지시 | `<span class="action">(청중을 본다)</span>` |
| 멈춤 | `<span class="pause">(잠깐)</span>` |

## 동기화 역할

- 발표자 뷰만 `slideChange`를 송신한다 (단일 송신자).
- 청중 뷰의 `requestSync` 질의를 받으면 현재 슬라이드를 회신한다 (초기 핸드셰이크).
- 대본 패널은 청중 뷰로 송신되지 않는다. 발표자만 본다.
