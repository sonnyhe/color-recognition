import socket
import sys
import time
import threading
# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = '192.168.9.175'                                                

# 设置端口号
port = 4366

# 连接服务，指定主机和端口
s.connect((host, port))

def run():
    # s.connect((host, port)) 
    msg = s.recv(1024)
    s.close()
    print(msg.decode('utf-8'))
while True:
    # 接收小于 1024 字节的数据
    thread1 = threading.Thread(name='t1', target=run)
    thread1.start()
    time.sleep(2)