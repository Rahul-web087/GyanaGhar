import os
import json
import smtplib
from email.mime.text import MIMEText
import xml.etree.ElementTree as ET
from flask import Response
from flask_mail import Mail
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect, session, flash, render_template
from datetime import datetime, timedelta

import requests

from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# ================= CONFIG =================

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"



app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# Database
database_url = os.getenv("DATABASE_URL")

if database_url:
    database_url = database_url.replace("postgres://", "postgresql://")
else:
    database_url = "sqlite:///local.db"  # fallback

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database connection settings
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

db = SQLAlchemy(app)


from flask_migrate import Migrate
migrate = Migrate(app, db)


# Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ====== new =======

import re
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)


#================= EMAIL FUNCTION =================


def send_otp_email(to_email, otp):

    print("BREVO API STARTED")

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": os.environ.get("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "GyanaGhar",
            "email": os.environ.get("MAIL_DEFAULT_SENDER")
        },

        "to": [
            {"email": to_email}
        ],

        "subject": "GyanaGhar OTP Verification",

        "htmlContent": f"""
        <div style="font-family: Arial, sans-serif; text-align:center; padding:20px;">

            <h2 style="color:#2563eb;">GyanaGhar Login OTP</h2>

            <p>Your One-Time Password (OTP) is:</p>

            <h1 style="
                color:#dc2626;
                letter-spacing:8px;
                background:#f3f4f6;
                display:inline-block;
                padding:12px 25px;
                border-radius:8px;">
                {otp}
            </h1>

            <p>This OTP is valid for <b>5 minutes</b>.</p>

            <p style="font-size:14px;color:#555;">
                If you cannot find this email, please check your
                <b>Spam</b> or <b>Junk</b> folder.
            </p>

            <hr>

            <p style="font-size:12px;color:#777;">
                If you did not request this OTP, you can safely ignore this email.
            </p>

            <p style="font-size:12px;color:#999;">
                © 2026 GyanaGhar
            </p>

        </div>
        """
    }

    try:

        if not headers["api-key"] or not data["sender"]["email"]:
            raise ValueError("Brevo API configuration missing")

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=15
        )

        response.raise_for_status()

        print("Brevo API: Email sent successfully")

        return True

    except Exception as e:

        print("Brevo API Email Error:", str(e))

        return False


# ================= MODELS =================

from datetime import datetime

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    # LOGIN OPTIONS
    email = db.Column(db.String(100), unique=True, nullable=True)
    mobile = db.Column(db.String(15), unique=True, nullable=True)

    password = db.Column(db.String(200), nullable=True)  # allow OTP-only users
    role = db.Column(db.String(20), default="student")

    # SECURITY
    secret_question = db.Column(db.String(200))
    secret_answer = db.Column(db.String(200))

    # VERIFICATION
    is_email_verified = db.Column(db.Boolean, default=False)
    is_mobile_verified = db.Column(db.Boolean, default=False)

    # OTP SYSTEM
    otp = db.Column(db.String(6))
    otp_created_at = db.Column(db.DateTime)
    otp_attempts = db.Column(db.Integer, default=0)

    # DELETE
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email or self.mobile}>"




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
    pdf_url = db.Column(db.String(500))


