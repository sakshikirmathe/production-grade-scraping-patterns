# real_captcha_solver.py
# Solves reCAPTCHA v2 using 2Captcha and Playwright

import time
import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CAPTCHA_API_KEY")  # 2Captcha API key from .env
PAGE_URL = "https://2captcha.com/demo/recaptcha-v2"
SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"  # Demo sitekey from 2Captcha

def solve_captcha(sitekey, pageurl):
    print("[+] Sending CAPTCHA to 2Captcha...")
    url = f"http://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={sitekey}&pageurl={pageurl}&json=1"
    resp = requests.get(url).json()

    if resp.get("status") != 1:
        raise Exception("Failed to submit CAPTCHA to 2Captcha")

    captcha_id = resp["request"]
    print(f"[+] CAPTCHA submitted. ID: {captcha_id}")

    # Poll for result
    result_url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
    for _ in range(20):
        time.sleep(5)
        res = requests.get(result_url).json()
        if res.get("status") == 1:
            print("[+] CAPTCHA solved.")
            return res["request"]
        print("[.] Waiting for CAPTCHA to be solved...")

    raise TimeoutError("CAPTCHA solving timed out")

def main():
    token = solve_captcha(SITE_KEY, PAGE_URL)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(PAGE_URL)

        # Inject token into response field expected by Google
        page.evaluate(f'''
            document.getElementById("g-recaptcha-response").innerHTML = "{token}";
        ''')
        time.sleep(1)  # Let token register in DOM

        # Submit the form
        page.click("button[type='submit']")
        print("[+] Submitted form with solved CAPTCHA.")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    main()