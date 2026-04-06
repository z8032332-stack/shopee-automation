# 蝦皮自動化工具 - 專案說明

## 核心裝置
- **Samsung Galaxy A52s 5G**（Android 11，1080x2400）
- ADB 連線方式：WiFi（TCP/IP），port 5555
- **IP 會隨手機重開機變動**，每次上傳前必須確認 `.env` 的 `PHONE_IP`

## 環境變數（.env）
所有路徑與 IP 集中在 `.env`，不寫死在程式碼。

| 變數 | 說明 |
|------|------|
| `PHONE_IP` | 手機 ADB WiFi 地址（192.168.x.x:5555），**重開機後要改** |
| `CHROME_PATH` | Chrome 瀏覽器執行檔路徑 |
| `EXCEL_PATH` | 蝦皮分潤清單 Excel 路徑（已移至外部資料夾） |
| `EXCEL_INDEX` | 欄位 JSON 對應，留空=自動用標題列（見下方說明） |
| `ADB_PATH` | adb.exe 路徑 |
| `VIDEO_DIR` | 本機影片輸出目錄 |
| `SCREENSHOT_DIR` | 截圖儲存目錄 |

## 家裡 vs 公司設定差異

| 項目 | 家裡電腦 | 公司電腦 |
|------|----------|----------|
| EXCEL_PATH | D:\Users\user\Downloads\Annie\... | 另一路徑，改 .env |
| EXCEL_INDEX | 留空（標題列自動對應） | 若欄位順序不同，填 JSON |
| ADB_PATH | D:\platform-tools\adb.exe | 依實際安裝位置 |

**EXCEL_INDEX 範例**（公司電腦欄位位置不同時）：
```
EXCEL_INDEX={"編號":0,"品名":2,"關鍵字文案":5}
```
索引為 0-based（第一欄=0）。

## 主要程式

| 檔案 | 用途 |
|------|------|
| `shopee_upload_a52s.py` | 蝦皮短影音批次上傳主程式（A52s 專用） |
| `dump_gallery.py` | Debug 用，傾印 UI hierarchy 找座標 |

## 注意事項
- Excel 已移至外部資料夾，路徑從 `EXCEL_PATH` 讀取
- `.env` 已加入 `.gitignore`，不會被 commit
- 手機解鎖 PIN 預設 `0000`
- 影片檔命名規則：`row{N:03d}_final.mp4`（N = Excel 行號，從 2 起）
