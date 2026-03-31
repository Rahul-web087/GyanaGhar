# # import os
# # from flask import Flask, render_template, redirect, url_for, request, send_from_directory, session
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# # from werkzeug.security import generate_password_hash, check_password_hash
# # from werkzeug.utils import secure_filename
# #
# # app = Flask(__name__)
# # app.config['SECRET_KEY'] = 'gyanaghar_secret'
# #
# # #  UPDATED DATABASE CONFIG
# # # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///database.db")
# # import os
# #
# # database_url = os.getenv("DATABASE_URL")
# #
# # if database_url:
# #     database_url = database_url.replace("postgres://", "postgresql://")
# #
# # app.config['SQLALCHEMY_DATABASE_URI'] = database_url
# # UPLOAD_FOLDER = 'uploads'
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# #
# # db = SQLAlchemy(app)
# #
# # login_manager = LoginManager()
# # login_manager.init_app(app)
# # login_manager.login_view = "login"
# #
# # # ---------------- DATABASE MODELS ---------------- #
# #
# # class User(UserMixin, db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100))
# #     email = db.Column(db.String(100), unique=True)
# #     password = db.Column(db.String(200))
# #     role = db.Column(db.String(20), default="student")
# #     secret_question = db.Column(db.String(200))
# #     secret_answer = db.Column(db.String(200))
# #
# # class Note(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     class_num = db.Column(db.Integer)
# #     subject = db.Column(db.String(100))
# #     chapter = db.Column(db.String(100))
# #     content = db.Column(db.Text)
# #     video_link = db.Column(db.String(300))
# #     pdf_file = db.Column(db.String(200))
# #
# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.query.get(int(user_id))
# #
# # # ---------------- HOME ---------------- #
# #
# # @app.route('/')
# # def home():
# #     return render_template('home.html')
# #
# # # ---------------- REGISTER ---------------- #
# #
# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'POST':
# #         name = request.form['name']
# #         email = request.form['email']
# #         password = generate_password_hash(request.form['password'])
# #         question = request.form['secret_question']
# #         answer = request.form['secret_answer'].lower()
# #
# #         new_user = User(
# #             name=name,
# #             email=email,
# #             password=password,
# #             secret_question=question,
# #             secret_answer=answer
# #         )
# #
# #         db.session.add(new_user)
# #         db.session.commit()
# #
# #         return redirect(url_for('login'))
# #
# #     return render_template('register.html')
# #
# # # ---------------- LOGIN ---------------- #
# #
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']
# #
# #         user = User.query.filter_by(email=email).first()
# #
# #         if user and check_password_hash(user.password, password):
# #             login_user(user)
# #
# #             if user.role == "admin":
# #                 return redirect(url_for('admin_dashboard'))
# #             else:
# #                 return redirect(url_for('dashboard'))
# #
# #     return render_template('login.html')
# #
# # # ---------------- DASHBOARD ---------------- #
# #
# # @app.route('/dashboard')
# # @login_required
# # def dashboard():
# #     return render_template('dashboard.html', name=current_user.name)
# #
# # # ---------------- PROFILE ---------------- #
# #
# # @app.route('/profile', methods=['GET', 'POST'])
# # @login_required
# # def profile():
# #
# #     if request.method == 'POST':
# #         current_user.name = request.form['name']
# #         db.session.commit()
# #         return "Profile Updated!"
# #
# #     return render_template('profile.html', user=current_user)
# #
# # # ---------------- FORGOT PASSWORD ---------------- #
# #
# # @app.route('/forgot_password', methods=['GET', 'POST'])
# # def forgot_password():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         user = User.query.filter_by(email=email).first()
# #
# #         if user:
# #             session['reset_user'] = user.id
# #             return render_template('secret_question.html', question=user.secret_question)
# #
# #         return "Email not found"
# #
# #     return render_template('forgot_password.html')
# #
# # # ---------------- VERIFY SECRET ---------------- #
# #
# # @app.route('/verify_secret', methods=['POST'])
# # def verify_secret():
# #     answer = request.form['answer'].lower()
# #     user = User.query.get(session['reset_user'])
# #
# #     if answer == user.secret_answer:
# #         return render_template('reset_password.html')
# #
# #     return "Wrong Answer"
# #
# # # ---------------- RESET PASSWORD ---------------- #
# #
# # @app.route('/reset_password', methods=['POST'])
# # def reset_password():
# #
# #     new_password = request.form['password']
# #     user = User.query.get(session['reset_user'])
# #
# #     user.password = generate_password_hash(new_password)
# #     db.session.commit()
# #
# #     session.pop('reset_user', None)
# #
# #     return redirect(url_for('login'))
# #
# # # ---------------- CLASS ---------------- #
# #
# # @app.route('/class/<int:class_num>')
# # @login_required
# # def class_page(class_num):
# #     subjects = ["Mathematics", "Science", "English", "Odia", "Social Science"]
# #     return render_template("subjects.html", class_num=class_num, subjects=subjects)
# #
# # # ---------------- SUBJECT ---------------- #
# #
# # @app.route('/class/<int:class_num>/<subject>')
# # @login_required
# # def subject_page(class_num, subject):
# #     chapters = ["Chapter 1", "Chapter 2", "Chapter 3"]
# #     return render_template("chapters.html",
# #                            class_num=class_num,
# #                            subject=subject,
# #                            chapters=chapters)
# #
# # # ---------------- CHAPTER ---------------- #
# #
# # @app.route('/class/<int:class_num>/<subject>/<chapter>')
# # @login_required
# # def chapter_page(class_num, subject, chapter):
# #
# #     note = Note.query.filter_by(
# #         class_num=class_num,
# #         subject=subject,
# #         chapter=chapter
# #     ).first()
# #
# #     if note:
# #         content = note.content
# #         video = note.video_link
# #         pdf = note.pdf_file
# #     else:
# #         content = "<p>No notes available yet.</p>"
# #         video = None
# #         pdf = None
# #
# #     return render_template(
# #         "notes.html",
# #         class_num=class_num,
# #         subject=subject,
# #         chapter=chapter,
# #         notes=content,
# #         video_link=video,
# #         pdf_file=pdf
# #     )
# #
# # # ---------------- ADMIN DASHBOARD ---------------- #
# #
# # @app.route('/admin')
# # @login_required
# # def admin_dashboard():
# #     if current_user.role != "admin":
# #         return "Access Denied"
# #     return render_template("admin_dashboard.html")
# #
# # # ---------------- ADMIN ADD NOTE ---------------- #
# #
# # @app.route('/admin/add_note', methods=['GET', 'POST'])
# # @login_required
# # def admin_add_note():
# #
# #     if current_user.role != "admin":
# #         return "Access Denied"
# #
# #     if request.method == "POST":
# #         class_num = request.form['class_num']
# #         subject = request.form['subject']
# #         chapter = request.form['chapter']
# #         content = request.form['content']
# #         video_link = request.form['video_link']
# #
# #         pdf = request.files['pdf_file']
# #         filename = None
# #
# #         if pdf and pdf.filename != "":
# #             filename = secure_filename(pdf.filename)
# #             pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# #
# #         new_note = Note(
# #             class_num=class_num,
# #             subject=subject,
# #             chapter=chapter,
# #             content=content,
# #             video_link=video_link,
# #             pdf_file=filename
# #         )
# #
# #         db.session.add(new_note)
# #         db.session.commit()
# #
# #         return redirect(url_for('admin_notes'))
# #
# #     return render_template("admin_add_note.html")
# #
# # # ---------------- ADMIN VIEW NOTES ---------------- #
# #
# # @app.route('/admin/notes')
# # @login_required
# # def admin_notes():
# #
# #     if current_user.role != "admin":
# #         return "Access Denied"
# #
# #     notes = Note.query.all()
# #     return render_template("admin_notes.html", notes=notes)
# #
# # # ---------------- DELETE NOTE ---------------- #
# #
# # @app.route('/admin/delete_note/<int:note_id>')
# # @login_required
# # def delete_note(note_id):
# #
# #     if current_user.role != "admin":
# #         return "Access Denied"
# #
# #     note = Note.query.get_or_404(note_id)
# #
# #     if note.pdf_file:
# #         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], note.pdf_file)
# #         if os.path.exists(pdf_path):
# #             os.remove(pdf_path)
# #
# #     db.session.delete(note)
# #     db.session.commit()
# #
# #     return redirect(url_for('admin_notes'))
# #
# # # ---------------- SERVE PDF ---------------- #
# #
# # @app.route('/uploads/<filename>')
# # def uploaded_file(filename):
# #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# #
# # # ---------------- CREATE ADMIN ---------------- #
# #
# # @app.route('/create_admin')
# # def create_admin():
# #     admin = User(
# #         name="Admin",
# #         email="admin@gyanaghar.com",
# #         password=generate_password_hash("admin123"),
# #         role="admin",
# #         secret_question="Your first school name?",
# #         secret_answer="demo"
# #     )
# #     db.session.add(admin)
# #     db.session.commit()
# #     return "Admin Created Successfully!"
# #
# # # ---------------- LOGOUT ---------------- #
# #
# # @app.route('/logout')
# # @login_required
# # def logout():
# #     logout_user()
# #     return redirect(url_for('home'))
# #
# # # ---------------- RUN APP ---------------- #
# #
# # if __name__ == "__main__":
# #     with app.app_context():
# #         db.create_all()
# #
# #     port = int(os.environ.get("PORT", 5000))
# #     app.run(host="0.0.0.0", port=port)
#
#
#
#
# #
# # import os
# # from flask import Flask, render_template, redirect, url_for, request, send_from_directory, session
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# # from werkzeug.security import generate_password_hash, check_password_hash
# # from werkzeug.utils import secure_filename
# #
# # app = Flask(__name__)
# # app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "gyanaghar_secret")
# #
# # # ================= DATABASE CONFIG =================
# # database_url = os.getenv("DATABASE_URL")
# #
# # if database_url:
# #     database_url = database_url.replace("postgres://", "postgresql://")
# # else:
# #     raise RuntimeError("DATABASE_URL not set!")
# #
# # app.config['SQLALCHEMY_DATABASE_URI'] = database_url
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# #
# # UPLOAD_FOLDER = 'uploads'
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# #
# # db = SQLAlchemy(app)
# #
# # login_manager = LoginManager()
# # login_manager.init_app(app)
# # login_manager.login_view = "login"
# #
# # # ================= CREATE TABLES =================
# # # with app.app_context():
# # #     db.create_all()
# #
# # # ================= MODELS =================
# #
# # class User(UserMixin, db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     name = db.Column(db.String(100))
# #     email = db.Column(db.String(100), unique=True)
# #     password = db.Column(db.String(200))
# #     role = db.Column(db.String(20), default="student")
# #     secret_question = db.Column(db.String(200))
# #     secret_answer = db.Column(db.String(200))
# #
# #
# # class Note(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     class_num = db.Column(db.Integer)
# #     subject = db.Column(db.String(100))
# #     chapter = db.Column(db.String(100))
# #     content = db.Column(db.Text)
# #     video_link = db.Column(db.String(300))
# #     pdf_file = db.Column(db.String(200))
# #
# #
# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.query.get(int(user_id))
# #
# # # ================= ROUTES =================
# #
# # @app.route('/')
# # def home():
# #     return render_template('home.html')
# #
# #
# # # -------- REGISTER --------
# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'POST':
# #         if User.query.filter_by(email=request.form['email']).first():
# #             return "Email already exists"
# #
# #         user = User(
# #             name=request.form['name'],
# #             email=request.form['email'],
# #             password=generate_password_hash(request.form['password']),
# #             secret_question=request.form['secret_question'],
# #             secret_answer=request.form['secret_answer'].lower()
# #         )
# #
# #         db.session.add(user)
# #         db.session.commit()
# #         return redirect(url_for('login'))
# #
# #     return render_template('register.html')
# #
# #
# # # db=-=-=
# #
# # @app.route('/init_db')
# # def init_db():
# #     db.create_all()
# #     return "Database Initialized Successfully!"
# #
# #
# # # -------- LOGIN --------
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         user = User.query.filter_by(email=request.form['email']).first()
# #
# #         if user and check_password_hash(user.password, request.form['password']):
# #             login_user(user)
# #             return redirect(url_for('dashboard'))
# #
# #         return "Invalid credentials"
# #
# #     return render_template('login.html')
# #
# #
# # # -------- DASHBOARD --------
# # @app.route('/dashboard')
# # @login_required
# # def dashboard():
# #     return render_template('dashboard.html', name=current_user.name)
# #
# #
# # # -------- PROFILE --------
# # @app.route('/profile', methods=['GET', 'POST'])
# # @login_required
# # def profile():
# #     if request.method == 'POST':
# #         current_user.name = request.form['name']
# #         db.session.commit()
# #         return "Profile Updated!"
# #     return render_template('profile.html', user=current_user)
# #
# #
# # # -------- FORGOT PASSWORD --------
# # @app.route('/forgot_password', methods=['GET', 'POST'])
# # def forgot_password():
# #     if request.method == 'POST':
# #         user = User.query.filter_by(email=request.form['email']).first()
# #         if user:
# #             session['reset_user'] = user.id
# #             return render_template('secret_question.html', question=user.secret_question)
# #         return "Email not found"
# #     return render_template('forgot_password.html')
# #
# #
# # # -------- VERIFY SECRET --------
# # @app.route('/verify_secret', methods=['POST'])
# # def verify_secret():
# #     user = User.query.get(session.get('reset_user'))
# #     if user and request.form['answer'].lower() == user.secret_answer:
# #         return render_template('reset_password.html')
# #     return "Wrong Answer"
# #
# #
# # # -------- RESET PASSWORD --------
# # @app.route('/reset_password', methods=['POST'])
# # def reset_password():
# #     user = User.query.get(session.get('reset_user'))
# #     if user:
# #         user.password = generate_password_hash(request.form['password'])
# #         db.session.commit()
# #         session.pop('reset_user', None)
# #         return redirect(url_for('login'))
# #     return "Session expired"
# #
# #
# # # -------- ADMIN DASHBOARD --------
# # @app.route('/admin')
# # @login_required
# # def admin_dashboard():
# #     if current_user.role != "admin":
# #         return "Access Denied"
# #     return render_template('admin_dashboard.html')
# #
# #
# # # -------- CREATE ADMIN --------
# # # @app.route('/create_admin')
# # # def create_admin():
# # #
# # #     if User.query.filter_by(email="admin@gyanaghar.com").first():
# # #         return "Admin already exists!"
# # #
# # #     admin = User(
# # #         name="Admin",
# # #         email="admin@gyanaghar.com",
# # #         password=generate_password_hash("admin123"),
# # #         role="admin",
# # #         secret_question="Your first school name?",
# # #         secret_answer="demo"
# # #     )
# # #
# # #     db.session.add(admin)
# # #     db.session.commit()
# # #     return "Admin Created Successfully!"
# #
# # @app.route('/create_admin')
# # def create_admin():
# #     try:
# #         if User.query.filter_by(email="admin@gyanaghar.com").first():
# #             return "Admin already exists!"
# #
# #         admin = User(
# #             name="Admin",
# #             email="admin@gyanaghar.com",
# #             password=generate_password_hash("admin123"),
# #             role="admin",
# #             secret_question="Your first school name?",
# #             secret_answer="demo"
# #         )
# #
# #         db.session.add(admin)
# #         db.session.commit()
# #         return "Admin Created Successfully!"
# #
# #     except Exception as e:
# #         return f"Error: {str(e)}"
# #
# #
# # # -------- LOGOUT --------
# # @app.route('/logout')
# # @login_required
# # def logout():
# #     logout_user()
# #     return redirect(url_for('home'))
# #
# #
# # # -------- LOCAL RUN --------
# # # if __name__ == "__main__":
# # #     app.run()
#
#
#
#
# import os
# from flask import Flask, render_template, redirect, url_for, request, send_from_directory, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "gyanaghar_secret")
#
# # ================= DATABASE CONFIG =================
#
# database_url = os.getenv("DATABASE_URL")
#
# if database_url:
#     database_url = database_url.replace("postgres://", "postgresql://")
#     app.config['SQLALCHEMY_DATABASE_URI'] = database_url
# else:
#     # fallback for local development
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
#
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # ================= FILE UPLOAD =================
#
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# # ================= DATABASE =================
#
# db = SQLAlchemy(app)
#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"
#
# # ================= MODELS =================
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
#
# class Note(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
#
#     content = db.Column(db.Text)
#
#     video_link = db.Column(db.String(300))
#
#     pdf_file = db.Column(db.String(200))
#
#  # ---- Update Databse models -----
#
# class Class(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#
#
# class Subject(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
#
#
# class Chapter(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# # ================= ROUTES =================
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
#
# # -------- REGISTER --------
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#
#     if request.method == 'POST':
#
#         if User.query.filter_by(email=request.form['email']).first():
#             return "Email already exists"
#
#         user = User(
#             name=request.form['name'],
#             email=request.form['email'],
#             password=generate_password_hash(request.form['password']),
#             secret_question=request.form['secret_question'],
#             secret_answer=request.form['secret_answer'].lower()
#         )
#
#         db.session.add(user)
#         db.session.commit()
#
#         return redirect(url_for('login'))
#
#     return render_template('register.html')
#
#
#
#
# # -------- LOGIN --------
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#
#     if request.method == 'POST':
#
#         user = User.query.filter_by(email=request.form['email']).first()
#
#         if user and check_password_hash(user.password, request.form['password']):
#             login_user(user)
#             return redirect(url_for('dashboard'))
#
#         return "Invalid credentials"
#
#     return render_template('login.html')
#
#
# # -------- DASHBOARD --------
# @app.route('/dashboard')
# @login_required
# def dashboard():
#
#     classes = Class.query.all()
#
#     return render_template(
#         'dashboard.html',
#         name=current_user.name,
#         classes=classes
#     )
#
# # ------- admin add note ------
# @app.route('/admin/add_note', methods=['GET', 'POST'])
# @login_required
# def admin_add_note():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     if request.method == "POST":
#
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
#         return "Course Added Successfully!"
#
#     return render_template("admin_add_note.html")
#
#
# # -------- PROFILE --------
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
#
# # -------- FORGOT PASSWORD --------
# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#
#     if request.method == 'POST':
#
#         user = User.query.filter_by(email=request.form['email']).first()
#
#         if user:
#             session['reset_user'] = user.id
#             return render_template('secret_question.html', question=user.secret_question)
#
#         return "Email not found"
#
#     return render_template('forgot_password.html')
#
#
# # -------- VERIFY SECRET --------
# @app.route('/verify_secret', methods=['POST'])
# def verify_secret():
#
#     user = User.query.get(session.get('reset_user'))
#
#     if user and request.form['answer'].lower() == user.secret_answer:
#         return render_template('reset_password.html')
#
#     return "Wrong Answer"
#
#
# # -------- RESET PASSWORD --------
# @app.route('/reset_password', methods=['POST'])
# def reset_password():
#
#     user = User.query.get(session.get('reset_user'))
#
#     if user:
#         user.password = generate_password_hash(request.form['password'])
#         db.session.commit()
#         session.pop('reset_user', None)
#         return redirect(url_for('login'))
#
#     return "Session expired"
#
#
# # -------- ADMIN DASHBOARD --------
# @app.route('/admin')
# @login_required
# def admin_dashboard():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     return render_template('admin_dashboard.html')
#
#
# # -------- CREATE ADMIN --------
# @app.route('/create_admin')
# def create_admin():
#
#     try:
#
#         if User.query.filter_by(email="admin@gyanaghar.com").first():
#             return "Admin already exists!"
#
#         admin = User(
#             name="Admin",
#             email="admin@gyanaghar.com",
#             password=generate_password_hash("admin123"),
#             role="admin",
#             secret_question="Your first school name?",
#             secret_answer="demo"
#         )
#
#         db.session.add(admin)
#         db.session.commit()
#
#         return "Admin Created Successfully!"
#
#     except Exception as e:
#         return f"Error: {str(e)}"
#
#
#
#
# # ---------- admin/add notes --------
#
#
# @app.route('/admin/notes')
# @login_required
# def admin_notes():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     notes = Note.query.all()
#
#     return render_template("admin_notes.html", notes=notes)
#
# # ----- admin add class ------
#
# @app.route('/admin/add_class', methods=['GET','POST'])
# @login_required
# def add_class():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     if request.method == "POST":
#
#         name = request.form['name']
#
#         new_class = Class(name=name)
#
#         db.session.add(new_class)
#         db.session.commit()
#
#         return redirect(url_for('admin_dashboard'))
#
#     return render_template("add_class.html")
# # ----- admin  add subject -----
# @app.route('/admin/add_subject', methods=['GET','POST'])
# @login_required
# def add_subject():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     classes = Class.query.all()
#
#     if request.method == "POST":
#
#         subject = Subject(
#             name=request.form['name'],
#             class_id=request.form['class_id']
#         )
#
#         db.session.add(subject)
#         db.session.commit()
#
#         return redirect(url_for('admin_dashboard'))
#
#     return render_template("add_subject.html", classes=classes)
# # ----- admin add chapter -----
# @app.route('/admin/add_chapter', methods=['GET','POST'])
# @login_required
# def add_chapter():
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     subjects = Subject.query.all()
#
#     if request.method == "POST":
#
#         chapter = Chapter(
#             name=request.form['name'],
#             subject_id=request.form['subject_id']
#         )
#
#         db.session.add(chapter)
#         db.session.commit()
#
#         return redirect(url_for('admin_dashboard'))
#
#     return render_template("add_chapter.html", subjects=subjects)
#
#
# #----- delete chapter ------
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
#
#
#
# # -------- Delete entire subject -----
# @app.route('/admin/delete_subject/<subject>')
# @login_required
# def delete_subject(subject):
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     Note.query.filter_by(subject=subject).delete()
#     db.session.commit()
#
#     return redirect(url_for('admin_notes'))
#
#
# # ----- delete entire class ----
# @app.route('/admin/delete_class/<int:class_num>')
# @login_required
# def delete_class(class_num):
#
#     if current_user.role != "admin":
#         return "Access Denied"
#
#     Note.query.filter_by(class_num=class_num).delete()
#     db.session.commit()
#
#     return redirect(url_for('admin_notes'))
#
#
# #-------- class -------
# @app.route('/class/<int:class_id>')
# @login_required
# def class_page(class_id):
#
#     subjects = Subject.query.filter_by(class_id=class_id).all()
#
#     return render_template(
#         "subjects.html",
#         subjects=subjects,
#         class_id=class_id
#     )
#
#
# # ------ Subject ---
# @app.route('/class/<int:class_id>/<int:subject_id>')
# @login_required
# def subject_page(class_id, subject_id):
#
#     chapters = Chapter.query.filter_by(subject_id=subject_id).all()
#
#     return render_template(
#         "chapters.html",
#         chapters=chapters,
#         class_id=class_id,
#         subject_id=subject_id
#     )
#
# # --- subject's chapter -----
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
#         content = "No notes available yet."
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
#
#
#
# # -------- LOGOUT --------
# @app.route('/logout')
# @login_required
# def logout():
#
#     logout_user()
#
#     return redirect(url_for('home'))








