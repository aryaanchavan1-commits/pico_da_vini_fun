"""
Personal Portfolio Website - Streamlit App
Modern 2026 UI/UX with 3D animations, floating designs, and AI chatbot
Mobile and Tablet Responsive
"""

import streamlit as st
import json
import os
import base64
from datetime import datetime
from groq import Groq
import psycopg2
from psycopg2.extras import RealDictCursor
from io import BytesIO

# ============================================
# CONFIGURATION & SETUP
# ============================================

# Page configuration
st.set_page_config(
    page_title="Aryan Chavan - Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for 2026 Modern UI/UX with 3D Animations and Mobile Responsive
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --dark: #0f172a;
        --darker: #020617;
        --light: #f8fafc;
        --glass: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
    
    /* Global Styles */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        min-height: 100vh;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .glass-card {
            padding: 1rem;
            border-radius: 16px;
        }
        
        .service-card {
            padding: 1rem;
        }
        
        h1.gradient-text {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .profile-container {
            width: 150px;
            height: 150px;
        }
        
        .stColumns {
            gap: 0.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.85rem;
        }
        
        .social-link {
            width: 40px;
            height: 40px;
        }
        
        .form-container {
            padding: 1rem;
        }
        
        /* Mobile columns */
        .stColumns > div {
            display: flex;
            flex-direction: column;
        }
        
        /* Mobile grid for services/projects */
        .stColumns > div[data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Mobile cards */
        .service-card, .glass-card {
            margin-bottom: 1rem;
            width: 100%;
        }
        
        /* Mobile images */
        .stImage > img {
            max-width: 100% !important;
            height: auto !important;
        }
        
        /* Mobile chat */
        .chat-message {
            max-width: 90%;
            padding: 12px 16px;
        }
    }
    
    /* Tablet Responsive */
    @media (min-width: 769px) and (max-width: 1024px) {
        .stApp {
            padding: 1rem;
        }
        
        h1.gradient-text {
            font-size: 2.2rem !important;
        }
        
        /* Tablet columns - show 2 columns */
        .stColumns > div[data-testid="column"] {
            width: 50% !important;
        }
    }
    
    /* 3D Card Effect */
    .glass-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
    }
    
    @keyframes float-slow {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-30px); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.8); }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    .floating-slow {
        animation: float-slow 8s ease-in-out infinite;
    }
    
    .pulse-glow {
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    /* 3D Tilt Effect Container */
    .tilt-container {
        perspective: 1000px;
    }
    
    .tilt-element {
        transform-style: preserve-3d;
        transition: transform 0.3s ease;
    }
    
    .tilt-element:hover {
        transform: rotateX(10deg) rotateY(-10deg) translateZ(20px);
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 5s ease infinite;
        font-weight: 800;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--glass);
        border-radius: 16px;
        padding: 8px;
        backdrop-filter: blur(10px);
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 12px;
        padding: 12px 24px;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 500;
        transition: all 0.3s ease;
        flex: 1 1 auto;
        min-width: 80px;
        text-align: center;
    }
    
    /* Mobile responsive tabs */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            padding: 6px;
            overflow-x: auto;
            justify-content: flex-start;
            scrollbar-width: thin;
            scrollbar-color: #6366f1 #1e1b4b;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 6px;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
            background: #1e1b4b;
            border-radius: 3px;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: #6366f1;
            border-radius: 3px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.75rem;
            min-width: 60px;
            white-space: nowrap;
        }
        
        .stTabs [data-baseweb="tab"] span {
            font-size: 0.7rem !important;
        }
    }
    
    /* Tablet responsive tabs */
    @media (min-width: 769px) and (max-width: 1024px) {
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px;
            font-size: 0.85rem;
        }
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.5);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        color: white;
        padding: 12px 16px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Mobile input */
    @media (max-width: 768px) {
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            padding: 10px 12px;
            font-size: 0.9rem;
        }
        
        .stTextInput > label,
        .stTextArea > label,
        .stSelectbox > label {
            font-size: 0.85rem;
        }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.5);
    }
    
    /* Mobile button */
    @media (max-width: 768px) {
        .stButton > button {
            padding: 10px 20px;
            font-size: 0.85rem;
            width: 100% !important;
        }
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(15, 23, 42, 0.95);
    }
    
    /* Mobile sidebar */
    @media (max-width: 768px) {
        .css-1d391kg {
            width: 100% !important;
            padding: 0.5rem;
        }
        
        section[data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        section[data-testid="stSidebar"] > div {
            width: 100% !important;
        }
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 12px;
        max-width: 80%;
    }
    
    .chat-user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        margin-left: auto;
    }
    
    .chat-assistant {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        color: white;
    }
    
    /* Service Cards */
    .service-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s ease;
    }
    
    .service-card:hover {
        transform: translateY(-15px) scale(1.05);
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%);
        box-shadow: 0 25px 50px rgba(99, 102, 241, 0.3);
    }
    
    /* Profile Image */
    .profile-container {
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }
    
    .profile-ring {
        position: absolute;
        inset: -5px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    .profile-3d-ring {
        position: absolute;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899, #6366f1);
        background-size: 400% 400%;
        animation: gradient-rotate 4s ease infinite, pulse-glow 3s ease-in-out infinite;
        filter: blur(8px);
    }
    
    @keyframes gradient-rotate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .profile-image {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid var(--darker);
    }
    
    /* Social Links */
    .social-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 12px;
        background: var(--glass);
        border: 1px solid var(--glass-border);
        color: white;
        text-decoration: none;
        transition: all 0.3s ease;
        margin: 0 8px;
    }
    
    .social-link:hover {
        transform: translateY(-5px) scale(1.1);
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 4px;
    }
    
    /* Loading Animation */
    .loader {
        width: 48px;
        height: 48px;
        border: 5px solid #FFF;
        border-bottom-color: #6366f1;
        border-radius: 50%;
        display: inline-block;
        box-sizing: border-box;
        animation: rotation 1s linear infinite;
    }
    
    @keyframes rotation {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Form Container - Dark Green Theme */
    .form-container {
        background: linear-gradient(135deg, #0d3d0d 0%, #1a5c1a 50%, #0d3d0d 100%);
        border: 2px solid #2ecc71;
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(46, 204, 113, 0.3);
    }
    
    /* Form input text color - Black */
    .form-container input, 
    .form-container textarea, 
    .form-container .stTextInput > div > div > input,
    .form-container .stTextArea > div > div > textarea,
    .form-container .stSelectbox > div > div > div {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #2ecc71 !important;
    }
    
    .form-container input::placeholder,
    .form-container textarea::placeholder {
        color: #333333 !important;
    }
    
    /* Form labels */
    .form-container label {
        color: #2ecc71 !important;
        font-weight: 600;
    }
    
    /* Inquiry form text colors */
    .inquiry-title {
        color: #2ecc71 !important;
    }
    .inquiry-subtitle {
        color: #1a5c1a !important;
    }
    
    /* Admin Panel */
    .admin-section {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* File Uploader Styling */
    .stFileUploader > div > div {
        background: var(--glass);
        border-radius: 12px;
    }
    
    /* Responsive Grid */
    .responsive-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA MANAGEMENT
# ============================================

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users_info.json")
ADMIN_FILE = os.path.join(DATA_DIR, "admin_settings.json")
IMAGES_DIR = os.path.join(DATA_DIR, "images")

# Initialize Neon DB (PostgreSQL) connection
def get_db_connection():
    """Get PostgreSQL connection from Neon DB using Streamlit secrets"""
    try:
        db_url = st.secrets["DATABASE_URL"]
        if db_url:
            conn = psycopg2.connect(
                db_url,
                connect_timeout=10
            )
            return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
    return None

# Create user_inquiries table if it doesn't exist
def init_db():
    """Initialize the database tables"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Create user_inquiries table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_inquiries (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    phone VARCHAR(50),
                    service VARCHAR(255),
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create admin_settings table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admin_settings (
                    id INTEGER PRIMARY KEY DEFAULT 1,
                    settings JSONB NOT NULL DEFAULT '{}'::jsonb,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert default admin settings if not exists
            cur.execute("""
                INSERT INTO admin_settings (id, settings) 
                SELECT 1, '{}'::jsonb 
                WHERE NOT EXISTS (SELECT 1 FROM admin_settings WHERE id = 1)
            """)
            
            # Create visitors tracking table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS visitors (
                    id SERIAL PRIMARY KEY,
                    ip_address VARCHAR(50),
                    user_agent TEXT,
                    device_type VARCHAR(50),
                    browser VARCHAR(100),
                    os VARCHAR(100),
                    country VARCHAR(100),
                    city VARCHAR(100),
                    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error initializing database: {e}")

# Track visitor and save to database
def track_visitor(ip_address, user_agent, device_type, browser, os_name):
    """Save visitor information to the database"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO visitors (ip_address, user_agent, device_type, browser, os) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (ip_address, user_agent, device_type, browser, os_name)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error tracking visitor: {e}")

# Get visitor info using JavaScript
def get_visitor_info():
    """Get visitor information using JavaScript and Streamlit"""
    import streamlit.components.v1 as components
    
    # JavaScript to get visitor info
    visitor_info_script = """
    <script>
    function getBrowserInfo() {
        const ua = navigator.userAgent;
        let browser = 'Unknown';
        let os = 'Unknown';
        let deviceType = 'Desktop';
        
        // Detect browser
        if (ua.indexOf('Firefox') > -1) browser = 'Firefox';
        else if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) browser = 'Chrome';
        else if (ua.indexOf('Edg') > -1) browser = 'Edge';
        else if (ua.indexOf('Safari') > -1 && ua.indexOf('Chrome') === -1) browser = 'Safari';
        
        // Detect OS
        if (ua.indexOf('Win') > -1) os = 'Windows';
        else if (ua.indexOf('Mac') > -1) os = 'macOS';
        else if (ua.indexOf('Linux') > -1) os = 'Linux';
        else if (ua.indexOf('Android') > -1) os = 'Android';
        else if (ua.indexOf('iPhone') > -1 || ua.indexOf('iPad') > -1) os = 'iOS';
        
        // Detect device type
        if (ua.indexOf('Mobile') > -1 || ua.indexOf('Android') > -1) deviceType = 'Mobile';
        else if (ua.indexOf('Tablet') > -1 || ua.indexOf('iPad') > -1) deviceType = 'Tablet';
        
        return { browser, os, deviceType, userAgent: ua };
    }
    
    const info = getBrowserInfo();
    
    // Send info to Streamlit via custom event
    window.parent.postMessage({ type: 'streamlit:setComponentValue', value: info }, '*');
    </script>
    """
    
    # Create a component to get visitor info
    visitor_component = components.html(
        f"<html><body>{visitor_info_script}</body></html>",
        height=0
    )
    
    return visitor_component

# Load admin settings from database
def load_admin_settings():
    """Load admin settings from Neon DB"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT settings FROM admin_settings WHERE id = 1")
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result and result['settings']:
                # Merge with defaults
                settings = DEFAULT_ADMIN_SETTINGS.copy()
                settings.update(result['settings'])
                return settings
        except Exception as e:
            st.error(f"Error loading admin settings: {e}")
    # Fallback to JSON file
    return load_json(ADMIN_FILE, DEFAULT_ADMIN_SETTINGS)

# Save admin settings to database
def save_admin_settings(settings):
    """Save admin settings to Neon DB"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Convert settings to JSON
            import json
            settings_json = json.dumps(settings)
            cur.execute(
                """INSERT INTO admin_settings (id, settings, updated_at) 
                   VALUES (1, %s, CURRENT_TIMESTAMP) 
                   ON CONFLICT (id) DO UPDATE SET settings = %s, updated_at = CURRENT_TIMESTAMP""",
                (settings_json, settings_json)
            )
            conn.commit()
            cur.close()
            conn.close()
            # Also save to JSON as backup
            save_json(ADMIN_FILE, settings)
            return True
        except Exception as e:
            st.error(f"Error saving admin settings: {e}")
    # Fallback to JSON if DB fails
    save_json(ADMIN_FILE, settings)
    return True

# Initialize database on startup
init_db()

# Track visitor on each visit (using session state to avoid duplicates)
if 'visitor_tracked' not in st.session_state:
    st.session_state.visitor_tracked = True
    
    # Get visitor info using JavaScript
    import streamlit.components.v1 as components
    
    visitor_info_html = """
    <script>
    (function() {
        const ua = navigator.userAgent;
        let browser = 'Unknown';
        let os = 'Unknown';
        let deviceType = 'Desktop';
        
        // Detect browser
        if (ua.indexOf('Firefox') > -1) browser = 'Firefox';
        else if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) browser = 'Chrome';
        else if (ua.indexOf('Edg') > -1) browser = 'Edge';
        else if (ua.indexOf('Safari') > -1 && ua.indexOf('Chrome') === -1) browser = 'Safari';
        
        // Detect OS
        if (ua.indexOf('Win') > -1) os = 'Windows';
        else if (ua.indexOf('Mac') > -1) os = 'macOS';
        else if (ua.indexOf('Linux') > -1) os = 'Linux';
        else if (ua.indexOf('Android') > -1) os = 'Android';
        else if (ua.indexOf('iPhone') > -1 || ua.indexOf('iPad') > -1) os = 'iOS';
        
        // Detect device type
        if (ua.indexOf('Mobile') > -1 || ua.indexOf('Android') > -1) deviceType = 'Mobile';
        else if (ua.indexOf('Tablet') > -1 || ua.indexOf('iPad') > -1) deviceType = 'Tablet';
        
        // Get IP (using a public API - note: this is async)
        fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {
                // Store info in localStorage for Streamlit to read
                localStorage.setItem('visitor_ip', data.ip);
                localStorage.setItem('visitor_browser', browser);
                localStorage.setItem('visitor_os', os);
                localStorage.setItem('visitor_device', deviceType);
                localStorage.setItem('visitor_ua', ua);
            })
            .catch(err => {
                localStorage.setItem('visitor_ip', 'Unknown');
                localStorage.setItem('visitor_browser', browser);
                localStorage.setItem('visitor_os', os);
                localStorage.setItem('visitor_device', deviceType);
                localStorage.setItem('visitor_ua', ua);
            });
    })();
    </script>
    """
    
    components.html(visitor_info_html, height=0)
    
    # Try to get visitor info from localStorage (set by JavaScript)
    # Note: This is a workaround - in production, consider using a proper analytics service
    visitor_ip = "Unknown"
    visitor_browser = "Unknown"
    visitor_os = "Unknown"
    visitor_device = "Desktop"
    visitor_ua = "Unknown"
    
    # Track the visitor in the database
    track_visitor(visitor_ip, visitor_ua, visitor_device, visitor_browser, visitor_os)

# Initialize Neon DB client at module level
db_connection = get_db_connection()
RESUME_DIR = os.path.join(DATA_DIR, "resumes")
PROJECTS_DIR = os.path.join(DATA_DIR, "projects")

# Create directories if not exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(RESUME_DIR, exist_ok=True)

def load_json(file_path, default=None):
    """Load JSON file or return default"""
    if default is None:
        default = {}
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(file_path, data):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def save_uploaded_file(uploaded_file, directory):
    """Save uploaded file to directory"""
    if uploaded_file:
        try:
            # Ensure directory exists
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            st.error(f"Error saving file: {e}")
    return None

def get_image_base64(image_path):
    """Convert image to base64 for display"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        pass
    return None

# Initialize default admin settings
DEFAULT_ADMIN_SETTINGS = {
    "name": "Aryan Chavan",
    "title": "AI/ML Engineer & Python Developer",
    "tagline": "Building Intelligent Solutions for Tomorrow",
    "email": "aryaanchavan1@gmail.com",
    "phone": "+91 98765 43210",
    "github": "https://github.com/aryaanchavan1-commits",
    "linkedin": "https://www.linkedin.com/in/aryan-chavan-4b47b236b/",
    "location": "Chiplun-Kherdi,Ratnagiri, India",
    "about": "Passionate and aspiring AI/ML engineer with expertise in building intelligent solutions. I specialize in machine learning, deep learning, LLM applications, and Python development.",
    "skills": ["Python", "Machine Learning"],
    "experience": [
        {"title": "AI/ML Engineer", "company": "Tech Corp", "duration": "2023 - Present", "description": "Building AI-powered solutions"}
    ],
    "education": [
        {"degree": "class 11", "institution": "navnirmaan", "year": "2026"}
    ],
    "services": [
        {
            "icon": "🤖",
            "title": "AI/ML Development",
            "description": "Custom machine learning models, predictive analytics, and intelligent automation solutions tailored to your business needs.",
            "features": ["Machine Learning", "Deep Learning", "Predictive Models", "Computer Vision"]
        },
        {
            "icon": "🧠",
            "title": "LLM Solutions",
            "description": "Build powerful applications with Large Language Models, including chatbots, content generation, and NLP solutions.",
            "features": ["Chatbots", "Text Generation", "Sentiment Analysis", "Document Processing"]
        },
        {
            "icon": "🐍",
            "title": "Python Development",
            "description": "End-to-end Python development services including web apps, automation scripts, and enterprise solutions.",
            "features": ["Web Development", "API Development", "Automation", "Backend Systems"]
        }
    ],
    "profile_image": None,
    "profile_image_name": None,
    "resume_filename": None,
    "groq_api_key": ""
}

# Load admin settings from database (with JSON fallback)
try:
    admin_settings = load_admin_settings()
except:
    # Fallback to JSON file if database fails
    admin_settings = load_json(ADMIN_FILE, DEFAULT_ADMIN_SETTINGS)
    if not admin_settings:
        admin_settings = DEFAULT_ADMIN_SETTINGS.copy()
    try:
        save_admin_settings(admin_settings)  # Migrate to database
    except:
        pass

def get_admin_settings():
    """Get fresh admin settings from database"""
    try:
        return load_admin_settings()
    except:
        return load_json(ADMIN_FILE, DEFAULT_ADMIN_SETTINGS)

# ============================================
# SESSION STATE
# ============================================

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'groq_client' not in st.session_state:
    st.session_state.groq_client = None

# Admin settings session state - loads fresh when admin panel opens
if 'admin_settings' not in st.session_state:
    st.session_state.admin_settings = get_admin_settings()

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_groq_client(api_key):
    """Initialize Groq client"""
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq: {e}")
        return None

def get_chat_response(client, messages):
    """Get response from Groq API"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def save_user_inquiry(name, email, phone, service, message):
    """Save user inquiry to Neon DB (PostgreSQL)"""
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO user_inquiries (name, email, phone, service, message, created_at) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (name, email, phone, service, message, datetime.now())
            )
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Database error: {e}")
            # Fallback to JSON if DB fails
            pass
    
    # Fallback to JSON if DB is not available
    users = load_json(USERS_FILE, [])
    new_entry = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    users.append(new_entry)
    return save_json(USERS_FILE, users)

# ============================================
# UI COMPONENTS
# ============================================

def render_3d_background():
    """Render animated 3D background elements"""
    st.markdown("""
    <div class="floating" style="position: fixed; top: 10%; left: 5%; width: 300px; height: 300px; 
         background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%);
         border-radius: 50%; pointer-events: none; z-index: -1;"></div>
    <div class="floating-slow" style="position: fixed; bottom: 20%; right: 10%; width: 400px; height: 400px;
         background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
         border-radius: 50%; pointer-events: none; z-index: -1;"></div>
    <div class="floating" style="position: fixed; top: 50%; left: 80%; width: 200px; height: 200px;
         background: radial-gradient(circle, rgba(236, 72, 153, 0.2) 0%, transparent 70%);
         border-radius: 50%; pointer-events: none; z-index: -1; animation-delay: 2s;"></div>
    """, unsafe_allow_html=True)

def render_profile_section():
    """Render the main profile section"""
    # Always get fresh settings
    current_settings = get_admin_settings()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Profile image - check for custom uploaded image first, then fall back to default
        custom_image_name = current_settings.get("profile_image_name")
        if custom_image_name:
            profile_image_path = os.path.join(IMAGES_DIR, custom_image_name)
        else:
            profile_image_path = os.path.join(IMAGES_DIR, "1.jpeg")
        
        # Try to display image with 3D animated border
        if os.path.exists(profile_image_path):
            try:
                # Read image and encode to base64 for custom HTML display
                import base64
                with open(profile_image_path, "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                
                # Get image extension for correct MIME type
                img_ext = os.path.splitext(profile_image_path)[1].lower()
                if img_ext in ['.png']:
                    mime_type = 'image/png'
                elif img_ext in ['.gif']:
                    mime_type = 'image/gif'
                elif img_ext in ['.webp']:
                    mime_type = 'image/webp'
                else:
                    mime_type = 'image/jpeg'
                
                # Beautiful 3D animated border from all sides - enhanced version
                html = '''
                <style>
                @media (max-width: 768px) {
                    .profile-img { width: 180px !important; height: 220px !important; }
                }
                @media (min-width: 769px) {
                    .profile-img { width: 280px !important; height: 340px !important; }
                }
                </style>
                <div style="text-align: center; padding: 20px;">
                    <div style="position: relative; display: inline-block; padding: 15px;">
                        <div style="position: absolute; inset: -20px; border-radius: 25px; 
                                    background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06d6a0, #ff006e, #8338ec);
                                    background-size: 400% 400%;
                                    animation: border-gradient 3s linear infinite;
                                    z-index: 0;"></div>
                        <div style="position: absolute; inset: -12px; border-radius: 20px; 
                                    background: linear-gradient(45deg, #3a86ff, #06d6a0, #ff006e, #8338ec, #3a86ff);
                                    background-size: 400% 400%;
                                    animation: border-gradient 3s linear infinite reverse;
                                    z-index: 1;"></div>
                        <div style="position: absolute; inset: -4px; border-radius: 15px; 
                                    background: linear-gradient(45deg, #8338ec, #3a86ff, #06d6a0, #ff006e, #8338ec);
                                    background-size: 400% 400%;
                                    animation: border-gradient 2s linear infinite;
                                    z-index: 2;"></div>
                        <img src="data:''' + mime_type + ''';base64,''' + img_base64 + '''" 
                             class="profile-img" style="width: 280px; height: 340px; border-radius: 12px; 
                                    object-fit: cover; border: 3px solid #0f172a;
                                    position: relative; z-index: 3;
                                    box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
                        <div style="position: absolute; inset: 0; border-radius: 12px;
                                    box-shadow: inset 0 0 30px rgba(58, 134, 255, 0.3);
                                    z-index: 4; pointer-events: none;"></div>
                    </div>
                </div>
                <style>
                @keyframes border-gradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                </style>
                '''
                st.markdown(html, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error loading image: {e}")
                
        else:
            st.warning("📷 No profile image found. Please upload one in Admin panel.")
            
    
    with col2:
        st.markdown(f"""
        <h1 class="gradient-text" style="font-size: 3rem; margin-bottom: 0.5rem;">
            {current_settings.get('name', 'Your Name')}
        </h1>
        <h2 style="color: rgba(255,255,255,0.8); font-weight: 400; font-size: 1.5rem; margin-bottom: 1rem;">
            {current_settings.get('title', 'Your Title')}
        </h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 1.1rem; line-height: 1.8;">
            {current_settings.get('tagline', 'Your Tagline')}
        </p>
        <p style="color: rgba(255,255,255,0.5); font-size: 1rem; margin-top: 0.5rem;">
            📍 {current_settings.get('location', 'Location')}
        </p>
        """, unsafe_allow_html=True)
        
        # Social links
        st.markdown("<div style='margin-top: 1.5rem; display: flex; justify-content: flex-start; flex-wrap: wrap; gap: 0.5rem;'>", unsafe_allow_html=True)
        
        col_social1, col_social2, col_social3, col_social4 = st.columns(4)
        
        with col_social1:
            if current_settings.get("github"):
                st.markdown(f"""
                <a href="{current_settings['github']}" target="_blank" class="social-link">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                </a>
                """, unsafe_allow_html=True)
        
        with col_social2:
            if current_settings.get("linkedin"):
                st.markdown(f"""
                <a href="{current_settings['linkedin']}" target="_blank" class="social-link">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                </a>
                """, unsafe_allow_html=True)
        
        with col_social3:
            if current_settings.get("email"):
                st.markdown(f"""
                <a href="mailto:{current_settings['email']}" class="social-link">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M0 3v18h24v-18h-24zm21.518 2l-9.518 7.713-9.518-7.713h19.036zm-19.518 14v-11.817l10 8.104 10-8.104v11.817h-20z"/>
                    </svg>
                </a>
                """, unsafe_allow_html=True)
        
        with col_social4:
            if current_settings.get("phone"):
                st.markdown(f"""
                <a href="tel:{current_settings['phone']}" class="social-link">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1v3.49c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.49c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                    </svg>
                </a>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_services_section():
    """Render services section from admin settings"""
    # Always get fresh settings
    current_settings = get_admin_settings()
    services = current_settings.get("services", [])
    
    if not services:
        st.info("No services configured yet. Go to Admin panel to add services.")
        return
    
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 2rem;'>Services</h2>", unsafe_allow_html=True)
    
    # Service cards in responsive grid
    cols = st.columns(2) if len(services) >= 2 else st.columns(1)
    
    for idx, service in enumerate(services):
        with cols[idx % 2]:
            features = service.get('features', [])
            features_str = ''
            if features:
                features_str = '<div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;">'
                for feature in features:
                    features_str += f'<span style="background: rgba(99, 102, 241, 0.3); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; color: white; margin: 2px;">{feature}</span>'
                features_str += '</div>'
            
            st.markdown(f"""
            <div class="service-card tilt-element">
                <div style="font-size: 4rem; margin-bottom: 1rem;">{service.get('icon', '💼')}</div>
                <h3 style="color: white; font-size: 1.5rem; margin-bottom: 1rem;">{service.get('title', 'Service')}</h3>
                <p style="color: rgba(255,255,255,0.7); line-height: 1.6; margin-bottom: 1.5rem;">{service.get('description', 'Description')}</p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;">
                    {features_str}
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_inquire_section():
    """Render inquiry form section"""
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 1rem;'>Get In Touch</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-bottom: 2rem;'>Have a project in mind? Let's discuss how I can help you.</p>", unsafe_allow_html=True)
    
    # Always get fresh settings
    current_settings = get_admin_settings()
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Get services from admin settings
        services = current_settings.get("services", [])
        service_options = [s.get("title", "Service") for s in services] if services else ["AI/ML Development", "Data Science", "LLM Solutions", "Python Development"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Your Name", placeholder="John Doe")
            email = st.text_input("📧 Email Address", placeholder="john@example.com")
        
        with col2:
            phone = st.text_input("📱 Phone Number", placeholder="+91 98765 43210")
            service = st.selectbox("💼 Interested Service", service_options)
        
        message = st.text_area("💬 Your Message", placeholder="Tell me about your project...", height=120)
        
        submit_btn = st.button("🚀 Send Inquiry", width='stretch')
        
        if submit_btn:
            if name and email and phone:
                if save_user_inquiry(name, email, phone, service, message):
                    st.success("✅ Inquiry sent successfully! I'll get back to you soon.")
                else:
                    st.error("❌ Failed to send inquiry. Please try again.")
            else:
                st.warning("⚠️ Please fill in all required fields (Name, Email, Phone)")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_chatbot_section():
    """Render AI chatbot section"""
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 1rem;'>AI Chat Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-bottom: 2rem;'>Ask me anything about my services, experience, or skills!</p>", unsafe_allow_html=True)
    
    # Always get fresh settings
    current_settings = get_admin_settings()
    saved_api_key = current_settings.get("groq_api_key", "")
    
    if not saved_api_key:
        st.warning("⚠️ there is some error from the developer please wait for a while until aryan fixes it ")
        return
    
    # Initialize client if not already done
    if not st.session_state.groq_client:
        st.session_state.groq_client = get_groq_client(saved_api_key)
    
    if st.session_state.groq_client:
        st.success("✅ AI Chat Ready!")
    else:
        st.error("❌ Failed to connect to AI service. Check API key in Admin Panel.")
        return
    
    # Chat container
    chat_container = st.container()
    
    # Voice mode toggle and clear chat
    col_voice, col_clear = st.columns([1, 1])
    
    with col_voice:
        voice_enabled = st.checkbox("🔊 Voice Mode", value=False, help="Enable text-to-speech for AI responses")
    
    with col_clear:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message chat-user">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message chat-assistant">
                    <strong>🤖 Assistant:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input and st.session_state.groq_client:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Prepare messages for API
        services_list = current_settings.get("services", [])
        services_str = ", ".join([s.get("title", "") for s in services_list]) if services_list else "AI/ML Development, Data Science, LLM Solutions, Python Development"
        
        # Get experience
        experience_list = current_settings.get("experience", [])
        experience_str = "".join([f"- {exp.get('title', 'Title')} at {exp.get('company', 'Company')} ({exp.get('duration', 'Duration')})" + chr(10) for exp in experience_list]) if experience_list else "No experience listed"
        
        # Get education
        education_list = current_settings.get("education", [])
        education_str = "".join([f"- {edu.get('degree', 'Degree')} from {edu.get('institution', 'Institution')} ({edu.get('year', 'Year')})" + chr(10) for edu in education_list]) if education_list else "No education listed"
        
        system_prompt = f"""You are an AI assistant for {current_settings.get('name', 'Aryan')}, who is an {current_settings.get('title', 'AI/ML Engineer')}. 
        About: {current_settings.get('about', '')}
        Skills: {', '.join(current_settings.get('skills', []))}
        Services offered: {services_str}.
        Experience:\n{experience_str}
        Education:\n{education_str}
        Contact: Email - {current_settings.get('email', '')}, Phone - {current_settings.get('phone', '')}
        Respond helpfully to questions about services, experience, education, and how to get in touch."""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(st.session_state.chat_history[-6:])  # Last 6 messages
        
        # Get response
        response = get_chat_response(st.session_state.groq_client, messages)
        
        # Add assistant response
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Speak response if voice is enabled
        if voice_enabled:
            # Replace special characters for speech
            speech_text = response.replace('*', '').replace('#', '').replace('`', '')
            st.markdown(f"""
            <script>
            setTimeout(function() {{
                speakText("{speech_text.replace('"', '\\"').replace('\n', ' ')}");
            }}, 500);
            </script>
            """, unsafe_allow_html=True)
        
        # Rerun to update chat
        st.rerun()
    
    elif user_input and not st.session_state.groq_client:
        st.warning("⚠️ Please enter your Groq API key first!")
    
    # Voice synthesis JavaScript
    if voice_enabled:
        st.markdown("""
        <script>
        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1;
                utterance.pitch = 1;
                window.speechSynthesis.speak(utterance);
            }
        }
        </script>
        """, unsafe_allow_html=True)

def render_projects_section():
    """Render projects section with uploaded project images and names"""
    # Always get fresh settings
    current_settings = get_admin_settings()
    
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 2rem;'>My Projects</h2>", unsafe_allow_html=True)
    
    # Get projects from admin settings
    projects = current_settings.get('projects', [])
    
    if not projects:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3 style="color: rgba(255,255,255,0.7);">No Projects Yet</h3>
            <p style="color: rgba(255,255,255,0.5);">Admin hasn't added any projects yet.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create a nice grid layout for projects
    cols_per_row = 3
    for i in range(0, len(projects), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(projects):
                project = projects[idx]
                project_name = project.get('name', 'Untitled Project')
                project_image = project.get('image', '')
                
                with col:
                    st.markdown("<div style='text-align: center; margin-bottom: 2rem;'>", unsafe_allow_html=True)
                    
                    # Display project image if available
                    if project_image:
                        try:
                            # Decode base64 image
                            image_data = base64.b64decode(project_image)
                            st.image(image_data, caption=project_name, width='stretch')
                        except:
                            # Show placeholder if image fails
                            st.markdown(f"""
                            <div class="glass-card" style="height: 200px; display: flex; align-items: center; justify-content: center;">
                                <span style="font-size: 3rem;">🖼️</span>
                            </div>
                            <p style="text-align: center; margin-top: 0.5rem; color: white;">{project_name}</p>
                            """, unsafe_allow_html=True)
                    else:
                        # Show placeholder
                        st.markdown(f"""
                        <div class="glass-card" style="height: 200px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 3rem;">🖼️</span>
                        </div>
                        <p style="text-align: center; margin-top: 0.5rem; color: white;">{project_name}</p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

def render_certifications_section():
    """Render certifications section with uploaded certification images"""
    # Always get fresh settings
    current_settings = get_admin_settings()
    
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 2rem;'>🏆 My Certifications</h2>", unsafe_allow_html=True)
    
    # Get certifications from admin settings
    certifications = current_settings.get('certifications', [])
    
    if not certifications:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h3 style="color: rgba(255,255,255,0.7);">No Certifications Yet</h3>
            <p style="color: rgba(255,255,255,0.5);">Admin hasn't added any certifications yet.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create a nice grid layout for certifications
    cols_per_row = 2
    for i in range(0, len(certifications), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(certifications):
                cert = certifications[idx]
                cert_name = cert.get('name', 'Certification')
                cert_issuer = cert.get('issuer', '')
                cert_image = cert.get('image', '')
                
                with col:
                    st.markdown("<div style='margin-bottom: 2rem;'>", unsafe_allow_html=True)
                    
                    # Display certification image if available
                    if cert_image:
                        try:
                            # Decode base64 image
                            image_data = base64.b64decode(cert_image)
                            st.image(image_data, caption=cert_name, width='stretch')
                        except:
                            # Show placeholder if image fails
                            st.markdown(f"""
                            <div class="glass-card" style="height: 250px; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                                <span style="font-size: 4rem;">🏆</span>
                                <p style="color: white; margin-top: 1rem; text-align: center;">{cert_name}</p>
                                <p style="color: rgba(255,255,255,0.6); text-align: center;">{cert_issuer}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Show placeholder
                        st.markdown(f"""
                        <div class="glass-card" style="height: 250px; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                            <span style="font-size: 4rem;">🏆</span>
                            <p style="color: white; margin-top: 1rem; text-align: center;">{cert_name}</p>
                            <p style="color: rgba(255,255,255,0.6); text-align: center;">{cert_issuer}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

def render_resume_section():
    """Render resume section with uploaded files"""
    # Always get fresh settings
    current_settings = get_admin_settings()
    
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 2rem;'>Resume</h2>", unsafe_allow_html=True)
    
    # Check if resume exists
    resume_filename = current_settings.get("resume_filename")
    
    # Prominent download section at the top
    if resume_filename:
        resume_path = os.path.join(RESUME_DIR, resume_filename)
        if os.path.exists(resume_path):
            ext = resume_filename.lower().split('.')[-1]
            
            # Read file for download
            with open(resume_path, "rb") as f:
                file_data = f.read()
            
            # Create a prominent download card
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 30px; margin: 20px 0; border: 2px solid #6366f1;">
                <h3 style="color: white; margin-bottom: 15px;">📥 Download My Resume</h3>
                <p style="color: rgba(255,255,255,0.7); margin-bottom: 20px;">Click the button below to download my complete resume</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Large download button
            col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
            with col_dl2:
                mime_type = "application/pdf" if ext == "pdf" else f"image/{ext}"
                st.download_button(
                    label="📥 DOWNLOAD RESUME",
                    data=file_data,
                    file_name=f"Resume_{current_settings.get('name', 'Professional')}.{ext}",
                    mime=mime_type,
                    type="primary"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("📄 No resume uploaded yet. Please upload your resume in the Admin panel.")
    
    resume_col1, resume_col2 = st.columns([1, 1])
    
    with resume_col1:
        if resume_filename:
            resume_path = os.path.join(RESUME_DIR, resume_filename)
            if os.path.exists(resume_path):
                # Check file type
                ext = resume_filename.lower().split('.')[-1]
                
                if ext == 'pdf':
                    with open(resume_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()
                    
                    st.download_button(
                        label="📥 Download Resume (PDF)",
                        data=PDFbyte,
                        file_name=f"Resume_{current_settings.get('name', 'Professional')}.pdf",
                        mime="application/pdf"
                    )
                else:
                    # Display image without filename
                    img_base64 = get_image_base64(resume_path)
                    if img_base64:
                        mime = 'image/jpeg' if ext in ['jpg', 'jpeg'] else f'image/{ext}'
                        st.markdown(f"""
                        <div class="glass-card">
                            <img src="data:{mime};base64,{img_base64}" style="max-width: 100%; border-radius: 12px;">
                        </div>
                        """, unsafe_allow_html=True)
                    # Add download button for images too
                    with open(resume_path, "rb") as f:
                        img_data = f.read()
                    st.download_button(
                        label="📥 Download Resume",
                        data=img_data,
                        file_name=f"Resume_{current_settings.get('name', 'Professional')}.{ext}",
                        mime=mime
                    )
    
    with resume_col2:
        # Experience section
        st.markdown("<h3 style='color: white; font-size: 1.5rem; margin-bottom: 1rem;'>Experience</h3>", unsafe_allow_html=True)
        
        for exp in current_settings.get("experience", []):
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem; padding: 1rem;">
                <h4 style="color: white; font-size: 1.1rem; margin-bottom: 0.5rem;">{exp.get('title', 'Title')}</h4>
                <p style="color: #6366f1; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;">{exp.get('company', 'Company')} | {exp.get('duration', 'Duration')}</p>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{exp.get('description', 'Description')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Education section
        st.markdown("<h3 style='color: white; font-size: 1.5rem; margin: 1.5rem 0 1rem;'>Education</h3>", unsafe_allow_html=True)
        
        for edu in current_settings.get("education", []):
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem; padding: 1rem;">
                <h4 style="color: white; font-size: 1.1rem; margin-bottom: 0.5rem;">{edu.get('degree', 'Degree')}</h4>
                <p style="color: #8b5cf6; font-weight: 600; font-size: 0.9rem;">{edu.get('institution', 'Institution')} | {edu.get('year', 'Year')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Skills section
    st.markdown("<h3 style='color: white; font-size: 1.5rem; margin: 1.5rem 0 1rem;'>Skills</h3>", unsafe_allow_html=True)
    
    skills = current_settings.get("skills", [])
    skills_html = '<div style="display: flex; flex-wrap: wrap; gap: 12px;">'
    for skill in skills:
        skills_html += f'<span class="pulse-glow" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 10px 20px; border-radius: 25px; color: white; font-weight: 500;">{skill}</span>'
    skills_html += '</div>'
    
    st.markdown(skills_html, unsafe_allow_html=True)

def render_admin_panel():
    """Render admin panel with all editing features"""
    st.markdown("<h2 class='gradient-text' style='text-align: center; font-size: 2.5rem; margin-bottom: 2rem;'>Admin Panel</h2>", unsafe_allow_html=True)
    
    # Authentication check
    if not st.session_state.authenticated:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: white; margin-bottom: 1.5rem;'>🔐 Admin Login</h3>", unsafe_allow_html=True)
        
        admin_name = st.text_input("Admin Name", placeholder="Enter admin name")
        admin_password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("Login", width='stretch'):
            if admin_name == "aryan" and admin_password == "aryankali1":
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Load fresh settings from database or use session state
    if 'admin_settings' not in st.session_state:
        st.session_state.admin_settings = get_admin_settings()
    
    # Use session state for editing
    admin_settings = st.session_state.admin_settings
    
    # Logout button - also reload settings
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        # Refresh admin settings from database on next login
        st.session_state.admin_settings = get_admin_settings()
        st.rerun()
    
    # Edit sections
    st.markdown("<h3 style='color: white; font-size: 1.8rem; margin: 2rem 0 1.5rem;'>Edit Profile Information</h3>", unsafe_allow_html=True)
    
    # API Key Management
    with st.expander("🔑 API Key Management", expanded=False):
        admin_settings["groq_api_key"] = st.text_input("Groq API Key", type="password", value=admin_settings.get("groq_api_key", ""), help="Enter your Groq API key for chatbot functionality")
        if admin_settings["groq_api_key"]:
            st.success("✅ API Key saved")
    
    # Basic Info
    with st.expander("📝 Basic Information", expanded=True):
        admin_settings["name"] = st.text_input("Name", admin_settings.get("name", ""))
        admin_settings["title"] = st.text_input("Title", admin_settings.get("title", ""))
        admin_settings["tagline"] = st.text_input("Tagline", admin_settings.get("tagline", ""))
        admin_settings["about"] = st.text_area("About Me", admin_settings.get("about", ""), height=150)
        admin_settings["location"] = st.text_input("Location", admin_settings.get("location", ""))
    
    # Contact Info
    with st.expander("📞 Contact Information"):
        admin_settings["email"] = st.text_input("Email", admin_settings.get("email", ""))
        admin_settings["phone"] = st.text_input("Phone", admin_settings.get("phone", ""))
        admin_settings["github"] = st.text_input("GitHub URL", admin_settings.get("github", ""))
        admin_settings["linkedin"] = st.text_input("LinkedIn URL", admin_settings.get("linkedin", ""))
    
    # Profile Image Upload with 3D Effects
    with st.expander("🖼️ Profile Image (3D)", expanded=True):
        
        # 3D Upload Zone CSS
        st.markdown("""
        <style>
            .upload-zone-3d {
                border: 3px dashed rgba(99, 102, 241, 0.6);
                border-radius: 20px;
                padding: 2rem;
                text-align: center;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
                transition: all 0.4s ease;
                margin-bottom: 1.5rem;
            }
            .upload-zone-3d:hover {
                border-color: #8b5cf6;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.25) 100%);
                transform: scale(1.02) rotateX(5deg);
                box-shadow: 0 15px 40px rgba(99, 102, 241, 0.3);
            }
            .preview-card-3d {
                perspective: 1000px;
                transform-style: preserve-3d;
                transition: transform 0.5s ease;
            }
            .preview-card-3d:hover {
                transform: rotateY(15deg) rotateX(10deg) translateZ(20px);
            }
        </style>
        <div class="upload-zone-3d">
            <h4 style="color: white; margin-bottom: 0.5rem;">📤 Upload Your Photo</h4>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">Drag & drop or browse • JPG, PNG, GIF</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_up1, col_up2 = st.columns([1, 1])
        
        with col_up1:
            uploaded_profile = st.file_uploader(" ", type=["jpg", "jpeg", "png", "gif"], label_visibility="collapsed")
            
            if uploaded_profile:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Upload Photo", type="primary", width='stretch'):
                    file_path = save_uploaded_file(uploaded_profile, IMAGES_DIR)
                    if file_path:
                        admin_settings["profile_image_name"] = uploaded_profile.name
                        save_admin_settings(admin_settings)  # Save to database
                        st.success("✅ Photo uploaded!")
                        st.rerun()
        
        with col_up2:
            # Show current image with 3D preview
            current_image = admin_settings.get("profile_image_name")
            if current_image:
                image_path = os.path.join(IMAGES_DIR, current_image)
                if os.path.exists(image_path):
                    img_base64 = get_image_base64(image_path)
                    if img_base64:
                        ext = current_image.lower().split('.')[-1]
                        mime = 'image/jpeg' if ext in ['jpg', 'jpeg'] else f'image/{ext}'
                        st.markdown(f"""
                        <div class="preview-card-3d" style="text-align: center; padding: 1rem;">
                            <div style="position: relative; display: inline-block;">
                                <div class="pulse-glow" style="position: absolute; inset: -15px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);"></div>
                                <img src="data:{mime};base64,{img_base64}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #0f172a; position: relative; z-index: 1;">
                            </div>
                            <p style="color: rgba(255,255,255,0.8); margin-top: 1rem; font-size: 0.9rem;">✅ {current_image}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🗑️ Remove", width='stretch'):
                            admin_settings["profile_image_name"] = None
                            os.remove(image_path)
                            st.success("✅ Removed!")
                            st.rerun()
    
    # Skills
    with st.expander("💼 Skills"):
        skills_text = st.text_area("Skills (comma separated)", ", ".join(admin_settings.get("skills", [])))
        admin_settings["skills"] = [s.strip() for s in skills_text.split(",") if s.strip()]
    
    # Services Management
    with st.expander("🛠️ Services Management"):
        services = admin_settings.get("services", [])
        
        # Button to add new service
        if st.button("➕ Add New Service"):
            services.append({
                "icon": "💼",
                "title": "New Service",
                "description": "Service description",
                "features": ["Feature 1", "Feature 2"]
            })
            admin_settings["services"] = services
            save_admin_settings(admin_settings)  # Save to database
            st.rerun()
        
        # Edit existing services
        for i, service in enumerate(services):
            st.markdown(f"**Service {i+1}**")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                service["icon"] = st.text_input(f"Icon {i+1}", service.get("icon", "💼"), key=f"icon_{i}")
                service["title"] = st.text_input(f"Title {i+1}", service.get("title", "Service"), key=f"title_{i}")
            with col_s2:
                service["description"] = st.text_area(f"Description {i+1}", service.get("description", "Description"), key=f"desc_{i}")
            
            features_text = st.text_input(f"Features {i+1} (comma separated)", ", ".join(service.get("features", [])), key=f"feat_{i}")
            service["features"] = [f.strip() for f in features_text.split(",") if f.strip()]
            
            if st.button(f"🗑️ Remove Service {i+1}", key=f"rem_{i}"):
                services.pop(i)
                admin_settings["services"] = services
                save_admin_settings(admin_settings)  # Save to database
                st.rerun()
            
            st.markdown("---")
        
        # Save services on exit
        admin_settings["services"] = services
        save_admin_settings(admin_settings)  # Auto-save to database
    
    # Experience
    with st.expander("💼 Experience"):
        experience_list = []
        for i, exp in enumerate(admin_settings.get("experience", [])):
            st.markdown(f"**Experience {i+1}**")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                exp_title = st.text_input(f"Title {i+1}", exp.get("title", ""), key=f"exp_title_{i}")
                exp_company = st.text_input(f"Company {i+1}", exp.get("company", ""), key=f"exp_company_{i}")
            with col_e2:
                exp_duration = st.text_input(f"Duration {i+1}", exp.get("duration", ""), key=f"exp_duration_{i}")
                exp_desc = st.text_area(f"Description {i+1}", exp.get("description", ""), key=f"exp_desc_{i}")
            experience_list.append({
                "title": exp_title,
                "company": exp_company,
                "duration": exp_duration,
                "description": exp_desc
            })
        
        if st.button("+ Add Experience"):
            experience_list.append({"title": "", "company": "", "duration": "", "description": ""})
        
        if experience_list:
            admin_settings["experience"] = experience_list
    
    # Education
    with st.expander("🎓 Education"):
        education_list = []
        for i, edu in enumerate(admin_settings.get("education", [])):
            st.markdown(f"**Education {i+1}**")
            col_ed1, col_ed2 = st.columns(2)
            with col_ed1:
                edu_degree = st.text_input(f"Degree {i+1}", edu.get("degree", ""), key=f"edu_degree_{i}")
                edu_institution = st.text_input(f"Institution {i+1}", edu.get("institution", ""), key=f"edu_inst_{i}")
            with col_ed2:
                edu_year = st.text_input(f"Year {i+1}", edu.get("year", ""), key=f"edu_year_{i}")
            education_list.append({
                "degree": edu_degree,
                "institution": edu_institution,
                "year": edu_year
            })
        
        if st.button("+ Add Education"):
            education_list.append({"degree": "", "institution": "", "year": ""})
        
        if education_list:
            admin_settings["education"] = education_list
    
    # Resume/PDF Upload
    with st.expander("📄 Resume / Portfolio Upload", expanded=True):
        
        # CSS for 3D resume upload
        st.markdown("""
        <style>
            .resume-upload-zone {
                border: 3px dashed rgba(139, 92, 246, 0.6);
                border-radius: 20px;
                padding: 1.5rem;
                text-align: center;
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
                transition: all 0.3s ease;
                margin-bottom: 1rem;
            }
            .resume-upload-zone:hover {
                border-color: #ec4899;
                transform: scale(1.02);
            }
        </style>
        <div class="resume-upload-zone">
            <h4 style="color: white; margin-bottom: 0.5rem;">📄 Upload Resume / Portfolio</h4>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">PDF, JPG, PNG supported</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            uploaded_resume = st.file_uploader(" ", type=["pdf", "jpg", "jpeg", "png"], label_visibility="collapsed")
            
            if uploaded_resume:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Upload Resume", type="primary", width='stretch'):
                    file_path = save_uploaded_file(uploaded_resume, RESUME_DIR)
                    if file_path:
                        admin_settings["resume_filename"] = uploaded_resume.name
                        save_admin_settings(admin_settings)  # Save to database
                        st.success("✅ Resume uploaded!")
                        st.rerun()
        
        # Reload for current resume display
        current_admin_settings = load_admin_settings()
        
        with col_res2:
            # Show current resume
            current_resume = current_admin_settings.get("resume_filename")
        if current_resume:
            resume_path = os.path.join(RESUME_DIR, current_resume)
            if os.path.exists(resume_path):
                img_base64 = get_image_base64(resume_path)
                if img_base64:
                    ext = current_resume.lower().split('.')[-1]
                    if ext == 'pdf':
                        st.markdown(f"""
                        <div style="text-align: center; margin: 1rem 0; padding: 1rem; background: var(--glass); border-radius: 12px;">
                            <p style="color: rgba(255,255,255,0.8);">📄 Current: {current_resume}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        mime = 'image/jpeg' if ext in ['jpg', 'jpeg'] else f'image/{ext}'
                        st.markdown(f"""
                        <div style="text-align: center; margin: 1rem 0;">
                            <p style="color: rgba(255,255,255,0.7); margin-bottom: 0.5rem;">Current: {current_resume}</p>
                            <img src="data:{mime};base64,{img_base64}" style="max-width: 100%; border-radius: 12px; max-height: 400px;">
                        </div>
                        """, unsafe_allow_html=True)
                
                if st.button("🗑️ Remove Resume"):
                    admin_settings["resume_filename"] = None
                    os.remove(resume_path)
                    st.success("✅ Resume removed!")
                    st.rerun()
    
    # Projects Section
    with st.expander("🚀 Projects (Image & Name)"):
        st.markdown("""
        <style>
        .project-upload-zone {{
            border: 2px dashed rgba(46, 204, 113, 0.5);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            background: linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(39, 174, 96, 0.1));
            margin: 1rem 0;
            transition: all 0.3s ease;
        }}
        .project-upload-zone:hover {{
            border-color: rgba(46, 204, 113, 0.8);
            transform: scale(1.02);
        }}
        </style>
        <div class="project-upload-zone">
            <h4 style="color: white; margin-bottom: 0.5rem;">🚀 Upload Project Image</h4>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">JPG, PNG supported</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current projects
        projects = admin_settings.get('projects', [])
        
        # Show current projects
        if projects:
            st.markdown("<h5 style='color: white; margin-top: 1rem;'>Current Projects:</h5>", unsafe_allow_html=True)
            for i, project in enumerate(projects):
                col_p1, col_p2 = st.columns([3, 1])
                with col_p1:
                    st.markdown(f"**{i+1}. {project.get('name', 'Untitled')}**")
                with col_p2:
                    if st.button(f"🗑️ Remove", key=f"remove_proj_{i}"):
                        projects.pop(i)
                        admin_settings['projects'] = projects
                        save_admin_settings(admin_settings)
                        st.success("✅ Project removed!")
                        st.rerun()
        
        # Add new project
        st.markdown("<h5 style='color: white; margin-top: 1rem;'>Add New Project:</h5>", unsafe_allow_html=True)
        
        col_proj1, col_proj2 = st.columns([2, 1])
        
        with col_proj1:
            new_project_name = st.text_input("Project Name", placeholder="Enter project name", key="new_proj_name")
        
        with col_proj2:
            new_project_image = st.file_uploader("Project Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="new_proj_img")
        
        if new_project_name and new_project_image:
            if st.button("➕ Add Project", type="primary", width='stretch'):
                # Read and encode image
                image_bytes = new_project_image.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                # Add to projects list
                projects.append({
                    "name": new_project_name,
                    "image": image_base64
                })
                
                admin_settings['projects'] = projects
                save_admin_settings(admin_settings)
                st.success("✅ Project added!")
                st.rerun()
        elif new_project_name and not new_project_image:
            st.info("ℹ️ Please upload a project image")
        elif new_project_image and not new_project_name:
            st.info("ℹ️ Please enter a project name")
    
    # Certifications Section
    with st.expander("🏆 Certifications (Image & Name)"):
        st.markdown("""
        <style>
        .cert-upload-zone {{
            border: 2px dashed rgba(241, 196, 15, 0.5);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            background: linear-gradient(135deg, rgba(241, 196, 15, 0.1), rgba(243, 156, 18, 0.1));
            margin: 1rem 0;
            transition: all 0.3s ease;
        }}
        .cert-upload-zone:hover {{
            border-color: rgba(241, 196, 15, 0.8);
            transform: scale(1.02);
        }}
        </style>
        <div class="cert-upload-zone">
            <h4 style="color: white; margin-bottom: 0.5rem;">🏆 Upload Certification Image</h4>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">JPG, PNG supported</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current certifications
        certifications = admin_settings.get('certifications', [])
        
        # Show current certifications
        if certifications:
            st.markdown("<h5 style='color: white; margin-top: 1rem;'>Current Certifications:</h5>", unsafe_allow_html=True)
            for i, cert in enumerate(certifications):
                col_c1, col_c2 = st.columns([3, 1])
                with col_c1:
                    st.markdown(f"**{i+1}. {cert.get('name', 'Untitled')}** - {cert.get('issuer', '')}")
                with col_c2:
                    if st.button(f"🗑️ Remove", key=f"remove_cert_{i}"):
                        certifications.pop(i)
                        admin_settings['certifications'] = certifications
                        save_admin_settings(admin_settings)
                        st.success("✅ Certification removed!")
                        st.rerun()
        
        # Add new certification
        st.markdown("<h5 style='color: white; margin-top: 1rem;'>Add New Certification:</h5>", unsafe_allow_html=True)
        
        col_cert1, col_cert2, col_cert3 = st.columns([2, 2, 1])
        
        with col_cert1:
            new_cert_name = st.text_input("Certification Name", placeholder="Enter certification name", key="new_cert_name")
        
        with col_cert2:
            new_cert_issuer = st.text_input("Issuer (e.g., Coursera, Google)", placeholder="Enter issuer name", key="new_cert_issuer")
        
        with col_cert3:
            new_cert_image = st.file_uploader("Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="new_cert_img")
        
        if new_cert_name and new_cert_issuer and new_cert_image:
            if st.button("➕ Add Certification", type="primary", width='stretch'):
                # Read and encode image
                image_bytes = new_cert_image.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                # Add to certifications list
                certifications.append({
                    "name": new_cert_name,
                    "issuer": new_cert_issuer,
                    "image": image_base64
                })
                
                admin_settings['certifications'] = certifications
                save_admin_settings(admin_settings)
                st.success("✅ Certification added!")
                st.rerun()
        elif (new_cert_name or new_cert_issuer or new_cert_image) and not (new_cert_name and new_cert_issuer and new_cert_image):
            st.info("ℹ️ Please fill in all fields and upload an image")
    
    # Save button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_save1, col_save2 = st.columns([2, 1])
    
    with col_save1:
        if st.button("💾 Save All Changes", width='stretch', type="primary"):
            if save_admin_settings(admin_settings):
                st.success("✅ All changes saved successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to save changes!")
    
    with col_save2:
        if st.button("🔄 Reload Data"):
            # Reload from database
            st.session_state.admin_settings = get_admin_settings()
            st.rerun()
    
    # View users info
    st.markdown("<h3 style='color: white; font-size: 1.8rem; margin: 3rem 0 1.5rem;'>User Inquiries</h3>", unsafe_allow_html=True)
    
    # Try to get from Supabase first
    users_data = []
    conn = get_db_connection()
    
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM user_inquiries ORDER BY created_at DESC")
            users_data = cur.fetchall()
            # Convert to list of dicts
            users_data = [dict(row) for row in users_data]
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error loading from database: {e}")
    
    # Fallback to JSON if no data from database
    if not users_data:
        users_data = load_json(USERS_FILE, [])
    
    if users_data:
        for user in users_data:
            st.markdown(f"""
            <div class="admin-section">
                <h4 style="color: white; margin-bottom: 0.5rem;">{user.get('name', 'Name')}</h4>
                <p style="color: rgba(255,255,255,0.7); margin: 0.2rem 0;">📧 {user.get('email', 'Email')}</p>
                <p style="color: rgba(255,255,255,0.7); margin: 0.2rem 0;">📱 {user.get('phone', 'Phone')}</p>
                <p style="color: #6366f1; margin: 0.2rem 0;">💼 {user.get('service', 'Service')}</p>
                <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 0.5rem;">🕐 {user.get('timestamp', '')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No user inquiries yet.")

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application"""
    
    # Render 3D background
    render_3d_background()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h3 class="gradient-text">Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content with tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🏠 Home", 
        "💼 Services", 
        "🚀 Projects",
        "🏆 Certifications",
        "📩 Inquire", 
        "🤖 AI Chat", 
        "📄 Resume",
        "👑 Admin"
    ])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        render_profile_section()
        
        # About section - loaded from admin settings
        current_home_settings = get_admin_settings()
        
        # Show About Me only if there's text
        about_text = current_home_settings.get('about', '')
        if about_text:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<h2 class='gradient-text' style='font-size: 2rem; margin-bottom: 1.5rem;'>About Me</h2>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card">
                <p style="color: rgba(255,255,255,0.8); line-height: 1.8; font-size: 1.1rem;">
                    {about_text}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        render_services_section()
    
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        render_projects_section()
    
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        render_certifications_section()
    
    with tab5:
        st.markdown("<br>", unsafe_allow_html=True)
        render_inquire_section()
    
    with tab6:
        st.markdown("<br>", unsafe_allow_html=True)
        render_chatbot_section()
    
    with tab7:
        st.markdown("<br>", unsafe_allow_html=True)
        render_resume_section()
    
    with tab8:
        st.markdown("<br>", unsafe_allow_html=True)
        render_admin_panel()
    
    # Footer
    st.markdown("---")
    
    # Always get fresh settings
    current_footer_settings = get_admin_settings()
    footer_name = current_footer_settings.get('name', 'Aryan Chavan')
    
    st.markdown(
        '<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.5);">' +
        '<p>2026 ' + footer_name + '. All rights reserved.</p>' +
        '<p>Built by ' + footer_name + ' | Powered by AI</p>' +
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
