# -*- coding: utf-8 -*- 
import socket
import json                                            # 导入json包
 
server = socket.socket()  
server.bind(('192.168.9.175', 4366))                       # 将socket绑定到本机IP并且设定一个端口
server.listen(5)                                       # 设置可以监听5个连接
 
exit = ''
while True:
    con, addr = server.accept()                        # 会一直等待，直到连接客户端成功
    print('连接到: ', addr)
    while con:
        msg = con.recv(1024).decode('utf-8')           # 接受数据并按照utf-8解码
        print('收到的数据是: ', msg)
        print('收到的数据类型是: ',type(msg))
        msg = json.loads(msg)                          # json对数据进行解析，得到dict数据
        for i in msg.keys():
                if isinstance(msg[i], dict):
                         for j in msg[i].keys():
                                   print('key ', j, ' with value ', msg[i][j]) 
        if msg == 'break':
                con.close()
                exit = 'break'
                break
    
    if exit == 'break':
        break
server.close()
