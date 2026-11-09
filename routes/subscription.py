from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from config import config
from models import db
from models.user import User
from models.subscription import Subscription, Coupon
from routes.auth import login_required
from services.seed_data import PLANS_INFO
from services.payment_service import (
    calculate_plan_price,
    create_order,
    process_demo_checkout,
    activate_subscription,
    cancel_user_subscription,
    is_razorpay_live
)

subscription_bp = Blueprint("subscription", __name__)

@subscription_bp.route("/pricing")
def pricing():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    
    required_plan = request.args.get("required_plan")
    return render_template(
        "subscription/pricing.html",
        user=user,
        plans=PLANS_INFO,
        required_plan=required_plan
    )


@subscription_bp.route("/checkout/<plan>")
@login_required
def checkout(plan):
    plan = plan.lower()
    if plan not in ["pro", "founder"]:
        flash("Invalid plan selected.", "warning")
        return redirect(url_for("subscription.pricing"))

    user = User.query.get(session["user_id"])
    cycle = request.args.get("cycle", "monthly")
    coupon_code = request.args.get("coupon", "").strip().upper()

    base_price, final_price, discount, coupon = calculate_plan_price(plan, cycle, coupon_code)
    order_data = create_order(user, plan, cycle, coupon_code)

    return render_template(
        "subscription/checkout.html",
        user=user,
        plan_name=plan.capitalize(),
        plan=plan,
        cycle=cycle,
        base_price=base_price,
        final_price=final_price,
        discount=discount,
        coupon=coupon,
        order=order_data,
        is_razorpay_live=is_razorpay_live(),
        razorpay_key=config.RAZORPAY_KEY_ID
    )


@subscription_bp.route("/subscription/demo-pay", methods=["POST"])
@login_required
def demo_pay():
    """
    1-Click Demo Checkout: Simulates payment gateway success and instantly unlocks plan.
    Works seamlessly out of the box without any third-party credentials.
    """
    user = User.query.get(session["user_id"])
    plan = request.form.get("plan", "pro").lower()
    cycle = request.form.get("cycle", "monthly")
    coupon_code = request.form.get("coupon", "").strip()

    if plan not in ["pro", "founder"]:
        plan = "pro"

    new_sub = process_demo_checkout(user, plan, cycle, coupon_code)
    flash(f"Payment successful! You are now upgraded to the PathForge {plan.capitalize()} Plan. All features unlocked!", "success")
    return redirect(url_for("main.dashboard"))


@subscription_bp.route("/subscription/verify", methods=["POST"])
@login_required
def razorpay_verify():
    """
    Receives and validates Razorpay frontend callback parameters.
    """
    user = User.query.get(session["user_id"])
    razorpay_order_id = request.form.get("razorpay_order_id")
    razorpay_payment_id = request.form.get("razorpay_payment_id")
    razorpay_signature = request.form.get("razorpay_signature")
    plan = request.form.get("plan", "pro")
    cycle = request.form.get("cycle", "monthly")
    amount = float(request.form.get("amount", 199.0))

    if not is_razorpay_live():
        # Fallback to demo activation if verified in demo state
        activate_subscription(user, plan, cycle, amount, razorpay_payment_id or "demo_pay", razorpay_order_id or "demo_order")
        flash(f"Payment verified! Upgraded to {plan.capitalize()}.", "success")
        return redirect(url_for("main.dashboard"))

    try:
        import razorpay
        client = razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))
        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)

        activate_subscription(
            user=user,
            plan=plan,
            billing_cycle=cycle,
            amount_paid=amount,
            payment_id=razorpay_payment_id,
            order_id=razorpay_order_id,
            payment_method="Razorpay Test Gateway"
        )
        flash(f"Payment verified via Razorpay! Upgraded to {plan.capitalize()}.", "success")
        return redirect(url_for("main.dashboard"))
    except Exception as e:
        flash(f"Payment verification failed: {e}. Please contact support or try demo checkout.", "danger")
        return redirect(url_for("subscription.pricing"))


@subscription_bp.route("/billing")
@login_required
def billing():
    """
    Billing page: current plan, invoices list, cancel subscription, upgrade.
    """
    user = User.query.get(session["user_id"])
    active_sub = user.active_subscription
    invoices = user.invoices
    return render_template(
        "subscription/billing.html",
        user=user,
        active_sub=active_sub,
        invoices=invoices
    )


@subscription_bp.route("/subscription/cancel", methods=["POST"])
@login_required
def cancel_subscription():
    user = User.query.get(session["user_id"])
    cancelled = cancel_user_subscription(user)
    if cancelled:
        flash("Your subscription has been cancelled. Your account has returned to the Free plan.", "info")
    else:
        flash("No active paid subscription found.", "warning")
    return redirect(url_for("subscription.billing"))

