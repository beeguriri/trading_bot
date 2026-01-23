# SQLite 연결

import sqlite3
import datetime


class SQLiteManager:
    def __init__(self, db_name="trading_bot.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """거래 기록 테이블 생성"""
        query = """
        CREATE TABLE IF NOT EXISTS trade_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ticker TEXT,
            side TEXT,          -- 'BUY' or 'SELL'
            price REAL,         -- 체결 가격
            amount REAL,        -- 체결 수량
            reason TEXT,        -- 매매 사유 (골든크로스, 손절 등)
            profit_rate REAL    -- 수익률 (매도 시에만 기록, 매수는 NULL)
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def log_trade(self, ticker, side, price, amount, reason, profit_rate=None):
        """매매 기록 저장"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = """
        INSERT INTO trade_history (timestamp, ticker, side, price, amount, reason, profit_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (timestamp, ticker, side, price, amount, reason, profit_rate))
        self.conn.commit()
        print(f"💾 [DB 저장] {side} {ticker} | {price:,.0f}원 | {reason}")

    def close(self):
        self.conn.close()

    def get_trade_history(self, limit=20):
        """최근 거래 내역 조회 (API용)"""
        query = "SELECT * FROM trade_history ORDER BY id DESC LIMIT ?"
        self.cursor.execute(query, (limit,))

        # 딕셔너리 형태로 변환 (JSON 응답을 위해)
        cols = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(cols, row)))

        return results

