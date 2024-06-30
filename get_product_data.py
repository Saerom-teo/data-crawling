from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import os

from lib.image_download import image_download, combine_images_vertically
from lib.lib import extract_number


def get_product_data(driver: WebDriver, data_dir: str='datas',code: str='0001'):
    # Name
    product_name_element = driver.find_element(By.CLASS_NAME, 'product_name_css')
    name = product_name_element.text

    # Price
    try:
        price_element = driver.find_element(By.ID, 'span_product_price_custom')
        price = extract_number(price_element.text)
    except NoSuchElementException:
        price_element = driver.find_element(By.ID, 'span_product_price_text')
        price = extract_number(price_element.text)

    # brand
    logo_element = driver.find_element(By.CLASS_NAME, 'topLogo')
    brand_element = logo_element.find_element(By.TAG_NAME, 'span')
    brand = brand_element.text.replace(' ▸', '')

    # ThumbImages
    thumb_image_elements = driver.find_elements(By.CLASS_NAME, 'ThumbImage')

    # DetailImages
    div_element = driver.find_element(By.ID, 'prdDetailContentLazy')
    detail_image_elements = div_element.find_elements(By.CSS_SELECTOR, 'img')

    # Path
    data_path = os.path.join(data_dir, code)
    os.makedirs(data_path, exist_ok=True)

    # Image download
    thumb_images = image_download(thumb_image_elements, 'thumbImage', download_folder=data_path)
    detail_images = image_download(detail_image_elements, 'detailImage', download_folder=data_path)

    combine_images_vertically(detail_images)

    data = {
        'name': name,
        'price': price,
        'brand': brand,
        'thumbnail': thumb_images,
        'detail': detail_images,
    }

    # JSON 파일로 저장
    output_path = os.path.join(data_path, 'product_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"📌 {code} - Thumbnail images: {len(thumb_images)}, Detail images: {len(detail_images)}, Data saved to: {output_path}")