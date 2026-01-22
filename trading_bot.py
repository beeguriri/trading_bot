# [Background] - 무한 루프 도는 봇 (실행 파일 1)

import time
import config

# 🔥 원하는 전략 구현체를 Import
from app.strategies.titans_pure import TitansStrategy
from app.adapters.sqlite_manager import SQLiteManager
from app.adapters.upbit_manager import UpbitManager


def run_job():
    # 1. 의존성 객체 생성
    upbit = UpbitManager()
    db_manager = SQLiteManager("trading_bot.db")

    print("===== 🤖 봇 가동 시작 [🛡️ Titans Pure Bot (BTC+ETH)] =====")

    # 2. 전략 주입
    # trade_service = GoldenCrossTrailingStop(upbit, db_manager, config.TICKER)
    # 2. 전략 인스턴스 생성 (BTC용, ETH용 각각 생성)
    strategies = []
    for ticker in config.TARGETS:
        strategy = TitansStrategy(
            upbit_client=upbit,
            db_client=db_manager,
            ticker=ticker,
            k=config.K_VALUE,
            ma_window=config.MA_WINDOW,
            invest_amount=config.INVEST_AMOUNT
        )
        strategies.append(strategy)

    # 잔고 출력
    print(f"💰 보유 KRW: {upbit.get_balance('KRW'):,.0f}원")

    # 3. 무한 루프 실행
    while True:
        # 등록된 모든 전략(BTC, ETH)을 한 번씩 실행
        for strategy in strategies:
            strategy.process()

        # ★ 중요: 돌파 매매는 타이밍 싸움이므로 1초 단위로 체크 권장
        # (API 요청 제한은 pyupbit 내부 혹은 UpbitManager에서 처리한다고 가정)
        time.sleep(1)


# ==========================================
# 실행 진입점 (Main)
# ==========================================
if __name__ == "__main__":
    run_job()
