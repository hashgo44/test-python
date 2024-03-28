from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    return webdriver.Chrome()

def load_page(driver, url):
    driver.get(url)

def wait_for_element(driver, locator, timeout=10):
    """Attend que l'élément spécifié soit visible"""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def click_element(element):
    """Clique sur un élément"""
    element.click()

def test_url(url, expected_url):
    """Vérifie si l'URL actuelle correspond à l'URL attendue"""
    if url == expected_url:
        print(f"L'URL est correcte : {expected_url}")
    else:
        print(f"L'URL n'est pas correcte : {expected_url}")

driver = init_driver()

load_page(driver, "http://localhost:3000")

connexion_link = wait_for_element(driver, (By.CSS_SELECTOR, 'a[href="/signin"]'))
signup_link = wait_for_element(driver, (By.CSS_SELECTOR, 'a[href="/signup"]'))
resources_link = wait_for_element(driver, (By.CSS_SELECTOR, 'a[href="/resources"]'))
main_link = wait_for_element(driver, (By.CSS_SELECTOR, 'a[href="/"]'))

try:
    # test signin page
    click_element(connexion_link)
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:3000/signin"))
    current_url = driver.current_url
    test_url(current_url, "http://localhost:3000/signin")

    # test signup page
    click_element(signup_link)
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:3000/signup"))
    current_url = driver.current_url
    test_url(current_url, "http://localhost:3000/signup")

    # test resources page
    click_element(resources_link)
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:3000/resources"))
    current_url = driver.current_url
    test_url(current_url, "http://localhost:3000/resources")

    # test main page
    click_element(main_link)
    WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:3000/"))
    current_url = driver.current_url
    test_url(current_url, "http://localhost:3000/")

except Exception as e:
    print("Une erreur s'est produite :", e)

finally:
    driver.quit()