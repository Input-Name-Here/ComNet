#test.py
# Testing of threading
from threading import Thread, Lock
import time
lst = [0]



def thr(l):
	global lst
	while True:
		lock.acquire()
		print(lst)
		print(hex(id(lst)))
		lock.release()
		time.sleep(0.3)


lock = Lock()
print(hex(id(lst)))
print("----")
thread = Thread(target=thr,args=(lock,))
thread.start()

time.sleep(1)
print("change")
lock.acquire()
lst=[1]
lock.release()
print(lst)
thread.join()