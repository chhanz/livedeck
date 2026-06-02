---
name: livedeck
description: "발표자용 대본 뷰 + 청중용 슬라이드 뷰를 BroadcastChannel로 실시간 동기화하는 듀얼 HTML 프레젠테이션 생성 스킬. 텍스트/마크다운 입력을 받아 청중용 풀스크린 슬라이드(index.html)와 발표자용 대본/미리보기/타이머 뷰(view/index.html)를 함께 만든다. 트리거 - \"발표자료 만들어줘\", \"대본 딸린 슬라이드\", \"듀얼 뷰 프레젠테이션\", \"livedeck\", \"발표 대본 슬라이드\"."
version: 1.0.0
author: chhanz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [presentation, slides, broadcastchannel, dual-view, speaker-notes]
---

# livedeck

발표자용 대본 뷰와 청중용 슬라이드 뷰를 한 쌍으로 생성하고, 같은 브라우저 내 탭/창 사이에서 BroadcastChannel로 슬라이드 전환을 실시간 동기화하는 스킬.

- 청중 뷰: 풀스크린 16:9 슬라이드 (`index.html`, 루트 `/`)
- 발표자 뷰: 75% 미리보기 + 25% 대본 패널 + 타이머 (`view/index.html`, `/view`)
- 동기화: 채널명 `livedeck-sync`, 발표자가 단일 송신자, 청중은 수신 전용

## 트리거

"발표자료 만들어줘", "대본 딸린 슬라이드", "듀얼 뷰 프레젠테이션", "livedeck", "발표 대본 슬라이드" 같은 요청.

## 범위 (v1)

- 입력: 텍스트, 마크다운(.md)만. (docx/pdf/pptx/URL/이미지는 v2.)
- 레이아웃 4종: `COVER` / `CONTENT` / `SECTION` / `CLOSING`. v2 신호가 보이면 `CONTENT`로 폴백.
- 발표자 뷰: iframe 미리보기, 대본 패널, 경과 타이머, 키보드 네비(방향키/Space/Home/End), 폰트 크기 조절, 다음 슬라이드 미리보기.
- 동기화: BroadcastChannel + 초기 핸드셰이크(`requestSync`) + URL 해시/localStorage 복원.

v2 기능(펜/스포트라이트, 무거운 파서, 나머지 레이아웃 5종, 페이스 바, 텔레프롬프터, PDF export, 원격 WebSocket)은 v1에서 구현하지 않는다.

## 작업 순서 (7단계)

1. **콘텐츠 수집**: 입력 소스(텍스트/마크다운)를 판별하고 텍스트와 구조를 뽑는다. (`references/content-ingestion.md`)
2. **구조화**: 슬라이드 배열로 정규화하고 각 슬라이드에 layout을 매핑한다. (`references/layouts.md`) id는 1부터 연속.
3. **대본 생성**: 슬라이드별 구어체 발표 대본을 쓴다. 강조/행동/멈춤 서식 사용. (`references/presenter-view-template.md`)
4. **테마 로드**: `DESIGN.md` 토큰을 읽어 CSS 변수를 정한다. footer 옵션과 lang 옵션을 반영한다.
5. **HTML 생성**: 두 템플릿의 `{{PLACEHOLDER}}`를 채워 `{topic}-deck/index.html`과 `{topic}-deck/view/index.html`을 출력한다. (`templates/`)
6. **정합성 검증**: 아래 체크리스트를 자동 확인한다. 하나라도 어긋나면 멈추고 고친다.
7. **안내**: 로컬 서버 실행법과 URL(`/`, `/view`)을 전달한다.

## 옵션

### footer (선택적 on-off, 기본값 비움)

```yaml
footer:
  enabled: false            # 전체 on-off (기본 off)
  logo_path: ""             # 없으면 생략
  copyright: ""             # 없으면 생략 (예시: "(c) 2026 Your Name")
  page_number: false        # 페이지 번호 표시
```

- 각 요소를 독립적으로 켤 수 있다 (로고만, copyright만, 번호만).
- `COVER`와 `CLOSING` 레이아웃에서는 footer를 자동으로 숨긴다.

### lang

- 기본 출력 언어는 한국어. 입력이 영문이거나 사용자가 "영문으로" 요청하면 영문으로 생성한다.
- HTML `lang` 속성을 `ko` 또는 `en`으로 설정한다.
- 폰트 스택 `'Noto Sans KR', 'Inter', system-ui, sans-serif`로 한/영 혼용을 자연스럽게 처리한다.

## 정합성 검증 체크리스트 (6단계)

- 청중 `index.html`의 `data-slide` 개수 == 발표자 `view/index.html`의 `SLIDES` 항목 수.
- 둘 다 `TOTAL_SLIDES` 값과 일치.
- `data-slide` 번호가 1부터 연속.
- 채널명이 양쪽 모두 `livedeck-sync`.
- 발표자 뷰 iframe `src`가 `../index.html`.

검증 스크립트: `scripts/check_consistency.py {topic}-deck` 로 자동 점검한다.

## 동기화 한계 (반드시 안내)

BroadcastChannel은 같은 브라우저, 같은 origin 내 탭/창에서만 동작한다. v1은 확장 디스플레이(노트북 + 빔프로젝터) 전용이며, 원격/화상 발표(다른 기기 접속)는 v1 미지원이다. 원격은 v2 WebSocket 백엔드 과제다.

## 설치

- A(Hermes): Hermes skills dir 아래 `presentation/livedeck`를 레포로 심링크한다.
- B(Claude Code): Claude Code skills dir 아래 `livedeck`를 레포로 심링크한다. `.claude-plugin`으로 마켓플레이스 등록도 가능하다.

자세한 사용법은 `README.md` 참조.
