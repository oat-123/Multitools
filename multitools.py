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

# ===== ฟังก์ชันสำหรับ Hi-Tech Login CSS =====
def load_hitech_css():
    st.markdown("""
    <style>
    /* Import Futuristic Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    body, .stApp {
        background: #000 !important;
        min-height: 100vh;
        font-family: 'Rajdhani', sans-serif;
        overflow-x: hidden;
    }
    
    /* Animated Space Background */
    .space-background {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -2;
        background: 
            radial-gradient(ellipse at center, #001122 0%, #000000 70%),
            linear-gradient(45deg, #000011 0%, #000033 50%, #000000 100%);
    }
    
    /* Animated Stars */
    .space-background::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.8), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(74,144,226,0.6), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.9), transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(74,144,226,0.4), transparent),
            radial-gradient(2px 2px at 160px 30px, rgba(255,255,255,0.7), transparent),
            radial-gradient(1px 1px at 200px 120px, rgba(74,144,226,0.5), transparent);
        background-repeat: repeat;
        background-size: 250px 150px;
        animation: starfield 25s linear infinite;
        opacity: 0.8;
    }
    
    /* Floating Particles */
    .space-background::after {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(1px 1px at 50px 100px, rgba(74,144,226,0.3), transparent),
            radial-gradient(1px 1px at 150px 200px, rgba(255,255,255,0.2), transparent),
            radial-gradient(1px 1px at 300px 50px, rgba(74,144,226,0.4), transparent);
        background-repeat: repeat;
        background-size: 400px 300px;
        animation: particles 30s linear infinite reverse;
        opacity: 0.6;
    }
    
    @keyframes starfield {
        from { transform: translateX(0) translateY(0); }
        to { transform: translateX(-250px) translateY(-150px); }
    }
    
    @keyframes particles {
        from { transform: translateX(0) translateY(0) rotate(0deg); }
        to { transform: translateX(400px) translateY(300px) rotate(360deg); }
    }
    
    /* Login Container */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        padding: 2rem;
        position: relative;
    }
    
    /* Holographic Grid Background */
    .login-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(74,144,226,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(74,144,226,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: grid-move 20s linear infinite;
        opacity: 0.3;
        z-index: -1;
    }
    
    @keyframes grid-move {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }
    
    /* Hi-Tech Login Card */
    .login-card {
        background: 
            linear-gradient(135deg, rgba(10,15,25,0.95) 0%, rgba(15,25,40,0.9) 100%),
            radial-gradient(circle at 50% 0%, rgba(74,144,226,0.1) 0%, transparent 50%);
        border: 2px solid transparent;
        border-radius: 20px;
        box-shadow: 
            0 0 50px rgba(74,144,226,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1),
            inset 0 -1px 0 rgba(0,0,0,0.5);
        padding: 3rem 2.5rem;
        max-width: 450px;
        width: 100%;
        position: relative;
        backdrop-filter: blur(20px);
        animation: card-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes card-glow {
        0% { 
            box-shadow: 
                0 0 30px rgba(74,144,226,0.2),
                inset 0 1px 0 rgba(255,255,255,0.1);
        }
        100% { 
            box-shadow: 
                0 0 60px rgba(74,144,226,0.4),
                0 0 100px rgba(74,144,226,0.1),
                inset 0 1px 0 rgba(255,255,255,0.2);
        }
    }
    
    /* Animated Border */
    .login-card::before {
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        background: linear-gradient(45deg, 
            #4A90E2, #357ABD, #4A90E2, #357ABD, 
            #4A90E2, #357ABD, #4A90E2, #357ABD);
        background-size: 400% 400%;
        border-radius: 20px;
        z-index: -1;
        animation: border-animation 4s ease infinite;
    }
    
    @keyframes border-animation {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Logo Section */
    .login-logo {
        text-align: center;
        margin-bottom: 2.5rem;
        position: relative;
    }
    
    .login-avatar {
        width: 100px;
        height: 100px;
        background: 
            linear-gradient(135deg, #4A90E2 0%, #357ABD 50%, #2E5F8A 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem auto;
        font-size: 3rem;
        position: relative;
        animation: logo-pulse 2s ease-in-out infinite;
        box-shadow: 
            0 0 30px rgba(74,144,226,0.5),
            inset 0 2px 10px rgba(255,255,255,0.2);
    }
    
    @keyframes logo-pulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 30px rgba(74,144,226,0.5);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 0 50px rgba(74,144,226,0.8);
        }
    }
    
    /* Holographic Ring */
    .login-avatar::before {
        content: '';
        position: absolute;
        top: -10px; left: -10px; right: -10px; bottom: -10px;
        border: 2px solid rgba(74,144,226,0.3);
        border-radius: 50%;
        animation: ring-rotate 8s linear infinite;
    }
    
    .login-avatar::after {
        content: '';
        position: absolute;
        top: -20px; left: -20px; right: -20px; bottom: -20px;
        border: 1px solid rgba(74,144,226,0.2);
        border-radius: 50%;
        animation: ring-rotate 12s linear infinite reverse;
    }
    
    @keyframes ring-rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Typography */
    .login-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-shadow: 
            0 0 10px rgba(74,144,226,0.5),
            0 0 20px rgba(74,144,226,0.3),
            0 0 30px rgba(74,144,226,0.1);
        animation: title-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes title-glow {
        0% { 
            text-shadow: 
                0 0 10px rgba(74,144,226,0.5),
                0 0 20px rgba(74,144,226,0.3);
        }
        100% { 
            text-shadow: 
                0 0 20px rgba(74,144,226,0.8),
                0 0 30px rgba(74,144,226,0.5),
                0 0 40px rgba(74,144,226,0.2);
        }
    }
    
    .login-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        font-weight: 500;
        color: rgba(74,144,226,0.8);
        margin-bottom: 2rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextInput input {
        background: 
            linear-gradient(135deg, rgba(15,25,40,0.8) 0%, rgba(10,15,25,0.9) 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(74,144,226,0.3) !important;
        border-radius: 12px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 1rem 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            inset 0 2px 10px rgba(0,0,0,0.3),
            0 0 0 rgba(74,144,226,0) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextInput input:focus {
        border: 2px solid rgba(74,144,226,0.8) !important;
        outline: none !important;
        box-shadow: 
            inset 0 2px 10px rgba(0,0,0,0.3),
            0 0 20px rgba(74,144,226,0.3) !important;
        background: 
            linear-gradient(135deg, rgba(15,25,40,0.9) 0%, rgba(20,30,45,0.9) 100%) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.5) !important;
        font-style: italic;
    }
    
    /* Labels */
    .stTextInput label {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Hi-Tech Button */
    .stButton > button {
        background: 
            linear-gradient(135deg, #4A90E2 0%, #357ABD 50%, #2E5F8A 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(74,144,226,0.5) !important;
        border-radius: 12px !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 1rem 2rem !important;
        margin-top: 1.5rem !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 0 20px rgba(74,144,226,0.3),
            inset 0 1px 0 rgba(255,255,255,0.2) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,255,255,0.2), 
            transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: 
            linear-gradient(135deg, #357ABD 0%, #4A90E2 50%, #5BA0F2 100%) !important;
        border-color: rgba(74,144,226,0.8) !important;
        box-shadow: 
            0 0 30px rgba(74,144,226,0.5),
            0 0 50px rgba(74,144,226,0.2),
            inset 0 1px 0 rgba(255,255,255,0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Error Messages */
    .stError {
        background: 
            linear-gradient(135deg, rgba(220,38,38,0.2) 0%, rgba(185,28,28,0.1) 100%) !important;
        border: 1px solid rgba(220,38,38,0.5) !important;
        border-radius: 10px !important;
        color: #ff6b6b !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
        animation: error-pulse 0.5s ease-in-out;
    }
    
    @keyframes error-pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Success Messages */
    .stSuccess {
        background: 
            linear-gradient(135deg, rgba(34,197,94,0.2) 0%, rgba(22,163,74,0.1) 100%) !important;
        border: 1px solid rgba(34,197,94,0.5) !important;
        border-radius: 10px !important;
        color: #4ade80 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Loading Animation */
    .login-loading {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
    }
    
    .loading-spinner {
        width: 30px;
        height: 30px;
        border: 3px solid rgba(74,144,226,0.3);
        border-top: 3px solid #4A90E2;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .login-card {
            margin: 1rem;
            padding: 2rem 1.5rem;
        }
        
        .login-title {
            font-size: 2.2rem;
        }
        
        .login-avatar {
            width: 80px;
            height: 80px;
            font-size: 2.5rem;
        }
        
        .login-subtitle {
            font-size: 1.1rem;
        }
    }
    
    @media (max-width: 480px) {
        .login-container {
            padding: 1rem;
        }
        
        .login-card {
            padding: 1.5rem 1rem;
        }
        
        .login-title {
            font-size: 1.8rem;
        }
        
        .login-avatar {
            width: 70px;
            height: 70px;
            font-size: 2rem;
        }
    }
    
    /* Dashboard Styles (keeping existing) */
    .spacex-header {
        display: flex; align-items: center; justify-content: space-between;
        background: rgba(20, 24, 32, 0.92);
        border-radius: 18px;
        margin: 2rem 0 2rem 0;
        padding: 1.2rem 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.18);
    }
    .spacex-logo {
        display: flex; align-items: center;
        gap: 1rem;
    }
    .spacex-logo h1 {
        color: #fff;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.12em;
    }
    .spacex-nav {
        display: flex; gap: 1.2rem;
    }
    .spacex-nav-item {
        background: none;
        color: #bfc9d1;
        border: none;
        font-size: 1.1rem;
        font-weight: 500;
        padding: 0.5em 1.2em;
        border-radius: 8px;
        transition: background 0.2s, color 0.2s;
        cursor: pointer;
    }
    .spacex-nav-item.active, .spacex-nav-item:hover {
        background: #232733;
        color: #4A90E2;
    }
    .user-profile {
        display: flex; align-items: center; gap: 0.7rem;
        background: #181c24;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        color: #fff;
    }
    .user-avatar {
        width: 36px; height: 36px; background: #4A90E2; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700;
    }
    .user-info h4 {
        margin: 0; color: #fff; font-size: 1.1rem; font-weight: 600;
    }
    .user-info p {
        margin: 0; color: #bfc9d1; font-size: 0.95rem;
    }
    .hero-section {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 45vh;
        margin-top: 2rem;
    }
    .hero-title {
        color: #fff;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    .hero-subtitle {
        color: #4A90E2;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    .hero-description {
        color: #bfc9d1;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-button {
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.7em 2em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: background 0.2s, color 0.2s;
        cursor: pointer;
    }
    .hero-button:hover {
        background: linear-gradient(90deg, #357ABD 0%, #4A90E2 100%);
        color: #fff;
    }
    .stats-section {
        margin: 2rem 0 0 0;
        display: flex; justify-content: center;
    }
    .stats-grid {
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem;
    }
    .stat-item {
        background: rgba(20, 24, 32, 0.92);
        border-radius: 14px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
        padding: 1.5rem 1rem;
        color: #fff;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #4A90E2;
        margin-bottom: 0.3rem;
    }
    .stat-label {
        font-size: 1.05rem;
        color: #bfc9d1;
    }
    @media (max-width: 900px) {
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
        .spacex-header { flex-direction: column; gap: 1.2rem; padding: 1rem 0.5rem; }
        .stats-grid { grid-template-columns: 1fr; }
        .hero-title { font-size: 1.5rem; }
        .hero-subtitle { font-size: 1.1rem; }
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
            <div class="login-logo">
                <div class="login-avatar">🛡️</div>
                <h1 class="login-title">J.A.R.V.I.S</h1>
                <p class="login-subtitle">Military Assistance System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form with better spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### 🔐 เข้าสู่ระบบ")
            
            username = st.text_input(
                "ชื่อผู้ใช้", 
                placeholder="กรอกชื่อผู้ใช้งาน...",
                help="ใช้ชื่อผู้ใช้ที่ได้รับจากระบบ"
            )
            
            password = st.text_input(
                "รหัสผ่าน", 
                type="password", 
                placeholder="กรอกรหัสผ่าน...",
                help="รหัสผ่านที่ได้รับจากผู้ดูแลระบบ"
            )
            
            # Add some spacing
            st.markdown("<br>", unsafe_allow_html=True)
            
            login_button = st.form_submit_button(
                "🚀 เข้าสู่ระบบ", 
                use_container_width=True
            )
            
            if login_button:
                if username and password:  # Check if fields are not empty
                    # Add loading effect
                    with st.spinner('กำลังตรวจสอบข้อมูล...'):
                        time.sleep(1)  # Simulate processing time
                        
                        if username in users and users[username]["password"] == password:
                            st.success("✅ เข้าสู่ระบบสำเร็จ!")
                            time.sleep(0.5)
                            
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.session_state["user_data"] = users[username]
                            st.session_state["current_page"] = "dashboard"
                            st.rerun()
                        else:
                            st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                else:
                    st.warning("⚠️ กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
        
        # Add system info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem;">
            <p>🔒 ระบบรักษาความปลอดภัยระดับสูง</p>
            <p>💻 รองรับทุกอุปกรณ์</p>
            <p>⚡ ประมวลผลด้วย AI</p>
        </div>
        """, unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับการแสดง Dashboard =====
def show_dashboard():
    st.markdown('<div class="space-background"></div>', unsafe_allow_html=True)
    current_page = st.session_state.get("current_page", "dashboard")
    nav_items = [
        ("dashboard", "หน้าหลัก"),
        ("night_duty", "เวรรักษาการณ์"),
        ("weekend_duty", "เวรเตรียมการ"),
        ("ceremony_duty", "จัดยอดพิธี"),
        ("home", "ยอดปล่อย"),
        ("count", "สถิติโดนยอด")
    ]
    st.markdown(f"""
    <div class="spacex-header">
        <div class="spacex-logo">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #4A90E2, #357ABD); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">🛡️</div>
            <h1>J.A.R.V.I.S</h1>
        </div>
        <div class="spacex-nav">
            {' '.join([f'<button class="spacex-nav-item {"active" if current_page == page_id else ""}" onclick="window.location.reload()">{title}</button>' for page_id, title in nav_items[1:]])}
        </div>
        <div class="user-profile">
            <div class="user-avatar">{st.session_state['username'][0].upper()}</div>
            <div class="user-info">
                <h4>{st.session_state['user_data']['display_name']}</h4>
                <p>{st.session_state['user_data']['sheet_name']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">THE FUTURE OF</h1>
        <h2 class="hero-subtitle">MILITARY ASSISTANCE</h2>
        <p class="hero-description">
            ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1 <br>ด้วยเทคโนโลยีที่ทันสมัยและใช้งานง่าย
        </p>
        <button class="hero-button" onclick="document.querySelector('[data-testid=\\"stSidebar\\"]')?.click()">เริ่มใช้งาน</button>
    </div>
    """, unsafe_allow_html=True)
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
    load_hitech_css()
    
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
