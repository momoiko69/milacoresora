import urllib.request
import re
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': '*/*'}

urls = [
    'https://www.linkvegastheme.com/category/windows-11-theme/',
    'https://www.linkvegastheme.com/category/windows-11-theme/page/2/',
    'https://www.linkvegastheme.com/category/windows-11-theme/page/3/',
    'https://www.linkvegastheme.com/category/windows-11-theme/page/4/'
]

presets_dir = r'C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable\Presets_LinkVegas'
folders = os.listdir(presets_dir)

def norm(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

all_cards = []
for page_num, u in enumerate(urls, 1):
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        articles = re.findall(r'<article[\s\S]*?</article>', html)
        print(f"Page {page_num}: found {len(articles)} articles")
        for a in articles:
            m_link = re.search(r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', a)
            m_img = re.search(r'<img[^>]*src="([^"]+)"', a)
            if not m_img:
                m_img = re.search(r'data-src="([^"]+)"', a)
            if m_link and m_img:
                all_cards.append({
                    'title': m_link.group(2).strip(),
                    'post_url': m_link.group(1).strip(),
                    'img_url': m_img.group(1).strip()
                })
    except Exception as e:
        print(f"Error page {page_num}: {e}")

print(f"Total cards captured: {len(all_cards)}")

def process_card(card):
    title = card['title']
    img_url = card['img_url']
    
    # Remove thumbnail dimensions to get original full-res image
    # e.g., ...-300x169.webp -> ....webp
    full_img_url = re.sub(r'-\d+x\d+\.(webp|jpg|jpeg|png)$', r'.\1', img_url)
    
    t_norm = norm(title)
    target_folder = None
    for f in folders:
        f_norm = norm(f)
        if f_norm == t_norm or f_norm in t_norm or t_norm in f_norm:
            target_folder = os.path.join(presets_dir, f)
            break
            
    if not target_folder:
        return f"Skipped (no folder match): {title}"

    wp_out = os.path.join(target_folder, 'wallpaper.jpg')
    if os.path.exists(wp_out) and os.path.getsize(wp_out) > 15000:
        return f"Already exists: {os.path.basename(target_folder)}"

    # Try full-res first, fallback to original img_url
    for try_url in [full_img_url, img_url]:
        try:
            req = urllib.request.Request(try_url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
            if len(data) > 5000:
                temp_p = os.path.join(target_folder, 'temp_dl')
                with open(temp_p, 'wb') as tf:
                    tf.write(data)
                im = Image.open(temp_p)
                im = im.convert('RGB')
                im.save(wp_out, 'JPEG', quality=95)
                os.remove(temp_p)
                return f"SUCCESS: {os.path.basename(target_folder)} ({os.path.getsize(wp_out)} bytes)"
        except Exception:
            continue
            
    return f"Failed to download: {title}"

print("Starting multithreaded downloads...")
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_card, c) for c in all_cards]
    for fut in as_completed(futures):
        print(fut.result())

print("ALL LINKVEGAS WALLPAPERS SYNCHRONIZED!")
