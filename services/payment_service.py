"""
PathForge Payment & Subscription Service
-----------------------------------------
Handles Razorpay Test Mode integration, Demo Checkout fallback,
coupon validations, invoice generation, and backend feature-gating decorators.
"""

import uuid
import logging
from functools import wraps
from datetime import datetime, timedelta, timezone
from flask import session, redirect, url_for, flash, request, abort
from config import config
from models import db
from models.user import User
from models.subscription import Subscription, PaymentInvoice, Coupon
from services.seed_data import PLANS_INFO

logger = logging.getLogger(__name__)

# Initialize Razorpay Client if credentials exist
razorpay_client = None
if config.has_razorpay_keys:
    try:
        import razorpay
        razorpay_client = razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))
        logger.info("Razorpay Client initialized in Test Mode.")
    except Exception as e:
        logger.warning(f"Could not initialize Razorpay Client: {e}. Demo mode active.")

def is_razorpay_live() -> bool:
    """Returns True if live Razorpay test keys are active."""
    return razorpay_client is not None

def calculate_plan_price(plan: str, billing_cycle: str = "monthly", coupon_code: str = None):
    """
    Computes final price in INR after applying cycle discounts and valid coupon codes.
    """
    plan_info = PLANS_INFO.get(plan.lower())
    if not plan_info:
        return 0.0, 0.0, 0, None

    base_price = plan_info["price_yearly"] if billing_cycle == "yearly" else plan_info["price_monthly"]
    base_price = float(base_price)

    discount_amount = 0.0
    applied_coupon = None

    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code.strip().upper(), is_active=True).first()
        if coupon and (coupon.times_used < coupon.max_uses):
            discount_amount = (coupon.discount_percentage / 100.0) * base_price
            applied_coupon = coupon

    final_price = max(0.0, base_price - discount_amount)
    return base_price, final_price, discount_amount, applied_coupon


def create_order(user: User, plan: str, billing_cycle: str = "monthly", coupon_code: str = None) -> dict:
    """
    Creates an order for checkout. Uses Razorpay order API if keys are present,
    otherwise generates a simulated demo order.
    """
    base_price, final_price, discount_amount, coupon = calculate_plan_price(plan, billing_cycle, coupon_code)

    # If it's a 100% discount or ₹0 Free plan
    if final_price <= 0:
        return {
            "is_free": True,
            "order_id": f"order_free_{uuid.uuid4().hex[:10]}",
            "amount": 0,
            "currency": "INR",
            "plan": plan,
            "billing_cycle": billing_cycle,
            "discount": discount_amount
        }

    # Razorpay Test Mode Order Creation
    if is_razorpay_live():
        try:
            amount_in_paise = int(final_price * 100)
            razorpay_order = razorpay_client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "receipt": f"rcpt_{user.id}_{int(datetime.now().timestamp())}",
                "notes": {
                    "user_id": user.id,
                    "plan": plan,
                    "billing_cycle": billing_cycle,
                    "coupon": coupon.code if coupon else ""
                }
            })
            return {
                "is_free": False,
                "is_razorpay": True,
                "key_id": config.RAZORPAY_KEY_ID,
                "order_id": razorpay_order["id"],
                "amount": final_price,
                "amount_paise": amount_in_paise,
                "currency": "INR",
                "plan": plan,
                "billing_cycle": billing_cycle,
                "discount": discount_amount
            }
        except Exception as e:
            logger.warning(f"Razorpay order creation failed: {e}. Falling back to demo mode.")

    # Demo Checkout Order
    demo_order_id = f"order_demo_{uuid.uuid4().hex[:12]}"
    return {
        "is_free": False,
        "is_razorpay": False,
        "order_id": demo_order_id,
        "amount": final_price,
        "currency": "INR",
        "plan": plan,
        "billing_cycle": billing_cycle,
        "discount": discount_amount,
        "demo_mode": True
    }


def activate_subscription(user: User, plan: str, billing_cycle: str, amount_paid: float,
                          payment_id: str, order_id: str, payment_method: str = "Demo Checkout") -> Subscription:
    """
    Stores or updates subscription state and creates an official payment invoice record.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    days = 365 if billing_cycle == "yearly" else 30
    renewal = now + timedelta(days=days)

    # Deactivate existing active subscriptions
    existing = Subscription.query.filter_by(user_id=user.id, status="active").all()
    for sub in existing:
        sub.status = "upgraded" if plan != "free" else "cancelled"

    new_sub = Subscription(
        user_id=user.id,
        plan=plan,
        billing_cycle=billing_cycle,
        status="active",
        amount_paid=amount_paid,
        currency="INR",
        payment_id=payment_id,
        order_id=order_id,
        start_date=now,
        renewal_date=renewal
    )
    db.session.add(new_sub)

    # Record Invoice
    invoice = PaymentInvoice(
        user_id=user.id,
        invoice_number=f"INV-{now.strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}",
        plan=plan.capitalize(),
        billing_cycle=billing_cycle.capitalize(),
        amount=amount_paid,
        currency="INR",
        payment_method=payment_method,
        payment_id=payment_id,
        status="paid",
        date=now
    )
    db.session.add(invoice)
    db.session.commit()
    logger.info(f"User {user.email} successfully subscribed to {plan} ({billing_cycle}).")
    return new_sub


def process_demo_checkout(user: User, plan: str, billing_cycle: str, coupon_code: str = None) -> Subscription:
    """
    Simulates a successful test payment transaction without needing third-party payment gateway keys.
    """
    _, final_price, _, coupon = calculate_plan_price(plan, billing_cycle, coupon_code)
    if coupon:
        coupon.times_used += 1

    payment_id = f"pay_demo_{uuid.uuid4().hex[:14]}"
    order_id = f"order_demo_{uuid.uuid4().hex[:12]}"

    return activate_subscription(
        user=user,
        plan=plan,
        billing_cycle=billing_cycle,
        amount_paid=final_price,
        payment_id=payment_id,
        order_id=order_id,
        payment_method="PathForge Demo Checkout"
    )


def cancel_user_subscription(user: User) -> bool:
    """
    Cancels the user's active paid subscription and resets to Free tier.
    """
    active_sub = Subscription.query.filter_by(user_id=user.id, status="active").first()
    if active_sub:
        active_sub.status = "cancelled"
        db.session.commit()
        return True
    return False


def subscription_required(required_tier: str = "pro"):
    """
    Backend route protection decorator.
    Enforces subscription gating on server-side actions (not just UI hiding).
    If user does not hold required plan, redirects to pricing with friendly prompt.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get("user_id")
            if not user_id:
                flash("Please log in to access this feature.", "warning")
                return redirect(url_for("auth.login", next=request.path))
            
            user = User.query.get(user_id)
            if not user or not user.has_access(required_tier):
                tier_name = "Pro" if required_tier == "pro" else "Founder"
                flash(f"The {tier_name} plan is required to unlock this feature. Check out our student pricing below!", "info")
                return redirect(url_for("subscription.pricing", required_plan=required_tier))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
