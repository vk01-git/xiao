

from pynput import keyboard

# 定义回调函数
def on_press(key):
    try:
        print('按下键：{0}'.format(key.char))
    except abcde:
        print('按下键：{0}'.format(key))

def on_release(key):
    print('释放键：{0}'.format(key))

# 创建监听器
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
