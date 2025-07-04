import streamlit as st
import pandas as pd
import random
from collections import defaultdict
from datetime import date
import time
import gspread
from google.oauth2 import service_account
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===== การตั้งค่าหน้าเว็บ =====
st.set_page_config(
    page_title="J.A.R.V.I.S - ระบบผู้ช่วย ฝอ.1",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== ข้อมูลผู้ใช้ =====
users = {
    "oat": {"password": "crma74", "sheet_name": "ชั้น4_พัน4", "display_name": "ผู้ใช้ OAT", "role": "ผู้ดูแลระบบ"},
    "time": {"password": "crma74", "sheet_name": "ชั้น4_พัน1", "display_name": "ผู้ใช้ TIME", "role": "ผู้ใช้งาน"},
    "chai": {"password": "crma74", "sheet_name": "ชั้น4_พัน3", "display_name": "ผู้ใช้ CHAI", "role": "ผู้ใช้งาน"}
}

# ===== ฟังก์ชันสำหรับ SpaceX Style CSS =====
def load_spacex_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles - SpaceX Theme */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #000000;
        color: #ffffff;
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Space Background with Stars */
    .space-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #000000 0%, #0a0a23 50%, #000000 100%);
        z-index: -2;
    }
    
    .space-background::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #ffffff, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #ffffff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ffffff, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 20s linear infinite;
        opacity: 0.6;
    }
    
    @keyframes sparkle {
        from { transform: translateX(0); }
        to { transform: translateX(200px); }
    }
    
    /* SpaceX Header Navigation */
    .spacex-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
    }
    
    .spacex-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .spacex-logo h1 {
        font-size: 1.8rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.2em;
    }
    
    .spacex-nav {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .spacex-nav-item {
        color: #ffffff;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        background: transparent;
    }
    
    .spacex-nav-item:hover {
        color: #4A90E2;
        background: rgba(74, 144, 226, 0.1);
    }
    
    .spacex-nav-item.active {
        color: #4A90E2;
        background: rgba(74, 144, 226, 0.2);
    }
    
    /* Mobile Navigation */
    .mobile-nav-toggle {
        display: none;
        background: transparent;
        border: 2px solid #ffffff;
        color: #ffffff;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    @media (max-width: 768px) {
        .spacex-nav {
            display: none;
        }
        .mobile-nav-toggle {
            display: block;
        }
    }
    
    /* Hero Section */
    .hero-section {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        position: relative;
    }
    
    .hero-title {
        font-size: clamp(3rem, 8vw, 8rem);
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 2rem;
        letter-spacing: 0.02em;
        line-height: 0.9;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .hero-subtitle {
        font-size: clamp(1.2rem, 3vw, 2rem);
        color: #4A90E2;
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    
    .hero-description {
        font-size: clamp(1rem, 2vw, 1.3rem);
        color: rgba(255, 255, 255, 0.8);
        max-width: 800px;
        margin: 0 auto 3rem auto;
        line-height: 1.6;
    }
    
    .hero-button {
        background: transparent;
        border: 2px solid #ffffff;
        color: #ffffff;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .hero-button:hover {
        background: #ffffff;
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(255,255,255,0.2);
    }
    
    /* Login Card - SpaceX Style */
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
                    url('https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    .login-card {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0;
        padding: 3rem;
        max-width: 400px;
        width: 100%;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 0.1em;
    }
    
    .login-subtitle {
        font-size: 1rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* Stats Section */
    .stats-section {
        background: #000000;
        padding: 5rem 2rem;
        text-align: center;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 4rem;
        font-weight: 900;
        color: #4A90E2;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    /* Module Content */
    .module-container {
        padding: 6rem 2rem 2rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .module-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .back-button {
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #ffffff;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    
    .back-button:hover {
        border-color: #4A90E2;
        color: #4A90E2;
    }
    
    .module-badge {
        background: rgba(74, 144, 226, 0.2);
        color: #4A90E2;
        padding: 0.5rem 1rem;
        border: 1px solid #4A90E2;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .module-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0;
        padding: 3rem;
        text-align: center;
    }
    
    .module-icon {
        width: 80px;
        height: 80px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 2rem auto;
        font-size: 2rem;
    }
    
    .module-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .module-description {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .module-button {
        background: transparent;
        border: 2px solid #4A90E2;
        color: #4A90E2;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .module-button:hover {
        background: #4A90E2;
        color: #ffffff;
    }
    
    /* User Profile */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: #ffffff;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        background: #4A90E2;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .user-info h4 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .user-info p {
        margin: 0;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .spacex-header {
            padding: 0 1rem;
        }
        
        .hero-section {
            padding: 1rem;
        }
        
        .login-card {
            margin: 1rem;
            padding: 2rem;
        }
        
        .module-container {
            padding: 6rem 1rem 2rem 1rem;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
        }
        
        .stat-number {
            font-size: 3rem;
        }
    }
    
    /* Streamlit Specific Overrides */
    .stButton > button {
        background: transparent !important;
        border: 2px solid #ffffff !important;
        color: #ffffff !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        border-radius: 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #ffffff !important;
        color: #000000 !important;
        border-color: #ffffff !important;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: #ffffff !important;
        border-radius: 0 !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
    }
    
    .stTextInput label,
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.2) !important;
        border: 1px solid #22c55e !important;
        color: #22c55e !important;
        border-radius: 0 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.2) !important;
        border: 1px solid #ef4444 !important;
        color: #ef4444 !important;
        border-radius: 0 !important;
    }
    
    .stInfo {
        background: rgba(74, 144, 226, 0.2) !important;
        border: 1px solid #4A90E2 !important;
        color: #4A90E2 !important;
        border-radius: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับการเชื่อมต่อ Google Sheets =====
@st.cache_resource
def connect_gsheet(sheet_name: str):
    try:
        creds_dict = st.secrets["gcp_service_account"]
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/1PfZdCw2iL65CPTZzNsCnkhF7EVJNFZHRvYAXqeOJsSk/edit?usp=drivesdk"
        )
        worksheet = sheet.worksheet(sheet_name)
        return worksheet
    except:
        return None

# ===== ฟังก์ชันสำหรับการแสดงหน้า Login =====
def show_login_page():
    st.markdown('<div class="space-background"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #4A90E2, #357ABD); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 2rem;">
                    🛡️
                </div>
                <h1 class="login-title">J.A.R.V.I.S</h1>
                <p class="login-subtitle">ระบบผู้ช่วย ฝอ.1</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("### เข้าสู่ระบบ")
            username = st.text_input("ชื่อผู้ใช้", placeholder="กรอกชื่อผู้ใช้")
            password = st.text_input("รหัสผ่าน", type="password", placeholder="กรอกรหัสผ่าน")
            
            login_button = st.form_submit_button("เข้าสู่ระบบ", use_container_width=True)
            
            if login_button:
                if username in users and users[username]["password"] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["user_data"] = users[username]
                    st.rerun()
                else:
                    st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

# ===== ฟังก์ชันสำหรับการแสดง Dashboard =====
def show_dashboard():
    st.markdown('<div class="space-background"></div>', unsafe_allow_html=True)
    
    # SpaceX Header Navigation
    current_page = st.session_state.get("current_page", "dashboard")
    
    # Create navigation buttons
    nav_items = [
        ("dashboard", "หน้าหลัก"),
        ("night_duty", "เวรรักษาการณ์"),
        ("weekend_duty", "เวรเตรียมการ"),
        ("ceremony_duty", "จัดยอดพิธี"),
        ("home", "ยอดปล่อย"),
        ("count", "สถิติโดนยอด")
    ]
    
    # Header
    st.markdown(f"""
    <div class="spacex-header">
        <div class="spacex-logo">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #4A90E2, #357ABD); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                🛡️
            </div>
            <h1>J.A.R.V.I.S</h1>
        </div>
        
        <div class="spacex-nav">
            {' '.join([f'<button class="spacex-nav-item {"active" if current_page == page_id else ""}" onclick="window.location.reload()">{title}</button>' for page_id, title in nav_items[1:]])}
        </div>
        
        <div class="user-profile">
            <div class="user-avatar">{st.session_state["username"][0].upper()}</div>
            <div class="user-info">
                <h4>{st.session_state["user_data"]["display_name"]}</h4>
                <p>{st.session_state["user_data"]["sheet_name"]}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile Navigation
    with st.sidebar:
        st.markdown("### 🛡️ J.A.R.V.I.S")
        st.markdown(f"**{st.session_state['user_data']['display_name']}**")
        st.markdown(f"*{st.session_state['user_data']['sheet_name']}*")
        st.markdown("---")
        
        for page_id, title in nav_items:
            if st.button(title, key=f"mobile_{page_id}", use_container_width=True):
                st.session_state["current_page"] = page_id
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 ออกจากระบบ", key="mobile_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Desktop Navigation Buttons
    col_nav = st.columns(len(nav_items[1:]))
    for i, (page_id, title) in enumerate(nav_items[1:]):
        with col_nav[i]:
            if st.button(title, key=f"desktop_{page_id}"):
                st.session_state["current_page"] = page_id
                st.rerun()
    
    # Logout button
    col_logout1, col_logout2 = st.columns([10, 1])
    with col_logout2:
        if st.button("🚪", key="desktop_logout", help="ออกจากระบบ"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    if current_page == "dashboard":
        # Hero Section
        st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">THE FUTURE OF</h1>
            <h2 class="hero-subtitle">MILITARY ASSISTANCE</h2>
            <p class="hero-description">
                ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1 
                ด้วยเทคโนโลยีที่ทันสมัยและใช้งานง่าย
            </p>
            <button class="hero-button" onclick="document.querySelector('[data-testid=\\"stSidebar\\"]').click()">
                เริ่มใช้งาน
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats Section
        st.markdown("""
        <div class="stats-section">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">150+</div>
                    <div class="stat-label">นักเรียนนายร้อย</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">ระบบพร้อมใช้งาน</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">5</div>
                    <div class="stat-label">ฟังก์ชันหลัก</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">99%</div>
                    <div class="stat-label">ความแม่นยำ</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับหน้าต่างๆ =====
def show_module_page(module_name, icon, description):
    st.markdown('<div class="space-background"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="module-container">
        <div class="module-header">
            <button class="back-button" onclick="window.location.reload()">← กลับหน้าหลัก</button>
            <div class="module-badge">{module_name}</div>
        </div>
        
        <div class="module-card">
            <div class="module-icon">{icon}</div>
            <h2 class="module-title">{module_name}</h2>
            <p class="module-description">{description}</p>
            <button class="module-button">เชื่อมต่อระบบเดิม</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← กลับหน้าหลัก", key="back_to_dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

def show_night_duty_page():
    show_module_page(
        "เวรรักษาการณ์", 
        "🛡️", 
        "จัดการและดูข้อมูลเวรยืนกลางคืน ระบบตรวจสอบตลอด 24 ชั่วโมง"
    )

def show_weekend_duty_page():
    show_module_page(
        "เวรเตรียมการ", 
        "📅", 
        "จัดการเวรเสาร์-อาทิตย์และวันหยุดราชการ"
    )

def show_ceremony_duty_page():
    show_module_page(
        "จัดยอดพิธี", 
        "🏅", 
        "สุ่มและจัดยอดสำหรับงานพิธีต่างๆ อัตโนมัติ"
    )

def show_home_page():
    show_module_page(
        "ยอดปล่อย", 
        "📝", 
        "พิมพ์และจัดทำรายงานยอดปล่อยประจำวัน"
    )

def show_count_page():
    show_module_page(
        "สถิติโดนยอด", 
        "📊", 
        "อัพเดตและตรวจสอบสถิติการโดนยอด"
    )

# ===== Main Application =====
def main():
    load_spacex_css()
    
    # ตรวจสอบสถานะการล็อกอิน
    if not st.session_state.get("logged_in", False):
        show_login_page()
        return
    
    # กำหนดหน้าปัจจุบัน
    current_page = st.session_state.get("current_page", "dashboard")
    
    # แสดงหน้าตามที่เลือก
    if current_page == "dashboard":
        show_dashboard()
    elif current_page == "night_duty":
        show_night_duty_page()
    elif current_page == "weekend_duty":
        show_weekend_duty_page()
    elif current_page == "home":
        show_home_page()
    elif current_page == "count":
        show_count_page()
    elif current_page == "ceremony_duty":
        show_ceremony_duty_page()
    
    # Footer
    st.markdown("""
    <div style="
        background: #000000;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        text-align: center;
        margin-top: 4rem;
    ">
        <p style="color: rgba(255, 255, 255, 0.7); margin: 0; letter-spacing: 0.05em;">
            J.A.R.V.I.S © 2025 | พัฒนาโดย Oat | ระบบผู้ช่วยอัจฉริยะ ฝอ.1
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
