from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "ewaste_secret_key"

def get_db():
    conn = sqlite3.connect('ewaste.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('common/home.html')

# ---------------- USER SIDE ----------------
@app.route('/user/dashboard')
def user_dashboard():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM ewaste").fetchone()[0]
    recycled = db.execute("SELECT COUNT(*) FROM ewaste WHERE status='Recycled'").fetchone()[0]
    pending = db.execute("SELECT COUNT(*) FROM ewaste WHERE status='Pending'").fetchone()[0]
    db.close()
    return render_template('user/user_dashboard.html', total=total, recycled=recycled, pending=pending)

@app.route('/user/submit', methods=['GET','POST'])
def user_submit():
    db = get_db()
    categories = db.execute("SELECT name FROM categories").fetchall()
    items = db.execute("SELECT name FROM items").fetchall()

    if request.method == 'POST':
        item = request.form['item']
        category = request.form['category']

        db.execute("""
            INSERT INTO ewaste (name,item,category,request_type,status)
            VALUES (?,?,?,?,?)
        """, (request.form['name'], item, category, 'submit', 'Pending'))
        db.commit()
        db.close()
        return redirect('/user/dashboard')
    db.close()
    return render_template('user/user_submit.html', categories=categories, items=items)


@app.route('/user/recycle', methods=['GET','POST'])
def user_recycle():
    db = get_db()
    categories = db.execute("SELECT name FROM categories").fetchall()
    items = db.execute("SELECT name FROM items").fetchall()

    if request.method == 'POST':
        item = request.form['item']
        category = request.form['category']

        db.execute("""
            INSERT INTO ewaste (name,item,category,request_type,status)
            VALUES (?,?,?,?,?)
        """, (request.form['name'], item, category, 'recycle', 'Pending'))
        db.commit()
        db.close()
        return redirect('/user/dashboard')
    db.close()
    return render_template('user/user_recycle.html', categories=categories, items=items)

@app.route('/user/track')
def user_track():
    db = get_db()
    data = db.execute("SELECT * FROM ewaste").fetchall()
    db.close()
    return render_template('user/user_track.html', data=data)

@app.route('/user/stats')
def user_stats():
    db = get_db()
    recycled = db.execute("SELECT COUNT(*) FROM ewaste WHERE status='Recycled'").fetchone()[0]
    db.close()
    return render_template('user/user_stats.html', recycled=recycled)

@app.route('/awareness')
def awareness():
    return render_template('user/awareness.html')


# ---------------- ADMIN SIDE ----------------
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        db = get_db()
        user = db.execute("""
            SELECT * FROM users WHERE username=? AND password=?
        """, (request.form['username'], request.form['password'])).fetchone()
        db.close()

        if user:
            session['admin'] = True
            return redirect('/admin/dashboard')
        return render_template('admin/admin_login.html', error="Invalid login")

    return render_template('admin/admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin/login')

    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM ewaste").fetchone()[0]
    recycle = db.execute("SELECT COUNT(*) FROM ewaste WHERE request_type='recycle'").fetchone()[0]
    recycled = db.execute("SELECT COUNT(*) FROM ewaste WHERE status='Recycled'").fetchone()[0]
    db.close()

    return render_template('admin/dashboard.html', total=total, recycle=recycle, recycled=recycled)

@app.route('/admin/manage', methods=['GET','POST'])
def admin_manage():
    if 'admin' not in session:
        return redirect('/admin/login')

    db = get_db()
    if request.method == 'POST':
        db.execute("UPDATE ewaste SET status=? WHERE id=?",
                   (request.form['status'], request.form['id']))
        db.commit()

    data = db.execute("SELECT * FROM ewaste").fetchall()
    db.close()
    return render_template('admin/admin_manage.html', data=data)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/')

# --------------------
# MAIN
# --------------------
if __name__ == '__main__':
    app.run()
