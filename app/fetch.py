import dota2api
import threading  
import time
import dota

D2_API_KEY = '0EB71FBD16527AF680B88D79067AF1B6'

api = dota2api.Initialise(D2_API_KEY)
dotaapi = dota.dota2sql()

class Fetch(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, method, params):  
        threading.Thread.__init__(self)  
        self.method = method  
        self.params = params

        # self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        # while not self.thread_stop:  
            # print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())  
            # time.sleep(self.interval)  
    # def stop(self):  
    #     self.thread_stop = True  
        if self.method == 'get_match_details':
            match = api.get_match_details(match_id=params)
            print(match)

        if self.method == 'get_match_history':
            hist = api.get_match_history(account_id=params)
            print(hist)
            dotaapi.update_hist(hist)

        if self.method == 'items':
            item = api.get_game_items()
            # for value in item['items']:
            #     print(value['name'])
            dotaapi.insert_item(item,'items')

        if self.method == 'heroes':
            item = api.get_game_heroes()
            # for value in item['items']:
            #     print(value['name'])
            dotaapi.insert_item(item,'heroes')

   
def test():  
    # thread1 = Fetch('get_match_details',0)  
    # thread2 = Fetch('get_match_history',1)  
    # thread1.start()  
    thread2 = Fetch('items',1) 
    thread2 = Fetch('heroes',1)  
    thread2.start()
    print('success!')  
    return  
   
if __name__ == '__main__':  
    test()
