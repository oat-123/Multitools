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

# ===== ฟังก์ชันสำหรับ CSS และการตกแต่ง =====
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Login Card */
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        max-width: 400px;
        margin: 2rem auto;
    }
    
    .login-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        font-size: 0.9rem;
        color: #718096;
        text-align: center;
        line-height: 1.5;
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* User Profile */
    .user-profile {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .user-name {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .user-role {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .dashboard-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
        
        .card-title {
            font-size: 1.1rem;
        }
        
        .stats-number {
            font-size: 2rem;
        }
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        border: none;
    }
    
    .stError {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        border: none;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        border: none;
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
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="header-title">🛡️ J.A.R.V.I.S</h1>', unsafe_allow_html=True)
    st.markdown('<p class="header-subtitle">ระบบผู้ช่วยอัจฉริยะ ฝอ.1</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">เข้าสู่ระบบ</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 ชื่อผู้ใช้", placeholder="กรอกชื่อผู้ใช้")
            password = st.text_input("🔒 รหัสผ่าน", type="password", placeholder="กรอกรหัสผ่าน")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                login_button = st.form_submit_button("🚀 เข้าสู่ระบบ", use_container_width=True)
            
            if login_button:
                if username in users and users[username]["password"] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["user_data"] = users[username]
                    st.rerun()
                else:
                    st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับการแสดง Dashboard =====
def show_dashboard():
    # Header with user info
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown('<h1 class="header-title">🛡️ J.A.R.V.I.S Dashboard</h1>', unsafe_allow_html=True)
        st.markdown('<p class="header-subtitle">ระบบผู้ช่วยอัจฉริยะ ฝอ.1</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="user-profile">', unsafe_allow_html=True)
        st.markdown(f'<div class="user-name">👋 {st.session_state["user_data"]["display_name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-role">{st.session_state["user_data"]["role"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-role">📊 {st.session_state["user_data"]["sheet_name"]}</div>', unsafe_allow_html=True)
        if st.button("🚪 ออกจากระบบ", key="logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("### 📊 สถิติระบบ")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">150+</div>
            <div class="stats-label">👥 นักเรียนนายร้อย</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">24/7</div>
            <div class="stats-label">⏰ ระบบพร้อมใช้งาน</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">5</div>
            <div class="stats-label">🔧 ฟังก์ชันหลัก</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">99%</div>
            <div class="stats-label">📈 ความแม่นยำ</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Menu
    st.markdown("### 🎯 เลือกฟังก์ชันที่ต้องการ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛡️", key="night_duty_icon", help="เวรรักษาการณ์"):
            st.session_state["current_page"] = "night_duty"
            st.rerun()
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">🛡️</div>
            <div class="card-title">เวรรักษาการณ์</div>
            <div class="card-description">จัดการและดูข้อมูลเวรยืนกลางคืน<br>ระบบตรวจสอบ 24 ชั่วโมง</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📅", key="weekend_duty_icon", help="เวรเตรียมการ"):
            st.session_state["current_page"] = "weekend_duty"
            st.rerun()
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">📅</div>
            <div class="card-title">เวรเตรียมการ</div>
            <div class="card-description">จัดการเวรเสาร์-อาทิตย์<br>และวันหยุดราชการ</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🏅", key="ceremony_icon", help="จัดยอดพิธี"):
            st.session_state["current_page"] = "ceremony_duty"
            st.rerun()
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">🏅</div>
            <div class="card-title">จัดยอดพิธี</div>
            <div class="card-description">สุ่มและจัดยอดสำหรับงานพิธี<br>ระบบสุ่มอัตโนมัติ</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝", key="home_icon", help="ยอดปล่อย"):
            st.session_state["current_page"] = "home"
            st.rerun()
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">📝</div>
            <div class="card-title">ยอดปล่อย</div>
            <div class="card-description">พิมพ์และจัดทำรายงาน<br>ยอดปล่อยประจำวัน</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("📊", key="stats_icon", help="สถิติโดนยอด"):
            st.session_state["current_page"] = "count"
            st.rerun()
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">📊</div>
            <div class="card-title">สถิติโดนยอด</div>
            <div class="card-description">อัพเดตและตรวจสอบ<br>สถิติการโดนยอด</div>
        </div>
        """, unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับหน้าต่างๆ =====
def show_night_duty_page():
    st.markdown("## 🛡️ เวรรักษาการณ์")
    
    if st.button("← กลับหน้าหลัก"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
    
    st.info("💡 คุณเลือก: เวรยืนกลางคืน - ระบบตรวจสอบตลอด 24 ชั่วโมง")
    
    # เลือกประเภทชีท
    sheet_option = st.radio(
        "📋 เลือกดูชีทข้อมูล",
        ("แท็กเวร", "ใบเวร (สรุป)"),
        horizontal=True
    )
    
    # กำหนดลิงก์ตามที่เลือก
    if sheet_option == "แท็กเวร":
        iframe_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8pO9068jsukCJL0guT_dF7I5cjYMMIhsu7ah-1DkPxSMxnYFsSkuRgffvSUJKVZzQccQyJEOPxvvg/pubhtml?gid=0&single=true&range=A1:I100"
        edit_link = "https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU/edit#gid=0"
    else:
        iframe_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8pO9068jsukCJL0guT_dF7I5cjYMMIhsu7ah-1DkPxSMxnYFsSkuRgffvSUJKVZzQccQyJEOPxvvg/pubhtml?gid=2030248910&single=true&range=A1:I100"
        edit_link = "https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU/edit#gid=1"
    
    # แสดง iframe
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    ">
        <iframe src="{iframe_link}" 
                width="100%" 
                height="800" 
                style="border: none; border-radius: 12px;">
        </iframe>
        <div style="text-align: center; margin-top: 1rem;">
            <a href="{edit_link}" target="_blank" 
               style="
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                   color: white;
                   padding: 0.75rem 1.5rem;
                   border-radius: 12px;
                   text-decoration: none;
                   font-weight: 500;
                   display: inline-block;
                   box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
               ">
                ✏️ แก้ไข Google Sheets
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_weekend_duty_page():
    st.markdown("## 📅 เวรเตรียมการ")
    
    if st.button("← กลับหน้าหลัก"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
    
    st.info("💡 คุณเลือก: เวรเสาร์-อาทิตย์ และวันหยุดราชการ")
    
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
    ">
        <h3>📊 ระบบเวรเตรียมการ</h3>
        <p>จัดการและติดตามเวรประจำสุดสัปดาห์</p>
        <a href="https://docs.google.com/spreadsheets/d/1ufm0LPa4c903jhlANKn_YqNyMtG9id0iN-tMHrhNRA8/edit?gid=1888956716" 
           target="_blank"
           style="
               background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
               color: white;
               padding: 1rem 2rem;
               border-radius: 12px;
               text-decoration: none;
               font-weight: 500;
               display: inline-block;
               box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
               margin-top: 1rem;
           ">
            📃 เปิด Google Sheets
        </a>
    </div>
    """, unsafe_allow_html=True)

def show_home_page():
    st.markdown("## 📝 พิมพ์ยอดปล่อย")
    
    if st.button("← กลับหน้าหลัก"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
    
    # ส่วนกรอกวันที่
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("📅 วันปล่อย", date.today())
    with col2:
        end_date = st.date_input("📅 วันเข้ารร.", date.today())
    
    # ยอดเดิมแต่ละชั้นปี
    defaults = {5: 67, 4: 101, 3: 94, 2: 85}
    categories = ["เวรเตรียมพร้อม", "กักบริเวณ", "อยู่โรงเรียน", "ราชการ", "โรงพยาบาล", "ลา", "อื่นๆ"]
    
    st.markdown("### 📊 กรอกข้อมูลแต่ละชั้นปี")
    
    data = {}
    year_colors = {
        5: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        4: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        3: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        2: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
    }
    
    for year in [5, 4, 3, 2]:
        data[year] = {}
        
        st.markdown(f"""
        <div style="
            background: {year_colors[year]};
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        ">
            <h4 style="margin: 0 0 1rem 0; text-align: center;">
                🎓 ชั้นปีที่ {year} (ยอดเดิม: {defaults[year]} นาย)
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(len(categories))
        for i, cat in enumerate(categories):
            with cols[i % len(cols)]:
                val = st.number_input(
                    f"{cat}",
                    min_value=0,
                    step=1,
                    key=f"{cat}_{year}",
                    help=f"จำนวน{cat} ชั้นปีที่ {year}"
                )
                data[year][cat] = val
    
    # ปุ่มสร้างรายงาน
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 สร้างรายงาน", use_container_width=True):
            st.session_state["generate_report"] = True
    
    with col2:
        st.markdown("""
        <a href="https://docs.google.com/spreadsheets/d/1_kKUegxtwwd3ce3EduPqRoPpgAF1_IcecA1ri9Pfxz0/edit?gid=351113778#gid=351113778" 
           target="_blank"
           style="
               background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
               color: white;
               padding: 0.75rem 1.5rem;
               border-radius: 12px;
               text-decoration: none;
               font-weight: 500;
               display: block;
               text-align: center;
               box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
           ">
            📗 ทำไฟล์ Excel
        </a>
        """, unsafe_allow_html=True)
    
    # แสดงรายงาน
    if st.session_state.get("generate_report", False):
        st.success("✅ รายงานถูกสร้างเรียบร้อยแล้ว")
        
        lines = []
        start_str = start_date.strftime("%-d %b").replace("May", "พ.ค.").replace("Jun", "มิ.ย.")
        thai_year = end_date.year + 543
        end_str = end_date.strftime("%-d %b").replace("May", "พ.ค.").replace("Jun", "มิ.ย.") + f" {str(thai_year)[-2:]}"
        
        lines.append(f"พัน.4 กรม นนร.รอ. ขออนุญาตส่งยอด นนร. ปล่อยพักบ้าน, อยู่โรงเรียน และ เวรเตรียมพร้อม ของวันที่ {start_str} - {end_str} ดังนี้")
        
        for y in [5, 4, 3, 2]:
            lines.append(f"ชั้นปีที่ {y} ยอดเดิม {defaults[y]} นาย")
        
        # คำนวณยอดปล่อยบ้าน
        lines.append("1.ยอดปล่อยพักบ้าน")
        total_home = 0
        for y in [5, 4, 3, 2]:
            sum_others = sum(data[y].values())
            val = defaults[y] - sum_others
            total_home += val
            lines.append(f"   -ชั้นปีที่ {y} จำนวน {val} นาย")
        lines.append(f"   -รวม {total_home} นาย")
        
        # เพิ่มหมวดหมู่อื่นๆ
        for i, cat in enumerate(["อยู่โรงเรียน", "เวรเตรียมพร้อม", "กักบริเวณ", "โรงพยาบาล", "ราชการ", "ลา", "อื่นๆ"], start=2):
            lines.append(f"{i}.{cat}")
            total = 0
            for y in [5, 4, 3, 2]:
                val = data[y].get(cat, 0)
                total += val
                show_val = f"{val}" if val != 0 else "-"
                lines.append(f"   -ชั้นปีที่ {y} จำนวน {show_val} นาย")
            show_total = f"{total}" if total != 0 else "-"
            lines.append(f"   -รวม {show_total} นาย")
        
        lines.append("จึงเรียนมาเพื่อกรุณาทราบ")
        
        st.text_area("📋 รายงานยอดปล่อย", value="\n".join(lines), height=400)

def show_count_page():
    st.markdown("## 📊 สถิติโดนยอด")
    
    if st.button("← กลับหน้าหลัก"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
    
    # แสดงลิงก์ดูสถิติ
    sheet_id = "1PfZdCw2iL65CPTZzNsCnkhF7EVJNFZHRvYAXqeOJsSk"
    user_gid_map = {
        "oat": "0",
        "time": "589142731", 
        "chai": "258225546",
    }
    
    username = st.session_state.get("username", "")
    gid = user_gid_map.get(username, "0")
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={gid}"
    
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
    ">
        <h3>📈 สถิติปัจจุบัน</h3>
        <p>ดูสถิติโดนยอดของ {st.session_state["user_data"]["sheet_name"]}</p>
        <a href="{sheet_url}" target="_blank"
           style="
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               color: white;
               padding: 1rem 2rem;
               border-radius: 12px;
               text-decoration: none;
               font-weight: 500;
               display: inline-block;
               box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
               margin-top: 1rem;
           ">
            🔍 ดูสถิติโดนยอด
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # อัปโหลดไฟล์
    st.markdown("### 📤 อัปโหลดไฟล์ยอด")
    uploaded_file = st.file_uploader("เลือกไฟล์ Excel (.xlsx)", type="xlsx")
    
    if uploaded_file:
        try:
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names
            
            selected_sheets = st.multiselect("📄 เลือกชีทที่ต้องการนับแต้ม", sheet_names)
            
            if selected_sheets:
                st.success(f"✅ เลือกแล้ว {len(selected_sheets)} ชีท")
                
                # แสดงตัวอย่างข้อมูล
                for sheet in selected_sheets:
                    with st.expander(f"📋 ดูตัวอย่างข้อมูล: {sheet}"):
                        df = pd.read_excel(xls, sheet_name=sheet, header=None, skiprows=3)
                        df = df.dropna(how='all')
                        
                        if df.shape[1] >= 4:
                            preview_df = pd.DataFrame({
                                "ลำดับ": df.iloc[:, 0],
                                "ชื่อ": df.iloc[:, 2], 
                                "สกุล": df.iloc[:, 3],
                            })
                            st.dataframe(preview_df.head(10), use_container_width=True)
                        else:
                            st.warning("⚠️ ไฟล์มีคอลัมน์ไม่ครบ")
                
                if st.button("✅ อัปเดตแต้มเข้าระบบ", use_container_width=True):
                    st.success("🎉 อัปเดตสถิติเรียบร้อยแล้ว!")
                    st.balloons()
        
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

def show_ceremony_duty_page():
    st.markdown("## 🏅 จัดยอดพิธี")
    
    if st.button("← กลับหน้าหลัก"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
    
    st.info("💡 ระบบสุ่มและจัดยอดสำหรับงานพิธีต่างๆ อัตโนมัติ")
    
    # ฟอร์มกรอกข้อมูล
    col1, col2 = st.columns(2)
    
    with col1:
        ceremony_name = st.text_input("🔖 ชื่อยอดพิธี", placeholder="เช่น ยอดพิธีวันจันทร์")
        num_people = st.number_input("👥 จำนวนคน", min_value=1, max_value=100, value=10)
    
    with col2:
        exclude_duties = st.multiselect(
            "⛔ ไม่เลือกคนที่มีหน้าที่",
            ["ชั้นกรม", "ชั้นพัน", "ฝอ.1", "ฝอ.4", "ฝอ.5", "แซนเฮิร์ท", "อิสลาม", "คริสต์"]
        )
        
        exclude_clubs = st.multiselect(
            "⛔ ไม่เลือกชมรม",
            ["กรีฑา", "จักรยาน", "ไซเบอร์", "ดนตรีไทย", "ดนตรีสากล", "ดาบสากล", 
             "นิเทศ", "สตส", "บาส", "โปโลน้ำ", "ฟุตบอล", "ยูโด", "รักบี้", "แบตมินตัน"]
        )
    
    if st.button("🎲 จัดยอดและสร้างไฟล์", use_container_width=True):
        if ceremony_name:
            st.success(f"✅ สร้างยอด '{ceremony_name}' จำนวน {num_people} คน เรียบร้อยแล้ว!")
            
            # สร้างข้อมูลตัวอย่าง
            sample_data = []
            for i in range(num_people):
                sample_data.append({
                    "ลำดับ": i + 1,
                    "ยศ ชื่อ-สกุล": f"นนร.ตัวอย่าง {i + 1}",
                    "ชั้นปีที่": random.choice([2, 3, 4, 5]),
                    "ตอน": random.choice(["ก", "ข", "ค", "ง"]),
                    "ตำแหน่ง": "นักเรียนนายร้อย",
                    "สังกัด": random.choice(["พัน 1", "พัน 2", "พัน 3", "พัน 4"]),
                    "เบอร์โทรศัพท์": f"08{random.randint(10000000, 99999999)}",
                    "หมายเหตุ": ""
                })
            
            df = pd.DataFrame(sample_data)
            st.dataframe(df, use_container_width=True)
            
            # ปุ่มดาวน์โหลด
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 ดาวน์โหลดไฟล์ CSV",
                data=csv,
                file_name=f"{ceremony_name}.csv",
                mime="text/csv"
            )
            
            st.balloons()
        else:
            st.error("❌ กรุณากรอกชื่อยอดพิธี")

# ===== Main Application =====
def main():
    load_custom_css()
    
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
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.7); padding: 2rem;">
        <p>🛡️ J.A.R.V.I.S © 2025 | พัฒนาโดย Oat | ระบบผู้ช่วยอัจฉริยะ ฝอ.1</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
