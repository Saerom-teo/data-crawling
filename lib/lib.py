import os
import shutil
import re


def recreate_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    
    os.makedirs(directory_path)

def extract_number(price_str):
    # 정규 표현식을 사용하여 숫자만 추출
    number = re.findall(r'\d+', price_str)
    # 추출한 숫자 리스트를 하나의 문자열로 합치고, 정수로 변환
    return int(''.join(number))

