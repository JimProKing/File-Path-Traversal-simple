# Web Security Academy Notes

[![PortSwigger](https://img.shields.io/badge/PortSwigger-Web%20Security%20Academy-orange)](https://portswigger.net/web-security)
[![Purpose](https://img.shields.io/badge/purpose-learning%20%26%20notes-blue)](#)
[![Lang](https://img.shields.io/badge/docs-KO%20%7C%20EN-lightgrey)](#한국어--korean)

PortSwigger **Web Security Academy** 학습 노트 · 실습 기록 · 학습용 도구 모음입니다.  
Study notes, lab walkthroughs, and helper tools for PortSwigger **Web Security Academy**.

> **교육 목적 / Educational use only**  
> Academy 의도적 취약 랩 전용입니다. 허가 없는 실 사이트 점검에 사용하지 마세요.  
> Intended only for official Academy labs. Do not use against systems without authorization.

---

## 한국어 / Korean

### 소개

웹 보안을 체계적으로 배우기 위해 **Web Security Academy** 랩을 풀면서 정리한 저장소입니다.

- 취약점 개념을 한글로 메모
- Burp Suite로 재현한 과정을 스크린샷·단계로 기록
- 같은 요청을 파이썬으로 다시 보내 보는 **학습용 자동화** 스크립트

목표: 개념 이해 → 수동 재현 → 짧은 자동화 → 다음 랩으로 확장.

### 구성

```text
web-security-academy-notes/
├── README.md
├── notes/
│   ├── file-path-traversal.md      # Path Traversal 랩 정리
│   └── images/
│       └── file-path-traversal.jpg # 손글씨·Burp 실습 메모
└── tools/
    ├── path_traversal_lab.py       # 이미지 filename 경로 탐색 재현
    └── requirements.txt
```

### Path Traversal 랩 (완료)

| 항목 | 내용 |
|------|------|
| 랩 | File path traversal, simple case |
| 핵심 | `GET /image?filename=` 의 `filename` 조작 |
| payload | `../../../etc/passwd` |
| 결과 | 응답 본문에 `/etc/passwd` 내용 확인 |

자세한 풀이: [notes/file-path-traversal.md](notes/file-path-traversal.md)

### 도구 사용법

```bash
cd tools
pip install -r requirements.txt

# 랩 URL 입력 (Access the lab 으로 받은 주소)
python path_traversal_lab.py https://YOUR-LAB-ID.web-security-academy.net/

# 세션 쿠키가 필요할 때
python path_traversal_lab.py https://YOUR-LAB-ID.web-security-academy.net/ --session SESSION_VALUE

# 여러 payload 시도
python path_traversal_lab.py https://YOUR-LAB-ID.web-security-academy.net/ --payloads
```

### 학습 원칙

1. **먼저 수동** — Burp History / Repeater로 원리를 이해한다.
2. **그다음 자동화** — 같은 요청을 스크립트로 재현해 본다.
3. **범위 준수** — Academy·허가된 환경에서만 실험한다.
4. **기록** — 요청·응답·한 줄 요약을 남긴다.

### 앞으로

Academy 트랙을 따라 노트를 계속 추가할 예정입니다.  
(Access control, XSS, Authentication, …)

---

## English

### About

Personal study repository for **PortSwigger Web Security Academy** labs.

- Concept notes (with Korean walkthroughs)
- Screenshot-based lab records (Burp Suite)
- Small **learning-only** Python helpers that replay the same requests

Goal: understand → manual reproduce → light automation → next lab.

### Layout

```text
web-security-academy-notes/
├── README.md
├── notes/
│   ├── file-path-traversal.md
│   └── images/
│       └── file-path-traversal.jpg
└── tools/
    ├── path_traversal_lab.py
    └── requirements.txt
```

### Lab: File path traversal (simple case) — Solved

| Item | Detail |
|------|--------|
| Lab | File path traversal, simple case |
| Key | Tamper with `filename` on `GET /image?filename=` |
| Payload | `../../../etc/passwd` |
| Result | Response body contains `/etc/passwd` |

Full write-up: [notes/file-path-traversal.md](notes/file-path-traversal.md)

### Tool usage

```bash
cd tools
pip install -r requirements.txt

python path_traversal_lab.py https://YOUR-LAB-ID.web-security-academy.net/
python path_traversal_lab.py https://YOUR-LAB-ID.web-security-academy.net/ --session SESSION_VALUE
python path_traversal_lab.py https://YOUR-LAB-ID.web-security-academy.net/ --payloads
```

### Principles

1. **Manual first** — learn with Burp History / Repeater.
2. **Then automate** — replay the same request in Python.
3. **Stay in scope** — Academy (or other authorized) targets only.
4. **Write it down** — request, response, one-line takeaway.

### Roadmap

More Academy topics will be added over time  
(Access control, XSS, Authentication, and more).

---

## Disclaimer

This project is for **education and personal portfolio**.  
Do **not** use the scripts or techniques against systems you do not own or lack permission to test.

이 저장소는 **학습·포트폴리오** 목적입니다.  
소유하지 않거나 허가받지 않은 시스템에 도구·기법을 사용하지 마세요.

## License

Learning notes and scripts — use freely for personal study.  
PortSwigger Web Security Academy content and labs belong to PortSwigger.
