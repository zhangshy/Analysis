#coding:utf-8
'''
url:http://dev.dota2.com/showthread.php?t=58317
'''
import urllib
from urllib2 import urlopen
import json
import threading
from multiprocessing import Pool
from config import STEAM_APIKEY

lock = threading.Lock()
match_details = []

'''
查找DAC:getLeagueListing('Asia_Ch')
DAC的leagueid=2339
'''
def getLeagueListing(name):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/"
    params = {'key':STEAM_APIKEY}
    f = urlopen("%s?%s" % (url, urllib.urlencode(params)))
    data = json.loads(f.read())
    ids = [d['leagueid'] for d in data['result']['leagues'] if d['name'].find(name)!=-1]
    print(ids)

'''
获取DAC比赛信息：matches = getMatchByLeagueid(2339)
'''
def getMatchByLeagueid(id):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/"
    params = {'key':STEAM_APIKEY, 'league_id':id}
    matches = []
    while True:
        f = urlopen("%s?%s" % (url, urllib.urlencode(params)))
        data = json.loads(f.read())
        matches += data['result']['matches']
        if data['result']['results_remaining']==0:
            break
        params['start_at_match_id'] = matches[-1]['match_id']
    '''
    print(matches)
    for match in matches:
        print(match['match_id'])
    for match in matches:
        if match['players']==[]:
            print(match['match_id'])
            matches.remove(match)
    '''
    print(len(matches))
    return matches

def getMatchDetails(match_id):
    url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
    params = {'key':STEAM_APIKEY, 'match_id':match_id}
    f = urlopen("%s?%s" % (url, urllib.urlencode(params)))
    detail = json.loads(f.read())['result']
    print('%d is end' % (match_id))
    return detail

def getMatchDetails2list(match_id):
    detail = getMatchDetails(match_id)
    print(detail)
    lock.acquire()
    match_details.append(detail)
    lock.release()
    print("%s end" % (threading.currentThread().name))


def saveJson2txt(data, txt):
    with open(txt, 'w') as fo:
        fo.write(json.dumps(data))

def getDataFromtxt(txt):
    data=[]
    with open(txt, 'r') as fi:
        data=json.loads(fi.read())
    return data

def getAllMatchDetails():
    matches = getDataFromtxt('dac_matches.txt')
    p = Pool(5)
    match_details = p.map(getMatchDetails, [match['match_id'] for match in matches])
    with open('dac_match_details.txt', 'w') as fo:
        fo.write(json.dumps(match_details))
    print(len(match_details))

if __name__=="__main__":
    pass

