# import os
# from flask import Flask, render_template, redirect, url_for, request, send_from_directory, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'gyanaghar_secret'
#
# #  UPDATED DATABASE CONFIG
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///database.db")
# import os
#
# database_url = os.getenv("DATABASE_URL")
#
# if database_url:
#     database_url = database_url.replace("postgres://", "postgresql://")
#
# app.config['SQLALCHEMY_DATABASE_URI'] = database_url
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# db = SQLAlchemy(app)
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"
#
# # ---------------- DATABASE MODELS ---------------- #
#
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(200))
#     role = db.Column(db.String(20), default="student")
#     secret_question = db.Column(db.String(200))
#     secret_answer = db.Column(db.String(200))
#
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     class_num = db.Column(db.Integer)
#     subject = db.Column(db.String(100))
#     chapter = db.Column(db.String(100))
#     content = db.Column(db.Text)
#     video_link = db.Column(db.String(300))
#     pdf_file = db.Column(db.String(200))
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
# # ---------------- HOME ---------------- #
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
# # ---------------- REGISTER ---------------- #
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])
#         question = request.form['secret_question']
#         answer = request.form['secret_answer'].lower()
#
#         new_user = User(
#             name=name,
#             email=email,
#             password=password,
#             secret_question=question,
#             secret_answer=answer
#         )
#
#         db.session.add(new_user)
#         db.session.commit()
#
#         return redirect(url_for('login'))
#
#     return render_template('register.html')
#
# # ---------------- LOGIN ---------------- #
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         user = User.query.filter_by(email=email).first()
#
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#
#             if user.role == "admin":
#                 return redirect(url_for('admin_dashboard'))
#             else:
#                 return redirect(url_for('dashboard'))
#
#     return render_template('login.html')
#
# # ---------------- DASHBOARD ---------------- #
#
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', name=current_user.name)
#
# # ---------------- PROFILE ---------------- #
#
# @app.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():
#
#     if request.method == 'POST':
#         current_user.name = request.form['name']
#         db.session.commit()
#         return "Profile Updated!"
#
#     return render_template('profile.html', user=current_user)
#
# # ---------------- FORGOT PASSWORD ---------------- #
#
# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email']
#         user = User.query.filter_by(email=email).first()
#
#         if user:
#             session['reset_user'] = user.id
#             return render_template('secret_question.html', question=user.secret_question)
#
#         return "Email not found"
#
#     return render_template('forgot_password.html')
#
# # ---------------- VERIFY SECRET ---------------- #
#
# @app.route('/verify_secret', methods=['POST'])
# def verify_secret():
#     answer = request.form['answer'].lower()
#     user = User.query.get(session['reset_user'])
#
#     if answer == user.secret_answer:
#         return render_template('reset_password.html')
#
#     return "Wrong Answer"
#
# # ---------------- RESET PASSWORD ---------------- #
#
# @app.route('/reset_password', methods=['POST'])
# def reset_password():
#
#     new_password = request.form['password']
#     user = User.query.get(session['reset_user'])
#
#     user.password = generate_password_hash(new_password)
#     db.session.commit()
#
#     session.pop('reset_user', None)
#
#     return redirect(url_for('login'))
#
# # ---------------- CLASS ---------------- #
#
# @app.route('/class/<int:class_num>')
# @login_required
# def class_page(class_num):
#     subjects = ["Mathematics", "Science", "English", "Odia", "Social Science"]
#     return render_template("subjects.html", class_num=class_num, subjects=subjects)
#
# # ---------------- SUBJECT ---------------- #
#
# @app.route('/class/<int:class_num>/<subject>')
# @login_required
# def subject_page(class_num, subject):
#     chapters = ["Chapter 1", "Chapter 2", "Chapter 3"]
#     return render_template("chapters.html",
#                            class_num=class_num,
#                            subject=subject,
#                            chapters=chapters)
#
# # ---------------- CHAPTER ---------------- #
#
# @app.route('/class/<int:class_num>/<subject>/<chapter>')
# @login_required
# def chapter_page(class_num, subject, chapter):
#
#     note = Note.query.filter_by(
#         class_num=class_num,
#         subject=subject,
#         chapter=chapter
#     ).first()
#
#     if note:
#         content = note.content
#         video = note.video_link
#         pdf = note.pdf_file
#     else:
#         content = "<p>No notes available yet.</p>"
#         video = None
#         pdf = None
#
#     return render_template(
#         "notes.html",
#         class_num=class_num,
#         subject=subject,
#         chapter=chapter,
#         notes=content,
#         video_link=video,
#         pdf_file=pdf
#     )
#
# # ---------------- ADMIN DASHBOARD ---------------- #
#
# @app.route('/admin')
# @login_required
# def admin_dashboard():
#     if current_user.role != "admin":
#         return "Access Denied"
#     return render_template("admin_dashboard.html")
#
# # ---------------- ADMIN ADD NOTE ---------------- #
#
# @app.route('/admin/add_note', methods=['GET', 'POST'])
# @login_required
# def admin_add_note():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     if request.method == "POST":
#         class_num = request.form['class_num']
#         subject = request.form['subject']
#         chapter = request.form['chapter']
#         content = request.form['content']
#         video_link = request.form['video_link']
#
#         pdf = request.files['pdf_file']
#         filename = None
#
#         if pdf and pdf.filename != "":
#             filename = secure_filename(pdf.filename)
#             pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#         new_note = Note(
#             class_num=class_num,
#             subject=subject,
#             chapter=chapter,
#             content=content,
#             video_link=video_link,
#             pdf_file=filename
#         )
#
#         db.session.add(new_note)
#         db.session.commit()
#
#         return redirect(url_for('admin_notes'))
#
#     return render_template("admin_add_note.html")
#
# # ---------------- ADMIN VIEW NOTES ---------------- #
#
# @app.route('/admin/notes')
# @login_required
# def admin_notes():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     notes = Note.query.all()
#     return render_template("admin_notes.html", notes=notes)
#
# # ---------------- DELETE NOTE ---------------- #
#
# @app.route('/admin/delete_note/<int:note_id>')
# @login_required
# def delete_note(note_id):
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     note = Note.query.get_or_404(note_id)
#
#     if note.pdf_file:
#         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], note.pdf_file)
#         if os.path.exists(pdf_path):
#             os.remove(pdf_path)
#
#     db.session.delete(note)
#     db.session.commit()
#
#     return redirect(url_for('admin_notes'))
#
# # ---------------- SERVE PDF ---------------- #
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# # ---------------- CREATE ADMIN ---------------- #
#
# @app.route('/create_admin')
# def create_admin():
#     admin = User(
#         name="Admin",
#         email="admin@gyanaghar.com",
#         password=generate_password_hash("admin123"),
#         role="admin",
#         secret_question="Your first school name?",
#         secret_answer="demo"
#     )
#     db.session.add(admin)
#     db.session.commit()
#     return "Admin Created Successfully!"
#
# # ---------------- LOGOUT ---------------- #
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))
#
# # ---------------- RUN APP ---------------- #
#
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)





