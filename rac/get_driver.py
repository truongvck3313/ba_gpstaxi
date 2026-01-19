# get_driver.py
from playwright.sync_api import sync_playwright
from typing import Optional, Tuple
import subprocess
import time
import os
import traceback
import tempfile
import psutil

def get_driver(headless: bool = False,
               downloads_path: Optional[str] = None,
               window_size=(1920, 1080),
               debug_mode: bool = False) -> Tuple:
    """
    Khởi tạo Playwright điều khiển Chrome thật (full màn hình, không ảnh hưởng Chrome cá nhân).
    - headless=False: mở Chrome thật qua CDP
    - debug_mode=True: giữ nguyên nếu lỗi
    """
    p = None
    try:
        # 1️⃣ Dọn Chrome CDP cũ nếu còn chạy
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    cmd = ' '.join(proc.info.get('cmdline') or [])
                    if '--remote-debugging-port=9222' in cmd:
                        proc.kill()
            except Exception:
                pass

        time.sleep(0.8)

        # 2️⃣ Mở Chrome thật qua subprocess (profile tạm)
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        temp_dir = os.path.join(tempfile.gettempdir(), "playwright_chrome_profile")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)

        launch_cmd = [
            chrome_path,
            "--remote-debugging-port=9222",
            f"--user-data-dir={temp_dir}",
            "--start-maximized",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-extensions",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
        ]

        print("🚀 Đang khởi chạy Chrome thật (full màn hình, profile tách biệt)...")
        subprocess.Popen(launch_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2.5)  # đợi Chrome mở hoàn tất

        # 3️⃣ Kết nối Playwright tới Chrome đó qua CDP
        p = sync_playwright().start()
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        # Lấy context đầu tiên
        context = browser.contexts[0] if browser.contexts else browser.new_context(ignore_https_errors=True,
                                                                                   accept_downloads=True)

        # Lấy tab đầu tiên, nếu không có thì tạo mới
        page = context.pages[0] if context.pages else context.new_page()


        # 4️⃣ Đặt thư mục download nếu có
        if downloads_path:
            try:
                context.set_default_downloads_path(downloads_path)
            except Exception:
                pass

        print("✅ Chrome full màn hình (qua CDP) đã sẵn sàng, không đụng Chrome cá nhân.")
        return p, browser, context, page

    except Exception as e:
        tb = traceback.format_exc()
        print("❌ Lỗi khi khởi tạo Chrome thật/CDP:", e)
        if debug_mode:
            print("⚠️ [DEBUG MODE] Giữ nguyên Chrome để debug.")
        else:
            try:
                if p:
                    p.stop()
            except Exception:
                pass
        raise RuntimeError(f"Không thể kết nối Chrome thật: {e}\n{tb}")
