from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# 模拟选手数据（包含学号、姓名、每题得分）
rankings = [
    {'id': '2024001', 'name': 'Alice', 'scores': {'A': 100, 'B': 50, 'C': 80,'D': 50}},
    {'id': '2024002', 'name': 'Bob', 'scores': {'A': 100, 'B': 90, 'C': 40,'D': 80}},
    {'id': '2024003', 'name': 'Peter', 'scores': {'A': 80, 'B': 70, 'C': 50,'D': 90}},
]

def calculate_total_score(rankings):
    """计算每个选手的总分，并添加到选手数据中"""
    for participant in rankings:
        total_score = sum(participant['scores'].values())  # 将每道题的分数相加
        participant['totalScore'] = total_score

def calculate_ranking(rankings):
    """按总分排序，处理相同分数排名相同"""
    calculate_total_score(rankings)
    rankings.sort(key=lambda x: (-x['totalScore'], x['id']))
    rank = 1
    for i in range(len(rankings)):
        if i > 0 and rankings[i]['totalScore'] == rankings[i-1]['totalScore']:
            rankings[i]['rank'] = rankings[i-1]['rank']
        else:
            rankings[i]['rank'] = rank
        rank += 1
    return rankings

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    sorted_rankings = calculate_ranking(rankings)
    emit('rankings_update', sorted_rankings)

if __name__ == '__main__':
    socketio.run(app, debug=True)
