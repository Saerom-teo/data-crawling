from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time

from get_product_data import get_product_data
from lib.lib import recreate_directory


def process(driver: WebDriver):
    data_dir = 'datas'
    recreate_directory(data_dir)

    product_list_element = driver.find_element(By.CLASS_NAME, 'prdList')
    product_items = product_list_element.find_elements(By.XPATH, './li')
    for idx, product_item in enumerate(product_items):
        product_list_element = driver.find_element(By.CLASS_NAME, 'prdList')
        product_items = product_list_element.find_elements(By.XPATH, './li')
        product_items[idx].click()
        
        code = str(idx + 1).zfill(4)
        get_product_data(driver, code=code)
        
        driver.back()

        time.sleep(1)
    
    time.sleep(2)