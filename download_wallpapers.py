import urllib.request
import re
import json
import os
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept': '*/*'}

catalog_file = r'C:\Users\k69-admin\.gemini\MilaCoreWinOS\themes_catalog.json'
with open(catalog_file, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

presets_dir = r'C:\Users\k69-admin\.gemini\MilaCore_ThemeEngine_Portable\Presets_LinkVegas'
folders = os.listdir(presets_dir)

def norm(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

def download_theme_wp(url, dest_folder):
    wp_out = os.path.join(dest_folder, 'wallpaper.jpg')
    if os.path.exists(wp_out) and os.path.getsize(wp_out) > 10000:
        return True

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        imgs = re.findall(r'https?://[^\s\"\'<>]+\.(?:webp|jpg|jpeg|png)', html)
        candidates = [img for img in imgs if 'uploads' in img and not any(k in img.lower() for k in ['logo', 'avatar', '150x150', '300x169'])]
        if not candidates:
            candidates = [img for img in imgs if 'uploads' in img and not any(k in img.lower() for k in ['logo', 'avatar'])]
        
        if candidates:
            best = sorted(candidates, key=lambda x: ('1920' in x or '1536' in x or '1024' in x or 'x2' in x or not any(sz in x for sz in ['-300x', '-768x', '-1024x'])), reverse=True)[0]
            print(f'Fetching: {best} -> {os.path.basename(dest_folder)}')
            img_req = urllib.request.Request(best, headers=headers)
            with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                data = img_resp.read()
            
            temp_path = os.path.join(dest_folder, 'temp_wp')
            with open(temp_path, 'wb') as f:
                f.write(data)
            
            im = Image.open(temp_path)
            im = im.convert('RGB')
            im.save(wp_out, 'JPEG', quality=95)
            os.remove(temp_path)
            print(f'SUCCESS: {wp_out} ({os.path.getsize(wp_out)} bytes)')
            return True
    except Exception as e:
        print(f'Error for {url}: {e}')
        return False

# Match and download
success_count = 0
for item in catalog:
    t_norm = norm(item['title'])
    for f in folders:
        f_norm = norm(f)
        if f_norm in t_norm or t_norm in f_norm:
            dest = os.path.join(presets_dir, f)
            if download_theme_wp(item['url'], dest):
                success_count += 1
            break

print(f'Finished! Successfully prepared {success_count} wallpapers.')
