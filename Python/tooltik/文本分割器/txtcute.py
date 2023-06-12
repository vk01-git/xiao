import sys
import os   
import re
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.font as tkFont
from _ast import Pass
#import xiao.ch2digit

root=tk.Tk()#定义程序界面主窗口
#变量定义区START
tk_ErrorCode=tk.StringVar()#错误代码
tk_Sfilename=tk.StringVar()#源文件(路径+文件名+扩展名)
tk_dirpath=tk.StringVar()#选择目录(批量处理文件)
tk_outputpath=tk.StringVar()#输出目录
tk_Dfilename=tk.StringVar()#目标文件(文件名)
tk_Sfilesize=tk.IntVar()#源文件大小
tk_Dfilesize=tk.IntVar()#目标文件大小
tk_filenum=tk.IntVar()#目标文件数量
tk_rbSplit=tk.IntVar()#分割方式单选框
tk_Unit=tk.StringVar()#文件大小单位
tk_Keyword=tk.StringVar()#保存搜索关键词
tk_CutMethod=0#(0:单文件操作 1:多文件操作)
vk_spanx=[0]#关键字分割坐标X
vk_spany=[]#关键字分割坐标X
vk_group=['序言']#关键字匹配到的内容当作目标文件名的组成部分
vk_dirs=[]#遍历指定目录下的所有文件含路径
vk_files=[]#遍历指定目录下的所有文件只有文件名


#变量定义区END
#设置变量默认值
tk_Sfilename.set("C:/")
tk_outputpath.set("C:/")
tk_Dfilename.set("文件名")
tk_Sfilesize.set(0)
tk_Dfilesize.set(1)
tk_filenum.set(1)
tk_rbSplit.set(1)
tk_Keyword.set("第.{1,5}章")
#设置变量默认值

def home(CutMethod):#Parament:CutMethod=(0：单文件分割，1：多文件分割)
    if CutMethod==0:
        if tk_rbSplit.get()==3:
            CutTxtForKeyWord(tk_Sfilename.get(),tk_outputpath.get(),tk_Keyword.get())
        else:
            if tk_Unit.get()=='字符':
                CutTxtFile(tk_Sfilename.get(),tk_outputpath.get(),tk_Dfilesize.get())
            else:
                CutBinFile(tk_Sfilename.get(),tk_outputpath.get(),tk_Dfilesize.get(),tk_Unit.get())
    elif CutMethod==1:
        CutTxtForBatch(tk_dirpath.get())
    else:
        print("参数错误(0：单文件分割，1：多文件分割)")
        
            
   
def CutBinFile(Sfilename,outputpath,Cutsize,CutUnit):#分割二进制文件(Sfilename=源文件,dirpath=目标文件输出目录,Cutsize=分割大小(int型),CutUnit=分割单位(1'Byte' 2'KB' 3'MB' 4'GB'))
    fs=open(Sfilename,'rb')
    print("源文件大小：%s%s\t分割后文件数量：%s\t分割后文件大小：%s%s"%(tk_Sfilesize.get(),tk_Unit.get(),tk_filenum.get(),tk_Dfilesize.get(),tk_Unit.get()))
    if CutUnit=='Byte':
        size=Cutsize
    elif CutUnit=='KB':
        size=int(Cutsize*1024)
    elif CutUnit=='MB':
        size=int(Cutsize*1024*1024)
    elif CutUnit=='GB':
        size=int(Cutsize*1024*1024*1024)
    else:
        print("二进制模式不能选择字符")
    
    for n in range(1,tk_filenum.get()+1):
        with open(outputpath+'/'+tk_Dfilename.get().split('.')[0]+'_'+'%02d'%n+'.'+tk_Dfilename.get().split('.')[-1],"wb") as f:
            ch=fs.read(size)
            f.write(ch)
        print("正在处理第%s个文件"%(n))
    fs.close()    
    print("文件分割完毕，请指示！")
      
