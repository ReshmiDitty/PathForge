import json
from flask import Blueprint, render_template
from models.user import User
from models.subscription import Subscription, PaymentInvoice
from routes.auth import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@admin_required
def dashboard():
    total_users = User.query.count()
    active_subs = Subscription.query.filter_by(status="active").all()
    active_subscribers_count = len(active_subs)
    
    pro_count = sum(1 for s in active_subs if s.plan == "pro")
    founder_count = sum(1 for s in active_subs if s.plan == "founder")
    free_count = max(0, total_users - active_subscribers_count)

    # Invoices / Revenue
    invoices = PaymentInvoice.query.filter_by(status="paid").all()
    total_revenue = sum(inv.amount for inv in invoices)
    
    pro_revenue = sum(inv.amount for inv in invoices if "Pro" in inv.plan)
    founder_revenue = sum(inv.amount for inv in invoices if "Founder" in inv.plan)

    recent_invoices = PaymentInvoice.query.order_by(PaymentInvoice.date.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    # Chart data
    plan_distribution = {
        "labels": ["Free Tier", "Pro Student", "Founder Suite"],
        "counts": [free_count, pro_count, founder_count]
    }

    revenue_by_plan = {
        "labels": ["Pro Student (₹199/₹1799)", "Founder Suite (₹499/₹4499)"],
        "amounts": [pro_revenue, founder_revenue]
    }

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        active_subscribers=active_subscribers_count,
        total_revenue=total_revenue,
        pro_count=pro_count,
        founder_count=founder_count,
        free_count=free_count,
        pro_revenue=pro_revenue,
        founder_revenue=founder_revenue,
        plan_distribution_json=json.dumps(plan_distribution),
        revenue_by_plan_json=json.dumps(revenue_by_plan),
        recent_invoices=recent_invoices,
        recent_users=recent_users
    )

