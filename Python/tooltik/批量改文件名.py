import os 
import sys
import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as fd

#定义主窗口
window = tk.Tk() 

#变量定义区START
tk_Sfilename=tk.StringVar()#源文件(路径+文件名+扩展名)
tk_Dfilename=tk.StringVar()#目标文件(文件名)
vk_filelist=[] #保存多选的所有文件
#变量定义区END
#设置变量默认值
tk_Sfilename.set("C:/")
tk_Dfilename.set("文件名")
#设置变量默认值

#定义主函数
def main():
    i=1
    for it in vk_filelist:
        tk_Sfilename.set(it)
        change_filename(it.split('/')[0:-1],tk_Dfilename.get(),i,it[-3:] )
        i+=1

def quit():#tkinter.Button 退出按钮
    sys.exit()
    
        
#定义更改文件名的函数
def change_filename(outdir,filename,n,ext): #4个参数分别代表输出目录，新文件名，序号，扩展名
    file_path = tk_Sfilename.get() # 获取文件路径 
    print("以下是changefile:",outdir,filename,n,ext)
    new_file_name = '/'.join(outdir)+'/'+filename+'%02d'%(n)+'.'+ext # 获取新文件名 
    os.rename(file_path, new_file_name) # 更改文件名 


def tkOpenfile():#tkinter.filedialog文件选择对话框
    vk_filelist.clear()
    filename=fd.askopenfilename(multiple=True)#选择打开的文件，返回路径+文件名
    if filename is not None:
        for it in filename:  
            vk_filelist.append(it) 
        tk_Sfilename.set(filename[0]) 
        print("以下是OPENFILE:",vk_filelist,tk_Sfilename.get(),tk_Dfilename.get())
    else:
        print("未选择文件!")


#创建窗口

window.title('批量更改文件名') 
window.geometry('450x300') 
#设置字体
font1 = tkFont.Font(family='microsoft yahei', size=10, weight='normal')

tk.Label(window,text="请 选 择 文 件：",font=font1).grid(row=1,column=0,padx=2,pady=10,sticky='W')
tk.Entry(window,width=30,font=font1,textvariable=tk_Sfilename).grid(row=1,column=1,padx=0,pady=0)
tk.Button(window,text="浏 览...",command=tkOpenfile,font=font1).grid(row=1,column=2,padx=10,pady=5)

tk.Label(window,text="命   名   方   式：",font=font1).grid(row=2,column=0,padx=2,pady=10,sticky='W')
tk.Entry(window,width=30,font=font1,textvariable=tk_Dfilename).grid(row=2,column=1,padx=0,pady=0)
tk.Label(window,text="+ 序号",font=font1).grid(row=2,column=2,padx=10,pady=0)

 #创建更改文件名按钮
change_filename_button = tk.Button(window, text='更改文件名', command=main).grid(row=3, column=1)
 #创建退出按钮
change_filename_button = tk.Button(window, text='退出', command=quit).grid(row=3, column=2)
 #运行主窗口
window.mainloop()