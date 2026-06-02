# URL Routing 과 로컬 서버

## 출력 구조

```
{topic}-deck/            (서빙 루트)
  index.html             청중용  -> /
  view/
    index.html           발표자용 -> /view
  assets/                (선택) 로고, 이미지
```

## same-origin 요건

BroadcastChannel은 같은 origin 안의 탭/창끼리만 메시지를 주고받는다. 청중 뷰(`/`)와 발표자 뷰(`/view`)를 같은 서버 루트 하위에 두어 origin을 일치시킨다. `file://`로 직접 열면 origin이 `null`이 되어 동기화가 불안정하므로 항상 http로 서빙한다.

## 로컬 서버

```
cd {topic}-deck
python3 -m http.server 8000
```

- 청중 화면: `http://localhost:8000/`
- 발표자 화면: `http://localhost:8000/view`

`/view`는 서버가 `/view/`로 301 리다이렉트한 뒤 `view/index.html`을 서빙한다.

## 발표 현장 구성 (v1 한계)

BroadcastChannel은 같은 브라우저, 같은 origin 내에서만 동작한다. 따라서 v1은 **확장 디스플레이 전용**이다.

- 권장: 노트북에 빔프로젝터를 확장 디스플레이로 연결한다. 같은 브라우저에서 청중 창을 프로젝터 모니터로 옮기고, 발표자 창은 노트북 화면에 둔다. 두 창이 같은 브라우저이므로 동기화된다.
- 미지원(v1): 원격/화상 발표처럼 청중이 다른 기기에서 접속하는 경우. 다른 브라우저/기기 사이에는 BroadcastChannel이 닿지 않는다. (원격은 v2 WebSocket 백엔드 과제.)

## 경로 참조 고정값

- 발표자 뷰 iframe `src` = `../index.html`
- 채널명 = `livedeck-sync`
