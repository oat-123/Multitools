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
    body, .stApp {
        background: #000 !important;
        min-height: 100vh;
    }
    .space-background {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        background: url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=1500&q=80') center center/cover no-repeat;
        filter: brightness(0.5);
    }
    .login-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 100vh;
    }
    .login-card {
        background: rgba(20, 24, 32, 0.92);
        border-radius: 18px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        max-width: 400px;
        margin: 2rem auto 0 auto;
        color: #fff;
        text-align: center;
        border: 1.5px solid #222b3a;
    }
    .login-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #4A90E2;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        font-size: 1.1rem;
        color: #bfc9d1;
        margin-bottom: 1.5rem;
    }
    .stTextInput>div>div>input, .stTextInput input, .stPasswordInput input {
        background: #181c24 !important;
        color: #fff !important;
        border-radius: 10px;
        border: 1.5px solid #2d3440;
        font-size: 1.1rem;
        padding: 0.7rem 1rem;
    }
    .stTextInput>div>div>input:focus, .stPasswordInput input:focus {
        border: 1.5px solid #4A90E2;
        outline: none;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.7em 1.5em;
        margin-top: 1.2em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: background 0.2s, color 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #357ABD 0%, #4A90E2 100%);
        color: #fff;
    }
    /* Dashboard */
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
        .login-card { padding: 1.2rem 0.5rem; }
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
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.markdown('<div style="width: 80px; height: 80px; background: linear-gradient(135deg, #4A90E2, #357ABD); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; font-size: 2rem;">🛡️</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">J.A.R.V.I.S</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">ระบบผู้ช่วย ฝอ.1</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("ชื่อผู้ใช้", placeholder="กรอกชื่อผู้ใช้")
        password = st.text_input("รหัสผ่าน", type="password", placeholder="กรอกรหัสผ่าน")
        login_button = st.form_submit_button("เข้าสู่ระบบ")
        if login_button:
            if username in users and users[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["user_data"] = users[username]
                st.session_state["current_page"] = "dashboard"
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
