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

st.image("assist.jpg", width=120)
st.markdown("<h1 style='text-align: center;'>ระบบผู้ช่วย ฝอ.1 <span style='color:#1f77b4;'>J.A.R.V.I.S</span></h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #bbb;'>", unsafe_allow_html=True)


# สร้าง Grid ของปุ่ม (เช่น 3 ปุ่มเรียงกัน)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("เวรยืนกลางคืน", use_container_width=True):
        st.session_state["mode"] = "night_duty"

with col2:
    if st.button("เวรเสา-อา", use_container_width=True):
        st.session_state["mode"] = "weekend_duty"

with col3:
    if st.button("จัดยอดพิธี", use_container_width=True):
        st.session_state["mode"] = "ceremony_duty"

with col4:
    if st.button("พิมพ์ยอดปล่อย", use_container_width=True):
        st.session_state["mode"] = "home"

with col5:
    if st.button("สถิติโดนยอด", use_container_width=True):
        st.session_state["mode"] = "count"

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
            ("แท็กเวร", "ใบเวร (สรุป)")
        )
        
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
    
    categories = [
        "เวรเตรียมพร้อม", "กักบริเวณ", "อยู่โรงเรียน",
        "ราชการ", "โรงพยาบาล", "ลา", "อื่นๆ"]
    
    # กรอกข้อมูล
    st.subheader("กรอกข้อมูลเเต่ละชั้นปี")
    data = {}
    for year in [5, 4, 3, 2]:
        data[year] = {}
        with st.expander(f"ชั้นปีที่ {year}"):
            for cat in categories:
                val = st.number_input(f"{cat} ชั้นปีที่ {year}", min_value=0, step=1, key=f"{cat}_{year}")
                data[year][cat] = val
    
    # ปุ่มสร้างรายงาน
    if st.button("สร้างรายงาน"):
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
    
        # 1. ยอดปล่อยบ้าน = ยอดเดิม - (ยอดอื่น ๆ)
        lines.append("1.ยอดปล่อยพักบ้าน")
        total_home = 0
        for y in [5, 4, 3, 2]:
            sum_others = sum(data[y].values())
            val = defaults[y] - sum_others
            total_home += val
            lines.append(f"   -ชั้นปีที่ {y} จำนวน {val} นาย")
        lines.append(f"   -รวม {total_home} นาย")
    
        # หมวดอื่น ๆ
        for i, cat in enumerate(["อยู่โรงเรียน", "เวรเตรียมพร้อม", "กักบริเวณ", "โรงพยาบาล", "ราชการ", "ลา", "อื่นๆ"], start=2):
            section(cat, i)
    
        lines.append("จึงเรียนมาเพื่อกรุณาทราบ")
    
        st.text_area("รายงานยอด", value="\n".join(lines), height=600)

elif mode == "count":
    # 1. เลือกระดับความเหนื่อย
    เหนื่อย = st.slider("ระดับความเหนื่อยของยอดนี้ (1–5)", 1, 5, 3)
    
    # 2. อัปโหลดไฟล์ยอด
    ยอด_file = st.file_uploader("📤 อัปโหลดไฟล์ยอด (.xlsx)", type="xlsx")
    
    # 2. โหลดไฟล์หลัก
    ชั้น4พัน4 = pd.read_excel("ชั้น4พัน4.xlsx")
    # สำหรับทั้ง 2 ตาราง: ชั้น4พัน4 และ ยอด_df
    ชั้น4พัน4["ชื่อเต็ม"] = ชั้น4พัน4["ชื่อ"].astype(str).str.strip() + " " + ชั้น4พัน4["สกุล"].astype(str).str.strip()
    ยอด_df["ชื่อเต็ม"] = ยอด_df["ชื่อ"].astype(str).str.strip() + " " + ยอด_df["สกุล"].astype(str).str.strip()
    
    # 3. โหลดยอด
    if ยอด_file:
        ยอด_df = pd.read_excel(ยอด_file, header=2)  # ปรับเลขให้ตรงกับแถวหัวจริง
        ยอด_df.columns = ยอด_df.columns.str.strip()
    
        def check_update(row):
            if row["ชื่อเต็ม"] in ยอด_df["ชื่อเต็ม"].values:
                return row["สถิติโดนยอด"] + เหนื่อย
            else:
                return row["สถิติโดนยอด"]
        
        ชั้น4พัน4["สถิติโดนยอด"] = ชั้น4พัน4.apply(check_update, axis=1)
        # ให้ดาวน์โหลดไฟล์ใหม่
        from io import BytesIO
        output = BytesIO()
        ชั้น4พัน4.to_excel(output, index=False)
        st.download_button("📥 ดาวน์โหลดไฟล์อัปเดต", output.getvalue(), file_name="ชั้น4พัน4_อัปเดต.xlsx")
        st.success("อัปเดตเรียบร้อย ✅")


