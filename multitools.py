import streamlit as st
import webbrowser
import subprocess
import pandas as pd
import random
from collections import defaultdict
from openpyxl.styles import Alignment, Border, Side
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import date
import io
from collections import defaultdict
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account

# ===== ระบบ Login =====
users = {
    "oat": {"password": "crma74", "sheet_name": "ชั้น4_พัน4"},
    "time": {"password": "crma74", "sheet_name": "ชั้น4_พัน1"},
    "chai": {"password": "crma74", "sheet_name": "ชั้น4_พัน3"}
}

st.sidebar.title("🔐 เข้าสู่ระบบ")
username = st.sidebar.text_input("ชื่อผู้ใช้")
password = st.sidebar.text_input("รหัสผ่าน", type="password")

if st.sidebar.button("เข้าสู่ระบบ"):
    if username in users and users[username]["password"] == password:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["sheet_name"] = users[username]["sheet_name"]
        st.rerun()  # รีโหลดเพื่อให้ค่าถูกต้อง
    else:
        st.sidebar.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

# ตรวจสอบสถานะการล็อกอิน
if not st.session_state.get("logged_in"):
    st.stop()  # หยุดโปรแกรมหากยังไม่ได้ล็อกอิน

# แสดงผลใน Sidebar หลังล็อกอิน
st.sidebar.success(f"ยินดีต้อนรับ {st.session_state['username']}")
st.sidebar.success(f"ฐานข้อมูล : {st.session_state['sheet_name']}")

# 1. เชื่อมต่อ Google Sheets
def connect_gsheet(sheet_name):
    creds_dict = st.secrets["gcp_service_account"]
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PfZdCw2iL65CPTZzNsCnkhF7EVJNFZHRvYAXqeOJsSk/edit?usp=drivesdk")
    worksheet = sheet.worksheet(sheet_name)
    return worksheet

worksheet = connect_gsheet(st.session_state["sheet_name"])

# ส่วนหัวและภาพ
st.markdown("""
    <style>
        .title-text {
            font-size: 36px;
            text-align: center;
            margin-top: 10px;
            color: #1f77b4;
            font-weight: bold;
        }
        .subtitle-text {
            text-align: center;
            font-size: 18px;
            color: #444;
            margin-bottom: 30px;
        }
        .card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            transition: 0.2s ease-in-out;
        }
        .card:hover {
            box-shadow: 4px 4px 12px rgba(0,0,0,0.15);
            transform: scale(1.01);
        }
        .card h4 {
            margin-bottom: 10px;
            color: #333;
        }
        .stButton > button {
            font-size: 16px;
            padding: 8px 20px;
            border-radius: 10px;
            border: 1px solid #1f77b4;
            background-color: #eaf4ff;
            color: #1f77b4;
            font-weight: bold;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #1f77b4;
            color: white;
        }
        hr {
            border: 1px solid #ccc;
            margin-top: 10px;
            margin-bottom: 25px;
        }
                @media (max-width: 768px) {
            .element-container .stColumns {
                flex-direction: column !important;
            }
            .element-container .stColumn {
                width: 100% !important;
                margin-bottom: 16px;
            }
        }
    </style>
    </style>
""", unsafe_allow_html=True)

