from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 数据库文件路径
DB_PATH = 'customers.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
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
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('index.html', customers=customers)

@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']
        
        if not name:
            flash('客户名称不能为空!', 'error')
            return redirect(url_for('add_customer'))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO customers (name, info) VALUES (?, ?)', (name, info))
        conn.commit()
        conn.close()
        
        flash('客户添加成功!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        info = request.form['info']
        
        if not name:
            flash('客户名称不能为空!', 'error')
            return redirect(url_for('edit_customer', id=id))
        
        conn.execute('UPDATE customers SET name = ?, info = ? WHERE id = ?', (name, info, id))
        conn.commit()
        conn.close()
        
        flash('客户信息更新成功!', 'success')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', customer=customer)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM customers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('客户已删除!', 'success')
    return redirect(url_for('index'))

@app.route('/search')
def search_customers():
    keyword = request.args.get('keyword', '').strip()
    
    if not keyword:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    query = "SELECT * FROM customers WHERE name LIKE ?"
    customers = conn.execute(query, ('%' + keyword + '%',)).fetchall()
    conn.close()
    
    return render_template('index.html', customers=customers, keyword=keyword)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)