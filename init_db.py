import sqlite3
import json

DB_NAME = 'vocab.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. 创建书籍表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        short_name TEXT NOT NULL,
        color TEXT NOT NULL
    )
    ''')

    # 2. 创建单词表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id TEXT,
        word TEXT NOT NULL,
        answer TEXT NOT NULL,
        exp TEXT,
        options TEXT,
        FOREIGN KEY(book_id) REFERENCES books(id)
    )
    ''')

    # 3. 创建造句题库表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sentences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chinese TEXT NOT NULL
    )
    ''')

    # --- 插入初始化数据 ---
    
    # 书籍元数据
    books_data = [
        ('cet4', '英语四级', 'CET-4', 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)'),
        ('cet6', '英语六级', 'CET-6', 'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)'),
        ('ielts', '雅思词汇', 'IELTS', 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)'),
        ('toefl', '托福词汇', 'TOEFL', 'linear-gradient(135deg, #fccb90 0%, #d57eeb 100%)')
    ]
    cursor.executemany('INSERT OR IGNORE INTO books VALUES (?,?,?,?)', books_data)

    # 单词数据 (此处仅为示例，实际使用请填入大量数据)
    words_data = [
        # CET4
        ('cet4', 'Abandon', '放弃', '遗弃，丢弃；放弃，中止。', json.dumps(["v. 放弃", "n. 能力", "adj. 绝对的", "n. 背景"])),
        ('cet4', 'Ability', '能力', '做某事的能力或才能。', json.dumps(["n. 能力", "v. 废除", "adj. 能够的", "n. 缺席"])),
        # CET6
        ('cet6', 'Abnormal', '反常的', '不正常的；反常的；变态的。', json.dumps(["adj. 反常的", "v. 废除", "adj. 突然的", "n. 缺席"])),
        # IELTS
        ('ielts', 'Academic', '学术的', '学院的；学术的；理论的。', json.dumps(["adj. 学术的", "v. 加速", "n. 途径", "v. 适应"])),
        # TOEFL
        ('toefl', 'Advocate', '提倡', '拥护；提倡；主张。', json.dumps(["v. 提倡", "v. 采用", "adj. 足够的", "adj. 美学的"]))
    ]
    cursor.executemany('INSERT INTO words (book_id, word, answer, exp, options) VALUES (?,?,?,?,?)', words_data)

    # 造句数据
    sentences_data = [
        ("那个男孩正在树下读书。",),
        ("虽然下雨了，但他还是去上班了。",),
        ("你能告诉我最近的银行在哪里吗？",),
        ("保持健康对我们要紧。",)
    ]
    cursor.executemany('INSERT INTO sentences (chinese) VALUES (?)', sentences_data)

    conn.commit()
    conn.close()
    print(f"数据库 {DB_NAME} 初始化成功！")

if __name__ == '__main__':
    init_db()