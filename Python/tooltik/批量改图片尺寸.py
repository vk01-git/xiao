import os 
import sys
import tkinter as tk
from tkinter.ttk import *
import tkinter.font as tkFont
import tkinter.filedialog as fd
from PIL import Image

#初始化GUI用户主界面
root = tk.Tk() 
#变量定义区START
tk_ImageFile=tk.StringVar()#图片源文件(路径+文件名+扩展名)
tk_Sfilename=tk.StringVar()#源文件(路径+文件名+扩展名)
tk_Dfilename=tk.StringVar()#目标文件(文件名)
tk_new_width=tk.IntVar()#图片宽
tk_new_height=tk.IntVar()#图片高
vk_filelist=[] #保存多选的所有文件
#变量定义区END
#设置变量默认值
tk_ImageFile.set("C:/")
tk_Sfilename.set("C:/")
#设置变量默认值


#定义主函数
def main_resize_image():
    new_size = (tk_new_width.get(),tk_new_height.get())
    i=1
    for it in vk_filelist:
        tk_ImageFile.set(it)
        resize_image(tk_ImageFile.get(),new_size)
        i+=1
    print(f"修改成功！共修改了{len(vk_filelist)}个文件")

def main_change_filename():
    i=1
    for it in vk_filelist:
        tk_Sfilename.set(it)
        change_filename(it.split('/')[0:-1],tk_Dfilename.get(),i,it[-3:] )
        i+=1
    

def quit():#tkinter.Button 退出按钮
    sys.exit()

 #定义更改图片尺寸的函数   
def resize_image(image_file, new_size):
    if os.path.exists(image_file):  # 打开图片
        try:
            img = Image.open(image_file)
        except IOError:
            print('文件不是图片文件')
        else:
            img_resize = img.resize(new_size)  # 调整尺寸
            img_resize.save(os.path.splitext(image_file)[0] + '_resize.jpg')  # 保存图片
    else:
        print('文件不存在')


#定义更改文件名的函数
def change_filename(outdir,filename,n,ext): # 4个参数分别代表输出目录，新文件名，序号，扩展名
    file_path = tk_Sfilename.get() # 获取文件路径 
    new_file_name = '/'.join(outdir)+'/'+filename+'%02d'%(n)+'.'+ext # 获取新文件名 
    os.rename(file_path, new_file_name) # 更改文件名 


def tkOpenImageFile():  # tkinter.filedialog选择图片文件对话框
    vk_filelist.clear()
    filename=fd.askopenfilename(multiple=True) # 选择打开的文件，返回路径+文件名
    if filename is not None:
        for it in filename:  
            vk_filelist.append(it) 
        tk_ImageFile.set(filename[0]) 
    else:
        print("未选择文件!")

def tkOpenfile(): # tkinter.filedialog文件选择对话框
    vk_filelist.clear()
    filename=fd.askopenfilename(multiple=True) # 选择打开的文件，返回路径+文件名
    if filename is not None:
        for it in filename:  
            vk_filelist.append(it) 
        tk_Sfilename.set(filename[0]) 
    else:
        print("未选择文件!")

#创建窗口
root.resizable(0,0)#主窗口 
root.title('我的自媒体工具') 
root.geometry('500x500') 
#设置字体
font1 = tkFont.Font(family='microsoft yahei', size=10, weight='normal')
#设置窗体容器
#创建页签
tk_notebook=Notebook(root)
tk_notebook.place(in_=root, anchor="center", relx=0.5, rely=0.5)
#创建选项卡
Frame1=tk.Frame(tk_notebook,bd=2,relief=tk.GROOVE,highlightthickness=1,width=480,height=470)#Frame1
Frame2=tk.Frame(tk_notebook,bd=2,relief=tk.GROOVE,highlightthickness=1,width=480,height=470)#Frame2
Frame3=tk.Frame(tk_notebook,bg='#436EEE',bd=2,relief=tk.FLAT,highlightthickness=1,width=480,height=470)#Frame3
#Frame1二级窗体
Frame1_1=tk.Frame(Frame1,bd=2,relief=tk.RIDGE,highlightthickness=1,width=470,height=150)#Frame1-1
Frame1_2=tk.Frame(Frame1,bd=2,relief=tk.RIDGE,highlightthickness=1,width=470,height=150)#Frame1-1
Frame1_3=tk.Frame(Frame1,bd=2,relief=tk.RIDGE,highlightthickness=1,width=470,height=160)#Frame1-1
#Frame2二级窗体
Frame2_1=tk.Frame(Frame2,bd=2,relief=tk.RIDGE,highlightthickness=1,width=470,height=150)#Frame1-1
Frame2_2=tk.Frame(Frame2,bd=2,relief=tk.RIDGE,highlightthickness=1,width=470,height=150)#Frame1-1
Frame2_3=tk.Frame(Frame2,bd=2,relief=tk.RIDGE,highlightthickness=1,width=470,height=160)#Frame1-1
tk_notebook.add(Frame1,text="批量改图片尺寸")
tk_notebook.add(Frame2,text="批量改文件名")
tk_notebook.add(Frame3,text="其它")

