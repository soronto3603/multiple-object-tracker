import time
from time import strftime

start_time = time.time()

f = open("./log"+str(int(start_time))+".txt","w+")
print("start_time", start_time) #출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
print("--- %s seconds ---" %(time.time() - start_time))
f.write( str(time.time() - start_time) )
