import streamlit as st
import webbrowser
import subprocess
import pandas as pd
import random
from collections import defaultdict
from openpyxl.styles import Alignment, Border, Side
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

st.title("ผู้ช่วย ฝอ.1")
# สร้าง Grid ของปุ่ม (เช่น 3 ปุ่มเรียงกัน)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("เวรยืนกลางคืน", use_container_width=True):
        st.session_state["mode"] = "night_duty"

with col2:
    if st.button("เวรเสาร์-อาทิตย์", use_container_width=True):
        st.session_state["mode"] = "weekend_duty"

with col3:
    if st.button("จัดยอดพิธี", use_container_width=True):
        st.session_state["mode"] = "ceremony_duty"
# ตรวจสอบและแสดง UI เฉพาะส่วนที่เลือก
mode = st.session_state.get("mode", None)



if mode == "night_duty":
    st.info("คุณเลือก: เวรยืนกลางคืน")
    st.markdown("https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU")

elif mode == "weekend_duty":
    st.info("คุณเลือก: เวรเสาร์-อาทิตย์")
    st.markdown("https://docs.google.com/spreadsheets/d/1ufm0LPa4c903jhlANKn_YqNyMtG9id0iN-tMHrhNRA8")

elif mode == "ceremony_duty":
    st.info("คุณเลือก: จัดยอดพิธี")
# อ่านไฟล์ Excel ชั้น4พัน4.xlsx
    @st.cache_data
    def load_data():
        return pd.read_excel("ชั้น4พัน4.xlsx")

    df = load_data()

    # อินพุตจากผู้ใช้
    ยอด_name = st.text_input("กรอกชื่อยอด")
    จำนวนคน = st.number_input("จำนวนคน", min_value=1, step=1)

    # Checkbox สำหรับกรองหน้าที่
    ตัวกรอง_หน้าที่ = st.multiselect("ไม่เลือกคนที่มีหน้าที่", ["ชั้นกรม", "ชั้นพัน", "ฝอ.1", "ฝอ.4", "ฝอ.5"])

    if st.button("จัดยอดและส่งออกไฟล์"):
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

        # ✅ ลบคอลัมน์ "ลำดับ" เดิม (ถ้ามี)
        if "ลำดับ" in selected_df.columns:
            selected_df = selected_df.drop(columns=["ลำดับ"])

        # เพิ่มคอลัมน์ลำดับ (เริ่มจาก 1)
        selected_df = selected_df.reset_index(drop=True)
        selected_df.index += 1
        if "ลำดับ" in selected_df.columns:
            selected_df = selected_df.drop(columns=["ลำดับ"])
        selected_df.insert(0, "ลำดับ", selected_df.index)
        
        # กำหนดลำดับคอลัมน์
        columns = ["ลำดับ", "ยศ", "ชื่อ", "สกุล", "ชั้นปีที่", "ตอน", "ตำแหน่ง", "สังกัด", "หมายเหตุ"]
        output_df = selected_df[columns]
        
        # สร้างไฟล์ Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "ยอดพิธี"
        
        # เขียนชื่อยอดและเว้นแถว
        ws.append([ยอด_name])
        ws.append([])
        
        # 👉 เขียนหัวตารางก่อน (เพื่อให้เซลล์ row=3 มีอยู่จริง)
        ws.append(columns)
        
        # 👉 Merge หัวข้อ “ยศ ชื่อ-สกุล” (B3-D3)
        ws.merge_cells(start_row=3, start_column=2, end_row=3, end_column=4)
        ws.cell(row=3, column=2).value = "ยศ ชื่อ-สกุล"
        ws.cell(row=3, column=2).alignment = Alignment(horizontal='center', vertical='center')
        
        # 👉 เขียนข้อมูลจาก DataFrame
        for r in dataframe_to_rows(output_df, index=False, header=False):
            ws.append(r)
        
        # จัดหัวข้อยอดให้อยู่กลาง
        ws.cell(row=1, column=1).alignment = Alignment(horizontal='center', vertical='center')
        
        # จัดข้อมูล ตั้งแต่แถวที่ 2 ยกเว้นคอลัมน์ B–D
        for row in ws.iter_rows(min_row=2):  # เริ่มจากแถวที่ 2
            for idx, cell in enumerate(row[:9]):  # คอลัมน์ A–I
                if idx < 1 or idx > 3:  # เว้นคอลัมน์ B (1), C (2), D (3)
                    cell.alignment = Alignment(horizontal='center', vertical='center')

        # 🔽 เรียงข้อมูลก่อน
        selected_df = selected_df.sort_values(by=["สังกัด", "ตำเเหน่ง", "ตอน"], ascending=True)
        
        # สร้างเส้นขอบบางๆ
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # ตั้งความกว้างคอลัมน์
        ws.column_dimensions['A'].width = 6
        ws.column_dimensions['B'].width = 5
        ws.column_dimensions['C'].width = 15  # ปรับตามความเหมาะสม
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 8
        ws.column_dimensions['F'].width = 8
        ws.column_dimensions['G'].width = 20
        ws.column_dimensions['H'].width = 15
        ws.column_dimensions['I'].width = 15

        ws.merge_cells('A1:I1')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        # จัดหัวตาราง (แถวที่ 1)
        for cell in ws[1]:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = thin_border
        
        for row in ws.iter_rows(min_row=1):  # รวมหัวตาราง
            if row[0].row == 2:
                continue  # ข้ามแถวที่ 2
            for cell in row:
                cell.border = thin_border



        
        output_filename = f"{ยอด_name}.xlsx"
        wb.save(output_filename)

        st.success(f"สร้างไฟล์สำเร็จ: {output_filename}")
        with open(output_filename, "rb") as f:
            st.download_button("ดาวน์โหลดไฟล์ Excel", f, file_name=output_filename)
