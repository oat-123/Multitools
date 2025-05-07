import streamlit as st
import webbrowser
import subprocess
import pandas as pd
import random
from collections import defaultdict
from openpyxl.styles import Alignment, Border, Side

st.title("แอปผู้ช่วยจัดเวร")


option = st.selectbox(
    "เลือกหน้าที่ที่ต้องการทำ",
    [
        "เลือกเมนู...",
        "เวรยืนกลางคืน",
        "เวรเสาร์อาทิตย์",
        "จัดยอดพิธีต่างๆ (รันอัตโนมัติ)"
    ]
)

if option == "เวรยืนกลางคืน":
    st.success("เปิด Google Sheet: เวรยืนกลางคืน")
    webbrowser.open("https://docs.google.com/spreadsheets/d/1PjT38W2Zx7KV764yv9Vjwo9i0TJPacRI0iUGzP0ItAU")

elif option == "เวรเสาร์อาทิตย์":
    st.success("เปิด Google Sheet: เวรเสาร์อาทิตย์")
    webbrowser.open("https://docs.google.com/spreadsheets/d/1ufm0LPa4c903jhlANKn_YqNyMtG9id0iN-tMHrhNRA8")

elif option == "จัดยอดพิธีต่างๆ (รันอัตโนมัติ)":
# อ่านไฟล์ Excel ชั้น4พัน4.xlsx
    @st.cache_data
    def load_data():
        return pd.read_excel("ชั้น4พัน4.xlsx")

    df = load_data()

    st.title("จัดยอดพิธีอัตโนมัติ")

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

        # เพิ่มคอลัมน์ใหม่
        selected_df.insert(0, "ลำดับ", selected_df.index)


        # คอลัมน์ที่ต้องการ
        columns = ["ลำดับ", "ยศ", "ชื่อ", "สกุล", "ชั้นปีที่", "ตอน", "ตำแหน่ง", "สังกัด", "หมายเหตุ"]
        output_df = selected_df[columns]

        # สร้างไฟล์ Excel
        from openpyxl import Workbook
        from openpyxl.utils.dataframe import dataframe_to_rows

        wb = Workbook()
        ws = wb.active
        ws.title = "ยอดพิธี"

        ws.append([ยอด_name])  # หัวข้อยอด
        ws.append([])           # เว้น 1 แถว

        for r in dataframe_to_rows(output_df, index=False, header=True):
            ws.append(r)

        # จัดหัวตาราง (แถวที่ 1) ให้กึ่งกลางทั้งหมด
        for cell in ws[1]:
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # จัดข้อมูล ตั้งแต่แถวที่ 2 ยกเว้นคอลัมน์ B–D
        for row in ws.iter_rows(min_row=2):  # เริ่มจากแถวที่ 2
            for idx, cell in enumerate(row[:9]):  # คอลัมน์ A–I
                if idx < 1 or idx > 3:  # เว้นคอลัมน์ B (1), C (2), D (3)
                    cell.alignment = Alignment(horizontal='center', vertical='center')

        # สร้างเส้นขอบบางๆ
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # ตั้งความกว้างคอลัมน์
        ws.column_dimensions['A'].width = 5
        ws.column_dimensions['B'].width = 5
        ws.column_dimensions['C'].width = 15  # ปรับตามความเหมาะสม
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 10
        ws.column_dimensions['F'].width = 10
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
