# -*- coding: utf-8 -*-
import pymysql
import traceback
import hashlib
import dota2api
import time
import queue
import threading

D2_API_KEY = '0EB71FBD16527AF680B88D79067AF1B6'


def md5(string):
    if type(string) is bytes:
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()
    else:
        return ''


# 该函数用于将其自动转换为int并判断是否加''
def get_value_sql(val):
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        if str.isdigit(val):
            return str(val)
    return '"%s"' % val


def get_update_sql(dic):
    sql = ''
    for k, v in dic.items():
        sql += '`' + k + '`= ' + get_value_sql(v) + ','
    return sql[:-1]


def get_insert_sql(dic, no_key_set=None):
    col = ''
    val = ''
    for k, v in dic.items():
        if no_key_set is None or k not in no_key_set:
            col += '`' + k + '`,'
            val += get_value_sql(v) + ','
    return '(' + col[:-1] + ') VALUES (' + val[:-1] + ');'


def get_insert_sql_key(dic, no_key_set=None):
    col = ''
    for k in dic:
        if no_key_set is None or k not in no_key_set:
            col += '`' + k + '`,'
    return '(' + col[:-1] + ') VALUE '


def get_insert_sql_value(dic, no_key_set=None):
    val = ''
    for k, v in dic.items():
        if no_key_set is None or k not in no_key_set:
            val += get_value_sql(v) + ','
    return '(' + val[:-1] + '), '


def get_insert_sql_lst(lst, no_key_set=None):
    sql = get_insert_sql_key(lst[0], no_key_set)
    for item in lst:
        sql += get_insert_sql_value(item, no_key_set)
    return sql[:-2]


