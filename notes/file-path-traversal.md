# File Path Traversal — simple case

Academy 랩. 풀었음.

![실습 메모](images/file-path-traversal.jpg)

## 뭐 했는지

1. 상품 페이지 들어가서 이미지 뜨게 함
2. Burp **HTTP history** 에서 `/image?filename=...` 찾음  
   (`/product?productId=...` 아님. 그거 HTML 페이지 요청임)
3. Repeater로 보냄 (Intercept 안 켜도 됨)
4. filename 바꿈:

```
../../../etc/passwd
```

5. 응답에 `root:x:0:0:` 이런 줄 나오면 성공

## 왜 됨

서버가 대충 이런 식으로 파일을 연다고 보면 됨:

```
이미지폴더/ + filename
```

`17.jpg` → 정상 이미지  
`../../../etc/passwd` → 상위 폴더 타고 시스템 파일

검증 없이 이어 붙이면 path traversal.

## 응답 볼 때

`Content-Type: image/jpeg` 떠도 본문은 텍스트일 수 있음.
중요한 건 본문에 passwd 내용이 있는지.

`/etc/passwd` 한 줄 형식:

```
이름:x:UID:GID:설명:홈:셸
```

`x` 는 비밀번호가 여기 없다는 뜻 (보통 shadow 쪽). 이 파일만으로 로그인되는 건 아님.

## 스크립트

같은 요청 다시 보내보기:

```bash
python ../tools/path_traversal_lab.py https://랩주소.web-security-academy.net/
```

---

## English

Solved the simple path traversal lab.

- Find `GET /image?filename=...` in Burp history (not the product HTML page)
- Repeater → set `filename=../../../etc/passwd`
- Body should show `/etc/passwd` lines

Server roughly does `image_dir + filename` with no checks, so `../` walks out of the folder.

Practice script: `../tools/path_traversal_lab.py` (Academy only).
