from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

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
        print(f"Test passed: {expected_url}")
    else:
        print(f"L'URL n'est pas correcte : {expected_url}")
  
def test_page_load_time(driver, url):
    """Teste le temps d'affichage de la page"""
    start_time = time.time()
    load_page(driver, url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    end_time = time.time()
    display_time = end_time - start_time
    print(f"Temps d'affichage de la page {url}: {display_time} secondes")

def test_api_connection(url, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'PUT':
            headers = {
                "accept": "*/*",
                "Content-Type": "application/json"
            }
            response = requests.put(url, headers=headers, json=data)
        
        response.raise_for_status()
        if response.status_code == 200:
            print(f"Test passed: {url}, method: {method}, Status : {response.status_code}")
        else:
            print(f"Test failed: {url}, method: {method},Status : {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("error :", e)

def test_api_with_wrong_data(url, method='PUT', data=None):
    try:
        if method == 'PUT':
            headers = {
                "accept": "*/*",
                "Content-Type": "application/json"
            }
            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 500:
                print(f"Test passed: {url}, method: {method}, Status : {response.status_code}")
            else:
                print(f"Test failed: {url}, method: {method},Status : {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("error :", e)

driver = init_driver()

test_page_load_time(driver, "http://localhost:3000/")

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

    api_url = "https://8443-ilanlo-apiressourcesrel-uz6mpifos28.ws-eu110.gitpod.io/ressources"
    test_api_connection(api_url)

    url = "https://8443-ilanlo-apiressourcesrel-uz6mpifos28.ws-eu110.gitpod.io/ressource"
    data = {
        "id": 1,
        "proprietaire": 1,
        "titre": "Test contenu from romain",
        "contenu": "Test contenu from romain"
    }
    test_api_connection(url, method='PUT', data=data)

    url = "https://8443-ilanlo-apiressourcesrel-uz6mpifos28.ws-eu110.gitpod.io/ressource"
    data = {
        "id": 0,
        "proprietaire": 0,
        "titre": "Test contenu from romain",
        "contenu": "Test contenu from romain"
    }
    test_api_with_wrong_data(url, method='PUT', data=data)

except Exception as e:
    print("Une erreur s'est produite :", e)

finally:
    driver.quit()