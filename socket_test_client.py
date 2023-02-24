import socket   
import sys
import time
from queue import Queue, LifoQueue
import multiprocessing

c=socket.socket()                                           # 创建socket对象
c.connect(('192.168.9.175',4323))    #建立连接
queue_obj = LifoQueue()

def run():
    while True:
        # ab=input('客户端发出：')
        # ab = str(i)
        # ab = "jksdfl{}[]://sdkfksdfkk''s'"
        # print(type(ab))
        # c.send(ab.encode('utf-8')) 
        time.sleep(2)
        # if ab=='quit':
            # c.close()                                               #关闭客户端连接
            # sys.exit(0)
        # else:
            # c.send(ab.encode('utf-8'))                               #发送数据
        data=c.recv(1024) #接收一个1024字节的数据
        queue_obj.put(data)
        # data = queue_obj.get()
        print('收到：',data.decode('utf-8'))
    
proc_loss = multiprocessing.Process(target=run(), args=('loss_incident'))
proc_loss.start()

# data = queue_obj.get()
# print('收到：',data.decode('utf-8'))