def CutTxtFile(Sfilename,outputpath,Cutsize):#分割文本文件:Sfilename=源文件,dirpath=目标文件输出目录,Cutsize=分割大小(int型)
    vk_seek=0#源文件指针定位器(单位：Byte)
    ch_size=0#读取字符数(单位：字符)
    n=1
    tk_Sfilesize.set(gettxtsize(Sfilename))
    tk_filenum.set(int(tk_Sfilesize.get()/Cutsize)+1)
    fs=open(Sfilename,'rt',encoding="utf-8")
    print("源文件大小：%s%s\t分割后文件数量：%s\t分割后文件大小：%s%s"%(tk_Sfilesize.get(),tk_Unit.get(),tk_filenum.get(),tk_Dfilesize.get(),tk_Unit.get()))
    print("输出目录：%s"%(tk_outputpath.get()))
    while (tk_Sfilesize.get()-ch_size)>tk_Dfilesize.get():
        
        with open(outputpath+'/'+tk_Dfilename.get().split('.')[0]+'_'+'%02d'%(n)+'.'+tk_Dfilename.get().split('.')[-1],"wt",encoding="utf-8") as f:
            ch_str=fs.read(Cutsize)
            ch_list=ch_str.split('\n')
            ch_seek='\r\n'.join(ch_list[:-1])#去掉了最后一个段落后面多余的字,将‘\n’替换为‘\r\n’是因为python在'utf-8'模式下读取文件时将"CRLF(\r\n)"自动替换成"LF(\n)",两个字节变一个字节，导致文件指针指向错误。UNIX下用'\n'表示回车换行，Windows下用'\r\n',OS下则用'\r'表示回车换行
            ch='\n'.join(ch_list[:-1])#ch是实际写进新文件的内容
            vk_seek+=len(ch_seek.encode())#vk_seek是文件指针，按字节移动
            ch_size+=len(ch)#ch_size表示实际读取了多少个字符
            f.write(ch)
        print("正在处理第%s个文件"%(n)) 
        fs.seek(vk_seek,0)#重新定位源文件指针，文本模式下文件指针不能倒退
        n+=1
        print("vk_seek=%s,ch_size=%s,step=%s"%(vk_seek,ch_size,tk_Sfilesize.get()-ch_size))
    else:
        print("vk_seek=%s,ch_size=%s,step=%s"%(vk_seek,ch_size,tk_Sfilesize.get()-ch_size))
        with open(outputpath+'/'+tk_Dfilename.get().split('.')[0]+'_'+'%02d'%(n)+'.'+tk_Dfilename.get().split('.')[-1],"wt",encoding="utf-8") as f:
            ch_str=fs.read(Cutsize)
            ch_list=ch_str.split('\n')
            ch_seek='\r\n'.join(ch_list[:-1])
            ch='\n'.join(ch_list[:])
            vk_seek+=len(ch_seek.encode())
            ch_size+=len(ch)
            f.write(ch)
        print("正在处理第%s个文件"%(n))                
    fs.close()    
    print("文件分割完毕，请指示！")  
    
