from Crypto.Cipher import AES
import base64

# 加密函数
def encrypt(text, key):
    # 将密钥转换为16字节的二进制数据
    key = key.encode('utf-8')
    key = key.ljust(16, b'\0')
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_ECB)
    # 将文本转换为16字节的二进制数据
    text = text.encode('utf-8')
    text = text.ljust(16, b'\0')
    # 加密文本
    encrypted_text = cipher.encrypt(text)
    # 将加密后的二进制数据转换为Base64编码的字符串
    encrypted_text = base64.b64encode(encrypted_text)
    return encrypted_text.decode('utf-8')

# 解密函数
def decrypt(encrypted_text, key):
    # 将密钥转换为16字节的二进制数据
    key = key.encode('utf-8')
    key = key.ljust(16, b'\0')
    # 创建AES解密器
    cipher = AES.new(key, AES.MODE_ECB)
    # 将Base64编码的字符串转换为二进制数据
    encrypted_text = base64.b64decode(encrypted_text)
    # 解密文本
    decrypted_text = cipher.decrypt(encrypted_text)
    # 去除填充的空字节
    decrypted_text = decrypted_text.rstrip(b'\0')
    # 将解密后的二进制数据转换为字符串
    decrypted_text = decrypted_text.decode('utf-8')
    return decrypted_text

# 测试
text = "Hello, World!"
key = "mysecretkey"
encrypted_text = encrypt(text, key)
print("加密后的文本：", encrypted_text)
decrypted_text = decrypt(encrypted_text, key)
print("解密后的文本：", decrypted_text)