#Frame1布局（批量改图片尺寸）
#选择文件部分
tk.Label(Frame1_1,text="请 选 择 文 件：",font=font1).grid(row=1,column=0,padx=0,pady=10,sticky='W')
tk.Entry(Frame1_1,width=30,font=font1,textvariable=tk_ImageFile).grid(row=1,column=1,padx=0,pady=10)
tk.Button(Frame1_1,text="浏 览...",command=tkOpenImageFile,font=font1).grid(row=1,column=2,padx=10,pady=10)
Frame1_1.grid(row=1,column=1,padx=10,pady=0)
Frame1_1.grid_propagate(0) #禁止组件调整大小，使其在grid布局中固定大小
#图片尺寸部分
tk.Label(Frame1_2,text="图片尺寸",font=font1).grid(row=2,column=0,padx=0,pady=20,sticky='W')
tk.Label(Frame1_2,text="宽：",font=font1).grid(row=2,column=1,padx=10,pady=10,sticky='W')
tk.Entry(Frame1_2,width=5,font=font1,textvariable=tk_new_width).grid(row=2,column=2,padx=0,pady=0)
tk.Label(Frame1_2,text="高：",font=font1).grid(row=2,column=3,padx=10,pady=10,sticky='W')
tk.Entry(Frame1_2,width=5,font=font1,textvariable=tk_new_height).grid(row=2,column=4,padx=0,pady=0)
Frame1_2.grid(row=2,column=1,padx=10,pady=0)
Frame1_2.grid_propagate(0) 
#功能按钮部分
change_filename_button = tk.Button(Frame1_3, text='确认修改', command=main_resize_image).grid(row=3, column=1,padx=100,pady=10)#创建确认按钮
change_filename_button = tk.Button(Frame1_3, text='退出', command=quit).grid(row=3, column=2,padx=50,pady=0)#创建退出按钮
Frame1_3.grid(row=3,column=1,padx=10,pady=0)
Frame1_3.grid_propagate(0) 

#Frame2布局（批量改文件名)
#选择文件部分
tk.Label(Frame2_1,text="请 选 择 文 件：",font=font1).grid(row=1,column=0,padx=0,pady=10,sticky='W')
tk.Entry(Frame2_1,width=30,font=font1,textvariable=tk_ImageFile).grid(row=1,column=1,padx=0,pady=10)
tk.Button(Frame2_1,text="浏 览...",command=tkOpenfile,font=font1).grid(row=1,column=2,padx=10,pady=10)
Frame2_1.grid(row=1,column=1,padx=10,pady=0)
Frame2_1.grid_propagate(0) #禁止组件调整大小，使其在grid布局中固定大小
#图片尺寸部分
tk.Label(Frame2_2,text="命   名   方   式：",font=font1).grid(row=2,column=0,padx=2,pady=10,sticky='W')
tk.Entry(Frame2_2,width=30,font=font1,textvariable=tk_Dfilename).grid(row=2,column=1,padx=0,pady=0)
tk.Label(Frame2_2,text="+ 序号",font=font1).grid(row=2,column=2,padx=10,pady=0)
Frame2_2.grid(row=2,column=1,padx=10,pady=0)
Frame2_2.grid_propagate(0) 
#功能按钮部分
change_filename_button = tk.Button(Frame2_3, text='确认修改', command=main_change_filename).grid(row=3, column=1,padx=100,pady=10)#创建确认按钮
change_filename_button = tk.Button(Frame2_3, text='退出', command=quit).grid(row=3, column=2,padx=50,pady=0)#创建退出按钮
Frame2_3.grid(row=3,column=1,padx=10,pady=0)
Frame2_3.grid_propagate(0) 




#Frame3布局



 #运行主窗口
root.mainloop()