import os
from flask import Flask, render_template, redirect, url_for, request, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "gyanaghar_secret")

# ================= DATABASE CONFIG =================
database_url = os.getenv("DATABASE_URL")

if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")
else:
    raise RuntimeError("DATABASE_URL not set!")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ================= CREATE TABLES =================
# with app.app_context():
#     db.create_all()

# ================= MODELS =================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="student")
    secret_question = db.Column(db.String(200))
    secret_answer = db.Column(db.String(200))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_num = db.Column(db.Integer)
    subject = db.Column(db.String(100))
    chapter = db.Column(db.String(100))
    content = db.Column(db.Text)
    video_link = db.Column(db.String(300))
    pdf_file = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ================= ROUTES =================

@app.route('/')
def home():
    return render_template('home.html')


# -------- REGISTER --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            return "Email already exists"

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password']),
            secret_question=request.form['secret_question'],
            secret_answer=request.form['secret_answer'].lower()
        )

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))

        return "Invalid credentials"

    return render_template('login.html')


# -------- DASHBOARD --------
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)


# -------- PROFILE --------
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form['name']
        db.session.commit()
        return "Profile Updated!"
    return render_template('profile.html', user=current_user)


# -------- FORGOT PASSWORD --------
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            session['reset_user'] = user.id
            return render_template('secret_question.html', question=user.secret_question)
        return "Email not found"
    return render_template('forgot_password.html')


# -------- VERIFY SECRET --------
@app.route('/verify_secret', methods=['POST'])
def verify_secret():
    user = User.query.get(session.get('reset_user'))
    if user and request.form['answer'].lower() == user.secret_answer:
        return render_template('reset_password.html')
    return "Wrong Answer"


# -------- RESET PASSWORD --------
@app.route('/reset_password', methods=['POST'])
def reset_password():
    user = User.query.get(session.get('reset_user'))
    if user:
        user.password = generate_password_hash(request.form['password'])
        db.session.commit()
        session.pop('reset_user', None)
        return redirect(url_for('login'))
    return "Session expired"


# -------- ADMIN DASHBOARD --------
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access Denied"
    return render_template('admin_dashboard.html')


# -------- CREATE ADMIN --------
@app.route('/create_admin')
def create_admin():

    if User.query.filter_by(email="admin@gyanaghar.com").first():
        return "Admin already exists!"

    admin = User(
        name="Admin",
        email="admin@gyanaghar.com",
        password=generate_password_hash("admin123"),
        role="admin",
        secret_question="Your first school name?",
        secret_answer="demo"
    )

    db.session.add(admin)
    db.session.commit()
    return "Admin Created Successfully!"


# -------- LOGOUT --------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# -------- LOCAL RUN --------
# if __name__ == "__main__":
#     app.run()