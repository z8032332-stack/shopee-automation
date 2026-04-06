# -*- coding: utf-8 -*-
"""
Debug: dump Shopee gallery UI hierarchy to find first video thumbnail coordinates.
Usage: python dump_gallery.py
"""
import subprocess, time, os, sys
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ADB   = os.getenv("ADB_PATH",       r"D:\platform-tools\adb.exe")
DEV   = os.getenv("PHONE_IP",       "192.168.0.30:5555")
SSDIR = os.getenv("SCREENSHOT_DIR", r"D:\Users\user\Desktop\蝦皮影片專案\screenshots")

def adb(cmd, timeout=30):
    r = subprocess.run(f'"{ADB}" -s {DEV} {cmd}', shell=True,
                       capture_output=True, timeout=timeout)
    return (r.stdout + r.stderr).decode('utf-8', errors='replace')

def ss(name):
    os.makedirs(SSDIR, exist_ok=True)
    p = os.path.join(SSDIR, f"{name}.png")
    subprocess.run(f'"{ADB}" -s {DEV} exec-out screencap -p',
                   shell=True, stdout=open(p,'wb'), timeout=15)
    print(f"  [screenshot] {p}")

def dump_ui(name):
    adb("shell uiautomator dump /sdcard/uidump.xml")
    time.sleep(1)
    out_path = os.path.join(SSDIR, f"{name}.xml")
    adb(f"pull /sdcard/uidump.xml \"{out_path}\"")
    print(f"  [dump] {out_path}")
    return out_path

import uiautomator2 as u2

print("連線...")
d = u2.connect(DEV)
print(f"  {d.info['productName']}")

print("\n開啟蝦皮...")
adb("shell monkey -p com.shopee.tw -c android.intent.category.LAUNCHER 1")
time.sleep(5)
ss("debug_01_shopee_open")

print("\n進入短影音 tab...")
d.press("back")
time.sleep(1)

# Navigate to create short video
btn = d(textContains='直播短影音')
if btn.exists(timeout=5):
    btn.click()
    print("  ✓ 點到直播短影音 tab")
else:
    d.click(540, 2205)
    print("  座標 fallback: (540, 2205)")
time.sleep(3)
ss("debug_02_shortvideo_tab")

print("\n點 + 按鈕...")
found = False
for desc in ['拍攝', '建立', '新增', '短片']:
    el = d(description=desc)
    if el.exists(timeout=2):
        el.click()
        found = True
        print(f"  ✓ 點到 description='{desc}'")
        break
if not found:
    d.click(1000, 157)
    print("  座標 fallback: (1000, 157)")
time.sleep(3)
ss("debug_03_after_plus")

print("\n點媒體庫...")
for txt in ['媒體庫', '相簿', '圖庫']:
    el = d(textContains=txt)
    if el.exists(timeout=3):
        el.click()
        print(f"  ✓ 點到 '{txt}'")
        break
else:
    d.click(862, 1899)
    print("  座標 fallback: (862, 1899)")
time.sleep(3)
ss("debug_04_gallery_open")

print("\n點短影音 tab...")
for txt in ['短影音', '影片']:
    el = d(textContains=txt)
    if el.exists(timeout=3):
        # show bounds before clicking
        info = el.info
        print(f"  找到 '{txt}' bounds={info['bounds']}")
        el.click()
        break
else:
    d.click(540, 170)
    print("  座標 fallback: (540, 170)")
time.sleep(3)
ss("debug_05_videotab")

print("\n== Dump UI hierarchy ==")
dump_path = dump_ui("debug_gallery_dump")

print("\n== 分析 clickable 元素 ==")
import xml.etree.ElementTree as ET
try:
    tree = ET.parse(dump_path)
    clickable_nodes = []
    for node in tree.iter('node'):
        if node.attrib.get('clickable') == 'true':
            bounds = node.attrib.get('bounds','')
            cls    = node.attrib.get('class','')
            text   = node.attrib.get('text','')
            desc   = node.attrib.get('content-desc','')
            # parse bounds [x1,y1][x2,y2]
            import re
            m = re.findall(r'\d+', bounds)
            if len(m) == 4:
                x1,y1,x2,y2 = map(int,m)
                cx,cy = (x1+x2)//2, (y1+y2)//2
                clickable_nodes.append((y1, x1, cls, text, desc, bounds, cx, cy))
    clickable_nodes.sort()
    print(f"  共 {len(clickable_nodes)} 個 clickable 元素：")
    for i, (y1, x1, cls, text, desc, bounds, cx, cy) in enumerate(clickable_nodes):
        short_cls = cls.split('.')[-1]
        print(f"  [{i}] {short_cls:30s} text={text[:20]:20s} desc={desc[:20]:20s} bounds={bounds} center=({cx},{cy})")
except Exception as e:
    print(f"  XML parse error: {e}")

print("\n截完整截圖...")
ss("debug_06_final")
print("\n完成！請把 screenshots 資料夾裡的 debug_*.png 和 debug_gallery_dump.xml 給我看。")