elif mode == "ceremony_duty":
    st.info("คุณเลือก: จัดยอดพิธี")
    
    # อ่านไฟล์ Excel ชั้น4พัน4.xlsx
    @st.cache_data
    def load_data():
        return pd.read_excel("ชั้น4พัน4.xlsx")

    df = load_data()

    # อินพุตจากผู้ใช้
    ยอด_name = st.text_input("🔖กรอกชื่อยอด")
    จำนวนคน = st.number_input("👥จำนวนคน", min_value=1, step=1)

    # Checkbox สำหรับกรองหน้าที่
    ตัวกรอง_หน้าที่ = st.multiselect("ไม่เลือกคนที่มีหน้าที่", ["ชั้นกรม", "ชั้นพัน", "ฝอ.1", "ฝอ.4", "ฝอ.5"])

    if st.button("🚀 จัดยอดและส่งออกไฟล์"):
        # กรองตามหน้าที่
        df_filtered = df[~df["หน้าที่"].isin(ตัวกรอง_หน้าที่)]
        
        # จัดกลุ่มตามสังกัด
        grouped = df_filtered.groupby("สังกัด")
        สังกัด_list = list(grouped.groups.keys())

        คนต่อสังกัด = defaultdict(list)

        # วนสุ่มกระจายให้สังกัดละเท่าๆกัน
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

        # เพิ่มลำดับ
        selected_df = selected_df.reset_index(drop=True)
        selected_df.index += 1

        # ลบคอลัมน์ "ลำดับ" เดิม (ถ้ามี)
        if "ลำดับ" in selected_df.columns:
            selected_df = selected_df.drop(columns=["ลำดับ"])
        
        # เพิ่มคอลัมน์ลำดับ (เริ่มจาก 1)
        selected_df = selected_df.reset_index(drop=True)
        selected_df.index += 1
        selected_df.insert(0, "ลำดับ", selected_df.index)
        
        # แยกคอลัมน์ "ยศ", "ชื่อ", "สกุล"
        selected_df["ยศ"] = "นนร."
        selected_df["ชื่อ"] = selected_df.iloc[:, 1].fillna("")
        selected_df["สกุล"] = selected_df.iloc[:, 2].fillna("")
        
        # กำหนดลำดับคอลัมน์ใหม่
        columns = ["ลำดับ", "ยศ", "ชื่อ", "สกุล", "ชั้นปีที่", "ตอน", "ตำแหน่ง", "สังกัด", "หมายเหตุ"]
        output_df = selected_df[columns]

        st.dataframe(output_df)

        # สร้างไฟล์ Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "ยอดพิธี"

        # เขียนชื่อยอดและเว้นแถว
        ws.append([ยอด_name])
        ws.append([])

        # 👉 เขียนหัวตารางก่อน (เพื่อให้เซลล์ row=3 มีอยู่จริง)
        ws.append(columns)

        # นำข้อมูลจากคอลัมภ์ B, C, D มาแยกในคอลัมภ์ที่ถูกต้อง
        selected_df["ยศ"] = selected_df.iloc[:, 1]  # คอลัมภ์ยศ
        selected_df["ชื่อ"] = selected_df.iloc[:, 2]  # คอลัมภ์ชื่อ
        selected_df["สกุล"] = selected_df.iloc[:, 3]  # คอลัมภ์สกุล
        
        # ปรับคอลัมภ์ใน output_df ให้มีลำดับที่ถูกต้อง
        columns = ["ลำดับ", "ยศ", "ชื่อ", "สกุล", "ชั้นปีที่", "ตอน", "ตำแหน่ง", "สังกัด", "หมายเหตุ"]
        output_df = selected_df[columns]

        # Merge หัวข้อ “ยศ ชื่อ-สกุล” (B3-D3)
        ws.merge_cells(start_row=3, start_column=2, end_row=3, end_column=4)
        ws.cell(row=3, column=2).value = "ยศ ชื่อ-สกุล"
        ws.cell(row=3, column=2).alignment = Alignment(horizontal='center', vertical='center')
        
        # เขียนข้อมูลแถวต่อจาก row 4
        for r in dataframe_to_rows(output_df, index=False, header=False):
            ws.append(r)

        # จัดหัวข้อยอดให้อยู่กลาง
        ws.cell(row=1, column=1).alignment = Alignment(horizontal='center', vertical='center')

        # ตั้งเส้นขอบบางๆ
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin'))

        # จัดการข้อมูลในแถว (ตั้งแต่แถวที่ 2)
        for row in ws.iter_rows(min_row=2):
            for idx, cell in enumerate(row[:9]):
                if idx < 1 or idx > 3:
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = thin_border

        # ตั้งความกว้างคอลัมน์
        ws.column_dimensions['A'].width = 6
        ws.column_dimensions['B'].width = 5
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 8
        ws.column_dimensions['F'].width = 8
        ws.column_dimensions['G'].width = 20
        ws.column_dimensions['H'].width = 15
        ws.column_dimensions['I'].width = 15

        # สร้างเส้นขอบที่หัวตาราง
        ws.merge_cells('A1:I1')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        for cell in ws[1]:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = thin_border

        # บันทึกไฟล์ Excel
        output_filename = f"{ยอด_name}.xlsx"
        wb.save(output_filename)

        # แจ้งผลสำเร็จและให้ดาวน์โหลด
        st.success(f"สร้างไฟล์สำเร็จ: {output_filename}")
        with open(output_filename, "rb") as f:
            st.download_button("ดาวน์โหลดไฟล์ Excel", f, file_name=output_filename)
st.markdown("<hr style='border:0.5px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>J.A.R.V.I.S © 2025 | Dev by Oat</p>", unsafe_allow_html=True)