def CutTxtForKeyWord(Sfilename,outputpath,keychar):#按关键字分割文件(Sfilename=源文件,dirpath=输出目录,keychar='正则表达式')
    vk_spanx=[0]#关键字分割坐标X(每调用一次函数清一次零)
    vk_spany=[]#关键字分割坐标X(每调用一次函数清一次零)
    vk_group=['序言']#(每调用一次函数清一次零)
    fs=open(Sfilename,'rt',encoding='utf-8')
    print("源文件大小：%s%s\t分割关键字：%s"%(tk_Sfilesize.get(),tk_Unit.get(),keychar))
    ch_str=fs.read()
    pattern=re.compile(r'%s'%(keychar))#生成正则表达式对象
    obj_fi=pattern.finditer(ch_str)#用Keyword匹配整个文件
    for n in obj_fi:#将匹配到的关键字在文件中的内容和位置存入变量
        print(n.group(),n.span())
        vk_spanx.append(n.span()[0])
        vk_spany.append(n.span()[0])
        vk_group.append(n.group())
    vk_spany.append(len(ch_str))
    print(vk_spanx)
    print(vk_spany)
    
    for m in range(len(vk_spanx)):
        if((os.path.getsize(tk_Sfilename.get()))>(100*1024))and(re.search(r'第.+章',tk_Dfilename.get())==None):
            with open(outputpath+'/'+tk_Dfilename.get().split('.')[0]+'%04d'%m+'_'+vk_group[m]+'.'+tk_Dfilename.get().split('.')[-1],'wt',encoding='utf-8')as f:
                ch=ch_str[vk_spanx[m]:vk_spany[m]]#通过List切片获取分割后的文本存入新文件
                f.write(ch)
                print("处理第%s个文件"%(m+1))
        else:
            with open(outputpath+'/'+tk_Dfilename.get().split('.')[0]+'%02d'%m+'_'+'.'+tk_Dfilename.get().split('.')[-1],'wt',encoding='utf-8')as f:
                ch=ch_str[vk_spanx[m]:vk_spany[m]]#通过List切片获取分割后的文本存入新文件
                f.write(ch)
                print("处理第%s个文件"%(m+1))    
    print("处理完毕")
    fs.close()  
                

def CutTxtForBatch(DirPath):#批量分割文本文件
    tk_outputpath.set(DirPath)
    for name in vk_dirs:
        if((os.path.getsize(name)>(100*1024))and(re.search(r'第.+章',name.split('/')[-1]))==None):
            dirpath=DirPath+'/'+(name.split('/')[-1]).split('.')[0]
            try: #如果目录已存在，则不再建立目录，而将该目录设置为当前工作目录
                os.mkdir(dirpath)
                tk_outputpath.set(dirpath)
            except FileExistsError:
                tk_outputpath.set(dirpath)
                print("文件夹已存在，无需创建...")   
        elif (re.search(r'第[1一壹]章',name.split('/')[-1])!=None):
            dirpath=DirPath+'/'+(name.split('/')[-1]).split('.')[0]
            try:
                os.mkdir(dirpath)
                tk_outputpath.set(dirpath)
            except FileExistsError:
                tk_outputpath.set(dirpath)
                print("文件夹已存在，无需创建...") 
        else:
            tk_outputpath.set(tk_outputpath.get())
            
        tk_Sfilename.set(name)
        tk_Dfilename.set(name.split('/')[-1])
        tk_Sfilesize.set(gettxtsize(name))
        
        if tk_rbSplit.get()==3:#按关键字分割
            CutTxtForKeyWord(tk_Sfilename.get(),tk_outputpath.get(),tk_Keyword.get())
        elif tk_Unit.get()=='字符':#按文本方式分割
            CutTxtFile(tk_Sfilename.get(),tk_outputpath.get(),tk_Dfilesize.get())
        else:#按二进制流分割
            CutBinFile(tk_Sfilename.get(),tk_outputpath.get(),tk_Dfilesize.get(),tk_Unit.get())
         
            
def ErrorDailog(ErrorCode):#错误对话框
    if ErrorCode=="PermissionError":
        _ErrorCode="请先选择要分割的文件^_^"
    elif ErrorCode=="NameError":
        _ErrorCode="NameError:尝试访问一个不存在的变量"
    elif ErrorCode=="SyntaxError":
        _ErrorCode="SyntaxError:Python的语法错误"
    elif ErrorCode=="UnicodeDecodeError":
        _ErrorCode="请检查您选择的是否是txt文本文件,再确保编码格式为'utf-8',开车前记得先系好安全带哦..."
    else:
        print("ok")
        
    tk.messagebox.showerror("错误提示",_ErrorCode)
        