class Dota2SQL:
    host = 'ali.banixc.com'
    user = 'dota'
    passwd = 'dotaer'
    db = 'dota'
    port = 3306
    charset = 'utf8'
    fetch_list = queue.Queue()
    api = dota2api.Initialise(api_key=D2_API_KEY)
    try:
        conn = pymysql.connect(host, user, passwd, db, port, charset)
        print('db conn')
    # except Exception as e:
    #     print(e)
    except:
        traceback.print_exc()

    # 以下函数请勿调用
    @staticmethod
    def fetch():

        def fetch_all(fetch_object):
            fetch_type = fetch_object['fetch_type']
            fetch_id = ''
            try:
                if fetch_type == 'match':
                    fetch_id = fetch_object['match_id']
                    data = Dota2SQL.api.get_match_details(**fetch_object)
                    Dota2SQL.__insert_match(data)

                elif fetch_type == 'history':
                    fetch_id = fetch_object['account_id']

                    sql = 'SELECT `last_update` FROM `account` WHERE `account_id` = %s LIMIT 1' % fetch_id
                    data = Dota2SQL.__query(sql)
                    if len(data) > 0:
                        fetch_object['date_min'] = data[0][0] + 1

                    results_remaining = 1
                    lst = []
                    last_match_start_time = 0
                    while results_remaining != 0:
                        data = Dota2SQL.api.get_match_history(**fetch_object)
                        if data['num_results'] > 0:
                            last_match = data['matches'][0]['start_time']
                            last_match_start_time = last_match if last_match > last_match_start_time else last_match_start_time
                            results_remaining = data['results_remaining']
                            templst = [match['match_id'] for match in data['matches']]
                            lst.extend(templst)
                            fetch_object['start_at_match_id'] = min(templst) - 1
                        else:
                            break

                    for match in lst:
                        Dota2SQL.update_match_details(match_id=match)

                    if last_match_start_time > 0:
                        sql = 'REPLACE INTO `account` (`account_id`,`last_update`) VALUE (%s,%s);' % (
                            fetch_id, last_match_start_time)
                        Dota2SQL.__exe(sql)

            except Exception as e:
                if fetch_object['fail'] == 6:
                    print(fetch_type + str(fetch_id) + '失败7次，已放弃')
                    sql = 'INSERT INTO `fail` (`id`,`type`) VALUES (%s,"%s");' % (fetch_id, fetch_type)
                    Dota2SQL.__exe(sql)
                else:
                    fetch_object['fail'] += 1
                    Dota2SQL.fetch_list.put(fetch_object)

        def loop():

            while True:
                time.sleep(0.1)
                if threading.active_count() > 5:
                    continue
                while not Dota2SQL.fetch_list.empty():
                    time.sleep(1)
                    fetch = Dota2SQL.fetch_list.get()
                    thread = threading.Thread(target=fetch_all, args=(fetch,))
                    # fetch_all(fetch)
                    print(fetch)
                    thread.start()

        threading.Thread(target=loop).start()

    @staticmethod
    def __query(sql):
        try:
            cur = Dota2SQL.conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            # print(data)
            return data  # 返回结果集
        except:
            traceback.print_exc()

    @staticmethod
    def __exe(sql):
        try:
            # conn = pymysql.connect(Dota2SQL.host, Dota2SQL.user, Dota2SQL.passwd, Dota2SQL.db, Dota2SQL.port,
            #                        Dota2SQL.charset)
            cur = Dota2SQL.conn.cursor()
            cul = cur.execute(sql)
            Dota2SQL.conn.commit()
            cur.close()
            return cul  # 返回受影响的行数
        except:
            print(sql)
            traceback.print_exc()

    @staticmethod
    def exe(sql):
        return Dota2SQL.__exe(sql)

    @staticmethod
    def __insert_match(match):
        no_key_set = (
            'lobby_name', 'lobby_name', 'players', 'game_mode_name', 'barracks_status_radiant', 'cluster_name')
        sql = 'INSERT INTO `match` %s' % get_insert_sql(match, no_key_set)
        # Dota2SQL.__exe(sql)

        match_id = match['match_id']
        if 'players' in match:
            for palyer in match['players']:
                palyer['match_id'] = match_id
                no_key_set = (
                    'leaver_status_description', 'hero_name', 'ability_upgrades', 'item_0_name', 'item_1_name',
                    'item_2_name', 'item_3_name', 'item_4_name', 'item_5_name', 'additional_units')
                sql += 'INSERT INTO `players` %s' % get_insert_sql(palyer, no_key_set)
                # Dota2SQL.__exe(sql)

                player_slot = palyer['player_slot']
                if 'ability_upgrades' in palyer:
                    def update_key(ability_upgrade):
                        ability_upgrade['player_slot'] = player_slot
                        ability_upgrade['match_id'] = match_id
                        return ability_upgrade

                    sql += 'INSERT INTO `ability_upgrades` %s;' % get_insert_sql_lst(
                        list(map(update_key, palyer['ability_upgrades'])))
                    # Dota2SQL.__exe(sql)

                if 'additional_units' in palyer:
                    for additional_unit in palyer['additional_units']:
                        additional_unit['match_id'] = match_id
                        additional_unit['player_slot'] = player_slot
                        # sql += 'INSERT INTO `additional_units` %s;' % get_insert_sql(additional_unit)
                        sql += 'INSERT INTO `additional_units` %s' % get_insert_sql(additional_unit)

                        # Dota2SQL.__exe(sql)
                        # print('INSERT INTO `additional_units` %s;' % get_insert_sql(additional_unit))
        # print(sql)
        return Dota2SQL.__exe(sql)

    # def update_steam_msg(self, dic):
    #     steamid = int(dic['steamid'])
    #     sql = 'REPLACE INTO `steam` %s' % get_insert_sql(dic)
    #     return self.__exe(sql)

    # 以上函数请勿调用

    # 以下函数可供View层调用
    @staticmethod
    def login(username, password):
        sql = 'select `uid`,`username`,`password` from `users` where `username` = "' + username + '";'
        data = Dota2SQL.__query(sql)
        if not data:
            return 'USER_NOT_FIND'
        if md5((username + password + '+5').encode('utf-8')) == data[0][2]:
            return data[0]
        return 'PASSWORD_ERROR'

    # 注册时将数据提交到数据库
    @staticmethod
    def register(username, password, email):
        sql = 'insert into `users` (`username`,`password`,`email`) VALUES ( "' + username + '" , "' + md5(
            (username + password + '+5').encode('utf-8')) + '","' + email + '");'
        return Dota2SQL.__exe(sql)

    # 注册时用于验证是否该用户名或者邮箱已经存在
    @staticmethod
    def judge_user(username, email):
        sql = 'select * FROM `users` WHERE `username` = "' + username + '" ;'
        data = Dota2SQL.__query(sql)
        if len(data) > 0:
            return 'USERNAME_EXIST'
        sql = 'select * FROM `users` WHERE `email` = "' + email + '";'
        data = Dota2SQL.__query(sql)

        if len(data) > 0:
            return 'EMAIL_EXIST'
        return 'NOTHING_EXIST'

    @staticmethod
    def get_user(username):
        sql = 'select * FROM `users` WHERE `username` = "' + username + '" ;'
        return Dota2SQL.__query(sql)

    @staticmethod
    def change_pwd(email, password):
        sql = 'select `uid`,`username`,`password` from `users` where `email` = "' + email + '";'
        data = Dota2SQL.__query(sql)
        username = data[0][1]
        sql = 'update `users` set `password` = "' + md5(
            (username + password + '+5').encode('utf-8')) + '" where email = "' + email + '";'
        Dota2SQL.__exe(sql)

    @staticmethod
    def get_heroes():
        sql = 'SELECT * FROM `heroes`;'
        return Dota2SQL.__query(sql)

    @staticmethod
    def get_heroes_abilities():
        sql = 'SELECT * FROM `heroes_abilities`;'
        return Dota2SQL.__query(sql)

    @staticmethod
    def get_items():
        sql = 'SELECT * FROM `items`;'
        return Dota2SQL.__query(sql)

    @staticmethod
    def get_steamid_user(username):
        sql = 'select steamid FROM `users` WHERE `username` = "' + username + '" ;'
        data = Dota2SQL.__query(sql)
        if len(data) > 0:
            return data[0][0]
        else:
            return None

    @staticmethod
    def get_watch_list(uid):
        sql = 'SELECT * FROM `watchs` WHERE `uid` = %d;' % uid;
        return Dota2SQL.__query(sql)

    @staticmethod
    def add_watch_list(uid, account_id):
        sql = 'INSERT INTO `watchs` (`uid`,`account_id`) VALUES (%d,%d)' % (uid, account_id)
        return Dota2SQL.__exe(sql)

    @staticmethod
    def get_steam_msg(steam_id):
        data = Dota2SQL.api.get_player_summaries(steamids=steam_id)
        # if len(data['players']) > 0:
        #     self.dsql.update_steam_msg(data['players'][0])
        # Fetch(method='get_player_summaries', steamids=steamid).start()
        # sql = 'SELECT * FROM `steam` WHERE `steamid` = %s' % steamid;
        # print(sql)
        # data = self.__query(sql)
        # print(data)
        if len(data) > 0:
            return data[0]
        else:
            return None

    @staticmethod
    def set_steam_id(uid, steam_id):
        data = Dota2SQL.get_steam_msg(steam_id)
        if data is not None:
            sql = 'UPDATE `users` SET `steamid` = %d WHERE `uid` = %d' % (steam_id, uid)
            return Dota2SQL.__exe(sql)
        else:
            return -1

    @staticmethod
    def set_account_id(uid, account_id):
        sql = 'UPDATE `users` SET `account_id` = %d WHERE `uid` = %d' % (account_id, uid)
        return Dota2SQL.__exe(sql)

    # def get_player_summaries(self, **kwargs):
    #     data = Dota2SQL.api.get_player_summaries(**kwargs)
    #     if len(data['players']) > 0:
    #         self.dsql.update_steam_msg(data['players'][0])

    @staticmethod
    def update_match_history(**kwargs):
        kwargs['fail'] = 0
        kwargs['fetch_type'] = 'history'
        Dota2SQL.fetch_list.put(kwargs)

    @staticmethod
    def update_match_details(**kwargs):
        kwargs['fail'] = 0
        kwargs['fetch_type'] = 'match'
        Dota2SQL.fetch_list.put(kwargs)

    @staticmethod
    def get_queue_size():
        return Dota2SQL.fetch_list.qsize()

    @staticmethod
    def get_match_details(match_id):
        sql = 'SELECT * FROM `match` WHERE `match_id` = %s LIMIT 1;' % match_id
        data = Dota2SQL.__query(sql)
        if len(data) > 0:
            match = data[0]
            sql = 'SELECT * FROM `players` WHERE `match_id` = %s LIMIT 1;' % match_id
            data = Dota2SQL.__query(sql)
            if len(data) > 0:
                # dic = map(lambda data: data['player_slot'], data, data)
                players = data

                sql = 'SELECT `player_slot`,`level`,`ability`,`time` FROM `ability_upgrades` WHERE `match_id` = %s LIMIT 1;' % match_id

                data = Dota2SQL.__query(sql)
                if len(data) > 0:
                    ability_upgrades = dict()

                    for ability_upgrade in data:
                        player_slot = ability_upgrade['player_slot']
                        ability_upgrade['player_slot'] = None
                        if ability_upgrades.get(player_slot) is None:
                            ability_upgrades[player_slot] = list()
                        ability_upgrades[player_slot].append(ability_upgrade)

                sql = 'SELECT `unitname`,`item_0`,`item_1`,`item_2`,`item_3`,`item_4`,`item_5`,`player_slot` FROM `additional_units` WHERE `match_id` = %s LIMIT 1;' % match_id
                data = Dota2SQL.__query(sql)
                if len(data) > 0:
                    additional_units = dict()

                    for additional_unit in data:
                        player_slot = additional_unit['player_slot']
                        additional_unit['player_slot'] = None
                        if additional_unit.get(player_slot) is None:
                            additional_unit[player_slot] = list()
                            additional_unit[player_slot].append(additional_unit)
            for player in players:
                if ability_upgrades.get(player['player_slot']) is not None:
                    player['ability_upgrades'] = ability_upgrades[player['player_slot']]
                if additional_unit.get(player['player_slot']) is not None:
                    player['additional_unit'] = additional_unit[player['player_slot']]
            match['players'] = players
            return match
        return None


    @staticmethod
    def get_match_history(account_id):
        sql = ''

def test():
    # thread1 = Fetch('heroes',1)  
    # thread2 = Fetch('items',1)  
    # thread1.start()
    # thread2.start()
    # thread3 = Fetch('get_match_details','1000193456').start()
    # thread4 = Fetch(method='get_player_summaries',steamids=76561198121063498).start()
    # thread5 = Fetch('get_match_history',account_id=76482434).start()
    pass


def test2():
    Dota2SQL.exe(
        'TRUNCATE `match`;TRUNCATE `players`;TRUNCATE `ability_upgrades`;TRUNCATE `additional_units`;TRUNCATE `account`;TRUNCATE `fail`;')
    Dota2SQL.fetch()
    # Dota2SQL.get_match_history(account_id=76482434)
    # Dota2SQL.get_match_details(match_id=2311948390)
    Dota2SQL.update_match_history(account_id=160797770)
    # print(dsql.set_account_id(31,1232131123))
    # print(
    # dsql.get_steam_msg(76561198299172651)
    # )

    print(Dota2SQL.get_queue_size())
    # Dota2SQL.close()


def test3():
    print(Dota2SQL.get_match_details(match_id=1192257920))


if __name__ == '__main__':
    test2()
    pass
