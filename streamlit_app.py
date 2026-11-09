"""
PathForge – AI-Enabled Career Guidance & Skills Intelligence Portal
Streamlit Cloud Entrypoint – 100% Visual & Interactive Parity with Localhost:5000
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import re
from app import app
from models import db
from models.user import User
from models.subscription import Subscription

# 1. Page Configuration
st.set_page_config(
    page_title="PathForge – AI-Enabled Career Guidance & Skills Intelligence Portal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Complete CSS Reset: Remove Streamlit Chrome, Header, Footer & Extra Navbars
st.markdown("""
<style>
    /* Completely hide Streamlit Header, Footer, Sidebar, and Toolbar */
    #MainMenu, header, footer, [data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Zero out container padding so the PathForge navbar sits at the very top */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100vw !important;
    }
    
    /* Full-bleed iframe */
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        min-height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


def ensure_demo_student_ready():
    """
    Ensures the demo student has an active Founder subscription so that
    every view (/assessment, /validator, /pitch-builder, etc.) renders
    directly without any redirect on fresh Streamlit Cloud deployments.
    """
    with app.app_context():
        student = User.query.filter_by(email="student@pathforge.edu").first()
        if student and not student.has_access("founder"):
            sub = Subscription(
                user_id=student.id,
                plan="founder",
                billing_cycle="monthly",
                status="active",
                amount_paid=499.0,
                payment_id="pay_streamlit_seed",
                order_id="order_streamlit_seed"
            )
            db.session.add(sub)
            db.session.commit()