def gettxtsize(filepath):#获取utf-8文本文件的长度（单位：字符）
    f=open(filepath,'rt',encoding="utf-8")
    num=len(f.read())
    f.close()
    return num
  
def tkOpenfile():#tkinter.filedialog文件选择对话框
    filename=fd.askopenfilename(multiple=False)#选择打开的文件，返回路径+文件名
    if filename.strip()!='':
        tk_Sfilename.set(filename) 
        tk_Dfilename.set(filename.split('/')[-1])
        tk_outputpath.set('/'.join(filename.split('/')[0:-1]))  
        tk_Sfilesize.set(os.path.getsize(filename))#默认为Byte
        print(tk_Sfilename.get(),tk_Dfilename.get(),tk_outputpath.get())
    else:
        print("未选择文件!")

def tkOpendir():#tkinter.filedialog目录选择对话框
    vk_dirs.clear()#清零
    vk_files.clear()#清零
    dirpath=fd.askdirectory()#选择目录，返回目录名
    if dirpath.strip()!='':
        tk_dirpath.set(dirpath)
    else:
        print("未选择目录!")
    for root,dirs,files in os.walk(tk_dirpath.get(), topdown=True):#遍历目录下的所有文件
        for name in files:
            vk_dirs.append('/'.join([root,name]))
            vk_files.append(name)
    print(vk_dirs)
    print(vk_files)
    tk_Sfilesize.set(0)
    

        
def tkEntrySize(Event):#EntryRbSize输入框热键触发
    num=int(tk_Sfilesize.get()/tk_Dfilesize.get())+1
    tk_filenum.set(num)
    
def tkRbSize():#tkinter.RiadioButton单选框事件函数1
    Entry_RbSize.config(state='normal')
    Entry_RbNum.config(state='disabled')
    Entry_RbKeyword.config(state='disabled')
        
def tkEntryNum(Event):#EntryRbNum输入框热键触发
    size=int(tk_Sfilesize.get()/tk_filenum.get())
    if size*tk_filenum.get()<tk_Sfilesize.get():
        tk_filenum.set(tk_filenum.get()+1)
    tk_Dfilesize.set(size)
    
def tkRbNum():#tkinter.RiadioButton单选框事件函数2
    Entry_RbSize.config(state='disabled')
    Entry_RbNum.config(state='normal')
    Entry_RbKeyword.config(state='disabled')
    
def tkEntryKeyword(Event):#EntryRbKeyword输入框热键触发
    ch=Entry_RbKeyword.get()
    tk_Keyword.set(ch)
    
def tkRbKeyword():#tkinter.RiadioButton单选框事件函数3
    Entry_RbSize.config(state='disabled')
    Entry_RbNum.config(state='disabled')
    Entry_RbKeyword.config(state='normal')

def tkSwitchUnit(Event):#源文件长度单位切换事件
    try:
        n=tk_Unit.get()
        size=tk_Sfilesize.get()#获取源文件的大小(byte) 
        if n=='Byte':
            tk_Sfilesize.set(size)
        elif n=='KB':
            tk_Sfilesize.set(round(size/1024,2)) 
        elif n=='MB':
            tk_Sfilesize.set(round(size/1024/1024,3))
        elif n=='GB':
            tk_Sfilesize.set(round(size/1024/1024/1024,4))
        elif n=='字符':
            size=gettxtsize(tk_Sfilename.get())#获取源文件的大小并在界面上显示（单位：字）
            tk_Sfilesize.set(size)
    except PermissionError:
        Pass
        #ErrorDailog("PermissionError")
    except UnicodeDecodeError:
        ErrorDailog("UnicodeDecodeError")
    except:
        print("未知错误")
    else:
        print("单位选择ok")
        
           
def tkCutStxt():#tkinter.Button 单文件分割
    tk_CutMethod=0
    home(tk_CutMethod)
    
