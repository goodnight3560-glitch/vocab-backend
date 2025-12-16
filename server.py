from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json
import sqlite3

app = Flask(__name__)
CORS(app) # 允许跨域请求

# === 配置 AI (请填入你的 Key) ===
client = OpenAI(
    api_key="sk-iltN89r7lrASCSTSVLOWVwWyXXVqywVHaUF1ckudrFJ2mvpp",  # <--- 在这里替换你的 Key
    base_url="https://api.moonshot.cn/v1",
)

DB_NAME = 'vocab.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 1. 获取书籍列表
@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in books])

# 2. 获取单词 (支持特定书或随机测试)
@app.route('/api/book_words', methods=['GET'])
def get_book_words():
    book_id = request.args.get('book_id')
    conn = get_db_connection()
    
    if book_id == 'all_test':
        # 词汇自测：随机取15个
        words = conn.execute('SELECT * FROM words ORDER BY RANDOM() LIMIT 15').fetchall()
    else:
        # 学习模式：取该书所有单词
        words = conn.execute('SELECT * FROM words WHERE book_id = ?', (book_id,)).fetchall()
    
    conn.close()
    
    result = []
    for w in words:
        w_dict = dict(w)
        # 将数据库里的字符串选项转回数组
        try:
            w_dict['options'] = json.loads(w_dict['options'])
        except:
            w_dict['options'] = []
        result.append(w_dict)
    return jsonify(result)

# 3. 获取造句题目
@app.route('/api/sentences', methods=['GET'])
def get_sentences():
    conn = get_db_connection()
    sentences = conn.execute('SELECT * FROM sentences').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in sentences])

# 4. AI 判题 (单词)
@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    word = data.get('word')
    user_input = data.get('user_input')
    
    system_prompt = "你是一个英语单词老师。判断用户的中文输入是否是该英文单词的正确释义之一。"
    user_prompt = f"英文单词: '{word}'\n用户输入: '{user_input}'\n请返回JSON: {{'is_correct': true/false, 'explanation': '简短解释'}}"

    try:
        completion = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(completion.choices[0].message.content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. AI 判题 (造句)
@app.route('/api/check_sentence', methods=['POST'])
def check_sentence():
    data = request.json
    q = data.get('question')
    u = data.get('user_input')
    
    system_prompt = "你是一位资深英语写作老师。检查用户的英文造句是否正确翻译了中文。"
    user_prompt = f"中文: '{q}'\n用户造句: '{u}'\n请返回JSON: {{'is_correct': true/false, 'feedback': '点评', 'better_version': '参考翻译'}}"

    try:
        completion = client.chat.completions.create(
            model="kimi-k2-turbo-preview",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return jsonify(json.loads(completion.choices[0].message.content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("API Server Running on port 5000...")
    app.run(debug=True, port=5000)