# 3. Generate Full-Fidelity SPA Bundle from Flask
def get_full_application_html():
    """
    Renders all views (including Sign In, Register, Sign Out flow, Admin Analytics,
    AI Assessment, Career Compass, Decision Meter, and Venture Studio) from the Flask
    application and packages them into a Single Page Application.
    """
    ensure_demo_student_ready()

    views_html = []
    captured_scripts = []

    def extract_view(client, view_name, route_path, default_display="none"):
        res = client.get(route_path, follow_redirects=True)
        html = res.data.decode('utf-8')
        m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
        content = m.group(1) if m else html

        # Extract inline scripts (e.g., Chart.js initializers, fillCreds)
        view_scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL)
        for s in view_scripts:
            s_clean = s.strip()
            if s_clean and s_clean not in captured_scripts:
                captured_scripts.append(s_clean)

        views_html.append(f'<div id="view-{view_name}" class="page-view" style="display:{default_display};">{content}</div>')
        return html

    with app.test_client() as client:
        # A. Fetch unauthenticated views first (Sign In & Register)
        client.get('/logout')
        extract_view(client, "login", "/login")
        extract_view(client, "register", "/register")

        # B. Authenticate as demo student and fetch all student views
        client.post('/login', data={'email': 'student@pathforge.edu', 'password': 'student123'})
        home_html = extract_view(client, "home", "/", default_display="block")

        student_routes = {
            "assessment": "/assessment",
            "compass": "/career-compass",
            "decision": "/decision-meter",
            "venture-hub": "/venture-studio",
            "ideas": "/venture-studio/ideas",
            "design-thinking": "/venture-studio/design-thinking",
            "validator": "/venture-studio/validator",
            "lean-canvas": "/venture-studio/lean-canvas",
            "mvp-planner": "/venture-studio/mvp-planner",
            "pitch-builder": "/venture-studio/pitch-builder",
            "founder-toolkit": "/venture-studio/founder-toolkit",
            "tracker": "/venture-studio/tracker",
            "dashboard": "/dashboard",
            "pricing": "/pricing",
            "billing": "/billing",
            "business-model": "/business-model"
        }
        for name, r in student_routes.items():
            extract_view(client, name, r)

        # C. Authenticate as admin and fetch Admin Analytics view
        client.get('/logout')
        client.post('/login', data={'email': 'admin@pathforge.edu', 'password': 'admin123'})
        extract_view(client, "admin", "/admin")

    # Read and inline static assets
    custom_css = ""
    if os.path.exists('static/css/custom.css'):
        with open('static/css/custom.css', 'r', encoding='utf-8') as f:
            custom_css = f.read()

    main_js = ""
    if os.path.exists('static/js/main.js'):
        with open('static/js/main.js', 'r', encoding='utf-8') as f:
            main_js = f.read()

    # 1. Inline CSS
    home_html = home_html.replace('<link rel="stylesheet" href="/static/css/custom.css">', f'<style>{custom_css}</style>')
    
    # 2. Inline JavaScript
    home_html = home_html.replace('<script src="/static/js/main.js"></script>', f'<script>{main_js}</script>')

    # 3. Replace <main>...</main> with combined views using a lambda to preserve all backslashes
    combined_views = '\n'.join(views_html)
    spa_html = re.sub(
        r'<main[^>]*>.*?</main>',
        lambda _: f'<main class="flex-grow">{combined_views}</main>',
        home_html,
        flags=re.DOTALL
    )

    # 4. Inject global SPA Navigation, Multi-User Account State & Blank Assessment Engine
    spa_nav_script = r"""
    <script>
    // Client-side User Directory (persists newly registered & logged-in student accounts)
    window.registeredUsers = {
        'student@pathforge.edu': {
            name: 'Aarav Sharma',
            email: 'student@pathforge.edu',
            hasAssessment: true,
            isAdmin: false,
            branch: 'Computer Science & Engineering',
            year: '3rd Year'
        },
        'admin@pathforge.edu': {
            name: 'PathForge Admin',
            email: 'admin@pathforge.edu',
            hasAssessment: true,
            isAdmin: true,
            branch: 'Platform Administration',
            year: 'Admin'
        }
    };

    try {
        var savedUsers = localStorage.getItem('pathforge_users');
        if (savedUsers) {
            var parsed = JSON.parse(savedUsers);
            for (var k in parsed) {
                window.registeredUsers[k] = parsed[k];
            }
        }
    } catch (e) {}

    window.saveUserStore = function() {
        try {
            localStorage.setItem('pathforge_users', JSON.stringify(window.registeredUsers));
        } catch (e) {}
    };

    // Active session user (starts as demo student)
    window.currentUser = window.registeredUsers['student@pathforge.edu'];

    // Update all DOM elements (Navbar, Dashboard, Career Compass) with the active user's profile
    window.applyUserProfile = function(user, isNewAccount) {
        window.currentUser = user;
        window.setNavbarAuthState(true, user.name, user.email, user.isAdmin);

        // Update Dashboard Welcome Title & Branch
        var dashWelcome = document.getElementById('dashboard-welcome-title');
        if (dashWelcome) {
            dashWelcome.innerText = (isNewAccount ? 'Welcome, ' : 'Welcome back, ') + user.name + '!';
        }
        var dashBranch = document.getElementById('dashboard-student-branch');
        if (dashBranch) {
            dashBranch.innerText = user.hasAssessment ? (user.branch || 'Engineering & Tech') : 'Complete Assessment to Set Branch';
        }

        // Toggle Dashboard Assessment vs Empty State
        var hasAssBox = document.getElementById('dashboard-has-assessment');
        var noAssBox = document.getElementById('dashboard-no-assessment');
        var matchBadge = document.getElementById('dashboard-match-badge');
        if (hasAssBox && noAssBox) {
            if (user.hasAssessment) {
                hasAssBox.classList.remove('hidden');
                noAssBox.classList.add('hidden');
                if (matchBadge) matchBadge.classList.remove('hidden');
            } else {
                hasAssBox.classList.add('hidden');
                noAssBox.classList.remove('hidden');
                if (matchBadge) matchBadge.classList.add('hidden');
            }
        }

        // Update Career Compass Student Header
        var compassView = document.getElementById('view-compass');
        if (compassView) {
            var subHeader = compassView.querySelector('p.mt-1.text-xs.text-slate-600');
            if (subHeader) {
                var bText = user.branch || 'Engineering & Tech';
                var yText = user.year ? ' (' + user.year + ')' : '';
                subHeader.innerHTML = 'Student: <strong>' + user.name + '</strong> &bull; Major: <strong>' + bText + '</strong>' + yText;
            }
        }
    };

    // Global SPA Navigation Engine
    window.navigateTo = function(viewName) {
        // Gate Career Compass & Decision Meter if a new student hasn't attended the assessment yet
        if ((viewName === 'compass' || viewName === 'decision') && window.currentUser && !window.currentUser.isAdmin && !window.currentUser.hasAssessment) {
            window.showToastBanner('Please complete your AI Career Assessment on your own first, ' + window.currentUser.name + '!', 'info');
            viewName = 'assessment';
        }

        var views = document.querySelectorAll('.page-view');
        views.forEach(function(el) {
            el.style.display = 'none';
        });
        var target = document.getElementById('view-' + viewName);
        if (target) {
            target.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // If opening the AI Assessment page, always reset to Step 1 and clear inputs for unassessed users
            if (viewName === 'assessment' && typeof window.resetAssessmentStep === 'function') {
                var shouldClear = !(window.currentUser && window.currentUser.email === 'student@pathforge.edu' && window.currentUser.hasAssessment);
                window.resetAssessmentStep(shouldClear);
            }

            // Re-trigger resize for responsive Chart.js rendering
            setTimeout(function() {
                window.dispatchEvent(new Event('resize'));
            }, 80);
        }
    };

    // Helper: Toggle Navbar between Logged-In and Signed-Out states
    window.setNavbarAuthState = function(isLoggedIn, name, email, isAdmin) {
        var loggedInBox = document.getElementById('nav-auth-logged-in');
        var loggedOutBox = document.getElementById('nav-auth-logged-out');
        if (!loggedInBox || !loggedOutBox) return;

        if (isLoggedIn) {
            loggedInBox.classList.remove('hidden');
            loggedInBox.classList.add('flex');
            loggedOutBox.classList.add('hidden');
            loggedOutBox.classList.remove('flex');

            if (name) {
                var avatarEl = document.getElementById('nav-avatar-letter');
                var firstEl = document.getElementById('nav-user-first-name');
                var dropNameEl = document.getElementById('nav-dropdown-name');
                if (avatarEl) avatarEl.innerText = name.trim().charAt(0).toUpperCase();
                if (firstEl) firstEl.innerText = name.trim().split(' ')[0];
                if (dropNameEl) dropNameEl.innerText = name.trim();
            }
            if (email) {
                var dropEmailEl = document.getElementById('nav-dropdown-email');
                if (dropEmailEl) dropEmailEl.innerText = email.trim();
            }
            var adminLink = document.getElementById('nav-admin-link');
            if (adminLink) {
                if (isAdmin) {
                    adminLink.classList.remove('hidden');
                } else {
                    adminLink.classList.add('hidden');
                }
            }
        } else {
            loggedInBox.classList.add('hidden');
            loggedInBox.classList.remove('flex');
            loggedOutBox.classList.remove('hidden');
            loggedOutBox.classList.add('flex');
        }
    };

    // Helper: Show feedback banner at the top of a view
    window.showToastBanner = function(message, category) {
        var existing = document.getElementById('spa-toast-banner');
        if (existing) existing.remove();
        var isInfo = (category === 'info');
        var colorClasses = isInfo
            ? 'bg-sky-50 text-sky-800 border-sky-200'
            : 'bg-emerald-50 text-emerald-800 border-emerald-200';
        var iconColor = isInfo ? 'text-sky-600' : 'text-emerald-600';

        var banner = document.createElement('div');
        banner.id = 'spa-toast-banner';
        banner.className = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full mt-4';
        banner.innerHTML = '<div class="flex items-center justify-between p-4 rounded-xl border text-sm shadow-xs ' + colorClasses + '">' +
            '<div class="flex items-center space-x-2.5">' +
            '<svg class="w-5 h-5 ' + iconColor + ' flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>' +
            '<span>' + message + '</span></div>' +
            '<button onclick="this.parentElement.parentElement.remove()" class="text-slate-400 hover:text-slate-600 p-1">✕</button></div>';
        var mainEl = document.querySelector('main');
        if (mainEl && mainEl.parentNode) {
            mainEl.parentNode.insertBefore(banner, mainEl);
            setTimeout(function() {
                if (banner.parentNode) banner.remove();
            }, 5000);
        }
    };

    // Global Link & Form Interception
    document.addEventListener('DOMContentLoaded', function() {
        var routeMap = {
            '/': 'home',
            '/home': 'home',
            '/login': 'login',
            '/register': 'register',
            '/admin': 'admin',
            '/assessment': 'assessment',
            '/career-compass': 'compass',
            '/decision-meter': 'decision',
            '/venture-studio': 'venture-hub',
            '/venture-studio/ideas': 'ideas',
            '/venture-studio/design-thinking': 'design-thinking',
            '/venture-studio/validator': 'validator',
            '/venture-studio/lean-canvas': 'lean-canvas',
            '/venture-studio/mvp-planner': 'mvp-planner',
            '/venture-studio/pitch-builder': 'pitch-builder',
            '/venture-studio/founder-toolkit': 'founder-toolkit',
            '/venture-studio/tracker': 'tracker',
            '/dashboard': 'dashboard',
            '/pricing': 'pricing',
            '/billing': 'billing',
            '/business-model': 'business-model'
        };

        // Intercept clicks on links
        document.body.addEventListener('click', function(e) {
            var a = e.target.closest('a');
            if (!a) return;
            var href = a.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

            var cleanHref = href.split('?')[0].replace(/\/$/, '') || '/';

            if (cleanHref === '/logout') {
                e.preventDefault();
                window.currentUser = null;
                window.setNavbarAuthState(false);
                window.showToastBanner('You have been signed out successfully.', 'info');
                window.navigateTo('login');
                return;
            }

            if (routeMap[cleanHref]) {
                e.preventDefault();
                // If clicking "Start AI Career Assessment", ensure form is completely blank
                if (routeMap[cleanHref] === 'assessment' && typeof window.resetAssessmentStep === 'function') {
                    window.resetAssessmentStep(true);
                }
                window.navigateTo(routeMap[cleanHref]);
            } else if (cleanHref.indexOf('/checkout/') === 0) {
                e.preventDefault();
                window.showToastBanner('Demo Checkout Activated! Your account is unlocked with Founder Tier access.');
                window.navigateTo('dashboard');
            }
        });

        // Live Interactive Assessment Form Submission Engine
        var assessmentForm = document.getElementById('assessment-form');
        if (assessmentForm) {
            assessmentForm.addEventListener('submit', function(e) {
                e.preventDefault();

                // Validate Step 5 fields
                var branchSelect = assessmentForm.querySelector('select[name="branch"]');
                var yearSelect = assessmentForm.querySelector('select[name="year_of_study"]');
                var skillInputs = assessmentForm.querySelectorAll('input[name="skill_rating"]');
                var goalRadio = assessmentForm.querySelector('input[name="primary_goal"]:checked');
                var riskInput = assessmentForm.querySelector('input[name="risk_appetite"]');
                var autonomyInput = assessmentForm.querySelector('input[name="stability_vs_autonomy"]');
                var hoursSelect = assessmentForm.querySelector('select[name="hours_per_week"]');
                var capitalSelect = assessmentForm.querySelector('select[name="capital_willing"]');

                if (!goalRadio || !hoursSelect || !hoursSelect.value || !capitalSelect || !capitalSelect.value) {
                    alert("Please select your Primary Post-College Goal, Available Weekly Hours, and Optional Budget to generate your report.");
                    return;
                }

                var branch = (branchSelect && branchSelect.value) ? branchSelect.value : 'Computer Science & Engineering';
                var year = (yearSelect && yearSelect.value) ? yearSelect.value : '3rd Year';
                var goal = goalRadio.value;
                var risk = riskInput ? parseInt(riskInput.value, 10) : 5;
                var autonomy = autonomyInput ? parseInt(autonomyInput.value, 10) : 5;
                var hours = parseInt(hoursSelect.value, 10) || 18;

                var ratings = [];
                skillInputs.forEach(function(inp) {
                    ratings.push(parseFloat(inp.value) || 5.0);
                });
                var avgSkill = ratings.length ? (ratings.reduce(function(a, b) { return a + b; }, 0) / ratings.length) : 5.0;

                // Mark current user's assessment as completed and update their profile
                var activeName = (window.currentUser && window.currentUser.name) ? window.currentUser.name : 'Student';
                if (window.currentUser) {
                    window.currentUser.hasAssessment = true;
                    window.currentUser.branch = branch;
                    window.currentUser.year = year;
                    window.registeredUsers[window.currentUser.email] = window.currentUser;
                    window.saveUserStore();
                    window.applyUserProfile(window.currentUser, false);
                }

                // Update Career Compass Header & Radar Chart
                var compassView = document.getElementById('view-compass');
                if (compassView) {
                    var subHeader = compassView.querySelector('p.mt-1.text-xs.text-slate-600');
                    if (subHeader) {
                        subHeader.innerHTML = 'Student: <strong>' + activeName + '</strong> &bull; Major: <strong>' + branch + '</strong> (' + year + ')';
                    }
                }

                var radarCanvas = document.getElementById('radarSkillChart');
                if (radarCanvas && window.Chart) {
                    var radarChart = Chart.getChart(radarCanvas);
                    if (radarChart && ratings.length >= 5) {
                        radarChart.data.datasets[0].data = ratings.slice(0, 5).map(function(v) { return Math.min(100, Math.round(v * 10)); });
                        radarChart.update();
                    }
                }

                // Recalculate Tri-Path Decision Meter Scores
                var jobScore = Math.round(65 + (avgSkill * 2.8) + (Math.min(autonomy, 7) * 0.8) + (goal === 'job' ? 10 : 0));
                jobScore = Math.max(50, Math.min(96, jobScore));

                var hsScore = Math.round(55 + (avgSkill * 2.2) + ((10 - risk) * 1.5) + (goal === 'higher_studies' ? 12 : 0));
                hsScore = Math.max(45, Math.min(94, hsScore));

                var timeFactor = Math.min(hours / 25.0, 1.0);
                var ventureScore = Math.round(40 + (risk * 2.5) + (autonomy * 2.2) + (timeFactor * 8) + (goal === 'startup' ? 10 : 0));
                ventureScore = Math.max(35, Math.min(92, ventureScore));

                var decisionView = document.getElementById('view-decision');
                if (decisionView) {
                    var scoreEls = decisionView.querySelectorAll('.text-5xl.font-black');
                    if (scoreEls.length >= 3) {
                        scoreEls[0].innerText = jobScore;
                        scoreEls[1].innerText = hsScore;
                        scoreEls[2].innerText = ventureScore;
                    }
                }

                var triCanvas = document.getElementById('triPathChart');
                if (triCanvas && window.Chart) {
                    var triChart = Chart.getChart(triCanvas);
                    if (triChart) {
                        triChart.data.datasets[0].data = [jobScore, hsScore, ventureScore];
                        triChart.update();
                    }
                }

                // Show confirmation banner and navigate to Career Compass
                window.showToastBanner('Assessment successfully analyzed for ' + activeName + '! Here is your personalized AI Career Compass Report.');
                window.navigateTo('compass');
            });
        }

        // Intercept Sign In, Register, and Venture Studio forms
        document.body.addEventListener('submit', function(e) {
            var form = e.target;
            if (!form || form.id === 'assessment-form') return;
            e.preventDefault();
            var action = (form.getAttribute('action') || '').split('?')[0];

            if (action === '/login') {
                var emailInp = form.querySelector('input[name="email"]');
                var emailVal = emailInp ? emailInp.value.trim().toLowerCase() : 'student@pathforge.edu';

                var userRec = window.registeredUsers[emailVal];
                if (!userRec) {
                    // A brand-new student logging in with their own email
                    var rawPrefix = emailVal.split('@')[0].replace(/[._-]+/g, ' ');
                    var formattedName = rawPrefix.replace(/\b\w/g, function(l) { return l.toUpperCase(); });
                    userRec = {
                        name: formattedName,
                        email: emailVal,
                        hasAssessment: false,
                        isAdmin: (emailVal.indexOf('admin') !== -1),
                        branch: '',
                        year: ''
                    };
                    window.registeredUsers[emailVal] = userRec;
                    window.saveUserStore();
                }

                window.applyUserProfile(userRec, !userRec.hasAssessment);

                if (userRec.isAdmin) {
                    window.showToastBanner('Welcome back, ' + userRec.name + '!');
                    window.navigateTo('admin');
                } else if (!userRec.hasAssessment) {
                    if (typeof window.resetAssessmentStep === 'function') {
                        window.resetAssessmentStep(true);
                    }
                    window.showToastBanner('Welcome, ' + userRec.name + '! Please attend the AI Career Assessment on your own to generate your report.', 'info');
                    window.navigateTo('assessment');
                } else {
                    window.showToastBanner('Welcome back, ' + userRec.name + '!');
                    window.navigateTo('dashboard');
                }
            } else if (action === '/register') {
                var nameInp = form.querySelector('input[name="name"]');
                var regEmailInp = form.querySelector('input[name="email"]');
                var passInp = form.querySelector('input[name="password"]');
                var confInp = form.querySelector('input[name="confirm_password"]');

                if (passInp && confInp && passInp.value !== confInp.value) {
                    alert("Passwords do not match. Please re-enter your password.");
                    return;
                }

                var newName = (nameInp && nameInp.value.trim()) ? nameInp.value.trim() : 'Student';
                var newEmail = (regEmailInp && regEmailInp.value.trim().toLowerCase()) ? regEmailInp.value.trim().toLowerCase() : 'student@college.edu';

                var newUserRec = {
                    name: newName,
                    email: newEmail,
                    hasAssessment: false,
                    isAdmin: false,
                    branch: '',
                    year: ''
                };
                window.registeredUsers[newEmail] = newUserRec;
                window.saveUserStore();

                // Apply new student's name everywhere (never Aarav) and clear the assessment form
                window.applyUserProfile(newUserRec, true);
                if (typeof window.resetAssessmentStep === 'function') {
                    window.resetAssessmentStep(true);
                }

                window.showToastBanner('Welcome to PathForge, ' + newName + '! Please complete your AI Career Assessment on your own below.');
                window.navigateTo('assessment');
            } else if (action.indexOf('/design-thinking/delete/') !== -1) {
                var card = form.closest('.rounded-xl');
                if (card) card.remove();
                window.showToastBanner('Sticky note removed from board.');
            } else if (action.indexOf('/design-thinking/add') !== -1) {
                var modal = document.getElementById('add-note-modal');
                if (modal) modal.classList.add('hidden');
                window.showToastBanner('New sticky note added to Design Thinking board!');
            } else if (action.indexOf('/lean-canvas') !== -1) {
                window.showToastBanner('Lean Canvas 9-Block model saved and updated!');
            } else if (action.indexOf('/ideas') !== -1) {
                window.showToastBanner('Active Venture updated across all Venture Studio tools!');
            } else {
                window.showToastBanner('Changes saved successfully!');
            }
        });
    });
    </script>
    """

    # Inject captured scripts and router before </body>
    injected_scripts = spa_nav_script + "\n" + "\n".join([f"<script>{s}</script>" for s in captured_scripts])
    spa_html = spa_html.replace('</body>', f'{injected_scripts}\n</body>')

    return spa_html


# 4. Render Pure Application
app_html = get_full_application_html()
components.html(app_html, height=2900, scrolling=True)
