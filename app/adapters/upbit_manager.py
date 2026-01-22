# Upbit API 통신 전담 (Wrapper)

import pyupbit
import config


class UpbitManager:
    def __init__(self):
        self.upbit = pyupbit.Upbit(config.UPBIT_ACCESS_KEY, config.UPBIT_SECRET)

    # 캔들 데이터 조회
    @staticmethod
    def get_ohlcv(ticker, interval, count=100):
        try:
            return pyupbit.get_ohlcv(ticker, interval=interval, count=count)
        except Exception as e:
            print(f"❌ 차트 데이터 조회 실패: {e}")
            return None

    # 현재가 조회 (BTC)
    @staticmethod
    def get_current_price(ticker):
        try:
            return pyupbit.get_current_price(ticker)  # KRW-BTC
        except Exception as e:
            print(f"❌ 현재가 조회 실패: {e}")
            return None

    # 잔고 조회 (통합)
    def get_balance(self, ticker):
        try:
            return self.upbit.get_balance(ticker)
        except Exception as e:
            print(f"❌ 잔고 조회 실패({ticker}): {e}")
            return 0

    # 평단 조회
    def get_avg_buy_price(self, ticker):
        try:
            return self.upbit.get_avg_buy_price(ticker)     # KRW-BTC
        except Exception as e:
            print(f"❌ 코인 평단가 조회 실패: {e}")
            return 0

    def buy_market(self, ticker, amount_krw):
        """시장가 매수 (매수할 원화 금액 입력)"""
        try:
            return self.upbit.buy_market_order(ticker, amount_krw)
        except Exception as e:
            print(f"❌ 매수 주문 실패: {e}")
            return None

    def sell_market(self, ticker, volume):
        try:
            return self.upbit.sell_market_order(ticker, volume)
        except Exception as e:
            print(f"❌ 매도 실패: {e}")
            return None
