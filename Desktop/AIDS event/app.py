from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, jsonify
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret123"
UPLOAD_FOLDER = "uploads/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    with get_db() as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            tokens INTEGER DEFAULT 50,
            bio TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS pdfs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            subject TEXT,
            description TEXT,
            filename TEXT,
            uploader_id INTEGER,
            views INTEGER DEFAULT 0,
            downloads INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS token_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            change INTEGER,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS download_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pdf_id INTEGER,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET","POST"])
def login():
    if 'user_id' in session:
        return redirect("/dashboard")
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        con=get_db();cur=con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        u=cur.fetchone()
        if u and check_password_hash(u[3],password):
            session["user_id"]=u[0]
            flash(f'Welcome back, {u[1]}!', 'success')
            return redirect("/dashboard")
        flash("Invalid email or password", "error")
    return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if 'user_id' in session:
        return redirect("/dashboard")
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        if len(password) < 6:
            flash("Password must be at least 6 characters", "error")
            return render_template("register.html")
        
        try:
            con=get_db();cur=con.cursor()
            cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                        (name, email, generate_password_hash(password)))
            cur.execute("INSERT INTO token_history(user_id,change,reason) VALUES((SELECT id FROM users WHERE email=?),50,'Welcome Bonus')",(email,))
            con.commit()
            flash("Registration successful! Please login.", "success")
            return redirect("/")
        except:
            flash("Email already exists", "error")
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    con=get_db();cur=con.cursor()
    cur.execute("SELECT name,tokens,created_at FROM users WHERE id=?",(session["user_id"],))
    user = cur.fetchone()
    
    # Get statistics
    cur.execute("SELECT COUNT(*) FROM pdfs WHERE uploader_id=?",(session["user_id"],))
    uploaded_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM download_history WHERE user_id=?",(session["user_id"],))
    downloaded_count = cur.fetchone()[0]
    
    cur.execute("SELECT SUM(views) FROM pdfs WHERE uploader_id=?",(session["user_id"],))
    total_views = cur.fetchone()[0] or 0
    
    # Recent uploads
    cur.execute("""SELECT id, title, subject, views, downloads, created_at 
                   FROM pdfs WHERE uploader_id=? ORDER BY created_at DESC LIMIT 5""",
                (session["user_id"],))
    recent_uploads = cur.fetchall()
    
    return render_template("dashboard.html", user=user, stats={
        'uploaded': uploaded_count,
        'downloaded': downloaded_count,
        'views': total_views
    }, recent_uploads=recent_uploads)

@app.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    if request.method=="POST":
        if 'pdf' not in request.files:
            flash("No file selected", "error")
            return redirect("/upload")
        
        f=request.files["pdf"]
        if f.filename == '':
            flash("No file selected", "error")
            return redirect("/upload")
        
        if not f.filename.endswith('.pdf'):
            flash("Only PDF files are allowed", "error")
            return redirect("/upload")
        
        title = request.form["title"]
        subject = request.form["subject"]
        description = request.form.get("description", "")
        
        if not title or not subject:
            flash("Title and subject are required", "error")
            return redirect("/upload")
        
        # Save file
        filename = f"{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{f.filename}"
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        
        con=get_db();cur=con.cursor()
        cur.execute("INSERT INTO pdfs(title,subject,description,filename,uploader_id) VALUES(?,?,?,?,?)",
                    (title, subject, description, filename, session["user_id"]))
        
        # Award bonus tokens for uploading
        cur.execute("UPDATE users SET tokens=tokens+10 WHERE id=?",(session["user_id"],))
        cur.execute("INSERT INTO token_history(user_id,change,reason) VALUES(?,10,'Uploaded PDF')",
                    (session["user_id"],))
        con.commit()
        flash("PDF uploaded successfully! You earned 10 tokens.", "success")
        return redirect("/dashboard")
    return render_template("upload.html")

@app.route("/pdfs")
@login_required
def pdfs():
    search = request.args.get('search', '')
    subject = request.args.get('subject', '')
    sort = request.args.get('sort', 'recent')
    
    con=get_db();cur=con.cursor()
    
    query = """SELECT pdfs.*, users.name FROM pdfs 
               JOIN users ON users.id=pdfs.uploader_id WHERE 1=1"""
    params = []
    
    if search:
        query += " AND (pdfs.title LIKE ? OR pdfs.description LIKE ?)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    if subject:
        query += " AND pdfs.subject=?"
        params.append(subject)
    
    if sort == 'popular':
        query += " ORDER BY pdfs.views DESC, pdfs.downloads DESC"
    elif sort == 'oldest':
        query += " ORDER BY pdfs.created_at ASC"
    else:  # recent
        query += " ORDER BY pdfs.created_at DESC"
    
    cur.execute(query, params)
    pdfs_list = cur.fetchall()
    
    # Get all subjects for filter
    cur.execute("SELECT DISTINCT subject FROM pdfs ORDER BY subject")
    subjects = [s[0] for s in cur.fetchall()]
    
    return render_template("view_pdfs.html", pdfs=pdfs_list, subjects=subjects, 
                         current_search=search, current_subject=subject, current_sort=sort)

