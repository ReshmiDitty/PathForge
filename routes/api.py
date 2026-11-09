from flask import Blueprint, request, jsonify, session
from models import db
from models.user import User
from models.subscription import Coupon
from models.venture import VentureIdea, DesignThinkingNote
from services import ai_service
from services.seed_data import PLANS_INFO

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Context-aware AI Mentor Chat API.
    Works for logged in users and guests alike.
    """
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"reply": "Please ask a question regarding your career or startup venture!"})

    user_profile = {"name": "Student", "branch": "Engineering"}
    active_idea_dict = None

    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if user:
            user_profile["name"] = user.name
            if user.latest_assessment:
                user_profile["branch"] = user.latest_assessment.branch
            if user.active_idea:
                active_idea_dict = {
                    "title": user.active_idea.title,
                    "problem_statement": user.active_idea.problem_statement,
                    "solution": user.active_idea.solution
                }

    reply = ai_service.mentor_chat_ai(query, user_profile, active_idea_dict)
    return jsonify({"reply": reply})


@api_bp.route("/api/coupon/validate", methods=["POST"])
def validate_coupon():
    data = request.get_json() or {}
    code = data.get("code", "").strip().upper()
    plan = data.get("plan", "pro").lower()
    cycle = data.get("cycle", "monthly")

    plan_info = PLANS_INFO.get(plan, PLANS_INFO["pro"])
    base_price = plan_info["price_yearly"] if cycle == "yearly" else plan_info["price_monthly"]

    coupon = Coupon.query.filter_by(code=code, is_active=True).first()
    if not coupon:
        return jsonify({"valid": False, "message": "Invalid coupon code."}), 400

    if coupon.times_used >= coupon.max_uses:
        return jsonify({"valid": False, "message": "This coupon has reached its maximum uses."}), 400

    discount_amount = (coupon.discount_percentage / 100.0) * base_price
    final_price = max(0.0, base_price - discount_amount)

    return jsonify({
        "valid": True,
        "code": coupon.code,
        "discount_percentage": coupon.discount_percentage,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "message": f"Coupon applied! {coupon.discount_percentage}% discount granted."
    })

