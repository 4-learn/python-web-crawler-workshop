from selenium.webdriver.chrome.service import Service
from shutil import which

from law_data_manager import LawDataManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_laws(manager):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_service = Service(executable_path=which("chromedriver"))
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    print("Accessing website...")

    try:
        driver.get("https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0060014")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "law-article"))
        )
        print("Page loaded successfully")

        rows = driver.find_elements(By.CLASS_NAME, "row")
        print(f"Found {len(rows)} rows")

        current_chapter = ""
        for index, row in enumerate(rows, 1):
            try:
                chapter_elements = row.find_elements(By.CLASS_NAME, "h3")
                if chapter_elements:
                    current_chapter = chapter_elements[0].text.strip()
                    print(f"\nNew chapter: {current_chapter}")
                    continue

                col_no_elements = row.find_elements(By.CLASS_NAME, "col-no")
                if not col_no_elements:
                    continue

                article_number = col_no_elements[0].text.strip()
                article_link = col_no_elements[0].find_element(By.TAG_NAME, "a").text.strip()
                content_element = row.find_element(By.CLASS_NAME, "law-article")
                content = content_element.text.strip()

                manager.laws_data.append({
                    'chapter': current_chapter,
                    'article_number': article_number,
                    'article_link': article_link,
                    'content': content
                })
                print(f"Processed: {article_number}")

            except Exception as e:
                print(f"\nError processing row {index}: {str(e)}")

        print("\n\nSample of scraped data (last 5 entries):")
        for item in manager.laws_data[-5:]:
            print("\n" + "="*50)
            print(f"Chapter: {item['chapter']}")
            print(f"Article Number: {item['article_number']}")
            print(f"Article Link: {item['article_link']}")
            print(f"Content: {item['content']}")

    finally:
        driver.quit()
        print("\nBrowser closed")

if __name__ == "__main__":
    print("Starting web scraper...")
    manager = LawDataManager("laws_data.json")
    scrape_laws(manager)
    manager.save_to_json()
    manager.show_laws_data()

    print("\n" + "="*50)
    print(f"Total articles scraped: {len(manager.laws_data)}")

    chapters = set(item['chapter'] for item in manager.laws_data if item['chapter'])
    print("\nChapters found:")
    for chapter in sorted(chapters):
        print(f"- {chapter}")