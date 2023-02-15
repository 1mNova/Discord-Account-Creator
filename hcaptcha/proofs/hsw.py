import os

from playwright.sync_api import sync_playwright

def get_proof(data):
    with sync_playwright() as page:
        browser = page.chromium.launch()
        page = browser.new_page()

        current = os.path.dirname(os.path.realpath(__file__))
        next_parent = os.path.abspath(os.path.join(current, os.pardir))
        final_parent = os.path.abspath(os.path.join(next_parent, os.pardir))
        
        page.add_script_tag(path=f"{final_parent}\\hcaptcha-js\\hsw.js")
        value = page.evaluate(f"hsw('{data}')")
        browser.close()

        return value