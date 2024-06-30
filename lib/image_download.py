from selenium.webdriver.remote.webelement import WebElement
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from typing import List
import requests
import os

def image_download(image_elements: List[WebElement], content_type: str, download_folder: str='downloaded_images'):
    download_dir = os.path.join(download_folder, content_type)
    os.makedirs(download_dir, exist_ok=True)

    image_count = 0
    image_paths = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for idx, image_element in enumerate(image_elements):
        if content_type == 'detailImage':
            if image_element.get_attribute('ec-data-src'):
                image_url = 'https:' + image_element.get_attribute('ec-data-src')
            elif image_element.get_attribute('src'):
                image_url = image_element.get_attribute('src')
        else:
            image_url = image_element.get_attribute('src')

        if image_url:
            try:
                image_response = requests.get(image_url, headers=headers, timeout=10)
                image = Image.open(BytesIO(image_response.content))

                image_path = os.path.join(download_dir, f'{content_type}_{idx}.jpg')
                image.save(image_path)
                image_count += 1
                image_paths.append(image_path)

                # print(f"Successfully downloaded image: {image_url} -> {image_path}")

            except UnidentifiedImageError:
                print(f"Failed to identify image: {image_url}")
                pass
            except requests.RequestException as e:
                print(f"Failed to download image: {image_url} with error {e}")
                pass
            except Exception as e:
                print(f"Failed to process image: {image_url} with error {e}")
                pass

    # print(f'{image_count} images have been saved to the folder: {download_dir}')

    return image_paths


def combine_images_vertically(image_paths: List[str], output_path: str='detailImage.jpg'):
    try:
        dir_name = os.path.dirname(image_paths[0])
        image_path = os.path.join(dir_name, output_path)
        images = [Image.open(image_path) for image_path in image_paths]

        max_width = max(image.width for image in images)
        total_height = sum(image.height for image in images)

        combined_image = Image.new('RGB', (max_width, total_height))

        y_offset = 0
        for image in images:
            combined_image.paste(image, (0, y_offset))
            y_offset += image.height

        combined_image.save(image_path)
        print(f"Combined image saved to: {image_path}")
    except OSError as e:
        print(f"Failed to save combined image due to OSError: {e}")
    except Exception as e:
        print(f"Failed to combine images with error: {e}")