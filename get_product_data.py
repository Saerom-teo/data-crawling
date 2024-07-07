from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import os

from lib.image_download import image_download, combine_images_vertically
from lib.lib import extract_number
from lib.upload_image import upload_to_s3


def get_product_data(driver: WebDriver, data_dir: str='datas', code: str='0001'):
    # Name
    product_name_element = driver.find_element(By.CLASS_NAME, 'product_title')
    full_name = product_name_element.text
    names = full_name.split('] ')

    name = names[1]
    brand = names[0].replace("[", "")

    # Price
    try:
        price_element = driver.find_element(By.ID, 'span_product_price_custom')
        price = extract_number(price_element.text)
    except NoSuchElementException:
        price_element = driver.find_element(By.ID, 'span_product_price_text')
        price = extract_number(price_element.text)

    # brand
    # logo_element = driver.find_element(By.CLASS_NAME, 'topLogo')
    # brand_element = logo_element.find_element(By.TAG_NAME, 'span')
    # brand = brand_element.text.replace(' ▸', '')

    # ThumbImages
    thumb_image_elements = driver.find_elements(By.CLASS_NAME, 'BigImage')

    # # DetailImages
    div_element = driver.find_element(By.CLASS_NAME, 'cont')
    detail_image_elements = div_element.find_elements(By.CSS_SELECTOR, 'img')

    # Path
    data_path = os.path.join(data_dir, code)
    os.makedirs(data_path, exist_ok=True)

    # Image download
    thumb_images = image_download(thumb_image_elements, 'thumbImage', download_folder=data_path)
    detail_images = image_download(detail_image_elements, 'detailImage', download_folder=data_path)

    combine_image = combine_images_vertically(detail_images)

    # Image upload
    thumb_image_url = upload_to_s3(thumb_images[0], p_type='thumb')
    detail_image_url = upload_to_s3(combine_image, p_type='detail')

    data = {
        'name': name,
        'price': price,
        'brand': brand,
        'thumbnail': thumb_image_url,
        'detail': detail_image_url,
    }

    print(data)
    # SQL 파일로 추가 저장
    save_product_data_to_sql(data, code, os.path.join(data_dir, 'insert_product_data.sql'))

    # # JSON 파일로 저장
    # output_path = os.path.join(data_path, 'product_data.json')
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    # print(f"📌 {code} - Thumbnail images: {len(thumb_images)}, Detail images: {len(detail_images)}, Data saved to: {output_path}")

    # print(name.split('] '))


def save_product_data_to_sql(data, code, sql_file_path='insert_product_data.sql'):
    product_code = code
    product_name = data['name']
    product_price = data['price']
    stock_quantity = 100
    # registration_date는 MySQL의 CURRENT_DATE를 사용합니다.
    env_mark = "NULL"  # NULL로 설정
    thumbnail = data['thumbnail']
    detail_image = data['detail']
    category_number = 1
    discount_code = 1
    brand = data['brand']

    sql = f"""INSERT INTO PRODUCT (product_code, product_name, product_price, stock_quantity, registration_date, env_mark, thumbnail, detail_image, category_number, discount_code, brand) VALUES ('{product_code}', '{product_name}', {product_price}, {stock_quantity}, CURRENT_DATE, {env_mark}, '{thumbnail}', '{detail_image}', {category_number}, {discount_code}, '{brand}');"""

    with open(sql_file_path, 'a', encoding='utf-8') as file:  # 'a' 모드로 파일 열기
        file.write(sql + "\n")  # SQL 문장 끝에 줄 바꿈 추가

    print(f"SQL 문장이 {sql_file_path} 파일에 추가되었습니다.")