import time
import _thread
import subprocess
import zipfile

charSource=['0','1','2','3','4','5','6','7','8','9']
global flag
flag=0

def brutecrack_number(st,ed):
    for a in range(st,ed):
        for b in range(0,10):
            for c in range(0,10):
                for d in range(0,10):
                    for e in range(0,10):
                        for f in range(0,10):
                            passwd=str(a)+str(b)+str(c)+str(d)+str(e)+str(f)
                            # x 表示按目录结构进行解压
                            # -o 表示输入到目录中
                            # -p 密码 abc为密码
                            # -aoa 直接覆盖现有文件，而没有任何提示
                            input_path='"d:\\暴力破解\\pj.7z"'
                            command='7z x '+input_path+' -p'+passwd+' -od:\\暴力破解\\pj.zip -aoa -y' #unzip没安装，安装了7Z https://www.7-zip.org/
                            # print(command)
                            print(passwd) 
                            if flag==1:#发现有其他线程已经找到密码，就断开
                                print("有线程已经找到密码，本线程直接退出")
                                return
                            child=subprocess.call(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                            #os.popen(command) #这个也可以用，但是不好监控解压状态
                            print(child) #这里是一直在打印暴力破解的密码
                            if child==0:
	                            flag=1
                                print("密码为:"+passwd)
                                return
                            elif flag==2:
	                            flag=1
	                            print("没有找到解压文件")
	                            return

def brutecrack_char():
    pass

if __name__=='__main__':
   try:
        _thread.start_new_thread(brutecrack_number,(1,2,))
        _thread.start_new_thread(brutecrack_number,(2,3,))
        _thread.start_new_thread(brutecrack_number,(3,4,))
        _thread.start_new_thread(brutecrack_number,(4,5,))
        _thread.start_new_thread(brutecrack_number,(5,6,))
        _thread.start_new_thread(brutecrack_number,(6,7,))
        _thread.start_new_thread(brutecrack_number,(7,8,))
        _thread.start_new_thread(brutecrack_number,(8,9,))
        _thread.start_new_thread(brutecrack_number,(9,10,))
    except:
        print("Error:无法启动线程")
    while 1:
        pass


