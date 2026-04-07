import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

import openpyxl

EXCEL_PATH  = os.getenv('EXCEL_PATH',  r'D:\Users\user\Desktop\蝦皮影片專案\蝦皮關鍵字選品_2026年3-4月new.xlsx')
FINAL_DIR   = os.getenv('FINAL_DIR',   r'D:\Users\user\Desktop\蝦皮影片專案\output_final')
COL_STATUS  = int(os.getenv('COL_STATUS', '10'))

wb = openpyxl.load_workbook(EXCEL_PATH)
ws = wb.active
cleared = 0

for row in ws.iter_rows(min_row=2):
    status_cell = row[COL_STATUS - 1]
    if status_cell.value == '影片完成':
        status_cell.value = 'clips_ok(3)'  # 保留clips_ok，只清影片完成
        cleared += 1

wb.save(EXCEL_PATH)
print(f'清除 {cleared} 筆「影片完成」→ 改回 clips_ok(3)')
