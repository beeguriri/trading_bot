from flask import Flask, jsonify, request
from app.container import account_service

app = Flask(__name__)


@app.route('/')
def health_check():
    return jsonify({"status": "ok", "message": "Bot is running with Flask"})


# @app.route('/status')
# def get_status():
#     """자산 현황 조회"""
#     try:
#         data = account_service.get_portfolio_status()
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#
# @app.route('/history')
# def get_history():
#     """거래 내역 조회"""
#     try:
#         limit = request.args.get('limit', default=10, type=int)
#         history = account_service.get_trade_history(limit)
#         return jsonify(history)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
