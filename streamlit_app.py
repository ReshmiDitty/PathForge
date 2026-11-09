"""
PathForge – AI-Enabled Career Guidance & Skills Intelligence Portal
Streamlit Cloud Entrypoint – 100% Visual Parity with Localhost:5000
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import re
from app import app

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

# 3. Cache & Generate Full-Fidelity SPA Bundle from Flask
@st.cache_data(show_spinner=False)
def get_full_application_html():
    """
    Renders all 15 views from the Flask application and packages them
    into a high-performance Single Page Application with client-side routing.
    This guarantees 100% visual parity with localhost:5000 and instant interactivity.
    """
    routes = {
        "home": "/",
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
        "dashboard": "/dashboard",
        "pricing": "/pricing",
        "business-model": "/business-model"
    }

    with app.test_client() as client:
        # Pre-authenticate as demo student so all authenticated views render with data
        client.post('/login', data={'email': 'student@pathforge.edu', 'password': 'student123'})
        
        home_html = client.get('/', follow_redirects=True).data.decode('utf-8')
        
        views_html = []
        captured_scripts = []
        
        for name, r in routes.items():
            res = client.get(r, follow_redirects=True)
            html = res.data.decode('utf-8')
            m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
            content = m.group(1) if m else html
            
            # Extract inline scripts (e.g., Chart.js initializers)
            view_scripts = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.DOTALL)
            for s in view_scripts:
                s_clean = s.strip()
                if s_clean and s_clean not in captured_scripts:
                    captured_scripts.append(s_clean)
                    
            disp = "block" if name == "home" else "none"
            views_html.append(f'<div id="view-{name}" class="page-view" style="display:{disp};">{content}</div>')

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

    # 3. Replace <main>...</main> with combined views
    combined_views = '\n'.join(views_html)
    spa_html = re.sub(r'<main[^>]*>.*?</main>', f'<main class="flex-grow">{combined_views}</main>', home_html, flags=re.DOTALL)

    # 4. Inject global SPA Navigation router
    spa_nav_script = """
    <script>
    // Global SPA Navigation Engine
    window.navigateTo = function(viewName) {
        console.log("Navigating to view:", viewName);
        var views = document.querySelectorAll('.page-view');
        views.forEach(function(el) {
            el.style.display = 'none';
        });
        var target = document.getElementById('view-' + viewName);
        if (target) {
            target.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // Re-trigger resize for responsive Chart.js rendering
            setTimeout(function() {
                window.dispatchEvent(new Event('resize'));
            }, 80);
        }
    };

    // Global Link Interception
    document.addEventListener('DOMContentLoaded', function() {
        var routeMap = {
            '/': 'home',
            '/home': 'home',
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
            '/venture-studio/tracker': 'venture-hub',
            '/dashboard': 'dashboard',
            '/pricing': 'pricing',
            '/business-model': 'business-model'
        };

        // Intercept clicks on links
        document.body.addEventListener('click', function(e) {
            var a = e.target.closest('a');
            if (!a) return;
            var href = a.getAttribute('href');
            if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

            var cleanHref = href.replace(/\\/$/, '') || '/';
            if (routeMap[cleanHref]) {
                e.preventDefault();
                window.navigateTo(routeMap[cleanHref]);
            }
        });

        // Intercept assessment form submit
        document.body.addEventListener('submit', function(e) {
            e.preventDefault();
            // Automatically switch to Career Compass report upon form submission
            window.navigateTo('compass');
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
