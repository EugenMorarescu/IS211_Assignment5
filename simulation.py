import argparse
import csv


class Server:
    def __init__(self):
        
        self.current_request=None
        self.current_time=0
        self.time_remaining=0
    
    def tick(self):
        if self.current_request != None:
            self.time_remaining = self.time_remaining-1
            if self.time_remaining<=0:
                self.current_request=None
        self.current_time+=1
                
    
    def busy(self):
        if self.current_request != None:
            return True
        else:
            return False
        
    def start_next(self,new_request):
        self.current_request = new_request
        self.time_remaining = new_request.get_processing_time() 
        
class Request:
    def __init__(self,req):
        self.timestamp=int(req[0])
        self.processing_time=int(req[2])
        
    def get_stamp(self):
        return self.timestamp
    
    def get_processing_time(self):
        return self.processing_time
    
    def wait_time(self, current_time):
        return current_time - self.timestamp

class Queue:
    def __init__(self):
        self.items=[]
    
    def is_empty(self):
        return self.items ==[]
    
    def enqueue(self,item):
        self.items.insert(0,item)
        
    def dequeue(self):
        return self.items.pop()
    
    def size(self):
        return len(self.items)
        
        
def getData(file):
    
    csvlist=[]
    
    with open(file) as response:
            data = response.read()
        
    new_file=data.strip().split('\n')
    reader=csv.reader(new_file)
    
    for row in reader:
        csvlist.append(row)
    
    return csvlist

def simulateOneServer(file_data):
    server = Server()
    server_queue = Queue()
    waiting_times=[]
    num_sec=11000
    
    for current_second in range(num_sec):
        for i in file_data:
            if int(i[0])==current_second:
                req = Request(i)
                server_queue.enqueue(req)
                
            if (not server.busy()) and (not server_queue.is_empty()):
                next_task = server_queue.dequeue()
                waiting_times.append(next_task.wait_time(current_second))
                server.start_next(next_task)
                
                avg_wait=sum(waiting_times)/len(waiting_times)
                print('The average wait time is ' + str(avg_wait) + ' seconds')
        server.tick()

def simulateManyServers(file_data,serv_num):
    server_list = []
    server_queue = Queue()
    waiting_times=[]
    
    num_sec=11000
    RRcount=0
    
    for n in range(serv_num):
        server_list.append(Server())
        
    for current_second in range(num_sec):
        for i in file_data:
            if int(i[0])==current_second:
                req = Request(i)
                server_queue.enqueue(req)
                
            if (not server_list[RRcount].busy()) and (not server_queue.is_empty()):
                next_task = server_queue.dequeue()
                waiting_times.append(next_task.wait_time(current_second))
                server_list[RRcount].start_next(next_task)
                
                avg_wait=sum(waiting_times)/len(waiting_times)
                print('The average wait time is ' + str(avg_wait) + ' seconds')
                
                RRcount+=1
                if RRcount == serv_num:
                    RRcount=0
                    
        for s in server_list:
            s.tick()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File needed')
    parser.add_argument("--file", type=str)
    parser.add_argument("--servers",type=int,default=1)
    args = parser.parse_args()
    
    file_data = getData(args.file)
    if args.servers == 1:
        simulateOneServer(file_data)
    else:
        simulateManyServers(file_data,args.servers)
        
'''

After running the results I have noticed that the more servers that arei ncluded, the lower the latency. 
This makes sense because if the workload is shared between servers, the wait time to process the data will drop exponentially as the server numbers increase.

'''
    
    