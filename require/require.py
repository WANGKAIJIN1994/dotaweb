# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_restful import Resource, Api
import dota2api

# dotaapi = dota2api.Initialise(language='zh-CN')
dotaapi = dota2api.Initialise()


app = Flask(__name__)
api = Api(app)

#所有游戏物品
class GetItems(Resource): 
    def get(self):
        #dotaapi.update_game_items() #更新游戏物品列表
        items = dotaapi.get_game_items()
        return items

#所有英雄
class GetHeroes(Resource): 
    def get(self):
        #dotaapi.update_heroes() #更新游戏英雄列表
        items = dotaapi.get_heroes()
        return items

#联赛列表
class GetLeagueListing(Resource): 
    def get(self):
        leist  = dotaapi.get_league_listing()
        return leist

#直播列表
class GetLiveLeagueGames(Resource): 
    def get(self):
        liveGames = dotaapi.get_live_league_games()
        return liveGames

#比赛详情
class GetMatch(Resource): 
    def get(self, match_id):
        match = dotaapi.get_match_details(match_id)
        return match

#比赛历史列表
class GetMatchHistory(Resource): 
    def get(self, account_id, **kwargs):
        params = request.args
        if 'account_id' not in kwargs:
            kwargs['account_id'] = account_id
        # kwargs['start_at_match_id'] = 1989691645
        # kwargs['start_time'] = 1460456786
        for key in params:
            kwargs[key] = params[key]
        print(kwargs)

        hist  = dotaapi.get_match_history(kwargs)
        return hist

#get_match_history_by_seq_num

#玩家摘要
class GetPlayerSummaries(Resource): 
    def get(self, steamids):
        summaries = dotaapi.get_player_summaries(steamids)
        return summaries

#战队详细
class GetTeamInfo(Resource):
    def get(self, start_at_team_id, **kwargs):
        #print(teams_requested)
        #if teams_requested  is None:
        team = dotaapi.get_team_info_by_team_id(start_at_team_id)
       # else:
          #  team = dotaapi.get_team_info_by_team_id(start_at_team_id)
        return team
#get_tournament_prize_pool

api.add_resource(GetItems, '/items/')
api.add_resource(GetHeroes, '/heroes/')
api.add_resource(GetLeagueListing, '/league/')
api.add_resource(GetLiveLeagueGames, '/live/')
api.add_resource(GetMatch, '/match/<string:match_id>/')
api.add_resource(GetMatchHistory, '/history/<string:account_id>/')
api.add_resource(GetPlayerSummaries, '/player/<string:steamids>/')
api.add_resource(GetTeamInfo, '/team/<string:start_at_team_id>/','/team/<string:start_at_team_id>/requested/<string:teams_requested>/')



if __name__ == '__main__':
    app.run(debug=True,port=8081)
    #app.run(debug=False)


