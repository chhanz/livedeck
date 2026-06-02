# livedeck

발표자는 대본과 타이머가 있는 화면을, 청중은 깔끔한 슬라이드 화면을 보는 "한 쌍의 발표 화면"을 만들어 줍니다. 발표자가 슬라이드를 넘기면 청중 화면도 자동으로 함께 넘어갑니다.

- 청중 뷰: 풀스크린 16:9 슬라이드 (`index.html`, 루트 `/`)
- 발표자 뷰: 75% 미리보기 + 25% 대본 패널 + 경과 타이머 (`view/index.html`, `/view`)
- 디자인: 모노크롬 라이트 톤 (커스텀 가능)

## 특징

- 텍스트나 마크다운을 넣으면 청중 슬라이드와 발표자 대본을 함께 생성한다.
- 발표자 화면에서 넘기면 청중 화면이 따라 넘어간다.
- 청중 화면을 늦게 열어도 자동으로 현재 슬라이드 위치에 맞춰진다.
- 화면을 새로고침해도 보던 슬라이드 위치를 그대로 복원한다.

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

두 화면의 자동 동기화는 **한 대의 컴퓨터 안에서 열린 창들 사이에서만** 동작한다. 따라서 현재 버전은 **빔프로젝터 같은 외부 화면을 연결해 발표하는 방식**에 맞춰져 있다.

- 권장: 노트북에 빔프로젝터(또는 외부 모니터)를 연결한 뒤, 청중 화면 창을 프로젝터 쪽으로 옮기고 발표자 화면은 노트북에 둔다. 한 화면에서 넘기면 다른 화면도 같이 넘어간다.
- 미지원: 청중이 각자 다른 기기(휴대폰, 다른 PC)로 접속하는 원격/화상 발표.

## 입력 / 레이아웃

- 입력: 텍스트, 마크다운.
- 레이아웃: `COVER`, `CONTENT`, `SECTION`, `IMAGE`, `CLOSING`.

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
