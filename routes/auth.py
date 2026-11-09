from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.venture import JourneyTracker

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "info")
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Admin access requires logging in.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        user = User.query.get(session["user_id"])
        if not user or user.role != "admin":
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("main.dashboard"))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Please fill in all required fields.", "warning")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password should be at least 6 characters long.", "warning")
            return render_template("auth/register.html")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists. Please log in.", "info")
            return redirect(url_for("auth.login"))

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()

        # Initialize Journey Tracker
        tracker = JourneyTracker(user_id=new_user.id, overall_progress=10, badges_raw='["Compass Explorer"]')
        db.session.add(tracker)
        db.session.commit()

        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        session["user_email"] = new_user.email
        session["user_role"] = new_user.role

        flash(f"Welcome to PathForge, {new_user.name}! Let's start with your Dual-Path Assessment.", "success")
        return redirect(url_for("assessment.start_assessment"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    next_url = request.args.get("next") or url_for("main.dashboard")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_email"] = user.email
            session["user_role"] = user.role

            if user.role != "admin" and not user.latest_assessment:
                flash(f"Welcome, {user.name}! Please attend your AI Career Assessment to generate your personalized Career Compass.", "info")
                return redirect(url_for("assessment.start_assessment"))

            flash(f"Welcome back, {user.name}!", "success")
            return redirect(next_url)
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("auth/login.html", next=next_url)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("main.index"))