def tkCutMtxt():#tkinter.Button 多文件分割
    tk_CutMethod=1
    home(tk_CutMethod)
    
def tkAddDelay():#tkinter.Button 增加延时修饰符
    for name in vk_dirs:
        fs=open(name,'rt',encoding='utf-8')
        ch=fs.readlines()
        fs.close()
        with open(name,'wt',encoding='utf-8') as f:
            for chs in ch:
                print(chs)
                if re.search(r'^\n$',chs)!=None:
                    Pass
                elif re.search(r'^\b第.+章\b',chs)!=None:
                    f.write(chs[0:-1]+'[1.5s]'+chs[-1])
                else:
                    f.write(chs[0:-1]+'[0.5s]'+chs[-1])
        print("正在处理%s"%(name.split('/')[-1]))
    print("处理完毕!")
        
                                    
def tkQuit():#tkinter.Button 退出按钮
    sys.exit()


root.resizable(0,0)#主窗口   
root.geometry('500x500')
root.title("萤火虫TXT文本分割器V1.0")
#root.iconbitmap("./logo.ico")

frame1=tk.Frame(root,bd=2,relief=tk.GROOVE,highlightthickness=2,width=480,height=160)#Frame上
frame2=tk.Frame(root,bd=2,relief=tk.GROOVE,highlightthickness=2,width=480,height=230)#Frame中
frame3=tk.Frame(root,bd=2,relief=tk.FLAT,highlightthickness=2,width=480,height=90)#Frame下

#字体设置
f1 = tkFont.Font(family='microsoft yahei', size=12, weight='normal')
f2 = tkFont.Font(family='microsoft yahei', size=10, weight='normal')
f3 = tkFont.Font(family='times', size=12, slant='italic')
f4 = tkFont.Font(family='Helvetica', size=12, underline=1, overstrike=1)
#字体设置
#Frame1布局
tk.Label(frame1,text="请选择文件(单文件处理)：",font=f2).grid(row=1,column=0,padx=2,pady=10,sticky='W')
tk.Entry(frame1,width=30,font=f2,textvariable=tk_Sfilename).grid(row=1,column=1,padx=0,pady=0)
tk.Button(frame1,text="浏 览...",command=tkOpenfile,font=f2).grid(row=1,column=2,padx=10,pady=5)

tk.Label(frame1,text="请选择目录(多文件处理)：",font=f2).grid(row=2,column=0,padx=2,pady=10,sticky='W')
tk.Entry(frame1,width=30,font=f2,textvariable=tk_dirpath).grid(row=2,column=1,padx=0,pady=0)
tk.Button(frame1,text="浏 览...",command=tkOpendir,font=f2).grid(row=2,column=2,padx=10,pady=5)

tk.Label(frame1,text="命   名   方   式：",font=f2).grid(row=3,column=0,padx=2,pady=10,sticky='W')
tk.Entry(frame1,width=30,font=f2,textvariable=tk_Dfilename).grid(row=3,column=1,padx=0,pady=0)
tk.Label(frame1,text="+ 序号",font=f2).grid(row=3,column=2,padx=10,pady=0)

frame1.grid(row=1,column=1,padx=11,pady=8)
frame1.grid_propagate(0)

#Frame2布局
tk.Label(frame2,text="分割方式",font=f1).grid(row=0,column=0,padx=2,pady=0,sticky='W')

tk.Label(frame2,text="文件总大小为：",font=f2).grid(row=1,column=0,padx=2,pady=8,sticky='W')
tk.Label(frame2,width=10,font=f2,textvariable=tk_Sfilesize).grid(row=1,column=1,padx=0,pady=0)   
Cbx_Sunit=ttk.Combobox(frame2, width = 4, height = 8, textvariable = tk_Unit)
Cbx_Sunit["values"]=("Byte","KB","MB","GB","字符")
Cbx_Sunit.current(0) #选择第一个
Cbx_Sunit.bind("<<ComboboxSelected>>",tkSwitchUnit) #绑定事件,(下拉列表框被选中时，绑定tkSwitchUnit()函数)
Cbx_Sunit.grid(row=1,column=2,padx=0,pady=0) 

