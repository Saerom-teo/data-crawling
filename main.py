from selenium import webdriver

from process import process
from get_product_data import get_product_data

# WebDriver 설정
driver_path = 'path/to/your/chromedriver.exe'
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")

# ChromeDriver 실행
driver = webdriver.Chrome(options=options)

try:
    # url = 'https://m.morestore.co.kr/supply/index.html?supplier_code=S00000DO'
    # url = 'https://m.morestore.co.kr/product/list_thumb.html?cate_no=130'
    url = 'https://morestore.co.kr/category/%EC%9D%98%EB%A5%98/128/'

    driver.get(url)

    process(driver)
    # get_product_data(driver)

finally:
    driver.quit()