st.image("assist.jpg", width=90)
st.markdown("<div class='title-text'>ระบบผู้ช่วย ฝอ.1 <span style='color:#ff4b4b;'>J.A.R.V.I.S</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>เลือกฟังก์ชันที่ต้องการจากด้านล่าง</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# แสดงแบบ card layout
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🛡 เวรรักษาการณ์")
    if st.button("ดู-อัพเดต", key="night_duty_btn"):
        st.session_state["mode"] = "night_duty"
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 📅 เวรเตรียมการ")
    if st.button("ดู-อัพเดต", key="weekend_duty_btn"):
        st.session_state["mode"] = "weekend_duty"
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 🏅 จัดยอดพิธี")
    if st.button("จัดยอด(สุ่ม)", key="ceremony_duty_btn"):
        st.session_state["mode"] = "ceremony_duty"
    st.markdown("</div>", unsafe_allow_html=True)

col4, col5, _ = st.columns([1, 1, 1])
with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 📝 พิมพ์ยอดปล่อย")
    if st.button("พิมพ์ยอดปล่อย", key="home_btn"):
        st.session_state["mode"] = "home"
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 สถิติโดนยอด")
    if st.button("อัพเดต-ตรวจสอบ", key="count_btn"):
        st.session_state["mode"] = "count"
    st.markdown("</div>", unsafe_allow_html=True)


# ตรวจสอบและแสดง UI เฉพาะส่วนที่เลือก
mode = st.session_state.get("mode", None)

if mode == "night_duty":
    st.info("คุณเลือก: เวรยืนกลางคืน")
        # ลิงก์ CSV export (จากชีทแรก)
    csv_url = "https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU/export?format=csv"

    try:
        # ให้ผู้ใช้เลือกระหว่างชีทแทกเวร หรือ ใบเวร (สรุป)
        sheet_option = st.radio(
            "เลือกดูชีท",
            ("แท็กเวร", "ใบเวร (สรุป)"))
        
        # สร้างลิงก์สำหรับชีทที่เลือก
        if sheet_option == "แท็กเวร":
            iframe_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8pO9068jsukCJL0guT_dF7I5cjYMMIhsu7ah-1DkPxSMxnYFsSkuRgffvSUJKVZzQccQyJEOPxvvg/pubhtml?gid=0&single=true&range=A1:I100"  # ลิงก์ชีทแทกเวร
            edit_link = "https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU/edit#gid=0"  # ลิงก์แก้ไขชีทแทกเวร
        else:
            iframe_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8pO9068jsukCJL0guT_dF7I5cjYMMIhsu7ah-1DkPxSMxnYFsSkuRgffvSUJKVZzQccQyJEOPxvvg/pubhtml?gid=2030248910&single=true&range=A1:I100"  # ลิงก์ใบเวร (สรุป)
            edit_link = "https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU/edit#gid=1"  # ลิงก์แก้ไขใบเวร (สรุป)
        
        # การฝัง iframe สำหรับชีทที่เลือก
        st.markdown(f"""
            <style>
                .iframe-container {{
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                .iframe-container iframe {{
                    width: 100%;
                    height: 600px;
                    border: none;
                    zoom: 0.75;
                }}
                .edit-link {{
                    text-align: right;
                    margin-top: 10px;
                    background-color: #4CAF50;
                    padding: 10px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                .edit-link a {{
                    color: white;
                    font-size: 16px;
                    text-decoration: none;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }}
                .edit-link a:hover {{
                    color: #FFEB3B;
                    text-decoration: underline;
                }}
            </style>
            <div class="iframe-container">
                <iframe src="{iframe_link}"></iframe>
            </div>
            <div class="edit-link">
                <a href="{edit_link}" target="_blank">✏️ แก้ไข Google Sheets คลิกที่นี่</a>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"โหลดข้อมูลไม่สำเร็จ: {e}")

elif mode == "weekend_duty":
    st.info("คุณเลือก: เวรเสาร์-อาทิตย์")
    st.markdown("https://docs.google.com/spreadsheets/d/1ufm0LPa4c903jhlANKn_YqNyMtG9id0iN-tMHrhNRA8/edit?gid=1888956716#gid=1888956716")

elif mode == "home":
    st.header("📋 พิมพ์ยอดปล่อย")

    # วันที่ของรายงาน
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("วันปล่อย", date.today())
    with col2:
        end_date = st.date_input("วันเข้ารร.", date.today())
    
    # ยอดเดิมแต่ละชั้นปี
    defaults = {5: 67, 4: 101, 3: 94, 2: 85}
    categories = ["เวรเตรียมพร้อม", "กักบริเวณ", "อยู่โรงเรียน","ราชการ", "โรงพยาบาล", "ลา", "อื่นๆ"]
    
    # กรอกข้อมูล
    st.subheader("กรอกข้อมูลเเต่ละชั้นปี")
    data = {}
    for year in [5, 4, 3, 2]:
        data[year] = {}
        with st.expander(f"ชั้นปีที่ {year}"):
            for cat in categories:
                val = st.number_input(f"{cat} ชั้นปีที่ {year}", min_value=0, step=1, key=f"{cat}_{year}")
                data[year][cat] = val
    
    # ปุ่ม "สร้างรายงาน" และ "ทำไฟล์" ในแถวเดียวกัน ตกแต่งด้วย CSS
    col1, col2 = st.columns([1, 1])
    
    with col1:
        generate = st.button("📘 สร้างรายงาน")
    
    with col2:
        st.markdown("""
            <style>
            .stButton>button.export-link {
                background-color: #28a745;
                color: white;
                border-radius: 6px;
                padding: 0.4em 1em;
                border: none;
                font-size: 14px;
            }
            .stButton>button.export-link:hover {
                background-color: #218838;
                color: white;
            }
            </style>
            <a href="https://docs.google.com/spreadsheets/d/1_kKUegxtwwd3ce3EduPqRoPpgAF1_IcecA1ri9Pfxz0/edit?gid=351113778#gid=351113778" target="_blank">
                <button class="export-link">📗 ทำไฟล์</button>
            </a>
        """, unsafe_allow_html=True)
    
    # ✅ ทำงานต่อเมื่อกดปุ่ม
    if generate:
        st.success("รายงานถูกสร้างเรียบร้อย")
    
        lines = []
        start_str = start_date.strftime("%-d %b").replace("May", "พ.ค.").replace("Jun", "มิ.ย.")
        end_str = end_date.strftime("%-d %b %y").replace("May", "พ.ค.").replace("Jun", "มิ.ย.")
    
        lines.append(f"พัน.4 กรม นนร.รอ. ขออนุญาตส่งยอด นนร. ปล่อยพักบ้าน, อยู่โรงเรียน และ เวรเตรียมพร้อม ของวันที่   {start_str} - {end_str} ดังนี้")
    
        for y in [5, 4, 3, 2]:
            lines.append(f"ชั้นปีที่ {y} ยอดเดิม {defaults[y]} นาย")
    
        def section(title, key):
            lines.append(f"{key+1}.{title}")
            total = 0
            for y in [5, 4, 3, 2]:
                val = data[y].get(title, 0)
                total += val
                show_val = f"{val}" if val != 0 else "-"
                lines.append(f"   -ชั้นปีที่ {y} จำนวน {show_val} นาย")
            show_total = f"{total}" if total != 0 else "-"
            lines.append(f"   -รวม {show_total} นาย")
    
        # 1. ยอดปล่อยบ้าน
        lines.append("1.ยอดปล่อยพักบ้าน")
        total_home = 0
        for y in [5, 4, 3, 2]:
            sum_others = sum(data[y].values())
            val = defaults[y] - sum_others
            total_home += val
            lines.append(f"   -ชั้นปีที่ {y} จำนวน {val} นาย")
        lines.append(f"   -รวม {total_home} นาย")
    
        for i, cat in enumerate(["อยู่โรงเรียน", "เวรเตรียมพร้อม", "กักบริเวณ", "โรงพยาบาล", "ราชการ", "ลา", "อื่นๆ"], start=2):
            section(cat, i)
        lines.append("จึงเรียนมาเพื่อกรุณาทราบ")
    
        st.text_area("รายงานยอด", value="\n".join(lines), height=600)


elif mode == "count":
    ยอด_file = st.file_uploader("📤 อัปโหลดไฟล์ยอด (.xlsx)", type="xlsx")

    if ยอด_file:
        try:
            ยอด_df = pd.read_excel(ยอด_file, header=None, skiprows=3)
            ยอด_df = ยอด_df.dropna(how='all')
        except Exception as e:
            st.error(f"❌ ไม่สามารถอ่านไฟล์: {e}")
            st.stop()

        if ยอด_df.shape[1] >= 4:
            # สร้างชื่อเต็มไว้เทียบกับ Google Sheet
            ยอด_df["ชื่อเต็ม"] = ยอด_df.iloc[:, 2].astype(str).str.strip() + " " + ยอด_df.iloc[:, 3].astype(str).str.strip()

            # พรีวิวเฉพาะลำดับ, ชื่อ, สกุล
            preview_df = pd.DataFrame({
                "ลำดับ": ยอด_df.iloc[:, 0],
                "ชื่อ": ยอด_df.iloc[:, 2],
                "สกุล": ยอด_df.iloc[:, 3],})
            st.info("👀 พรีวิวรายชื่อจากไฟล์ยอด:")
            st.dataframe(preview_df, use_container_width=True)

            # Slider เลือกความเหนื่อย
            เหนื่อย = st.slider("ระดับความเหนื่อยของยอดนี้ (1–5)", 1, 5, 3)

            # ปุ่มอัปเดตแต้ม
            if st.button("✅ อัปเดตแต้มเข้า Google Sheets"):
                # 1. โหลดข้อมูลจาก Google Sheet
                ws = connect_gsheet()
                gsheet_data = ws.get_all_values()

                # 2. สร้าง DataFrame พร้อม header
                gsheet_df = pd.DataFrame(gsheet_data)
                gsheet_df.columns = gsheet_df.iloc[0]
                gsheet_df = gsheet_df[1:].reset_index(drop=True)

                # 3. สร้างคอลัมน์ชื่อเต็ม
                gsheet_df["ชื่อเต็ม"] = gsheet_df.iloc[:, 2].astype(str).str.strip() + " " + gsheet_df.iloc[:, 3].astype(str).str.strip()

                # 4. ตรวจสอบหรือเพิ่มคอลัมน์ 'สถิติโดนยอด'
                if "สถิติโดนยอด" not in gsheet_df.columns:
                    gsheet_df["สถิติโดนยอด"] = 0
                gsheet_df["สถิติโดนยอด"] = pd.to_numeric(gsheet_df["สถิติโดนยอด"], errors='coerce').fillna(0).astype(int)

                # 5. บวกแต้มเฉพาะคนที่มีชื่อในยอด
                gsheet_df["สถิติโดนยอด"] = gsheet_df.apply(lambda row: row["สถิติโดนยอด"] + เหนื่อย if row["ชื่อเต็ม"] in ยอด_df["ชื่อเต็ม"].values else row["สถิติโดนยอด"],axis=1)

                # 6. เขียนค่ากลับเฉพาะคอลัมน์ N
                updated_column_values = gsheet_df["สถิติโดนยอด"].astype(str).tolist()
                start_cell = 'N2'
                end_cell = f'N{1 + len(updated_column_values)}'
                cell_range = f'{start_cell}:{end_cell}'
                ws.update(cell_range, [[val] for val in updated_column_values])

                st.success("✅ อัปเดต 'สถิติโดนยอด' สำเร็จ")
                st.markdown("[🔗 เปิดดู Google Sheets](https://docs.google.com/spreadsheets/d/e/2PACX-1vSf6OB3YE98NPUBjuN7c7tdp93kmj0kEAQMvMiu4FECY4OgbQgQ-AWwz31TcabtrlzWPgcilDmsG4uZ/pubhtml)")
        else:
            st.error("❌ ไฟล์ยอดไม่ครบคอลัมน์ A–D กรุณาตรวจสอบไฟล์ก่อนอัปโหลด")



# โค้ดเวอร์ชันปรับปรุงแล้ว สำหรับฟีเจอร์ "จัดยอดพิธี"

elif mode == "ceremony_duty":
    st.info("คุณเลือก: จัดยอดพิธี")

    sheet = connect_gsheet(st.session_state["sheet_name"])
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])  # ข้าม header แรก

    if "สถิติโดนยอด" in df.columns:
        df["สถิติโดนยอด"] = pd.to_numeric(df["สถิติโดนยอด"], errors="coerce").fillna(0)

    ยอด_name = st.text_input("🔖กรอกชื่อยอด")
    จำนวนคน = st.number_input("👥จำนวนคน", min_value=1, step=1)

    ตัวเลือก_หน้าที่ = ["ชั้นกรม", "ชั้นพัน", "ฝอ.1", "ฝอ.4", "ฝอ.5", "เเซนเฮิร์ท", "อิสลาม", "คริสต์"]
    ตัวเลือก_หน้าที่_ทั้งหมด = ["เลือกทั้งหมด"] + ตัวเลือก_หน้าที่
    ตัวกรอง_หน้าที่_เลือก = st.multiselect("⛔ไม่เลือกคนที่มีหน้าที่", ตัวเลือก_หน้าที่_ทั้งหมด)
    
    ตัวเลือก_ชมรม = ["กรีฑา", "จักรยาน", "ไซเบอร์", "ดนตรีไทย", "ดนตรีสากล", "ดาบสากล", "นิเทศ", "สตส", "บาส", "โปโลน้ำ", "ฟุตบอล", "ยูโด", "รักบี้", "แบตมินตัน"]
    ตัวเลือก_ชมรม_ทั้งหมด = ["เลือกทั้งหมด"] + ตัวเลือก_ชมรม
    excluded_clubs = st.multiselect("⛔ไม่เลือกชมรม", ตัวเลือก_ชมรม_ทั้งหมด)
    
    if st.button("📤 จัดยอดและส่งออกไฟล์"):
        # จัดการเงื่อนไข "เลือกทั้งหมด"
        ตัวกรอง_หน้าที่ = ตัวเลือก_หน้าที่ if "เลือกทั้งหมด" in ตัวกรอง_หน้าที่_เลือก else ตัวกรอง_หน้าที่_เลือก
        filtered_clubs = ตัวเลือก_ชมรม if "เลือกทั้งหมด" in excluded_clubs else excluded_clubs

        df_filtered = df.copy()
        if "หน้าที่" in df_filtered.columns and ตัวกรอง_หน้าที่:
            df_filtered = df_filtered[~df_filtered["หน้าที่"].isin(ตัวกรอง_หน้าที่)]
        if "ชมรม" in df_filtered.columns and filtered_clubs:
            df_filtered = df_filtered[~df_filtered["ชมรม"].isin(filtered_clubs)]
        if "สถิติโดนยอด" in df_filtered.columns:
            df_filtered = df_filtered.sort_values(by="สถิติโดนยอด", ascending=True)

        grouped = df_filtered.groupby("สังกัด")
        สังกัด_list = list(grouped.groups.keys())
        คนต่อสังกัด = defaultdict(list)

        while sum(len(v) for v in คนต่อสังกัด.values()) < จำนวนคน:
            for สังกัด in สังกัด_list:
                available = grouped.get_group(สังกัด)
                used_indices = set().union(*คนต่อสังกัด.values())
                choices = available[~available.index.isin(used_indices)]
                if not choices.empty and sum(len(v) for v in คนต่อสังกัด.values()) < จำนวนคน:
                    chosen = choices.sample(1)
                    คนต่อสังกัด[สังกัด].append(chosen.index[0])

        selected_indices = [i for indices in คนต่อสังกัด.values() for i in indices]
        selected_df = df.loc[selected_indices]
        selected_df = selected_df.reset_index(drop=True)
        selected_df.index += 1

        if "ลำดับ" in selected_df.columns:
            selected_df = selected_df.drop(columns=["ลำดับ"])
        selected_df.insert(0, "ลำดับ", selected_df.index)

        selected_df["ยศ"] = "นนร."
        selected_df["ชื่อ"] = selected_df.iloc[:, 2].fillna("")
        selected_df["สกุล"] = selected_df.iloc[:, 3].fillna("")
        selected_df["ยศ ชื่อ-สกุล"] = selected_df["ยศ"] + " " + selected_df["ชื่อ"] + " " + selected_df["สกุล"]

        columns = ["ลำดับ", "ยศ ชื่อ-สกุล", "ชั้นปีที่", "ตอน", "ตำแหน่ง", "สังกัด", "หมายเหตุ"]
        output_df = selected_df[columns]
        
        # ใส่ฟังก์ชันนี้ก่อนมีการเรียกใช้ render_centered_table
        def render_centered_table(df):
            html = """
            <style>
                table.custom-table {
                    width: 100%;
                    border-collapse: collapse;
                    table-layout: auto;
                    font-size: 11px;
                }
                table.custom-table th, table.custom-table td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                    height: 40px;
                }
                table.custom-table th {
                    font-weight: bold;
                }
                table.custom-table th:nth-child(1), table.custom-table td:nth-child(1) { width: 5%; }
                table.custom-table th:nth-child(2), table.custom-table td:nth-child(2) { width: 20%; }
                table.custom-table th:nth-child(3), table.custom-table td:nth-child(3) { width: 8%; }
                table.custom-table th:nth-child(4), table.custom-table td:nth-child(4) { width: 5%; }
                table.custom-table th:nth-child(5), table.custom-table td:nth-child(5) { width: 15%; }
                table.custom-table th:nth-child(6), table.custom-table td:nth-child(6) { width: 15%; }
                table.custom-table th:nth-child(7), table.custom-table td:nth-child(7) { width: 10%; }
                table.custom-table td:nth-child(2) {
                    text-align: left;
                    padding-left: 10px;
                }
            </style>
            """
            html += "<table class='custom-table'>"
            html += "<thead><tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr></thead>"
            html += "<tbody>"
            for _, row in df.iterrows():
                html += "<tr>"
                for i, cell in enumerate(row):
                    value = "" if pd.isna(cell) and i == 6 else cell
                    html += f"<td>{value}</td>"
                html += "</tr>"
            html += "</tbody></table>"
            st.markdown(html, unsafe_allow_html=True)

        render_centered_table(output_df)
        
        wb = Workbook()
        ws = wb.active
        ws.title = "ยอดพิธี"
        ws.append([ยอด_name])
        ws.append([])
        ws.append(columns)
        ws.merge_cells('A2:I2')

        selected_df["ยศ"] = "นนร."
        selected_df["ชื่อ"] = selected_df.iloc[:, 2]
        selected_df["สกุล"] = selected_df.iloc[:, 3]
        columns_excel = ["ลำดับ", "ยศ", "ชื่อ", "สกุล", "ชั้นปีที่", "ตอน", "ตำแหน่ง", "สังกัด", "หมายเหตุ"]
        output_df_excel = selected_df[columns_excel]

        ws.merge_cells(start_row=3, start_column=2, end_row=3, end_column=4)
        ws.cell(row=3, column=2).value = "ยศ ชื่อ-สกุล"
        ws.cell(row=3, column=2).alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(row=3, column=5).value = "ชั้นปีที่"
        ws.cell(row=3, column=6).value = "ตอน"
        ws.cell(row=3, column=7).value = "ตำแหน่ง"
        ws.cell(row=3, column=8).value = "สังกัด"
        ws.cell(row=3, column=9).value = "หมายเหตุ"

        for r in dataframe_to_rows(output_df_excel, index=False, header=False):
            ws.append(r)

        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        for row in ws.iter_rows(min_row=2):
            for idx, cell in enumerate(row[:9]):
                if idx < 1 or idx > 3:
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = thin_border

        ws.column_dimensions['A'].width = 6
        ws.column_dimensions['B'].width = 5
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 8
        ws.column_dimensions['F'].width = 8
        ws.column_dimensions['G'].width = 20
        ws.column_dimensions['H'].width = 15
        ws.column_dimensions['I'].width = 15
        ws.merge_cells('A1:I1')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        for cell in ws[1]:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = thin_border

        output_filename = f"{ยอด_name}.xlsx"
        wb.save(output_filename)
        st.success(f"✅ สร้างไฟล์ Excel สำเร็จ: {output_filename}")
        with open(output_filename, "rb") as f:
            st.download_button("📥 ดาวน์โหลด Excel", f, file_name=output_filename)

st.markdown("<hr style='border:0.5px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>J.A.R.V.I.S © 2025 | Dev by Oat</p>", unsafe_allow_html=True)


