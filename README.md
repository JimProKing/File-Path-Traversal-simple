# File Path Traversal (simple)

Web Security Academy 랩 메모.
노트 + 연습용 스크립트.

| 분류 | 상태 | 스택 | 바로 보기 |
| --- | --- | --- | --- |
| 웹 보안 · write-up | 완료 | Burp Suite · Python | — |

**학습용만.** 허가 없는 사이트에 돌리지 말 것.

풀었음.

## 풀이 메모 (손글씨 주석)

Burp 화면을 캡처한 뒤 요청 → 변조 → 응답 흐름을 손으로 적었습니다.

<p align="center"><img src="notes/images/file-path-traversal.jpg" alt="Path Traversal 풀이 메모" width="90%"></p>

## 요약

- 상품 이미지 요청: `GET /image?filename=17.jpg`
- Burp history → Repeater
- `filename` 을 `../../../etc/passwd` 로 바꿈
- 응답에 passwd 내용 나옴 (Content-Type은 image/jpeg 이어도 상관없음)

글로 풀어쓴 건 → [notes/file-path-traversal.md](notes/file-path-traversal.md)

### 파이썬으로 같은 거 (Burp 없이)

```bash
cd tools
pip install -r requirements.txt
python path_traversal_lab.py https://랩주소.web-security-academy.net/
```

세션 쿠키 필요하면 `--session 값`  
여러 payload 시도는 `--payloads`

---

## 폴더

```
notes/          랩 메모, 스크린샷
tools/          연습용 스크립트
```

앞으로 랩 더 풀면 여기다 이어서 올릴 예정.

---

## English (short)

Personal notes while working through PortSwigger Web Security Academy labs.
Screenshot notes + small practice scripts. **Labs / authorized targets only.**

Path traversal (simple): solved — see image above and `notes/file-path-traversal.md`.
Helper: `tools/path_traversal_lab.py`.

---

**관련 저장소** · [webhacking-bible-lab](https://github.com/JimProKing/webhacking-bible-lab) · [VulnBoard](https://github.com/JimProKing/VulnBoard) · [sql-injection-lab](https://github.com/JimProKing/sql-injection-lab) · [api-hacking-notes](https://github.com/JimProKing/api-hacking-notes) · [Unprotected-Admin-Functionality-simple](https://github.com/JimProKing/Unprotected-Admin-Functionality-simple) · [dreamhack](https://github.com/JimProKing/dreamhack)

<sub>[JimProKing](https://github.com/JimProKing) · 이영찬 — 전체 저장소는 프로필의 프로젝트 지도에서 분야별로 볼 수 있습니다.</sub>
<!-- jpk-footer -->
