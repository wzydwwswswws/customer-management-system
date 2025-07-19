import sqlite3
import os

DB_PATH = 'customers.db'

if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            info TEXT NOT NULL
        )
    ''')
    
    # 添加示例数据
    sample_data = [
        ("江西省古赣酒有限责任公司", "帮我吧012323123，帮我吧密码123456"),
        ("北京科技发展有限公司", "联系人：张经理，电话：13800138000"),
        ("上海国际贸易集团", "邮箱：contact@shanghaitrade.com")
    ]
    
    c.executemany('INSERT INTO customers (name, info) VALUES (?, ?)', sample_data)
    
    conn.commit()
    conn.close()
    print("数据库初始化完成！")
else:
    print("数据库已存在，无需初始化。")