@app.route("/open/<int:i>")
@login_required
def open_pdf(i):
    con=get_db();cur=con.cursor()
    cur.execute("SELECT uploader_id,filename,title FROM pdfs WHERE id=?",(i,))
    p=cur.fetchone()
    
    if not p:
        flash("PDF not found", "error")
        return redirect("/pdfs")
    
    cur.execute("SELECT tokens FROM users WHERE id=?",(session["user_id"],))
    t=cur.fetchone()[0]
    
    # Deduct tokens if viewing someone else's PDF
    if session["user_id"]!=p[0]:
        if t<5:
            flash("Insufficient tokens! You need 5 tokens to view this PDF.", "error")
            return redirect("/pdfs")
        
        cur.execute("UPDATE users SET tokens=tokens-5 WHERE id=?",(session["user_id"],))
        cur.execute("UPDATE users SET tokens=tokens+5 WHERE id=?",(p[0],))
        cur.execute("INSERT INTO token_history VALUES(NULL,?, -5,'Viewed: "+p[2]+"', datetime('now'))",(session["user_id"],))
        cur.execute("INSERT INTO token_history VALUES(NULL,?, 5,'PDF Viewed: "+p[2]+"', datetime('now'))",(p[0],))
    
    cur.execute("UPDATE pdfs SET views=views+1 WHERE id=?",(i,))
    con.commit()
    return send_from_directory(UPLOAD_FOLDER,p[1])

@app.route("/download/<int:i>")
@login_required
def download_pdf(i):
    con=get_db();cur=con.cursor()
    cur.execute("SELECT uploader_id,filename,title FROM pdfs WHERE id=?",(i,))
    p=cur.fetchone()
    
    if not p:
        flash("PDF not found", "error")
        return redirect("/pdfs")
    
    cur.execute("SELECT tokens FROM users WHERE id=?",(session["user_id"],))
    t=cur.fetchone()[0]
    
    # Deduct tokens if downloading someone else's PDF
    if session["user_id"]!=p[0]:
        if t<3:
            flash("Insufficient tokens! You need 3 tokens to download this PDF.", "error")
            return redirect("/pdfs")
        
        cur.execute("UPDATE users SET tokens=tokens-3 WHERE id=?",(session["user_id"],))
        cur.execute("UPDATE users SET tokens=tokens+3 WHERE id=?",(p[0],))
        cur.execute("INSERT INTO token_history VALUES(NULL,?, -3,'Downloaded: "+p[2]+"', datetime('now'))",(session["user_id"],))
        cur.execute("INSERT INTO token_history VALUES(NULL,?, 3,'PDF Downloaded: "+p[2]+"', datetime('now'))",(p[0],))
    
    cur.execute("UPDATE pdfs SET downloads=downloads+1 WHERE id=?",(i,))
    cur.execute("INSERT INTO download_history(user_id,pdf_id) VALUES(?,?)",(session["user_id"],i))
    con.commit()
    
    return send_from_directory(UPLOAD_FOLDER, p[1], as_attachment=True)

@app.route("/tokens")
@login_required
def tokens():
    con=get_db();cur=con.cursor()
    cur.execute("SELECT change,reason,created_at FROM token_history WHERE user_id=? ORDER BY created_at DESC",
                (session["user_id"],))
    return render_template("token_history.html",history=cur.fetchall())

@app.route("/leaderboard")
@login_required
def leaderboard():
    con=get_db();cur=con.cursor()
    cur.execute("""SELECT users.name, users.tokens, 
                   COUNT(DISTINCT pdfs.id) as uploads,
                   COALESCE(SUM(pdfs.views),0) as total_views
                   FROM users 
                   LEFT JOIN pdfs ON users.id = pdfs.uploader_id
                   GROUP BY users.id
                   ORDER BY users.tokens DESC, total_views DESC
                   LIMIT 20""")
    leaders = cur.fetchall()
    return render_template("leaderboard.html", leaders=leaders)

@app.route("/profile")
@login_required
def profile():
    con=get_db();cur=con.cursor()
    cur.execute("SELECT name,email,tokens,bio,created_at FROM users WHERE id=?",(session["user_id"],))
    user = cur.fetchone()
    
    cur.execute("SELECT COUNT(*) FROM pdfs WHERE uploader_id=?",(session["user_id"],))
    upload_count = cur.fetchone()[0]
    
    cur.execute("SELECT SUM(views) FROM pdfs WHERE uploader_id=?",(session["user_id"],))
    total_views = cur.fetchone()[0] or 0
    
    return render_template("profile.html", user=user, stats={
        'uploads': upload_count,
        'views': total_views
    })

@app.route("/edit-profile", methods=["POST"])
@login_required
def edit_profile():
    name = request.form.get("name")
    bio = request.form.get("bio", "")
    
    if not name:
        flash("Name cannot be empty", "error")
        return redirect("/profile")
    
    con=get_db();cur=con.cursor()
    cur.execute("UPDATE users SET name=?, bio=? WHERE id=?", (name, bio, session["user_id"]))
    con.commit()
    flash("Profile updated successfully!", "success")
    return redirect("/profile")

@app.route("/my-uploads")
@login_required
def my_uploads():
    con=get_db();cur=con.cursor()
    cur.execute("""SELECT id, title, subject, description, views, downloads, created_at 
                   FROM pdfs WHERE uploader_id=? ORDER BY created_at DESC""",
                (session["user_id"],))
    uploads = cur.fetchall()
    return render_template("my_uploads.html", uploads=uploads)

@app.route("/delete-pdf/<int:i>", methods=["POST"])
@login_required
def delete_pdf(i):
    con=get_db();cur=con.cursor()
    cur.execute("SELECT filename, uploader_id FROM pdfs WHERE id=?",(i,))
    pdf = cur.fetchone()
    
    if not pdf:
        flash("PDF not found", "error")
        return redirect("/my-uploads")
    
    if pdf[1] != session["user_id"]:
        flash("You can only delete your own PDFs", "error")
        return redirect("/my-uploads")
    
    # Delete file
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, pdf[0]))
    except:
        pass
    
    cur.execute("DELETE FROM pdfs WHERE id=?",(i,))
    con.commit()
    flash("PDF deleted successfully", "success")
    return redirect("/my-uploads")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)