def encrypt(text):
    # 定义替换字典
    replace_dict = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '0'}
    # 将文本中的小写字母替换为数字
    encrypted_text = ''.join([replace_dict.get(c, c) for c in text])
    return encrypted_text

def decrypt(encrypted_text):

    # 将数字替换回小写字母
    replace_dict = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', '0': 'j'}
    decrypted_text = ''.join([replace_dict.get(c, c) for c in encrypted_text])
    return decrypted_text

a=encrypt("xiao1314")
b=decrypt(a)
print(a,b)
