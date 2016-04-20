# -*- coding: utf-8 -*-
import dota2api
import threading  
import time
import dota

D2_API_KEY = '0EB71FBD16527AF680B88D79067AF1B6'

api = dota2api.Initialise(api_key=D2_API_KEY)
sql = dota.dota2sql()

class Fetch(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, method, **kwargs):  
        threading.Thread.__init__(self)  
        self.method = method  
        self.kwargs = kwargs

        # self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        # while not self.thread_stop:  
            # print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())  
            # time.sleep(self.interval)  
    # def stop(self):  
    #     self.thread_stop = True  
        # if self.method == 'get_match_details':
            # match = api.get_match_details(match_id=self.params)
            # print(match)

        if self.method == 'get_match_history':
            self.get_match_history()

        if self.method == 'get_player_summaries':
            self.get_player_summaries()


    def get_necessary_params(self,*args):
        dic = {}
        for params in args:
            # if params not in self.kwargs:
            #     raise TypeError('missing necessary argument '+ params)
            dic[params] = self.kwargs[params]
            self.kwargs[params] = None
        return dic

    def get_player_summaries(self):
        # params = self.get_necessary_params('steamid')
        # return api.get_player_summaries(params['steamid'])
        data = api.get_player_summaries(**self.kwargs)
        if len(data['players']) > 0:
            sql.update_steam_msg(data['players'][0])


    def get_match_history(self):
        match = api.get_match_history(self.get_necessary_params('account_id'))
        return match




   
def test():  
    # thread1 = Fetch('heroes',1)  
    # thread2 = Fetch('items',1)  
    # thread1.start()
    # thread2.start()
    # thread3 = Fetch('get_match_details','1000193456').start()
    thread4 = Fetch(method='get_player_summaries',steamids=76561198121063498).start()
    # thread5 = Fetch('get_match_history',account_id=76482434).start()

    return  
   
if __name__ == '__main__':  
    test()
