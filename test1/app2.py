from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__,static_url_path="",static_folder="static")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# 设定题目编号和数量，例如3道题，编号为A、B、C
problem_labels = ['A', 'B','C','D','E','F','G','H','I','J','K']
# URL for contest data
DATA_URL = 'http://172.23.71.17/contestrank-oi.php?cid=1000'

def fetch_contest_data():
    """从URL获取并解析榜单数据，并进行分组"""
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table')
        all_participants = []
        pro_group = []
        non_pro_group = []

        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all('td')
                try:
                    scores = {}
                    total_score = 0
                    for i, label in enumerate(problem_labels):
                        score = int(cols[6 + i].text.strip()) if cols[6 + i].text.strip().isdigit() else 0 if not cols[6 + i].text.strip() else 100
                        scores[label] = score
                        total_score += score

                    participant = {
                        'id': cols[1].text.strip(),
                        'name': cols[2].text.strip(),
                        'scores': scores,
                        'totalScore': total_score
                    }

                    all_participants.append(participant)
                    # 按组分组
                    if participant['id'].startswith('241001'):
                        pro_group.append(participant)
                    else:
                        non_pro_group.append(participant)

                except ValueError as e:
                    print(f"解析数据时出错: {e}")

        return all_participants, pro_group, non_pro_group

    except requests.exceptions.RequestException as e:
        print(f"获取数据失败: {e}")
        return [], [], []


def sort_rankings(data):
    """根据总分对榜单排序，并处理并列排名"""
    data.sort(key=lambda x: x['totalScore'], reverse=True)
    rank = 1
    previous_score = None
    for i, participant in enumerate(data):
        if participant['totalScore'] != previous_score:
            rank = i + 1
        participant['rank'] = rank
        previous_score = participant['totalScore']
    return data


@app.route('/')
def all_rankings():
    """展示所有选手的排名"""
    all_participants, _, _ = fetch_contest_data()
    sorted_participants = sort_rankings(all_participants)
    return render_template('index.html', participants=sorted_participants, category='所有选手')


@app.route('/pro')
def pro_rankings():
    """展示专业组的排名"""
    _, pro_group, _ = fetch_contest_data()
    sorted_pro_group = sort_rankings(pro_group)
    return render_template('index.html', participants=sorted_pro_group, category='专业组')


@app.route('/non_pro')
def non_pro_rankings():
    """展示非专业组的排名"""
    _, _, non_pro_group = fetch_contest_data()
    sorted_non_pro_group = sort_rankings(non_pro_group)
    return render_template('index.html', participants=sorted_non_pro_group, category='非专业组')


if __name__ == '__main__':
    socketio.run(app, debug=True)