class Progress(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

    completed = db.Column(db.Boolean, default=True)

    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#  PUBLIC SEO HOME

@app.route('/')
def home():

    classes = Class.query.order_by(Class.id.asc()).all()

    return render_template(
        "home.html",
        classes=classes
    )



# =====================================================
#              PUBLIC SEO ROUTES
# =====================================================


# ================= PUBLIC CLASS =================

@app.route('/learn/class/<int:class_id>')
def public_class(class_id):

    cls = Class.query.get_or_404(class_id)

    subjects = Subject.query.filter_by(
        class_id=class_id
    ).order_by(Subject.name.asc()).all()

    seo_title = f"Class {cls.name} Study Materials | GyanaGhar"

    seo_description = (
        f"Explore free Class {cls.name} study materials, "
        f"subjects, chapters and educational notes on GyanaGhar."
    )

    return render_template(
        "public_class.html",
        cls=cls,
        subjects=subjects,
        seo_title=seo_title,
        seo_description=seo_description
    )


# ================= PUBLIC SUBJECT =================

@app.route('/learn/subject/<int:subject_id>')
def public_subject(subject_id):

    subject = Subject.query.get_or_404(subject_id)

    cls = Class.query.get_or_404(subject.class_id)

    chapters = Chapter.query.filter_by(
        subject_id=subject_id
    ).order_by(Chapter.id.asc()).all()

    seo_title = (
        f"{subject.name} Class {cls.name} Notes "
        f"and Chapters | GyanaGhar"
    )

    seo_description = (
        f"Study {subject.name} for Class {cls.name}. "
        f"Explore free chapters, notes and learning materials on GyanaGhar."
    )

    return render_template(
        "public_subject.html",
        subject=subject,
        cls=cls,
        chapters=chapters,
        seo_title=seo_title,
        seo_description=seo_description
    )


# ================= PUBLIC CHAPTER =================

@app.route('/learn/chapter/<int:chapter_id>')
def public_chapter(chapter_id):

    chapter = Chapter.query.get_or_404(chapter_id)

    subject = Subject.query.get_or_404(
        chapter.subject_id
    )

    cls = Class.query.get_or_404(subject.class_id)

    notes = Note.query.filter_by(
        chapter_id=chapter_id
    ).order_by(Note.id.asc()).all()

    seo_title = (
        f"{chapter.name} - {subject.name} "
        f"Class {cls.name} | GyanaGhar"
    )

    seo_description = (
        f"Learn {chapter.name} from {subject.name}, "
        f"Class {cls.name}. Find free study notes and learning resources on GyanaGhar."
    )

    return render_template(
        "public_chapter.html",
        chapter=chapter,
        subject=subject,
        cls=cls,
        notes=notes,
        seo_title=seo_title,
        seo_description=seo_description
    )


# ================= PUBLIC NOTE PREVIEW =================

@app.route('/learn/note/<int:note_id>')
def public_note_preview(note_id):

    note = Note.query.get_or_404(note_id)

    chapter = Chapter.query.get_or_404(
        note.chapter_id
    )

    subject = Subject.query.get_or_404(
        chapter.subject_id
    )

    cls = Class.query.get_or_404(subject.class_id)

    preview = ""

    if note.content:
        preview = note.content[:180].strip()

    seo_title = (
        f"{chapter.name} {subject.name} "
        f"Class {cls.name} Notes | GyanaGhar"
    )

    seo_description = (
        f"Read study notes for {chapter.name}, "
        f"{subject.name}, Class {cls.name} on GyanaGhar. "
        f"Explore free educational resources."
    )

    return render_template(
        "public_note_preview.html",
        note=note,
        chapter=chapter,
        subject=subject,
        cls=cls,
        preview=preview,
        seo_title=seo_title,
        seo_description=seo_description
    )

# ================= REGISTER =================


#  Password validation function
def is_strong_password(password):
    return (
        len(password) >= 6 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )



# STUDENT / ADMIN REGISTRATION

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Email validation
        if not is_valid_email(email):
            return "Invalid email format"

        # Check existing user
        if User.query.filter_by(email=email).first():
            return "Email already exists"

        # Password confirmation
        if password != confirm:
            return "Passwords do not match"

        # Strong password validation
        if not is_strong_password(password):
            return (
                "Password must be at least 6 characters and include "
                "uppercase, lowercase, number, and special character"
            )

        # Generate OTP
        otp = generate_otp()

        # Admin logic
        # IMPORTANT: Replace this with secure server-side admin configuration.
        if email == "your_email@gmail.com":
            role = "admin"
            is_email_verified = True
        else:
            role = "student"
            is_email_verified = False

        # Create user
        user = User(
            name=request.form.get('name', '').strip(),
            email=email,
            password=generate_password_hash(password),
            secret_question=request.form.get('secret_question'),
            secret_answer=request.form.get('secret_answer', '').lower(),
            otp=otp if role != "admin" else None,
            role=role,
            is_email_verified=is_email_verified,
            otp_created_at=datetime.utcnow() if role != "admin" else None,
            otp_attempts=0
        )

        db.session.add(user)
        db.session.commit()

        # Send OTP to student
        if role == "student":

            try:
                email_sent = send_otp_email(email, otp)
                if not email_sent:
                    raise RuntimeError("Brevo did not confirm email delivery")

            except Exception:
                app.logger.exception("Registration OTP email failed")

                db.session.delete(user)
                db.session.commit()

                return "Unable to send OTP. Please try again."

            session['otp_user_id'] = user.id
            session['otp_purpose'] = 'register'

            return redirect('/verify_otp')

        return redirect('/login')

    return render_template("register.html")


# ==========================================
# SEND OTP - FORGOT PASSWORD
# ==========================================

@app.route('/send-otp', methods=['POST'])
def send_otp():

    email = request.form.get('email', '').strip().lower()

    if not email:
        flash("Enter email")
        return redirect('/forgot_password')

    # Find existing user
    user = User.query.filter_by(
        email=email,
        is_deleted=False
    ).first()

    # Do not create incomplete users
    if not user or not user.is_email_verified:
        flash("If the account is eligible, an OTP will be sent.")
        return redirect('/forgot_password')

    # Generate OTP
    otp = generate_otp()

    # Save OTP
    user.otp = otp
    user.otp_created_at = datetime.utcnow()
    user.otp_attempts = 0

    db.session.commit()

    # Session
    session['otp_user_id'] = user.id
    session['otp_purpose'] = 'reset_password'

    # Send OTP through Brevo
    try:

        if not send_otp_email(email, otp):
            raise RuntimeError("Brevo did not confirm email delivery")

        flash("OTP sent! Check Inbox or Spam folder.")

        return redirect('/verify_otp')

    except Exception:

        app.logger.exception("Password reset OTP email failed")

        user.otp = None
        user.otp_created_at = None

        db.session.commit()

        session.pop('otp_user_id', None)
        session.pop('otp_purpose', None)

        flash("Unable to send OTP. Please try again.")

        return redirect('/forgot_password')


# ==========================================
# VERIFY OTP
# ==========================================

@app.route('/verify_otp', methods=['GET', 'POST'])
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():

    user_id = session.get('otp_user_id')
    purpose = session.get('otp_purpose')

    # Check session
    if not user_id or not purpose:
        return redirect('/login')

    user = db.session.get(User, user_id)

    if not user:
        session.pop('otp_user_id', None)
        session.pop('otp_purpose', None)
        return redirect('/login')

    if user.otp_attempts is None:
        user.otp_attempts = 0

    if request.method == "POST":

        user_otp = request.form.get('otp', '').strip()

        # Maximum attempts
        if user.otp_attempts >= 5:

            return render_template(
                "verify_otp.html",
                error="Too many attempts. Try again later."
            )

        # OTP expiry check
        if (
            not user.otp_created_at or
            datetime.utcnow() - user.otp_created_at > timedelta(minutes=5)
        ):

            return render_template(
                "verify_otp.html",
                error="OTP expired. Please request a new OTP."
            )

        # OTP verification
        if not user.otp or user.otp != user_otp:

            user.otp_attempts += 1
            db.session.commit()

            return render_template(
                "verify_otp.html",
                error="Invalid OTP"
            )

        # ==================================
        # OTP SUCCESS
        # ==================================

        user.is_email_verified = True
        user.otp = None
        user.otp_created_at = None
        user.otp_attempts = 0

        db.session.commit()

        # Registration verification
        if purpose == 'register':

            session.pop('otp_user_id', None)
            session.pop('otp_purpose', None)

            flash("Email verified successfully. Please login.")

            return redirect('/login')

        # Password reset verification
        elif purpose == 'reset_password':

            session['reset_verified'] = True
            session.pop('otp_purpose', None)

            return redirect('/reset-password')

        # Login email verification
        elif purpose == 'login_verification':

            session.pop('otp_user_id', None)
            session.pop('otp_purpose', None)
            flash("Email verified successfully. Please login.")
            return redirect('/login')

        # Invalid purpose
        session.pop('otp_user_id', None)
        session.pop('otp_purpose', None)

        return redirect('/login')

    return render_template("verify_otp.html")



# ================= ALL LEGAL TEARM ==============

@app.route("/privacy-policy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")




# ================= LOGIN =================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Find user
        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template(
                "login.html",
                error="Invalid email or password"
            )

        # Deleted account check
        if user.is_deleted:
            return render_template(
                "login.html",
                error="This account has been deleted by admin"
            )

        # Password check FIRST
        if not user.password or not check_password_hash(user.password, password):
            session['attempts'] = session.get('attempts', 0) + 1

            if session['attempts'] >= 5:
                return render_template(
                    "login.html",
                    error="Too many attempts. Try later."
                )

            return render_template(
                "login.html",
                error="Invalid email or password"
            )

        # Successful password check
        session['attempts'] = 0

        # Student email verification
        if not user.is_email_verified and user.role != "admin":

            otp = generate_otp()

            user.otp = otp
            user.otp_created_at = datetime.utcnow()
            user.otp_attempts = 0

            db.session.commit()

            try:
                if not send_otp_email(user.email, otp):
                    raise RuntimeError("Brevo did not confirm email delivery")

            except Exception:
                app.logger.exception("Login OTP email failed")

                user.otp = None
                user.otp_created_at = None
                db.session.commit()

                return render_template(
                    "login.html",
                    error="Unable to send OTP. Please try again."
                )

            session['otp_user_id'] = user.id
            session['otp_purpose'] = 'login_verification'

            return redirect('/verify_otp')

        # Login successful
        login_user(user)

        # Clear previous OTP session data
        session.pop('otp_user_id', None)
        session.pop('otp_purpose', None)
        session.pop('reset_verified', None)

        # Role-based redirect
        if user.role == "admin":
            return redirect(url_for('dashboard'))

        return redirect(url_for('student_dashboard'))

    return render_template("login.html")



# =========== Resend OTP ========
@app.route('/resend_otp', methods=['POST'])
def resend_otp():

    user_id = session.get('otp_user_id')   #  FIXED

    if not user_id:
        return redirect("/login")

    user = User.query.get(user_id)

    if not user:
        return redirect("/login")

    otp = generate_otp()

    user.otp = otp
    user.otp_created_at = datetime.utcnow()
    user.otp_attempts = 0   # reset attempts

    db.session.commit()

    if not send_otp_email(user.email, otp):
        user.otp = None
        user.otp_created_at = None
        db.session.commit()
        flash("Unable to send OTP. Please try again.")
        return redirect("/login")

    flash("OTP sent again!")   # better UX

    return redirect("/verify_otp")

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



@app.template_filter('from_json')
def from_json(value):
    import json
    try:
        return json.loads(value)
    except:
        return []




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
    answer = request.form.get('answer', '').strip().lower()

    if user and answer == (user.secret_answer or '').strip().lower():
        # Allow the existing reset-password route to process this verified flow.
        session['otp_user_id'] = user.id
        session['reset_verified'] = True
        session.pop('reset_user', None)
        return redirect('/reset-password')

    return "Wrong Answer", 400


# -------- RESET PASSWORD --------


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

    # Check OTP verification session
    user_id = session.get('otp_user_id')

    if not user_id or session.get('reset_verified') is not True:
        return redirect('/login')

    user = db.session.get(User, user_id)

    if not user:
        session.pop('otp_user_id', None)
        session.pop('reset_verified', None)
        return redirect('/login')

    if request.method == "POST":

        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Password match check
        if password != confirm:
            return render_template(
                "reset_password.html",
                error="Passwords do not match"
            )

        # Strong password check
        if not is_strong_password(password):
            return render_template(
                "reset_password.html",
                error="Password must include uppercase, lowercase, number and special character, and be at least 6 characters."
            )

        # Hash new password
        user.password = generate_password_hash(password)

        # Clear OTP fields
        user.otp = None
        user.otp_created_at = None
        user.otp_attempts = 0

        db.session.commit()

        # Clear reset session
        session.pop('otp_user_id', None)
        session.pop('reset_verified', None)
        session.pop('otp_purpose', None)

        flash("Password changed successfully. Please login.")

        return redirect('/login')

    return render_template("reset_password.html")



# temporary file

from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if current_user.role != "admin":
        return "Unauthorized", 403

    if request.method == "POST":

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(
            current_user.password,
            current_password
        ):
            return render_template(
                "change_password.html",
                error="Current password is incorrect"
            )

        if new_password != confirm_password:
            return render_template(
                "change_password.html",
                error="New passwords do not match"
            )

        if len(new_password) < 8:
            return render_template(
                "change_password.html",
                error="Password must be at least 8 characters"
            )

        current_user.password = generate_password_hash(new_password)

        db.session.commit()

        return render_template(
            "change_password.html",
            success="Password changed successfully"
        )

    return render_template("change_password.html")


# ========= Google html route ========
from flask import send_from_directory

@app.route('/googlee1fd71ed91d76751.html')
def google_verify():
    return send_from_directory('static', 'googlee1fd71ed91d76751.html')


# ========= Roboots txt =======



@app.route('/robots.txt')
def robots():
    return Response("""User-agent: *
Allow: /

Sitemap: https://gyanaghar.onrender.com/sitemap.xml
""", mimetype="text/plain")





# ========== sitemap =======





import xml.etree.ElementTree as ET

from flask import Response, url_for


@app.route("/sitemap.xml")
def sitemap():

    base_url = "https://gyanaghar.onrender.com"

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"

    ET.register_namespace("", namespace)

    # Create XML root
    urlset = ET.Element(f"{{{namespace}}}urlset")

    # Prevent duplicate URLs
    added_urls = set()

    def add_url(url):
        if url not in added_urls:
            added_urls.add(url)

            url_element = ET.SubElement(
                urlset, f"{{{namespace}}}url"
            )

            ET.SubElement(
                url_element, f"{{{namespace}}}loc"
            ).text = url

    # Homepage
    add_url(base_url + "/")

    # Public information pages
    add_url(base_url + "/about")
    add_url(base_url + "/privacy-policy")
    add_url(base_url + "/terms")
    add_url(base_url + "/disclaimer")

    # Dynamic class URLs
    classes = Class.query.order_by(Class.id.asc()).all()

    for cls in classes:

        add_url(
            base_url + url_for(
                "public_class",
                class_id=cls.id
            )
        )

        # Subjects
        subjects = Subject.query.filter_by(
            class_id=cls.id
        ).all()

        for subject in subjects:

            add_url(
                base_url + url_for(
                    "public_subject",
                    subject_id=subject.id
                )
            )

            # Chapters
            chapters = Chapter.query.filter_by(
                subject_id=subject.id
            ).all()

            for chapter in chapters:

                add_url(
                    base_url + url_for(
                        "public_chapter",
                        chapter_id=chapter.id
                    )
                )

                # Notes
                notes = Note.query.filter_by(
                    chapter_id=chapter.id
                ).all()

                for note in notes:

                    add_url(
                        base_url + url_for(
                            "public_note_preview",
                            note_id=note.id
                        )
                    )

    # Generate XML
    xml_data = ET.tostring(
        urlset,
        encoding="utf-8",
        xml_declaration=True
    )

    return Response(
        xml_data,
        mimetype="application/xml"
    )






# ================= DASHBOARD =================


@app.route("/dashboard")
@app.route("/admin/dashboard")  # Backward-compatible URL used by older links
@login_required
def dashboard():

    if current_user.role != "admin":
        return redirect(url_for("student_dashboard"))

    total_subjects = Subject.query.count()
    total_chapters = Chapter.query.count()
    total_notes = Note.query.count()
    total_users = User.query.count()

    #  SOFT DELETE STATS
    active_users = User.query.filter_by(is_deleted=False).count()
    deleted_users = User.query.filter_by(is_deleted=True).count()

    # classes
    classes = Class.query.all()

    return render_template(
        "dashboard.html",
        subjects=total_subjects,
        chapters=total_chapters,
        notes=total_notes,
        total_users=total_users,
        active_users=active_users,
        deleted_users=deleted_users,
        classes=classes
    )





# ========== VIEW PDF ============

@app.route("/view_pdf")
@login_required
def view_pdf():
    pdf_url = request.args.get("url")
    return render_template("pdf_viewer.html", pdf_url=pdf_url)






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

            import os

            pdf = request.files["pdf_file"]

            if pdf and pdf.filename != "":
                upload = cloudinary.uploader.upload(
                    pdf,
                    resource_type="raw"
                )

                note.pdf_url = upload['secure_url']

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

    if current_user.role != "admin":
        return "Access Denied", 403

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

    if current_user.role != "admin":
        return "Access Denied", 403

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
        pdf_url = None

        if pdf and pdf.filename != "":
            upload = cloudinary.uploader.upload(
                pdf,
                resource_type="raw"
            )

            pdf_url = upload['secure_url']

        # Save in DB
        new_note = Note(
            title=title,
            qa_data=qa_json,
            chapter_id=chapter_id,
            video_link=video_link,
            pdf_url=pdf_url
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

    try:
        cls = Class.query.get(class_id)

        if not cls:
            return "Class not found"

        #  Delete related data step-by-step

        subjects = Subject.query.filter_by(class_id=class_id).all()

        for subject in subjects:

            chapters = Chapter.query.filter_by(subject_id=subject.id).all()

            for chapter in chapters:

                notes = Note.query.filter_by(chapter_id=chapter.id).all()

                for note in notes:
                    # Delete progress first
                    Progress.query.filter_by(note_id=note.id).delete()

                # Delete notes
                Note.query.filter_by(chapter_id=chapter.id).delete()

            # Delete chapters
            Chapter.query.filter_by(subject_id=subject.id).delete()

        # Delete subjects
        Subject.query.filter_by(class_id=class_id).delete()

        # Delete class
        db.session.delete(cls)

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

    if current_user.role == "admin":
        return redirect(url_for("dashboard"))

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


# ======== Admin User Find =======
@app.route('/admin/users')
@login_required
def admin_users():

    if current_user.role != "admin":
        return "Access Denied"

    users = User.query.all()

    return render_template("admin_users.html", users=users)



# ====== Admin Delete User =========

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):

    if current_user.role != "admin":
        return "Access Denied"

    user = User.query.get(user_id)

    if not user:
        return "User not found"

    #  prevent deleting admin
    if user.role == "admin":
        return "Cannot delete admin"

    #  prevent deleting yourself
    if user.id == current_user.id:
        return "You cannot delete yourself"

    #  SOFT DELETE
    user.is_deleted = True
    db.session.commit()

    return redirect("/admin/users")


# ======= Admin restore USer =======

@app.route('/admin/restore_user/<int:user_id>', methods=['POST'])
@login_required
def restore_user(user_id):

    if current_user.role != "admin":
        return "Access Denied"

    user = User.query.get(user_id)

    if not user:
        return "User not found"

    #  RESTORE
    user.is_deleted = False
    db.session.commit()

    return redirect("/admin/deleted_users")
#  ====== Admin deleted user =======

@app.route('/admin/deleted_users')
@login_required
def deleted_users():

    if current_user.role != "admin":
        return "Access Denied"

    users = User.query.filter_by(is_deleted=True).all()

    return render_template("deleted_users.html", users=users)



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
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1"
    )
