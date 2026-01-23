# 🤖 Trading Bot

![Build Status](https://img.shields.io/github/actions/workflow/status/beeguriri/trading_bot/deploy-dev.yml?branch=develop&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS-EC2-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-PostgreSQL-2496ED?style=flat-square&logo=docker&logoColor=white)

**Trading Bot**은 업비트(Upbit) API를 활용하여 24시간 암호화폐 시장을 감시하고, 알고리즘에 따라 자동으로 매매를 수행하는 서버 사이드 애플리케이션입니다.

감정에 휘둘리지 않는 투자를 목표로 하며, **`안정성(Stability)`** 과 **`자산 방어(Safety)`** 를 최우선으로 설계되었습니다.

---

## 📚 Documentation (Wiki)

이 프로젝트의 상세한 기획, 아키텍처, 트러블슈팅 내역은 **[GitHub Wiki](https://github.com/beeguriri/titans-bot/wiki)**에서 관리되고 있습니다.

| Category | Description |
|---|---|
| **[👋 Introduction](https://github.com/beeguriri/trading_bot/wiki/Project-Vision)** | 프로젝트 목표 및 핵심 철학 |
| **[🏗️ Architecture](https://github.com/beeguriri/trading_bot/wiki/System-Design)** | 시스템 구성도 및 기술 스택 결정(ADR) |
| **[📋 Planning](https://github.com/beeguriri/trading_bot/wiki/Functional-Requirements)** | 기능 명세서 및 개발 로드맵 |
| **[🚀 DevOps](https://github.com/beeguriri/trading_bot/wiki/Deployment-Guide)** | AWS EC2 자동 배포 가이드 및 트러블슈팅 |

---

## ✨ Key Features

* **Algorithmic Trading**: RSI, 이동평균선 등 보조지표 기반의 자동 매수/매도.
* **Health Check System**: Flask 웹 서버를 내장하여 봇의 생존 여부(Heartbeat) 실시간 모니터링.
* **CI/CD Pipeline**: GitHub Actions를 통해 `develop` 브랜치 푸시 시 AWS EC2로 자동 배포 및 재시작.
* **Panic Sell**: 급락장 발생 시 관리자 모드에서 '비상 탈출' 버튼으로 전량 시장가 매도 (Planned).
* **Data Archiving**: PostgreSQL(JSONB)을 활용한 체결 내역 및 자산 흐름 저장 (Planned).

---

## 🛠️ Tech Stack

* **Language**: Python 3.10
* **Framework**: Flask (Health Check API)
* **Infrastructure**: AWS EC2 (Ubuntu)
* **Database**: PostgreSQL (Dockerized)
* **CI/CD**: GitHub Actions
* **Libraries**: `pyupbit`, `pandas`, `schedule`, `requests`

---

## 🚀 Quick Start

로컬 개발 환경을 세팅하려면 아래 명령어를 따르세요. 더 자세한 내용은 **[Getting Started](https://github.com/beeguriri/trading_bot/wiki/Getting-Started)** 위키를 참고하세요.

```bash
# 1. Clone Repository
git clone [https://github.com/beeguriri/trading_bot.git](https://github.com/beeguriri/trading_bot.git)

# 2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Run Bot
python trading_bot.py
