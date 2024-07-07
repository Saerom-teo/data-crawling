from dotenv import load_dotenv
import boto3
import os
import uuid


load_dotenv()

ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
SECRET_KEY = os.getenv('S3_SECRET_KEY')
REGION_NAME = os.getenv('S3_REGION_NAME')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

S3_ACCESS = True


# def upload_image(save_dir: str, image_path: str):
#     os.makedirs(save_dir, exist_ok=True)

#     for result in results:
#         image_path = os.path.join(save_dir, f"{os.path.basename(result.path)}")
#         result.save(filename=image_path)

#         url = upload_to_s3(image_path)

#         result_images.append(url)

#     return result_images


def upload_to_s3(file_name, object_name=None, p_type='thumb'):
    if not S3_ACCESS:
        return file_name
    
    if object_name is None:
        object_name = os.path.basename(file_name)

    # 랜덤 문자열 생성
    random_string = uuid.uuid4().hex
    object_name = f"{random_string}_{object_name}"

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    object_name = f'product/{p_type}/{object_name}'
    s3.upload_file(
        file_name, 
        BUCKET_NAME, 
        object_name, 
    )

    file_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{object_name}"

    os.remove(file_name)
    return file_url
