from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def clean_name(name):
    name = name.strip()
    # Remove 'per kg', 'Per KG', etc. (case-insensitive)
    name = re.sub(r'\s*[Pp]er\s*[Kk][Gg]\s*$', '', name)
    return name.strip()

def scrape_vegetables():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    url = "https://nepalipatro.com.np/vegetables"
    driver.get(url)

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
                name = clean_name(cols[0].get_text(strip=True))
                min_price = cols[2].get_text(strip=True)
                max_price = cols[3].get_text(strip=True)

                vegetables.append({
                    "name": name,
                    "price": f"{min_price}-{max_price}"
                })
    return vegetables
