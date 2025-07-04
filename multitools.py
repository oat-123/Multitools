import streamlit as st
import pandas as pd
import random
from collections import defaultdict
from datetime import date, datetime
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
    "oat": {"password": "crma74", "sheet_name": "ชั้น4_พัน4", "display_name": "ผู้ใช้ OAT", "role": "ผู้ดูแลระบบ", "avatar": "👨‍💼"},
    "time": {"password": "crma74", "sheet_name": "ชั้น4_พัน1", "display_name": "ผู้ใช้ TIME", "role": "ผู้ใช้งาน", "avatar": "👨‍🎓"},
    "chai": {"password": "crma74", "sheet_name": "ชั้น4_พัน3", "display_name": "ผู้ใช้ CHAI", "role": "ผู้ใช้งาน", "avatar": "👨‍🎓"}
}

# ===== ฟังก์ชันสำหรับ Enhanced CSS =====
def load_enhanced_css():
    st.markdown("""
    <style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stDecoration {display: none;}
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0e4b99 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
        z-index: -1;
        animation: backgroundShift 20s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Main Container */
    .main .block-container {
        padding: 1rem;
        max-width: 1400px;
    }
    
    /* ===== LOGIN PAGE STYLES ===== */
    
    /* Login Container */
    .login-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        position: relative;
    }
    
    /* Floating Particles */
    .login-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 100px 50px, rgba(255,255,255,0.4), transparent),
            radial-gradient(1px 1px at 200px 100px, rgba(74,144,226,0.6), transparent),
            radial-gradient(1px 1px at 300px 200px, rgba(255,255,255,0.3), transparent),
            radial-gradient(2px 2px at 400px 150px, rgba(74,144,226,0.4), transparent);
        background-size: 500px 300px;
        animation: floatingParticles 25s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes floatingParticles {
        0% { transform: translateX(0) translateY(0); }
        100% { transform: translateX(-500px) translateY(-300px); }
    }
    
    /* Login Header */
    .login-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 3rem 2rem;
        background: rgba(15, 25, 45, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(74, 144, 226, 0.2);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 80px rgba(74, 144, 226, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 2;
        max-width: 600px;
        width: 100%;
    }
    
    /* Animated Logo */
    .login-logo {
        width: 140px;
        height: 140px;
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 30%, #2E5F8A 60%, #1E3A8A 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 2rem auto;
        font-size: 4.5rem;
        position: relative;
        animation: logoFloat 6s ease-in-out infinite;
        box-shadow: 
            0 0 40px rgba(74, 144, 226, 0.6),
            0 0 80px rgba(74, 144, 226, 0.3),
            inset 0 2px 20px rgba(255, 255, 255, 0.2);
    }
    
    .login-logo::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border: 2px solid rgba(74, 144, 226, 0.4);
        border-radius: 50%;
        animation: logoRing1 4s linear infinite;
    }
    
    .login-logo::after {
        content: '';
        position: absolute;
        top: -20px;
        left: -20px;
        right: -20px;
        bottom: -20px;
        border: 1px solid rgba(74, 144, 226, 0.2);
        border-radius: 50%;
        animation: logoRing2 6s linear infinite reverse;
    }
    
    @keyframes logoFloat {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-10px) scale(1.05); }
    }
    
    @keyframes logoRing1 {
        0% { transform: rotate(0deg) scale(1); opacity: 1; }
        100% { transform: rotate(360deg) scale(1.1); opacity: 0.5; }
    }
    
    @keyframes logoRing2 {
        0% { transform: rotate(0deg) scale(1); opacity: 0.5; }
        100% { transform: rotate(-360deg) scale(1.2); opacity: 0; }
    }
    
    /* Typography */
    .login-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 1rem 0;
        letter-spacing: 0.1em;
        text-shadow: 
            0 0 20px rgba(74, 144, 226, 0.8),
            0 0 40px rgba(74, 144, 226, 0.4);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 0 0 20px rgba(74, 144, 226, 0.8), 0 0 40px rgba(74, 144, 226, 0.4); }
        100% { text-shadow: 0 0 30px rgba(74, 144, 226, 1), 0 0 60px rgba(74, 144, 226, 0.6); }
    }
    
    .login-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.4rem;
        color: rgba(74, 144, 226, 0.9);
        margin: 0 0 1.5rem 0;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-weight: 500;
    }
    
    .login-description {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        max-width: 500px;
        margin: 0 auto;
    }
    
    /* Login Form */
    .login-form-container {
        background: rgba(15, 25, 45, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        border: 1px solid rgba(74, 144, 226, 0.3);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        max-width: 450px;
        width: 100%;
        position: relative;
        z-index: 2;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(20, 30, 50, 0.8) 0%, rgba(15, 25, 40, 0.9) 100%) !important;
        border: 2px solid rgba(74, 144, 226, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 1.2rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(74, 144, 226, 0.8) !important;
        box-shadow: 
            0 0 0 3px rgba(74, 144, 226, 0.2),
            inset 0 2px 10px rgba(0, 0, 0, 0.2) !important;
        outline: none !important;
        background: linear-gradient(135deg, rgba(25, 35, 55, 0.9) 0%, rgba(20, 30, 45, 0.95) 100%) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        font-style: italic;
    }
    
    .stTextInput label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Enhanced Button */
    .stButton > button {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 50%, #2E5F8A 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 1.2rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 10px 30px rgba(74, 144, 226, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #357ABD 0%, #4A90E2 50%, #5BA0F2 100%) !important;
        box-shadow: 
            0 15px 40px rgba(74, 144, 226, 0.4),
            0 0 60px rgba(74, 144, 226, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-3px) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Status Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(22, 163, 74, 0.1) 100%) !important;
        border: 1px solid rgba(34, 197, 94, 0.6) !important;
        border-radius: 12px !important;
        color: #4ade80 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.6) !important;
        border-radius: 12px !important;
        color: #ff6b6b !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.1) 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.6) !important;
        border-radius: 12px !important;
        color: #fbbf24 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Info Box */
    .info-box {
        background: rgba(74, 144, 226, 0.1);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .info-item {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .info-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    .info-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .info-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .info-desc {
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* ===== DASHBOARD STYLES ===== */
    
    /* Dashboard Header */
    .dashboard-header {
        background: rgba(15, 25, 45, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 2rem;
    }
    
    .dashboard-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .dashboard-logo-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #4A90E2, #357ABD);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.4);
    }
    
    .dashboard-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.1em;
        text-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
    }
    
    .user-profile {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(74, 144, 226, 0.1);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #4A90E2, #357ABD);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 0 15px rgba(74, 144, 226, 0.4);
    }
    
    .user-info h4 {
        margin: 0;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .user-info p {
        margin: 0;
        color: rgba(255, 255, 255, 0.7);
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    
    /* Navigation Buttons */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .nav-card {
        background: rgba(15, 25, 45, 0.8);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    .nav-card:hover {
        background: rgba(74, 144, 226, 0.1);
        border-color: rgba(74, 144, 226, 0.6);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(74, 144, 226, 0.2);
    }
    
    .nav-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 0 10px rgba(74, 144, 226, 0.5));
    }
    
    .nav-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }
    
    .nav-desc {
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(74, 144, 226, 0.1);
        border-radius: 24px;
        margin: 3rem 0;
        border: 1px solid rgba(74, 144, 226, 0.2);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(74, 144, 226, 0.1) 50%, transparent 70%);
        animation: heroShine 3s ease-in-out infinite;
    }
    
    @keyframes heroShine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: 0.1em;
        text-shadow: 0 0 30px rgba(74, 144, 226, 0.6);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #4A90E2;
        margin-bottom: 2rem;
        letter-spacing: 0.1em;
        position: relative;
        z-index: 1;
    }
    
    .hero-description {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto 3rem auto;
        position: relative;
        z-index: 1;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: rgba(15, 25, 45, 0.8);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4A90E2, #357ABD, #2E5F8A);
        border-radius: 20px 20px 0 0;
    }
    
    .stat-card:hover {
        border-color: rgba(74, 144, 226, 0.6);
        box-shadow: 0 20px 50px rgba(74, 144, 226, 0.2);
        transform: translateY(-8px);
    }
    
    .stat-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #4A90E2;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
        line-height: 1;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        letter-spacing: 0.05em;
    }
    
    .stat-description {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 0.5rem;
        line-height: 1.4;
    }
    
    /* Time Display */
    .time-display {
        background: rgba(74, 144, 226, 0.1);
        border: 1px solid rgba(74, 144, 226, 0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .current-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        color: #4A90E2;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .current-date {
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
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
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.8rem;
        }
        
        .dashboard-nav {
            flex-direction: column;
            text-align: center;
        }
        
        .nav-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
        
        .info-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(74, 144, 226, 0.3);
        border-radius: 50%;
        border-top-color: #4A90E2;
        animation: spin 1s ease-in-out infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Footer */
    .footer {
        background: rgba(15, 25, 45, 0.8);
        border-top: 1px solid rgba(74, 144, 226, 0.2);
        padding: 3rem 2rem;
        text-align: center;
        margin-top: 4rem;
        backdrop-filter: blur(10px);
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .footer-text {
        color: rgba(255, 255, 255, 0.7);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        margin: 0;
        letter-spacing: 0.05em;
    }
    
    .footer-links {
        margin-top: 1rem;
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .footer-link {
        color: rgba(74, 144, 226, 0.8);
        text-decoration: none;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        transition: color 0.3s ease;
    }
    
    .footer-link:hover {
        color: #4A90E2;
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

# ===== ฟังก์ชันสำหรับการแสดงเวลาปัจจุบัน =====
def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S"), now.strftime("%d/%m/%Y")

# ===== ฟังก์ชันสำหรับการแสดงหน้า Login =====
def show_login_page():
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="login-logo">🛡️</div>
            <h1 class="login-title">J.A.R.V.I.S</h1>
            <p class="login-subtitle">MILITARY ASSISTANCE SYSTEM</p>
            <p class="login-description">
                ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1<br>
                ด้วยเทคโนโลยี AI และการประมวลผลที่ทันสมัย พร้อมระบบรักษาความปลอดภัยระดับสูง
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        
        st.markdown("### 🔐 เข้าสู่ระบบ")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "👤 ชื่อผู้ใช้", 
                placeholder="กรอกชื่อผู้ใช้งาน...",
                help="ใช้ชื่อผู้ใช้ที่ได้รับจากระบบ"
            )
            
            password = st.text_input(
                "🔒 รหัสผ่าน", 
                type="password", 
                placeholder="กรอกรหัสผ่าน...",
                help="รหัสผ่านที่ได้รับจากผู้ดูแลระบบ"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            login_button = st.form_submit_button("🚀 เข้าสู่ระบบ")
            
            if login_button:
                if username and password:
                    with st.spinner('🔍 กำลังตรวจสอบข้อมูล...'):
                        time.sleep(1.5)
                        
                        if username in users and users[username]["password"] == password:
                            st.success("✅ เข้าสู่ระบบสำเร็จ! กำลังเปลี่ยนหน้า...")
                            time.sleep(1)
                            
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.session_state["user_data"] = users[username]
                            st.session_state["current_page"] = "dashboard"
                            st.session_state["login_time"] = datetime.now()
                            st.rerun()
                        else:
                            st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                else:
                    st.warning("⚠️ กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System Info
        st.markdown("""
        <div class="info-box">
            <h3 style="text-align: center; color: #4A90E2; margin-bottom: 1.5rem; font-family: 'Inter', sans-serif;">ระบบคุณสมบัติ</h3>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-icon">🔒</span>
                    <div class="info-title">ความปลอดภัย</div>
                    <div class="info-desc">ระบบรักษาความปลอดภัยระดับสูง</div>
                </div>
                <div class="info-item">
                    <span class="info-icon">💻</span>
                    <div class="info-title">รองรับทุกอุปกรณ์</div>
                    <div class="info-desc">ใช้งานได้บนคอมพิวเตอร์และมือถือ</div>
                </div>
                <div class="info-item">
                    <span class="info-icon">⚡</span>
                    <div class="info-title">ประมวลผล AI</div>
                    <div class="info-desc">ระบบอัจฉริยะช่วยจัดการงาน</div>
                </div>
                <div class="info-item">
                    <span class="info-icon">🌐</span>
                    <div class="info-title">เชื่อมต่อ Cloud</div>
                    <div class="info-desc">ข้อมูลซิงค์แบบเรียลไทม์</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับการแสดง Dashboard =====
def show_dashboard():
    current_time, current_date = get_current_time()
    
    # Header
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-nav">
            <div class="dashboard-logo">
                <div class="dashboard-logo-icon">🛡️</div>
                <div>
                    <h1 class="dashboard-title">J.A.R.V.I.S</h1>
                    <div class="time-display">
                        <div class="current-time">{current_time}</div>
                        <div class="current-date">{current_date}</div>
                    </div>
                </div>
            </div>
            <div class="user-profile">
                <div class="user-avatar">{st.session_state['user_data']['avatar']}</div>
                <div class="user-info">
                    <h4>{st.session_state['user_data']['display_name']}</h4>
                    <p>{st.session_state['user_data']['role']}</p>
                    <p>{st.session_state['user_data']['sheet_name']}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Cards
    st.markdown("## 🎯 เลือกฟังก์ชันการทำงาน")
    
    nav_items = [
        ("night_duty", "🛡️", "เวรรักษาการณ์", "จัดการและดูข้อมูลเวรยืนกลางคืน"),
        ("weekend_duty", "📅", "เวรเตรียมการ", "จัดการเวรเสาร์-อาทิตย์และวันหยุด"),
        ("ceremony_duty", "🏅", "จัดยอดพิธี", "สุ่มและจัดยอดสำหรับงานพิธีต่างๆ"),
        ("home", "📝", "ยอดปล่อย", "พิมพ์และจัดทำรายงานยอดปล่อย"),
        ("count", "📊", "สถิติโดนยอด", "อัพเดตและตรวจสอบสถิติการโดนยอด"),
        ("logout", "🚪", "ออกจากระบบ", "ออกจากระบบและกลับสู่หน้าเข้าสู่ระบบ")
    ]
    
    cols = st.columns(3)
    for i, (page_id, icon, title, desc) in enumerate(nav_items):
        with cols[i % 3]:
            if st.button(f"{icon} {title}", key=f"nav_{page_id}", use_container_width=True):
                if page_id == "logout":
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
                else:
                    st.session_state["current_page"] = page_id
                    st.rerun()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">THE FUTURE OF</h1>
        <h2 class="hero-subtitle">MILITARY ASSISTANCE</h2>
        <p class="hero-description">
            ระบบผู้ช่วยอัจฉริยะสำหรับการจัดการงานต่างๆ ของ ฝอ.1<br>
            ด้วยเทคโนโลยีที่ทันสมัยและใช้งานง่าย พร้อมการเชื่อมต่อ Google Sheets<br>
            และระบบวิเคราะห์ข้อมูลแบบเรียลไทม์
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("## 📈 สถิติระบบ")
    
    stats_data = [
        ("150+", "นักเรียนนายร้อย", "จำนวนผู้ใช้งานในระบบ"),
        ("24/7", "ระบบพร้อมใช้งาน", "บริการตลอด 24 ชั่วโมง"),
        ("5", "ฟังก์ชันหลัก", "โมดูลการทำงานที่สำคัญ"),
        ("99%", "ความแม่นยำ", "ประสิทธิภาพการทำงาน")
    ]
    
    cols = st.columns(4)
    for i, (number, label, desc) in enumerate(stats_data):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
                <div class="stat-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent Activity (Mock Data)
    st.markdown("## 📋 กิจกรรมล่าสุด")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(15, 25, 45, 0.8); border: 1px solid rgba(74, 144, 226, 0.3); border-radius: 16px; padding: 2rem; backdrop-filter: blur(10px);">
            <h4 style="color: #4A90E2; margin-bottom: 1rem;">🕐 เวรล่าสุด</h4>
            <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <p>• เวรรักษาการณ์: 03/01/2025</p>
                <p>• เวรเตรียมการ: 05/01/2025</p>
                <p>• จัดยอดพิธี: 07/01/2025</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(15, 25, 45, 0.8); border: 1px solid rgba(74, 144, 226, 0.3); border-radius: 16px; padding: 2rem; backdrop-filter: blur(10px);">
            <h4 style="color: #4A90E2; margin-bottom: 1rem;">📊 สถิติการใช้งาน</h4>
            <div style="color: rgba(255, 255, 255, 0.8); line-height: 1.6;">
                <p>• การเข้าใช้งานวันนี้: 25 ครั้ง</p>
                <p>• ฟังก์ชันที่ใช้บ่อย: เวรรักษาการณ์</p>
                <p>• เวลาใช้งานเฉลี่ย: 15 นาที</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== ฟังก์ชันสำหรับหน้าต่างๆ =====
def show_module_page(module_name, icon, description):
    current_time, current_date = get_current_time()
    
    # Header
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-nav">
            <div class="dashboard-logo">
                <div class="dashboard-logo-icon">{icon}</div>
                <div>
                    <h1 class="dashboard-title">{module_name}</h1>
                    <div class="time-display">
                        <div class="current-time">{current_time}</div>
                        <div class="current-date">{current_date}</div>
                    </div>
                </div>
            </div>
            <div class="user-profile">
                <div class="user-avatar">{st.session_state['user_data']['avatar']}</div>
                <div class="user-info">
                    <h4>{st.session_state['user_data']['display_name']}</h4>
                    <p>{st.session_state['user_data']['role']}</p>
                    <p>{st.session_state['user_data']['sheet_name']}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back Button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← กลับหน้าหลัก", key="back_to_dashboard"):
            st.session_state["current_page"] = "dashboard"
            st.rerun()
    
    # Module Content
    st.markdown(f"""
    <div class="hero-section">
        <div style="font-size: 5rem; margin-bottom: 2rem;">{icon}</div>
        <h1 class="hero-title">{module_name}</h1>
        <p class="hero-description">{description}</p>
        <div style="margin-top: 3rem;">
            <div style="background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 12px; padding: 2rem; color: rgba(255, 193, 7, 0.9);">
                <h3>🚧 ฟังก์ชันกำลังพัฒนา</h3>
                <p>ฟังก์ชันนี้จะเชื่อมต่อกับ Google Sheets และระบบฐานข้อมูลเดิม<br>
                รอการอัพเดตในเวอร์ชันถัดไป</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_night_duty_page():
    show_module_page(
        "เวรรักษาการณ์", 
        "🛡️", 
        "จัดการและดูข้อมูลเวรยืนกลางคืน ระบบตรวจสอบตลอด 24 ชั่วโมง พร้อมการแจ้งเตือนอัตโนมัติและการจัดตารางเวรอัจฉริยะ"
    )

def show_weekend_duty_page():
    show_module_page(
        "เวรเตรียมการ", 
        "📅", 
        "จัดการเวรเสาร์-อาทิตย์และวันหยุดราชการ พร้อมระบบจัดตารางอัตโนมัติและการแจ้งเตือนล่วงหน้า"
    )

def show_ceremony_duty_page():
    show_module_page(
        "จัดยอดพิธี", 
        "🏅", 
        "สุ่มและจัดยอดสำหรับงานพิธีต่างๆ อัตโนมัติ ด้วยอัลกอริทึมที่ยุติธรรมและระบบติดตามประวัติ"
    )

def show_home_page():
    show_module_page(
        "ยอดปล่อย", 
        "📝", 
        "พิมพ์และจัดทำรายงานยอดปล่อยประจำวัน พร้อมการส่งออกเป็น PDF และระบบอนุมัติอิเล็กทรอนิกส์"
    )

def show_count_page():
    show_module_page(
        "สถิติโดนยอด", 
        "📊", 
        "อัพเดตและตรวจสอบสถิติการโดนยอด พร้อมกราฟและการวิเคราะห์ข้อมูลแบบเรียลไทม์"
    )

# ===== Main Application =====
def main():
    load_enhanced_css()
    
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
    <div class="footer">
        <div class="footer-content">
            <p class="footer-text">
                J.A.R.V.I.S © 2025 | พัฒนาโดย Oat | ระบบผู้ช่วยอัจฉริยะ ฝอ.1
            </p>
            <div class="footer-links">
                <a href="#" class="footer-link">เกี่ยวกับระบบ</a>
                <a href="#" class="footer-link">คู่มือการใช้งาน</a>
                <a href="#" class="footer-link">ติดต่อสนับสนุน</a>
                <a href="#" class="footer-link">นโยบายความเป็นส่วนตัว</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
