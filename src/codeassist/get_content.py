from urllib.parse import urlparse
import urllib.request
import os
import hashlib
import pathlib

# Hash a string
def md5_of_str(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# Hash a file
def md5_of_file(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def get_url_content(url, cache=False):
    path = None
    if cache:
        path = os.path.abspath(f'{pathlib.Path(__file__).parent}/../../.cache/{md5_of_str(url)}.html')
        os.makedirs(pathlib.Path(path).parent, exist_ok=True)
        if os.path.exists(path):
            return get_file_content(path)
    content = _get_url_content(url)
    if cache:
        save(path, content)
    return content

def _get_url_content(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            return html
    except urllib.error.URLError as e:
        print(f"Error opening URL: {e.reason}")

def get_file_content(fn):
    with open(fn, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def save(fn, text): 
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, "w", encoding="utf-8") as f:
        print(text, file=f)

def filepath_from_url(basepath, url, start, end, filename):
    l = [str(basepath)]
    parsed_url = urlparse(url)
    l.extend(parsed_url.path.strip("/").split("/")[start:end])
    l.append(filename)
    return "/".join(l)

def toc(tocfn, title, path, parts):
    l = path.strip("/").split("/")[-parts:]
    with open(tocfn, "a", encoding='utf-8') as file:
        file.write(f"{title} || {"/".join(l)}\n")