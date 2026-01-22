# Firebase DB 읽기/쓰기 전담

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone, timedelta
import config


class FirebaseManager:
    def __init__(self):
        self.db = None
        self._connect()

    def _connect(self):
        """Firebase 연결 초기화"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(config.FIREBASE_KEY_PATH)
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("✅ Firebase(DBManager) 초기화 완료")
        except Exception as e:
            print(f"⚠️ Firebase 연결 실패: {e}")

    def save_log(self, collection_name, data):
        """데이터 저장 (공통 메서드)"""
        if self.db is None:
            return

        try:
            # timestamp 자동 추가
            if 'timestamp' not in data:
                # KST (UTC+9) 시간대 정의
                KST = timezone(timedelta(hours=9))
                # 현재 시간을 KST로 설정 (이제 DB가 헷갈리지 않음)
                data['timestamp'] = datetime.now(KST)

            self.db.collection(collection_name).add(data)
            print(f"📝 [DB 저장] {collection_name}: {data.get('reason', '')}")
        except Exception as e:
            print(f"❌ DB 저장 에러: {e}")
