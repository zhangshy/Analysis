#coding:utf-8
'''
从V社的api中获取dota2数据
api参考：url:http://dev.dota2.com/showthread.php?t=58317
'''
import urllib
from urllib2 import urlopen
import json
from multiprocessing import Pool
from config import STEAM_APIKEY

'''
根据比赛名称获取比赛leagueId
'''
def getLeagueIdByName(names):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/"
    params = {'key':STEAM_APIKEY}
    f = urlopen("%s?%s" % (url, urllib.urlencode(params)))
    data = json.loads(f.read())
    data = data['result']['leagues']
    leagueIds = []
    if isinstance(names, list):
        for name in names:
            for d in data:
                if d['name']==name:
                    leagueIds.append(d['leagueid'])
                    break
    return leagueIds

'''
根据赛事的LeagueId获取赛事的比赛记录
'''
def getMatchByLeagueid(id):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/"
    params = {'key':STEAM_APIKEY, 'league_id':id}
    matches = []
    while True:
        f = urlopen("%s?%s" % (url, urllib.urlencode(params)))
        data = json.loads(f.read())
        matches.append(data['result']['matches'])
        if data['result']['results_remaining']==0:
            break
        params['start_at_match_id'] = matches[-1]['match_id']
    print(len(matches[0]))
    return matches[0]

'''
根据赛事的LeagueId获取赛事的比赛记录，输入LeagueId的list
'''
def getMatchByLeagueids(ids):
    matches=[]
    if isinstance(ids, list):
        p = Pool(processes=4)
        tmp = p.map(getMatchByLeagueid, ids)
        for t in tmp:
            matches+=t
    return matches

'''
根据匹配的match_id获取详细信息
'''
def getMatchDetails(match_id):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
    params = {'key':STEAM_APIKEY, 'match_id':match_id}
    detail={}
    try:
        f = urlopen("%s?%s" % (url, urllib.urlencode(params)), timeout=5)
        detail = json.loads(f.read())['result']
    except Exception, e:
        print("%d %s:%s" %(match_id, Exception, e))
    print('%d is end' % (match_id))
    return detail

if __name__=='__main__':
    leagueNames = ['#DOTA_Item_Major_Allstars_Tournament_Ticket',
                   '#DOTA_Item_SLTV_Star_Series_Season_12_Ticket',
                   '#DOTA_Item_D2CL_Season_5_Ticket']
    leagueIds = getLeagueIdByName(leagueNames)
    print(leagueIds)
    matches = getMatchByLeagueids(leagueIds)
    with open('matches.txt', 'w') as fo:
        fo.write(json.dumps(matches))
    print(len(matches))
    match_details=[]
    p = Pool(processes=4)
    match_details = p.map(getMatchDetails, [match['match_id'] for match in matches])
    with open('match_details.txt', 'w') as fo:
        fo.write(json.dumps(match_details))
    print(len(match_details))
