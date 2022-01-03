import requests
from msal import PublicClientApplication
import os

c = open("CLIENT_ID")
g = open("TENANT_ID")
CLIENT_ID = c.read().replace("\n", "")
TENANT_ID = g.read().replace("\n", "")

app = PublicClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}")

USERNAME = input("username (including domain) : ")
PASSWORD =  input("Password : ")
SCOPES = ["Files.ReadWrite.All", "Sites.ReadWrite.All"]

API_URL = "https://graph.microsoft.com/v1.0/me/drive/root:/EncUpload"

token = app.acquire_token_by_username_password(USERNAME,PASSWORD,SCOPES)

header = {"Authorization" : f"Bearer {token['access_token']}"}

def upload_file(file_path, remote_path=None):
    file_path = os.path.expanduser(file_path)
    if not os.path.isfile(file_path):
        print("notafile")
        return

    if not remote_path:
        remote_path = file_path
    file_data = open(file_path, "rb")
    file_size = os.path.getsize(file_path)

    if file_size < 4100000:
        requests.put(f"{API_URL}/{remote_path}:/content", data=file_data, headers=header)
    else:
        url = requests.post(f"{API_URL}/{remote_path}:/createUploadSession", headers=header).json()["uploadUrl"]
        chunk_size = 4000000
        chunks_amount = file_size // chunk_size
        chunk_number = 0
        while chunk_number <= chunks_amount:
            chunk_begin = chunk_number * chunk_size
            chunk_end = chunk_begin + chunk_size
            data = file_data.read(chunk_end - chunk_begin)
            chunk_end -= 1
            if chunk_number == chunks_amount:
                chunk_end = file_size - 1
            print(f"data length = {len(data)}")
            print(f"content range = {chunk_begin}-{chunk_end}")
            theader = {"Content-Lenght" : str(chunk_end - chunk_begin), "Content-Range" : f"bytes {chunk_begin}-{chunk_end}/{file_size}"}
            print(theader)
            print(requests.put(f"{url}", data=data, headers=theader).text)
            chunk_number += 1

def delete_file(remote_path):
    requests.delete(f"{API_URL}/{remote_path}", headers=header)

def list_directory():
    print(requests.get(f"{API_URL}:/children", headers=header).text)

def download_file(remote_path, file_path=None):
    r = requests.get(f"{API_URL}/{remote_path}", headers=header)
    j = r.json()
    if "error" in j.keys():
        raise Exception("File Doesn't exist")
        # we will assume this means that the file doesn't exisst
        # there is a chance that you're just being late limited but yk
    r = requests.get(f"{API_URL}/{remote_path}:/content", headers=header)
    if not file_path:
        file_path = remote_path
    f = open(file_path, "wb")
    f.write(r.content)
    f.close()
