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

## shopee_video_maker_home2.py 開發狀態（2026-04-06）

**目前卡關：評論影片抓取回傳 0 個**

| 項目 | 狀態 |
|------|------|
| Playwright connect_over_cdp | 棄用（Python 3.14 + Chrome 146 不相容） |
| 改用 requests + browser_cookie3 | 完成，但需要系統管理員執行才能讀 cookie |
| Edge cookie 讀取 | 改成先嘗試 Edge 再 fallback Chrome |
| 評論影片 API | 連得到但回傳 0，疑似 cookie 未帶入 session |
| 字幕逐句顯示 | 完成（以句號切分，FFmpeg drawtext，畫面正中央） |
| 標題疊字 | 已移除 |
| 環境變數隔離 | 完成（EXCEL_PATH / VIDEO_DIR / BGM_DIR / FFMPEG_PATH / GEMINI_KEY）|

**下次繼續方向：確認 cookie 是否正確帶入 API 請求（印出 cookie 數量與 SPC_EC 是否存在）**

## Excel 影片抓取進度（2026-04-06）

- **處理到 Row 21**，Row 22 以後尚未有影片
- **以下 Row 無評論影片**（跳過）：Row 1、2、3、6、7、8、22以後全部
- 有影片的：Row 4、5、9、10、11、12、13、14、15、16、17、18、19、20、21（待驗證）
- 明天繼續從 **Row 22** 開始抓

## 注意事項
- Excel 已移至外部資料夾，路徑從 `EXCEL_PATH` 讀取
- `.env` 已加入 `.gitignore`，不會被 commit
- 手機解鎖 PIN 預設 `0000`
- 影片檔命名規則：`row{N:03d}_final.mp4`（N = Excel 行號，從 2 起）
