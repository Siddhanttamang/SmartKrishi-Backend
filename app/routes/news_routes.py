from flask import jsonify, Blueprint
from selenium import webdriver
from flask_restful import Api
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

news_bp = Blueprint('news_bp', __name__)
api = Api(news_bp)

# Simple in-memory cache
cache = {
    "data": [],
    "last_updated": 0,
    "ttl": 3000 
}

def scrape_vegetables():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)

    url = "https://nepalipatro.com.np/vegetables"
    driver.get(url)

    # Use WebDriverWait instead of time.sleep
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "vegetable_table"))
        )
    except Exception:
        driver.quit()
        raise Exception("Failed to load vegetable table.")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    vegetables = []
    table = soup.find("table", {"id": "vegetable_table"})
    if table:
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 4:
                name = cols[0].get_text(strip=True)
                min_price = cols[2].get_text(strip=True)
                max_price = cols[3].get_text(strip=True)

                vegetables.append({
                    "name": name,
                    "price": f"{min_price}-{max_price}"
                })
    return vegetables

@news_bp.route('/news', methods=['GET'])
def get_vegetables():
    now = time.time()
    # Use cache if within TTL
    if now - cache["last_updated"] < cache["ttl"]:
        return jsonify({
            "status": "success",
            "source": "cache",
            "data": cache["data"]
        }), 200
    try:
        data = scrape_vegetables()
        # Save to cache
        cache["data"] = data
        cache["last_updated"] = now
        return jsonify({
            "status": "success",
            "source": "scraped",
            "data": data
        }), 1000
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
