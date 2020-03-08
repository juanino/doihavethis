
# sample worker function

import requests
from filehash import FileHash


def count_words_at_url(url):
    resp = requests.get(url)
    print(len(resp.text.split()))
    return len(resp.text.split())

def make_hash(fullpath):
    md5hasher = FileHash('md5')
    try:
        checksum = md5hasher.hash_file(fullpath)
    except:
        print("failure")
    output = str(checksum) + ":" + str(fullpath)
    return output