tk.Radiobutton(frame2,text="固定大小：",variable=tk_rbSplit,value=1,font=f2,command=tkRbSize).grid(row=2,column=0,padx=2,pady=8,sticky='W')
Entry_RbSize=tk.Entry(frame2,width=10,font=f2,textvariable=tk_Dfilesize)
Entry_RbSize.bind( "<Return>", tkEntrySize)
Entry_RbSize.grid(row=2,column=1,padx=0,pady=0,sticky='W')
tk.Label(frame2,textvariable=tk_Unit,font=f2).grid(row=2,column=2,padx=0,pady=5)
tk.Label(frame2,text="分割数量：",font=f2).grid(row=2,column=3,padx=0,pady=5)
tk.Entry(frame2,width=8,font=f2,textvariable=tk_filenum,state='disabled').grid(row=2,column=4,padx=0,pady=5)
tk.Label(frame2,text="个",font=f2).grid(row=2,column=5,padx=0,pady=5)

tk.Radiobutton(frame2,text="固定数量：",variable=tk_rbSplit,value=2,font=f2,command=tkRbNum).grid(row=3,column=0,padx=2,pady=8,sticky='W')
Entry_RbNum=tk.Entry(frame2,width=10,font=f2,textvariable=tk_filenum)
Entry_RbNum.bind( "<Return>", tkEntryNum)
Entry_RbNum.grid(row=3,column=1,padx=0,pady=0,sticky='W')
tk.Label(frame2,text="个",font=f2).grid(row=3,column=2,padx=0,pady=0)
tk.Label(frame2,text="分割大小：",font=f2).grid(row=3,column=3,padx=0,pady=0)
tk.Entry(frame2,width=8,font=f2,textvariable=tk_Dfilesize,state='disabled').grid(row=3,column=4,padx=0,pady=5)
tk.Label(frame2,textvariable=tk_Unit,font=f2).grid(row=3,column=5,padx=0,pady=0)

tk.Radiobutton(frame2,text="关键字分割：",variable=tk_rbSplit,value=3,font=f2,command=tkRbKeyword).grid(row=4,column=0,padx=2,pady=8,sticky='W')
Entry_RbKeyword=tk.Entry(frame2,width=24,font=f2,textvariable=tk_Keyword)
Entry_RbKeyword.bind( "<Return>", tkEntryKeyword)
Entry_RbKeyword.grid(row=4,column=1,columnspan=3,padx=0,pady=0,sticky='W')
tk.Label(frame2,text="正则表达式",font=f2).grid(row=4,column=4,padx=0,pady=0)


frame2.grid(row=2,column=1,padx=10,pady=5)
frame2.grid_propagate(0)

#Frame3布局
tk.Button(frame3,text="单文件分割",font=f1,command=tkCutStxt).grid(row=0,column=0,padx=10,pady=5,sticky='W')
tk.Button(frame3,text="多文件分割",font=f1,command=tkCutMtxt).grid(row=0,column=1,padx=0,pady=5,sticky='W')
tk.Button(frame3,text="加断句修鉓",font=f1,command=tkAddDelay).grid(row=0,column=2,padx=10,pady=5,sticky='W')
tk.Button(frame3,text="退出程序",font=f1,command=tkQuit).grid(row=0,column=3,padx=50,pady=5,sticky='E')
tk.Label(frame3,text="www.xiao.com 版权所有(C)2022",font=f2).grid(row=1,column=0,padx=0,columnspan=3,pady=12,sticky='W')

frame3.grid(row=3,column=1,padx=10,pady=0)
frame3.grid_propagate(0)

root.mainloop()

