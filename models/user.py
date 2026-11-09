from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="student")  # 'student' or 'admin'
    created_at = db.Column(db.DateTime, default=utc_now)

    # Usage tracking
    ai_generations_count = db.Column(db.Integer, default=0)
    last_generation_reset = db.Column(db.DateTime, default=utc_now)

    # Relationships
    subscriptions = db.relationship("Subscription", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    assessments = db.relationship("Assessment", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    ideas = db.relationship("VentureIdea", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    canvases = db.relationship("LeanCanvas", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    design_notes = db.relationship("DesignThinkingNote", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    mvp_plans = db.relationship("MVPPlan", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    pitch_decks = db.relationship("PitchDeck", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    tracker = db.relationship("JourneyTracker", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def active_subscription(self):
        """Returns the user's current active subscription, or default to a virtual Free plan."""
        sub = self.subscriptions.filter_by(status="active").order_by(Subscription.id.desc()).first()
        return sub

    @property
    def current_plan(self) -> str:
        """Returns 'free', 'pro', or 'founder'."""
        if self.role == "admin":
            return "founder"
        sub = self.active_subscription
        if sub and sub.is_active:
            return sub.plan
        return "free"

    def has_access(self, required_plan: str) -> bool:
        """
        Check feature tier access:
        'free' tier: free, pro, founder
        'pro' tier: pro, founder
        'founder' tier: founder
        """
        if self.role == "admin":
            return True
        plan = self.current_plan
        levels = {"free": 0, "pro": 1, "founder": 2}
        return levels.get(plan, 0) >= levels.get(required_plan, 0)

    @property
    def can_generate_ai_ideas(self) -> bool:
        """Free users get 3 AI generations per month; Pro and Founder get unlimited."""
        if self.has_access("pro"):
            return True
        return self.ai_generations_count < 3

    def increment_ai_usage(self):
        self.ai_generations_count += 1
        db.session.commit()

    @property
    def latest_assessment(self):
        return self.assessments.order_by(Assessment.created_at.desc()).first()

    @property
    def active_idea(self):
        """Returns the venture idea marked as active, or the most recent one."""
        idea = self.ideas.filter_by(is_active_venture=True).first()
        if not idea:
            idea = self.ideas.order_by(VentureIdea.created_at.desc()).first()
        return idea

# Import at the end to prevent circular dependencies in model relationships
from models.subscription import Subscription
from models.assessment import Assessment
from models.venture import VentureIdea, LeanCanvas, DesignThinkingNote, MVPPlan, PitchDeck, JourneyTracker
