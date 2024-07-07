from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time

from get_product_data import get_product_data
from lib.lib import recreate_directory


def process(driver: WebDriver):
    data_dir = 'datas'
    existing_folders = recreate_directory(data_dir)

    existing_codes = sorted([int(folder) for folder in existing_folders if folder.isdigit()])
    next_code = existing_codes[-1] + 1 if existing_codes else 1

    product_list_element = driver.find_element(By.CLASS_NAME, 'prdList')
    product_items = product_list_element.find_elements(By.XPATH, './li')

    for idx, product_item in enumerate(product_items[:]):
        product_list_element = driver.find_element(By.CLASS_NAME, 'prdList')
        product_items = product_list_element.find_elements(By.XPATH, './li')
        product_items[idx].click()
        
        code = str(next_code).zfill(4)
        next_code += 1
        get_product_data(driver, code=code)
        
        driver.back()

        time.sleep(1)
    
    time.sleep(2)