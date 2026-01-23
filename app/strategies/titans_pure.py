from datetime import datetime
import time
import pyupbit


class TitansStrategy:
    def __init__(self, upbit_client, db_client, ticker, k=0.5, ma_window=5, invest_amount=50000):
        self.upbit = upbit_client
        self.db = db_client
        self.ticker = ticker
        self.k = k
        self.ma_window = ma_window
        self.invest_amount = invest_amount

        # 내부 상태 변수
        self.today_bought = False
        self.target_price = None
        self.ma5 = None

        # 로그 주기를 위한 변수
        self.last_log_time = time.time()
        self.log_interval = 60  # 60초마다 상태 로그 출력

        # 시작 시 1회 갱신
        self.update_indicators()

        # 재시작 시 보유 여부 체크
        if self.get_coin_balance() > 5000:
            self.today_bought = True
            print(f"[{ticker}] ℹ️ 기존 보유 물량 감지됨. 홀딩 모드로 시작.")

    def get_coin_balance(self):
        """현재 코인 보유 평가금 조회"""
        currency = self.ticker.split('-')[1]
        balance = self.upbit.get_balance(currency)
        current_price = self.upbit.get_current_price(self.ticker)
        if balance is None:
            return 0
        return float(balance) * float(current_price)

    def get_avg_buy_price(self):
        """평단가 조회"""
        currency = self.ticker.split('-')[1]
        balances = self.upbit.get_balances()
        for b in balances:
            if b['currency'] == currency:
                return float(b['avg_buy_price'])
        return 0

    def update_indicators(self):
        """목표가 및 5일선 갱신"""
        try:
            df = pyupbit.get_ohlcv(self.ticker, interval="day", count=self.ma_window + 2)
            if df is None or len(df) < self.ma_window + 1:
                return

            # 1. 5일 이평선 (전일 종가 기준)
            # -2 인덱스가 '어제' 날짜
            self.ma5 = df['close'].rolling(self.ma_window).mean().iloc[-2]

            # 2. 목표가 (시가 + 변동폭 * K)
            yesterday = df.iloc[-2]
            today_open = df.iloc[-1]['open']
            range_val = yesterday['high'] - yesterday['low']
            self.target_price = today_open + (range_val * self.k)

            # 로그 출력
            print(f"[{self.ticker}] 🎯 기준 갱신 완료 | 5일선: {self.ma5:,.0f} | 목표가: {self.target_price:,.0f}")

        except Exception as e:
            print(f"[{self.ticker}] 지표 갱신 에러: {e}")

    def sell_all(self):
        """전량 매도 (시장가)"""
        currency = self.ticker.split('-')[1]
        balance = self.upbit.get_balance(currency)

        # 5000원 어치 이상 있을 때만 매도
        if balance and (float(balance) * self.upbit.get_current_price(self.ticker)) > 5000:
            self.upbit.sell_market_order(self.ticker, balance)
            print(f"[{self.ticker}] 🌅 아침 9시 전량 매도 완료 (Time-Cut)")

    def print_heartbeat(self, current_price):
        """주기적인 생존 신고 로그"""
        now = datetime.now().strftime('%H:%M:%S')

        # 1. 보유 중일 때 (수익률 표시)
        if self.today_bought:
            avg_price = self.get_avg_buy_price()
            if avg_price > 0:
                roi = (current_price - avg_price) / avg_price * 100
                status = f"💎 홀딩중 | 수익률: {roi:+.2f}%"
            else:
                status = "💎 홀딩중"

        # 2. 미보유 & 하락장 (5일선 아래)
        elif current_price < self.ma5:
            gap = (self.ma5 - current_price) / current_price * 100
            status = f"💤 휴식중 (5일선 아래) | 추세회복까지 +{gap:.2f}% 필요"

        # 3. 미보유 & 상승장 (감시 중)
        else:
            gap = (self.target_price - current_price) / current_price * 100
            if gap > 0:
                status = f"👀 감시중 (5일선 위) | 돌파까지 {gap:.2f}% 남음"
            else:
                status = f"🔥 돌파 임박/진행중!"

        print(f"[{now}] {self.ticker} : {current_price:,.0f}원 | {status}")

    def process(self):
        """메인 루프에서 호출되는 함수"""
        try:
            now = datetime.now()

            # 1. [09:00 ~ 09:00:10] 아침 리셋 로직
            if now.hour == 9 and now.minute == 0 and 0 <= now.second <= 10:
                if self.today_bought:  # 보유 중이라면 매도
                    self.sell_all()

                # 상태 초기화 및 지표 갱신
                self.today_bought = False
                self.update_indicators()
                print(f"[{self.ticker}] 📅 하루가 시작되었습니다. 전략 재설정 완료.")
                time.sleep(1)  # 중복 실행 방지용 짧은 대기
                return

            # 3. 데이터가 없으면 패스
            if self.target_price is None or self.ma5 is None:
                self.update_indicators()
                return

            # 4. [매수 감시]
            current_price = self.upbit.get_current_price(self.ticker)

            # [생존 신고] 60초마다 로그 출력
            if time.time() - self.last_log_time > self.log_interval:
                self.print_heartbeat(current_price)
                self.last_log_time = time.time()

            # 2. 이미 매수했으면 추가 로직 없음 (손절X, 익절X -> 내일 아침 매도)
            if self.today_bought:
                return

            # 조건 A: 5일선 위에 있는가? (하락장 필터)
            # 조건 B: 목표가를 돌파했는가?
            if current_price > self.ma5 and current_price > self.target_price:
                # 잔고 확인
                krw_balance = self.upbit.get_balance("KRW")
                if krw_balance >= self.invest_amount:
                    # 매수 실행
                    self.upbit.buy_market_order(self.ticker, self.invest_amount)
                    self.today_bought = True
                    print(f"[{self.ticker}] 🚀 매수 체결! (가격: {current_price:,.0f} > 5일선 & 목표가 돌파)")
                else:
                    # 잔고 부족 로그는 너무 자주 뜨지 않게 처리 필요
                    pass

        except Exception as e:
            print(f"[{self.ticker}] 프로세스 에러: {e}")
