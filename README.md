# livedeck

발표자용 대본 뷰와 청중용 슬라이드 뷰를 한 쌍으로 만들고, 같은 브라우저 내 탭/창 사이에서 BroadcastChannel로 슬라이드 전환을 실시간 동기화하는 듀얼 HTML 프레젠테이션 생성 스킬.

- 청중 뷰: 풀스크린 16:9 슬라이드 (`index.html`, 루트 `/`)
- 발표자 뷰: 75% 미리보기 + 25% 대본 패널 + 경과 타이머 (`view/index.html`, `/view`)
- 디자인: 모노크롬 라이트 톤 (커스텀 가능)

## 특징

- 텍스트나 마크다운을 넣으면 청중 슬라이드와 발표자 대본을 함께 생성한다.
- 발표자 화면에서 넘기면 청중 화면이 따라 넘어간다.
- 늦게 연 청중 화면도 초기 핸드셰이크로 현재 슬라이드에 맞춰진다.
- 새로고침해도 URL 해시와 localStorage로 위치를 복원한다.

## 빠른 시작

```bash
# 1. 예제 슬라이드로 deck 생성
python3 scripts/build_deck.py examples/sample_slides.json sample-deck --title "Sample Deck"

# 2. 정합성 검증
python3 scripts/check_consistency.py sample-deck

# 3. 로컬 서버로 열기
cd sample-deck
python3 -m http.server 8000
```

- 청중 화면: `http://localhost:8000/`
- 발표자 화면: `http://localhost:8000/view`

## 발표 현장 구성 (중요)

BroadcastChannel은 같은 브라우저, 같은 origin 내 탭/창에서만 동작한다. 따라서 현재 버전은 **확장 디스플레이 전용**이다.

- 권장: 노트북에 빔프로젝터를 확장 디스플레이로 연결하고, 같은 브라우저에서 청중 창을 프로젝터로 옮긴다. 발표자 창은 노트북에 둔다.
- 미지원: 원격/화상 발표처럼 청중이 다른 기기에서 접속하는 경우. (원격 지원은 향후 과제.)

## 입력 / 레이아웃

- 입력: 텍스트, 마크다운.
- 레이아웃: `COVER`, `CONTENT`, `SECTION`, `CLOSING`.

## 디자인 커스텀

`DESIGN.md`의 토큰 값을 바꾸면 두 뷰의 테마가 함께 바뀐다. 예를 들어 강조색을 바꾸려면 `primary` 값만 수정한다.

## 설치 (스킬로 사용)

레포를 받은 뒤 스킬 디렉토리로 심링크한다. 경로는 환경에 맞게 바꾼다.

```bash
# 예: 레포가 ~/livedeck 에 있을 때
ln -s ~/livedeck "<Hermes skills dir>/presentation/livedeck"
ln -s ~/livedeck "<Claude Code skills dir>/livedeck"
```

설치 후 "발표자료 만들어줘" 같은 요청이나 `/livedeck`로 트리거한다.

## 라이선스

MIT. `LICENSE` 참조.
