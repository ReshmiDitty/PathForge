from flask import Blueprint, render_template, session, redirect, url_for
from models.user import User
from models.venture import VentureIdea, LeanCanvas, PitchDeck
from routes.auth import login_required
from services.seed_data import PLANS_INFO

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return render_template("index.html", user=user, plans=PLANS_INFO)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get(session["user_id"])
    latest_assessment = user.latest_assessment
    active_idea = user.active_idea
    saved_ideas = user.ideas.order_by(VentureIdea.created_at.desc()).all()
    saved_canvases = user.canvases.order_by(LeanCanvas.last_updated.desc()).all()
    saved_pitches = user.pitch_decks.order_by(PitchDeck.created_at.desc()).all()
    tracker = user.tracker

    # Determine limits
    plan = user.current_plan
    ai_limit = "Unlimited" if user.has_access("pro") else f"{max(0, 3 - user.ai_generations_count)} remaining (3/mo)"

    return render_template(
        "dashboard.html",
        user=user,
        plan=plan,
        assessment=latest_assessment,
        active_idea=active_idea,
        ideas=saved_ideas,
        canvases=saved_canvases,
        pitches=saved_pitches,
        tracker=tracker,
        ai_limit=ai_limit
    )


@main_bp.route("/business-model")
def business_model():
    """
    PathForge's Own Business Model Page.
    Applies the course concepts (Lean Canvas, Unit Economics, GTM) to the product itself.
    """
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return render_template("business_model.html", user=user)

