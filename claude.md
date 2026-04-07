# 蝦皮自動化工具 - 專案說明

## 核心裝置
- **Samsung Galaxy A52s 5G**（Android 11，1080x2400）
- ADB 連線方式：WiFi（TCP/IP），port 5555
- **IP 會隨手機重開機變動**，每次上傳前必須確認 `.env` 的 `PHONE_IP`

---

## 環境變數（.env）— 公司電腦版
所有路徑集中在 `.env`，不寫死在程式碼。

```
EXCEL_PATH=D:\Users\user\Desktop\蝦皮影片專案\蝦皮關鍵字選品_2026年3-4月new.xlsx
OUTPUT_DIR=D:\Users\user\Desktop\蝦皮影片專案\output_videos
FINAL_DIR=D:\Users\user\Desktop\蝦皮影片專案\output_final
BGM_DIR=D:\Users\user\Desktop\蝦皮影片專案\music
COOKIES_FILE=D:\Users\user\Desktop\蝦皮影片專案\shopee_cookies.json
GEMINI_KEY=AIzaSyDch3A7cNovcocVUBeSBIzngiKDGN9A6UE
START_ROW=22
COL_NAME=2, COL_LINK=3, COL_COPY=8, COL_TITLE=9, COL_STATUS=10
TTS_VOICE=zh-TW-HsiaoChenNeural
```

`.env` 已加入 `.gitignore`，不會被 commit。

---

## 主要程式（目前版本）

| 檔案 | 用途 |
|------|------|
| `shopee_video_maker_home3.py` | **抓影片主程式**，undetected_chromedriver，抓評論影片存到 `_clips_XXX/` |
| `shopee_video_producer.py` | **後製主程式 v2**，讀 clips → resize → 合併 → TTS旁白 + 逐句字幕 + BGM |
| `clear_status.py` | 清除 Excel 狀態欄（「影片完成」→「clips_ok(3)」），重跑用 |
| `shopee_upload_a52s.py` | 蝦皮短影音批次上傳（A52s 專用，ADB WiFi） |
| `dump_gallery.py` | Debug 用，傾印 UI hierarchy 找座標 |

**廢棄不用（勿刪，留著備查）：**
`shopee_video_maker_home.py` / `shopee_video_maker_home2.py`

---

## 兩階段工作流程

```
Step 1 抓影片
  python shopee_video_maker_home3.py
  → Chrome 彈出 → 登入蝦皮 → 按 Enter 繼續
  → 結果存到 output_videos/_clips_XXX/clip_00~02.mp4
  → Excel 狀態寫 clips_ok(3)

Step 2 後製
  python shopee_video_producer.py
  → 讀 _clips_XXX/ → FFmpeg resize 1080x1920
  → edge-tts 逐句生成旁白 MP3
  → 字幕貼在畫面垂直正中央（逐句同步）
  → BGM 25% + TTS 100% 混音
  → 影片循環補足 TTS 時長 + 1.5s
  → 輸出 output_final/XXX_品名.mp4
  → Excel 狀態寫「影片完成」
```

---

## 後製程式重點設定（shopee_video_producer.py v2）

| 項目 | 設定 |
|------|------|
| TTS 聲音 | `zh-TW-HsiaoChenNeural`（.env 的 TTS_VOICE 可換） |
| 字幕位置 | 畫面垂直正中央 `(VIDEO_H - box_h) // 2` |
| 字幕顯示 | 一句一句，與 TTS 同步（start_time + duration） |
| 影片無標題文字 | ✅ 標題只用於上傳平台，不疊在影片上 |
| BGM 音量 | 25%（TTS 100%） |
| 影片尺寸 | 1080 × 1920（直式） |
| rate-limit 防護 | 每句 TTS 間隔 0.8s，失敗最多重試 3 次 |
| 斷句規則 | 以 `。！？` 切分，純標點/無中文的句子過濾掉 |

---

## Excel 欄位設定

| 欄位 | COL 編號 | 內容 |
|------|----------|------|
| 品名 | 2 | 商品名稱 |
| 蝦皮連結 | 3 | 商品短網址（affiliate） |
| 文案 | 8 | 旁白內容（TTS + 字幕來源） |
| 標題 | 9 | 上傳平台用標題（不出現在影片） |
| 狀態 | 10 | clips_ok(3) / 影片完成 / 後製失敗 |

---

## 已知問題與解法

| 問題 | 解法 |
|------|------|
| TTS 奇偶句失敗（rate-limit） | 每句間隔 0.8s + 重試 3 次 |
| TTS 純標點句失敗 | split_sentences 過濾無中文句 |
| PermissionError WinError 32 | `ignore_cleanup_errors=True` + `gc.collect()` |
| ChromeDriver 版本不符 | 下載 ChromeDriver 147 放 `C:\ffmpeg\bin\` |
| 短網址無法取得 shopid/itemid | driver.get() 先導航，再從 current_url 取 ID |
| clear_status 重跑 | `python clear_status.py` 清狀態後再跑 producer |

---

## 網站專案（smileladypicks.com）

**路徑：** `D:\Users\user\Desktop\蝦皮影片專案\sites\smileladypicks\`
**部署：** Cloudflare Pages（GitHub repo: z8032332-stack/smileladypicks）
**Hugo 版本：** v0.159.1 extended
**主題：** PaperMod（git submodule）

### 網站結構

```
content/
├── about.md                    關於我：微笑小姐是誰
├── posts/
│   ├── shopee-automation.md    蝦皮分潤30天：從手動到自動化
│   ├── shopee-is-it-for-you.md 這個副業適不適合你
│   └── shopee-30-days.md       日入$100真實真相（主打文）
├── beauty/
│   ├── hair-care.md            護髮好物（舊文恢復）
│   └── eye-makeup.md           眼部彩妝（舊文恢復）
├── home/
│   └── sleep-goods.md          睡眠改善好物（舊文恢復）
└── daily/
    ├── baby-shampoo.md         兒童洗髮精推薦
    ├── bath-mat.md             兒童浴室防滑墊
    └── bath-toys.md            浴室洗澡玩具
```

### 首頁版型（layouts/index.html）
4 區塊：Hero → 副業入口🔥 → 選物🛍️ → 輕教學💡

### 待辦

| 項目 | 狀態 |
|------|------|
| 域名換為 smileladypicks.com | ✅ 完成 |
| 舊文章 3 篇恢復 | ✅ 完成 |
| 新文章 7 篇上線 | ✅ 完成 |
| H1/H2/H3 + TOC + keywords | ✅ 完成 |
| Cloudflare 自訂域名綁定 | ✅ 用戶自行完成 |
| Google Analytics GA4 接入 | ⏳ 待辦（hugo.toml 第8行填 G-XXXXXXXXXX） |

### GA4 接入步驟（下次做）
1. 前往 analytics.google.com → 建立資源 → 取得 `G-XXXXXXXXXX`
2. 編輯 `hugo.toml` 第 8 行：`ID = "G-XXXXXXXXXX"`
3. `hugo --minify` → `git add -A` → `git commit` → `git push`

---

## 注意事項
- 手機解鎖 PIN：`0000`
- S25 FE 使用前確認手機 IP（DHCP 每次可能不同）
- `.env` 不進 git
- 影片無標題文字，標題只用於上傳蝦皮時填入
