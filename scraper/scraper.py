# scraper/scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_ecourts(cnr_number):
    driver = webdriver.Chrome()  # make sure chromedriver.exe is in PATH
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")

    # Select "CNR" option
    driver.find_element(By.ID, "case_type").send_keys("CNR")

    # Enter CNR number
    driver.find_element(By.ID, "cnr_number").send_keys(cnr_number)

    # Wait for user to enter Captcha manually and press Check
    print("Please solve the captcha in the browser window manually...")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "results"))
    )

    # Parse results
    soup = BeautifulSoup(driver.page_source, "html.parser")
    results_div = soup.find(id="results")
    if results_div:
        case_number = results_div.find("span", {"id": "case_number"}).text
        listed_date = results_div.find("span", {"id": "listed_date"}).text
        serial_number = results_div.find("span", {"id": "serial_number"}).text
        court_name = results_div.find("span", {"id": "court_name"}).text
        pdf_available = bool(results_div.find("a", {"id": "pdf_link"}))
        driver.quit()
        return {
            "Case Number": case_number,
            "Listed Date": listed_date,
            "Serial Number": serial_number,
            "Court Name": court_name,
            "PDF Available": pdf_available
        }
    driver.quit()
    return None
