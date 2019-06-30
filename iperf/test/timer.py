"""
# '專案名稱: 計時器
# '功能描述:
# '
# '版權所有: Dunk
# '程式撰寫: Dunk
# '撰寫日期：2018/11/17
# '
# '改版日期:
# '改版備註:
# '
http://dunkkm.blogspot.com/2018/11/python_62.html
"""
import time
import requests
import threading 

def clock_timer():
    """console計時器"""
    #初始目前時間
    print('Timer start，press"Enter" button to calcuate interval，Keyin "exit" to escape timer.')
    in_value = input()
    if in_value == 'exit':
        return
    print('Start Timer!!!')
    start_time = time.time()
    last_time = start_time
    lap_num = 1
    #紀錄並列印時間
    try:
        while True:
            in_value = input()
            if in_value == 'exit':
                break
            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            #print('Lap #%s: %s (%s)'\
            #      %(lap_num, total_time, lap_time), end='')
            print("{}: {} {}".format(lap_num, total_time, lap_time))
            lap_num += 1
            last_time = time.time()
        print('End Timer!!!')
    except KeyboardInterrupt:
        exit()
def func():
    pass

def continuous_clock_timer(duration_sec):
    #print('Timer start，press"Enter" button to calcuate interval，Press "Ctrl+C" to escape timer.')
    #in_value = input()
    #if in_value == 'exit':
    #    return
    print('Start Time Duratin:{} sec(s)!!!'.format(duration_sec))
    start_time = time.time()
    last_time = start_time
    total_time = round(time.time() - start_time, 2)
    lap_num = 1
    try:
        while True:
            if total_time > duration_sec:
                print('Duratin:{}sec(s) End Timer!!!'.format(duration_sec))
                break

            lap_time = round(time.time() - last_time, 2)
            total_time = round(time.time() - start_time, 2)
            print("{}: {} {}".format(lap_num, total_time, lap_time))
            
            timer = threading.Timer(0,func)
            timer.start()
            time.sleep(2) ## 等待5s
            timer.cancel()##停止定時器
            #print("5s到了定時器退出")

            lap_num += 1
            last_time = time.time()
        
    except KeyboardInterrupt:
        print('\nEnd Timer!!!')
        exit()

# https://www.itread01.com/p/517098.html
def run(): 
    print("timer run:" ,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
def run_timer():
    timer = threading.Timer(1, run)
    timer.start()
    time.sleep(5) ## 等待5s
    timer.cancel()##停止定時器
    print("5s到了定時器退出")
    print("timer end:" ,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def run_continuous_clock_timer():
    timer = threading.Timer(1, continuous_clock_timer)
    timer.start()
    time.sleep(5) ## 等待5s
    timer.cancel()##停止定時器
    print("5s到了定時器退出")
    print("timer end:" ,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

class ProgramCounter():
    """程式計時器"""
    def __init__(self, start_time=0, end_time=0):
        self.start_time = start_time
        self.end_time = end_time

    def set_start_time(self):
        """開始時間"""
        self.start_time = time.time()

    def set_end_time(self):
        """結束時間"""
        self.end_time = time.time()

    def get_time_interval(self):
        """取得執行時間"""
        return str(round(self.end_time - self.start_time, 2))

if __name__ == '__main__':
    PC = ProgramCounter()
    PC.set_start_time()
    URL = r'https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json'
    RESPONSE = requests.get(URL)
    RESPONSE.raise_for_status()
    PC.set_end_time()
    print(PC.get_time_interval())    

    #clock_timer()
    #continuous_clock_timer()
    
    #run_timer()
    continuous_clock_timer(10)