import os
import json
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

app = Flask(__name__)

# ================= CONFIG =================



UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "gyanaghar_secret")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

database_url = os.getenv("DATABASE_URL")

if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ================= MODELS =================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))

    role = db.Column(db.String(20), default="student")

    secret_question = db.Column(db.String(200))

    secret_answer = db.Column(db.String(200))


class Class(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50))




class Subject(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))


class Chapter(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    qa_data = db.Column(db.Text)
    content = db.Column(db.Text)
    chapter_id = db.Column(db.Integer)
    video_link = db.Column(db.String(200))
    pdf_file = db.Column(db.String(200))
    question = db.Column(db.Text)
    answer = db.Column(db.Text)


class Progress(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

    completed = db.Column(db.Boolean, default=True)

    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ================= HOME =================

@app.route('/')
def home():
    return render_template("home.html")
# ================= REGISTER =================

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password']),
            secret_question=request.form['secret_question'],
            secret_answer=request.form['secret_answer'].lower()
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ================= LOGIN =================

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect("/dashboard")

    return render_template("login.html")


# =============== Profile =============

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():

    if request.method == "POST":

        current_user.name = request.form.get("name")
        current_user.email = request.form.get("email")

        db.session.commit()

        return redirect("/profile")

    total_chapters = Chapter.query.count()

    completed_chapters = Progress.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    progress = 0

    if total_chapters > 0:
        progress = int((completed_chapters / total_chapters) * 100)

    return render_template(
        "profile.html",
        user=current_user,
        total_chapters=total_chapters,
        completed_chapters=completed_chapters,
        progress=progress
    )


# ============ Json ===========

import json

@app.template_filter('from_json')
def from_json(value):
    import json
    try:
        return json.loads(value)
    except:
        return []


#
# ================delete =========== it --=-=-

# @app.route("/init_db")
# def init_db():
#     db.drop_all()
#     db.create_all()
#     return "Database recreated successfully!"



# # ======= admin =====
# @app.route("/create_admin")
# def create_admin():
#
#     existing = User.query.filter_by(email="admin@gyanaghar.com").first()
#
#     if existing:
#         return "Admin already exists"
#
#     admin = User(
#         name="Admin",
#         email="admin@gyanaghar.com",
#         password=generate_password_hash("admin123"),
#         role="admin"
#     )
#
#     db.session.add(admin)
#     db.session.commit()
#
#     return "Admin created successfully"


# -------- CREATE ADMIN --------

#
# @app.route('/create_admin')
# def create_admin():
#
#     try:
#
#         if User.query.filter_by(email="admin@gyanaghar.com").first():
#             return "Admin already exists!"
#
#         admin = User(
#             name="Admin",
#             email="admin@gyanaghar.com",
#             password=generate_password_hash("Rahul@001"),
#             role="admin",
#             secret_question="Your first school name?",
#             secret_answer="demo"
#         )
#
#         db.session.add(admin)
#         db.session.commit()
#
#         return "Admin Created Successfully!"
#
#     except Exception as e:
#         return f"Error: {str(e)}"
#
#

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








# ================= DASHBOARD =================

@app.route('/dashboard')
@login_required
def dashboard():

    classes = Class.query.all()

    return render_template(
        "dashboard.html",
        name=current_user.name,
        classes=classes
    )


# ================= CLASS PAGE =================

@app.route('/class/<int:class_id>')
@login_required
def class_page(class_id):

    subjects = Subject.query.filter_by(class_id=class_id).all()

    return render_template(
        "subjects.html",
        subjects=subjects,
        class_id=class_id
    )


# ================= SUBJECT PAGE =================

@app.route('/subject/<int:subject_id>')
@login_required
def subject_page(subject_id):

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()

    return render_template(
        "chapters.html",
        chapters=chapters,
        subject_id=subject_id
    )


# ================= CHAPTER PAGE =================

@app.route('/chapter/<int:chapter_id>')
@login_required
def chapter_page(chapter_id):

    notes = Note.query.filter_by(chapter_id=chapter_id).all()

    note_ids = [note.id for note in notes]

    completed_notes = Progress.query.filter(
        Progress.user_id == current_user.id,
        Progress.note_id.in_(note_ids)
    ).all()

    #  ADD THIS LINE
    completed_note_ids = [p.note_id for p in completed_notes]

    total_notes = len(notes)
    completed_count = len(completed_notes)

    if total_notes > 0:
        progress_percent = int((completed_count / total_notes) * 100)
    else:
        progress_percent = 0

    return render_template(
        "notes.html",
        notes=notes,
        progress_percent=progress_percent,
        completed_note_ids=completed_note_ids   #  PASS THIS
    )





# ================= COMPLETE CHAPTER =================

@app.route('/complete/<int:chapter_id>')
@login_required
def complete_chapter(chapter_id):

    progress = Progress.query.filter_by(
        user_id=current_user.id,
        chapter_id=chapter_id
    ).first()

    if not progress:

        progress = Progress(
            user_id=current_user.id,
            chapter_id=chapter_id,
            completed=True
        )

        db.session.add(progress)

    else:
        progress.completed = True

    db.session.commit()

    return redirect(url_for("chapter_page", chapter_id=chapter_id))


# ================= SEARCH NOTES =================

@app.route('/search')
@login_required
def search():

    query = request.args.get('q')

    results = Note.query.filter(
        Note.content.ilike(f"%{query}%")
    ).all()

    return render_template(
        "search.html",
        results=results,
        query=query
    )

# ============ View Notes ===========

@app.route("/note/<int:note_id>")
@login_required
def view_note(note_id):

    note = Note.query.get_or_404(note_id)

    try:
        progress = Progress.query.filter_by(
            user_id=current_user.id,
            note_id=note_id
        ).first()

        if not progress:
            progress = Progress(
                user_id=current_user.id,
                note_id=note_id
            )
            db.session.add(progress)
            db.session.commit()

    except Exception as e:
        print("Progress Error:", e)

    return render_template("view_note.html", note=note)



# ================= LEADERBOARD =================

@app.route('/leaderboard')
@login_required
def leaderboard():

    data = db.session.execute("""

    SELECT "user".name, COUNT(progress.id) as completed

    FROM progress
    JOIN "user" ON progress.user_id = "user".id

    WHERE progress.completed = true

    GROUP BY "user".name

    ORDER BY completed DESC

    """).fetchall()

    return render_template("leaderboard.html", data=data)


# ================= ADMIN ADD CLASS =================

@app.route('/admin/add_class', methods=['GET','POST'])
@login_required
def add_class():

    if current_user.role != "admin":
        return "Access Denied"

    if request.method == "POST":

        new_class = Class(
            name=request.form.get('name')
        )

        db.session.add(new_class)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("add_class.html")


# ================= ADMIN ADD SUBJECT =================

@app.route('/admin/add_subject', methods=['GET','POST'])
@login_required
def add_subject():

    if current_user.role != "admin":
        return "Access Denied"

    classes = Class.query.all()

    if request.method == "POST":

        subject = Subject(
            name=request.form['name'],
            class_id=request.form['class_id']
        )

        db.session.add(subject)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("add_subject.html", classes=classes)



# ======= Admin Edit Note ==========


@app.route("/admin/edit_note/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):

    if current_user.role != "admin":
        return "Access Denied"

    note = Note.query.get_or_404(note_id)

    if request.method == "POST":

        note.title = request.form["title"]
        note.video_link = request.form.get("video_link")

        #  MULTIPLE Q&A UPDATE (SAFE)
        questions = request.form.getlist("question[]")
        answers = request.form.getlist("answer[]")

        qa_list = []

        for q, a in zip(questions, answers):
            q = q.strip()
            a = a.strip()

            if q and a:
                qa_list.append({
                    "question": q,
                    "answer": a
                })

        # if not
        if not qa_list:
            qa_list = []

        note.qa_data = json.dumps(qa_list)

        #  PDF UPDATE (SAFE)
        pdf = request.files.get("pdf_file")

        if pdf and pdf.filename:
            from werkzeug.utils import secure_filename
            import os

            filename = secure_filename(pdf.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            pdf.save(filepath)

            note.pdf_file = filename

        #  SAFE COMMIT
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}"

        return redirect("/admin/courses")

    return render_template("edit_note.html", note=note)




# ================= ADMIN ADD CHAPTER =================

@app.route("/admin/add_chapter", methods=["GET", "POST"])
@login_required
def add_chapter():

    classes = Class.query.all()
    subjects = Subject.query.all()

    if request.method == "POST":

        name = request.form["name"]
        subject_id = request.form["subject_id"]

        new_chapter = Chapter(
            name=name,
            subject_id=subject_id
        )

        db.session.add(new_chapter)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "add_chapter.html",
        classes=classes,
        subjects=subjects
    )


# ================= ADMIN ADD NOTE =================


import json

@app.route("/admin/add_note", methods=["GET", "POST"])
@login_required
def add_note():

    classes = Class.query.all()
    subjects = Subject.query.all()
    chapters = Chapter.query.all()

    if request.method == "POST":

        title = request.form["title"]
        chapter_id = request.form["chapter_id"]
        video_link = request.form["video_link"]

        # MULTIPLE Q&A
        questions = request.form.getlist("question[]")
        answers = request.form.getlist("answer[]")

        qa_list = []

        for q, a in zip(questions, answers):
            if q.strip() and a.strip():
                qa_list.append({
                    "question": q,
                    "answer": a
                })

        qa_json = json.dumps(qa_list)

        # PDF upload
        pdf = request.files["pdf_file"]
        filename = None

        if pdf and pdf.filename != "":
            from werkzeug.utils import secure_filename
            import os

            filename = secure_filename(pdf.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            pdf.save(filepath)

        # Save in DB
        new_note = Note(
            title=title,
            qa_data=qa_json,   #  STORE JSON
            chapter_id=chapter_id,
            video_link=video_link,
            pdf_file=filename
        )

        db.session.add(new_note)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "admin_add_note.html",
        classes=classes,
        subjects=subjects,
        chapters=chapters
    )







# ================= ADMIN ANALYTICS =================

@app.route('/admin/analytics')
@login_required
def analytics():

    if current_user.role != "admin":
        return "Access Denied"

    users = User.query.count()
    classes = Class.query.count()
    subjects = Subject.query.count()
    chapters = Chapter.query.count()
    notes = Note.query.count()

    return render_template(
        "analytics.html",
        users=users,
        classes=classes,
        subjects=subjects,
        chapters=chapters,
        notes=notes
    )


# ================= ADMIN COURSE MANAGER =================


@app.route('/admin/courses')
@login_required
def admin_courses():

    if current_user.role != "admin":
        return "Access Denied"

    courses = db.session.execute(text("""
        SELECT 
            chapter.id AS chapter_id,
            chapter.name AS chapter_name,

            subject.id AS subject_id,
            subject.name AS subject_name,

            class.id AS class_id,
            class.name AS class_name,

            note.id AS note_id

        FROM chapter
        JOIN subject ON chapter.subject_id = subject.id
        JOIN class ON subject.class_id = class.id
        LEFT JOIN note ON note.chapter_id = chapter.id

        ORDER BY class.name, subject.name, chapter.name
    """)).fetchall()

    return render_template("admin_courses.html", courses=courses)

# ======== Admin Edit Note ======
@app.route("/admin/delete_note/<int:note_id>")
@login_required
def delete_note(note_id):

    if current_user.role != "admin":
        return "Access Denied"

    note = Note.query.get_or_404(note_id)

    db.session.delete(note)
    db.session.commit()

    return redirect("/admin/courses")

# ============ Delete Class ===============


@app.route("/admin/delete_class/<int:class_id>")
@login_required
def delete_class(class_id):

    if current_user.role != "admin":
        return "Access Denied"

    # 1. Subjects
    subjects = Subject.query.filter_by(class_id=class_id).all()

    for subject in subjects:

        # 2. Chapters
        chapters = Chapter.query.filter_by(subject_id=subject.id).all()

        for chapter in chapters:

            # 3. Notes
            notes = Note.query.filter_by(chapter_id=chapter.id).all()

            for note in notes:
                # 4. Delete Progress first
                Progress.query.filter_by(note_id=note.id).delete()

            # 5. Delete Notes
            Note.query.filter_by(chapter_id=chapter.id).delete()

        # 6. Delete Chapters
        Chapter.query.filter_by(subject_id=subject.id).delete()

    # 7. Delete Subjects
    Subject.query.filter_by(class_id=class_id).delete()

    # 8. Delete Class
    Class.query.filter_by(id=class_id).delete()

    # TRY-EXCEPT HERE
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"

    return redirect("/admin/courses")





# ======== Delete Subject ============


@app.route("/admin/delete_subject/<int:subject_id>")
@login_required
def delete_subject(subject_id):

    if current_user.role != "admin":
        return "Access Denied"

    subject = Subject.query.get_or_404(subject_id)

    # delete chapters first
    for chapter in subject.chapters:
        db.session.delete(chapter)

    db.session.delete(subject)
    db.session.commit()

    return redirect(url_for("admin_courses"))





# ================= DELETE COURSE =================

@app.route("/admin/delete_course/<int:chapter_id>")
@login_required
def delete_course(chapter_id):

    if current_user.role != "admin":
        return "Access Denied"

    chapter = Chapter.query.get_or_404(chapter_id)

    # delete notes inside this chapter first
    Note.query.filter_by(chapter_id=chapter_id).delete()

    db.session.delete(chapter)
    db.session.commit()

    return redirect(url_for("admin_courses"))


# ======= Edit Chapter  ==========
@app.route('/admin/edit_chapter/<int:chapter_id>', methods=['GET','POST'])
@login_required
def edit_chapter(chapter_id):

    if current_user.role != "admin":
        return "Access Denied"

    chapter = Chapter.query.get_or_404(chapter_id)

    subjects = Subject.query.all()
    classes = Class.query.all()

    # find current class
    current_subject = Subject.query.get(chapter.subject_id)
    current_class_id = current_subject.class_id

    if request.method == "POST":

        chapter.name = request.form['name']
        chapter.subject_id = request.form['subject_id']

        db.session.commit()

        return redirect("/admin/courses")

    return render_template(
        "edit_chapter.html",
        chapter=chapter,
        subjects=subjects,
        classes=classes,
        current_class_id=current_class_id
    )


# ========== Mark as complete =========

@app.route("/mark_complete/<int:note_id>")
@login_required
def mark_complete(note_id):

    note = Note.query.get_or_404(note_id)

    # check already completed
    existing = Progress.query.filter_by(
        user_id=current_user.id,
        note_id=note_id
    ).first()

    if not existing:
        progress = Progress(
            user_id=current_user.id,
            note_id=note_id,
            chapter_id=note.chapter_id
        )
        db.session.add(progress)
        db.session.commit()

    return redirect(url_for("chapter_page", chapter_id=note.chapter_id))


# ======== Student Dashboard ======
@app.route("/student/dashboard")
@login_required
def student_dashboard():

    total_notes = Note.query.count()

    completed_notes = Progress.query.filter_by(
        user_id=current_user.id
    ).count()

    if total_notes == 0:
        progress = 0
    else:
        progress = int((completed_notes / total_notes) * 100)

    return render_template(
        "student_dashboard.html",
        total_notes=total_notes,
        completed_notes=completed_notes,
        progress=progress
    )



# ======= user delete account ========

# ================= DELETE ACCOUNT =================

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():

    user = User.query.get(current_user.id)

    db.session.delete(user)
    db.session.commit()

    logout_user()

    return redirect("/")


# ================= LOGOUT =================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect("/login")


# ================= CREATE TABLES =================

with app.app_context():
    db.create_all()


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)