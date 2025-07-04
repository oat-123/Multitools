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

# ===== ฟังก์ชันสำหรับ Streamlit-Compatible CSS =====
def load_streamlit_css():
    st.markdown("""
    <style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Global App Background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Login Page Styles */
    .login-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(74,144,226,0.1) 0%, rgba(53,122,189,0.05) 100%);
        border-radius: 20px;
        border: 1px solid rgba(74,144,226,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .login-logo {
        width: 120px;
        height: 120px;
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 50%, #2E5F8A 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 2rem auto;
        font-size: 4rem;
        box-shadow: 
            0 0 30px rgba(74,144,226,0.5),
            0 0 60px rgba(74,144,226,0.2);
        animation: logoPulse 3s ease-in-out infinite;
    }
    
    @keyframes logoPulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 30px rgba(74,144,226,0.5), 0 0 60px rgba(74,144,226,0.2);
        }
        50% { 
            transform: scale(1.05);
            box-shadow: 0 0 40px rgba(74,144,226,0.8), 0 0 80px rgba(74,144,226,0.3);
        }
    }
    
    .login-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 1rem 0;
        letter-spacing: 0.2em;
        text-shadow: 0 0 20px rgba(74,144,226,0.6);
    }
    
    .login-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        color: rgba(74,144,226,0.9);
        margin: 0;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    .login-description {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        color: rgba(255,255,255,0.7);
        margin-top: 1rem;
        line-height: 1.6;
    }
    
    /* Form Container */
    .login-form {
        background: linear-gradient(135deg, rgba(15,25,40,0.9) 0%, rgba(10,15,25,0.95) 100%);
        border: 2px solid rgba(74,144,226,0.3);
        border-radius: 20px;
        padding: 3rem 2rem;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Streamlit Form Elements */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(20,30,45,0.8) 0%, rgba(15,25,40,0.9) 100%) !important;
        border: 2px solid rgba(74,144,226,0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(74,144,226,0.8) !important;
        box-shadow: 0 0 20px rgba(74,144,226,0.3) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.5) !important;
    }
    
    .stTextInput label {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 50%, #2E5F8A 100%) !important;
        color: #ffffff !important;
        border: 2px solid rgba(74,144,226,0.6) !important;
        border-radius: 12px !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(74,144,226,0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #357ABD 0%, #4A90E2 50%, #5BA0F2 100%) !important;
        border-color: rgba(74,144,226,0.9) !important;
        box-shadow: 0 12px 35px rgba(74,144,226,0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(34,197,94,0.2) 0%, rgba(22,163,74,0.1) 100%) !important;
        border: 1px solid rgba(34,197,94,0.6) !important;
        border-radius: 10px !important;
        color: #4ade80 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(220,38,38,0.2) 0%, rgba(185,28,28,0.1) 100%) !important;
        border: 1px solid rgba(220,38,38,0.6) !important;
        border-radius: 10px !important;
        color: #ff6b6b !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245,158,11,0.2) 0%, rgba(217,119,6,0.1) 100%) !important;
        border: 1px solid rgba(245,158,11,0.6) !important;
        border-radius: 10px !important;
        color: #fbbf24 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, rgba(74,144,226,0.1) 0%, rgba(53,122,189,0.05) 100%);
        border: 1px solid rgba(74,144,226,0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        text-align: center;
    }
    
    .info-item {
        display: inline-block;
        margin: 0.5rem 1rem;
        color: rgba(255,255,255,0.8);
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .info-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
        color: #4A90E2;
    }
    
    /* Dashboard Styles */
    .dashboard-header {
        background: linear-gradient(135deg, rgba(15,25,40,0.9) 0%, rgba(10,15,25,0.95) 100%);
        border: 1px solid rgba(74,144,226,0.3);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .dashboard-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .dashboard-logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #4A90E2, #357ABD);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .dashboard-title {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.1em;
    }
    
    .user-profile {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(74,144,226,0.1);
        border: 1px solid rgba(74,144,226,0.3);
        border-radius: 15px;
        padding: 1rem 1.5rem;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #4A90E2, #357ABD);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        color: white;
    }
    
    .user-info h4 {
        margin: 0;
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .user-info p {
        margin: 0;
        color: rgba(255,255,255,0.7);
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.9rem;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, rgba(74,144,226,0.1) 0%, rgba(53,122,189,0.05) 100%);
        border-radius: 20px;
        margin: 2rem 0;
        border: 1px solid rgba(74,144,226,0.2);
    }
    
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: 0.1em;
        text-shadow: 0 0 20px rgba(74,144,226,0.5);
    }
    
    .hero-subtitle {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: #4A90E2;
        margin-bottom: 1.5rem;
        letter-spacing: 0.1em;
    }
    
    .hero-description {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.3rem;
        color: rgba(255,255,255,0.8);
        margin-bottom: 2rem;
        line-height: 1.6;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Stats Grid */
    .stats-container {
        margin: 3rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(15,25,40,0.9) 0%, rgba(10,15,25,0.95) 100%);
        border: 1px solid rgba(74,144,226,0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: rgba(74,144,226,0.6);
        box-shadow: 0 10px 30px rgba(74,144,226,0.2);
        transform: translateY(-5px);
    }
    
    .stat-number {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 800;
        color: #4A90E2;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(74,144,226,0.5);
    }
    
    .stat-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.8);
        font-weight: 500;
        letter-spacing: 0.05em;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .login-title {
            font-size: 2.5rem;
        }
        
        .login-logo {
            width: 100px;
            height: 100px;
            font-size: 3rem;
        }
        
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
        }
        
        .dashboard-header {
            flex-direction: column;
            text-align: center;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
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
    # Header Section
    st.markdown("""
    <div class="login-header">
        <div class="login-logo">🛡️</div>
        <h1 class="login-title">J.A.R.V.I.S</h1>
        <p class="login-subtitle">Military Assistance System</p>
        <p class="login-description">
            ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1<br>
            ด้วยเทคโนโลยี AI และการประมวลผลที่ทันสมัย
        </
