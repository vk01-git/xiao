from PIL import ImageGrab
import datetime
from pynput import keyboard

def VKscreenshot(path):
    # 截取整个屏幕
    im = ImageGrab.grab()
    curr_time=datetime.datetime.now()
    curr_time_str='sc_'+datetime.datetime.strftime(curr_time,'%Y-%m-%d_%H%M%S')
    filename=path+curr_time_str+'.png'
    # 保存截图
    im.save(filename)
    return(filename)


# 定义回调函数
def on_press(key):
    try:
        if key==keyboard.Key.page_up:
            VKscreenshot('d:\\ScreenShot\\')
            print("正在截图",key)
        elif key==keyboard.Key.page_down:
            listener.stop()
            print("正在退出...",key)
        else:
            print("PageUp:截图,PageDown:退出")
    except AttributeError:
        print("Error:PageUp:截图,PageDown:退出")
    
def on_release(key):
    pass

# 创建监听器
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
