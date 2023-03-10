import base64
import pyDes
import json
import os
import subprocess


# 8个字节
Key = "DAPPDAPP"
Iv = None


def bytesToHexString(bs):
    return ''.join(['%02X ' % b for b in bs])


def hexStringTobytes(str):
    str = str.replace(" ", "")
    return bytes.fromhex(str)

# 加密


def encrypt_str(data):
    # 加密方法
    method = pyDes.des(Key, pyDes.ECB, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 执行加密码
    k = method.encrypt(data)
    data = bytesToHexString(k).replace(' ', '')
    return data


# 解密
def decrypt_str(data):
    method = pyDes.des(Key, pyDes.ECB, Iv, pad=None, padmode=pyDes.PAD_PKCS5)
    # 对base64编码解码
    k = hexStringTobytes(data)
    return method.decrypt(k)

try:
    import pyDes
    print("pyDes is installed.")
except ImportError:
    # 执行 pip install 命令安装 pyDes 库
    print("pyDes is not installed.")
    subprocess.check_call(['pip', 'install', 'pyDes'])


urls = ["https://www.nbox.io/upload/config/config.json",
        "https://fcwrsmall.github.io/config/config.json"]

isExit = os.path.exists("src/config.json")
if isExit:
    configFile = open("src/config.json", "rb+")
    bytes = configFile.read()
    configFile.close()
    jsonObj = json.loads(bytes)
    print("config file:", bytes)
    print("Json :", jsonObj)
    print("Json dump:", json.dumps(jsonObj))
    encryptText = json.dumps(jsonObj)
    Encrypt = encrypt_str(encryptText)
    print("Encrypt:", Encrypt)

    # 写入加密后的json
    encryptFile = open("config.json", 'w')
    encryptFile.write(json.dumps({"text": Encrypt}))
    encryptFile.close()
    # 输出加密后的url
    
    encryptFile = open("url.txt", 'w')
    for url in urls:
        encryptFile.write(json.dumps({'"'+ url + '"': encrypt_str(url)}))
        print("url: ", url, " -> ", encrypt_str(url))
    encryptFile.close()  


else:
    print("请在同目录下放config.json")
