from datetime import datetime, timedelta, timezone
from models import db

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def normalize_dt(dt):
    if dt is not None and getattr(dt, "tzinfo", None) is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan = db.Column(db.String(20), nullable=False, default="free")  # 'free', 'pro', 'founder'
    billing_cycle = db.Column(db.String(20), default="monthly")       # 'monthly', 'yearly'
    status = db.Column(db.String(20), default="active")             # 'active', 'cancelled', 'trial'
    amount_paid = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default="INR")
    
    # Razorpay or Demo payment references
    payment_id = db.Column(db.String(100), nullable=True)
    order_id = db.Column(db.String(100), nullable=True)
    
    start_date = db.Column(db.DateTime, default=utc_now)
    renewal_date = db.Column(db.DateTime, default=lambda: utc_now() + timedelta(days=30))
    created_at = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", back_populates="subscriptions")

    @property
    def is_active(self) -> bool:
        if self.status != "active":
            return False
        r_date = normalize_dt(self.renewal_date)
        if r_date and r_date < utc_now():
            return False
        return True

    @property
    def days_remaining(self) -> int:
        r_date = normalize_dt(self.renewal_date)
        if not r_date:
            return 0
        diff = r_date - utc_now()
        return max(0, diff.days)


class PaymentInvoice(db.Model):
    __tablename__ = "payment_invoices"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    billing_cycle = db.Column(db.String(20), default="monthly")
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="INR")
    payment_method = db.Column(db.String(50), default="Razorpay Test / Demo")
    payment_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default="paid")  # 'paid', 'pending', 'refunded'
    date = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", backref="invoices")


class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    discount_percentage = db.Column(db.Integer, nullable=False, default=20)
    is_active = db.Column(db.Boolean, default=True)
    max_uses = db.Column(db.Integer, default=500)
    times_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    def apply_discount(self, amount: float) -> float:
        discount = (self.discount_percentage / 100.0) * amount
        return max(0.0, amount - discount)
