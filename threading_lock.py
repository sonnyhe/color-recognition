import threading
import time
# 共享资源
shared_resource = 0

# 创建线程锁
lock = threading.Lock()

def increment():
    global shared_resource
    for _ in range(100000):
        with lock:
            # time.sleep(1)
            shared_resource += 1

def decrement():
    global shared_resource
    for _ in range(100000):
        with lock:
            # time.sleep(1)
            shared_resource -= 1

# 创建两个线程
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=decrement)

# 启动线程
thread1.start()
thread2.start()

# 等待线程执行完成
thread1.join()
thread2.join()
while True:
    time.sleep(1)
    print("共享资源的值:", shared_resource)
