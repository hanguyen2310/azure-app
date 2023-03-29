from django.utils import timezone
import os
import io
from PIL import Image 
import requests

def get_folder_name(title, type = "post"):
    '''
    the folder name will be create at the time the function is called
    it will be created in the blog/static/blog/content/posts<date created>
    '''
    dt = timezone.datetime.now()
    if type == "post":
        folder_name = "blog/static/blog/content/posts/" + dt.strftime('%Y%m%d')
    elif type == "author":
        folder_name = "blog/static/blog/content/author/" 

    if os.path.exists(folder_name) == False:
        os.mkdir(folder_name)

    folder_name = f'{folder_name}/{title}'
    if os.path.exists(folder_name) == False:
        os.mkdir(folder_name)

    if os.path.exists(f"{folder_name}/img") == False:
        os.mkdir(f"{folder_name}/img")

    return folder_name


def handle_uploaded_file(f, file_name):
    '''
    this function will save uploaded file to the folder
    file_name: the title of the blog

    return: 
        file_path: the path of the file (this will be saved in DB)
    '''
    folder_name = get_folder_name(file_name)
    file_path = f'{folder_name}/{file_name}.md'

    with open(file_path, 'wb+') as destination:
        body = f.read()
        destination.write(body)

    print(f"[Info] File writen to {file_path}")

    return file_path

def save_md_to_file(md_text, file_name):
    '''
    this function will save the md text to the file
    file_name: the title of the blog

    return: 
        file_path: the path of the file (this will be saved in DB)
    '''
    folder_name = get_folder_name(file_name)
    file_path = f'{folder_name}/{file_name}.md'

    with open(file_path, 'w+', encoding="utf-8") as f:
        f.write(md_text)

    return file_path

def read_md_file(file_path):
    '''
    this will read the md file and return the md text
    '''
    with open(file_path, 'r', encoding="utf-8") as f:
        md_text = f.read()

    return md_text

def update_md_file(file_path, md_text):
    '''
    this will update the md file
    '''
    with open(file_path, 'w+', encoding="utf-8") as f:
        f.write(md_text)

# def string_escape(s, encoding='unicode-escape'):
#     return (s.encode('iso-8859-1')         # To bytes, required by 'unicode-escape'
#              .decode('unicode-escape') # Perform the actual octal-escaping decode
#              .encode('iso-8859-1')         # 1:1 mapping back to bytes
#              .decode(encoding))        # Decode original encoding
def save_image(image, file_name, type="post"):
    '''
    this will save the image to the folder
    '''
    extension = str(image).split('.')[-1]
    folder_name = get_folder_name(file_name, type)
    file_path = f'{folder_name}/img/{file_name}.{extension}'
    with Image.open(image) as im:
        print(im.info)
        im.save(file_path)

    return file_path

def get_random_thumbnail(file_name, type="post"):
    '''
    this will return a random thumbnail
    '''
    folder_name = get_folder_name(file_name, type)
    file_path = f'{folder_name}/img/{file_name}.jpg'

    download_image('https://picsum.photos/200/300/?random.jpg', file_path)

    file_path_to_save = "/".join(file_path.split("/")[2:])

    return file_path_to_save

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)

    print('Image downloaded from url: {} and saved to: {}.'.format(url, image_file_path))
