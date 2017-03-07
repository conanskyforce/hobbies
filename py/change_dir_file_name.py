# -*- coding:utf-8  -*-
import os 

curpos = os.getcwd()#获得当前目录

curdirs = os.listdir()#当前目录所有文件、目录

os.chdir(curpos+'\\'+curdirs[0])#切换到目的目录
curpos = os.getcwd()
curdirs = os.listdir()#显示目录文件的目录、文件

#目的：进入到每一个文件夹下遍历所有文件，并将它们的名字改为0——最后一个结尾的jpg
q = 1
for a in curdirs:
    i = 1
    os.chdir(curpos+'\\'+a)#进入每个底层文件夹
    curdirs = os.listdir()
    for b in curdirs:
        if os.path.isfile(b):
            if os.path.exists(str(i)+'.jpg'):
                i = i+1
                continue
            os.rename(b,str(i)+'.jpg')
            i = i+1
        print('file: ',b,'rename: ',str(i)+'.jpg')
    print('dir: ',a)
    os.chdir(curpos)
    if os.path.exists(str(q)):
        q=q+1
        continue
    os.rename(a,str(q))
    q=q+1
