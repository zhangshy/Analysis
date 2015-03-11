打算分析下dota2比赛数据，第一步先获取数据，参考V社提供的[webapi](http://dev.dota2.com/showthread.php?t=58317)，可以获取dota2数据，使用这些接口需要apikey。以DAC为例先获取DAC数据然后进行分析。
# 一、获取数据 #
## 1.1 获取赛事列表 ##
	https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/?key=XXXXX
	将key换成自己的apikey，此接口可以返回dota2赛事列表
从返回值中查找“DOTA_Item_Dota_2_Asia_Championship_2015”，得到"leagueid": 2339，及DAC的leagueid为2339
## 1.2 根据leagueid获取赛事信息 ##
	https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key=XXXXX&league_id=2339
	返回DAC的所有比赛和比赛的简要信息，可以从中找到每场比赛的"match_id"，比如返回值中的第一个match_id为1223581106
根据match_id可以获取比赛的详细信息
## 1.3 根据match_id获取比赛的详细信息 ##
	https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key=XXXXXX&match_id=1223581106
	返回match_id为1223581106的比赛的详细信息，将match_id换成DAC其它比赛的match_id就可以获取DAC其它比赛的详细信息
## 1.4 获取所有比赛数据 ##
使用python的multiprocessing.Pool多线程获取比赛数据

	def getMatchDetails(match_id):
	    url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/"
	    params = {'key':STEAM_APIKEY, 'match_id':match_id}
	    f = urlopen("%s?%s" % (url, urllib.urlencode(params)))
	    detail = json.loads(f.read())['result']
	    print('%d is end' % (match_id))
	    return detail
	
	matches = getDataFromtxt('dac_matches.txt')
    p = Pool(5)
    match_details = p.map(getMatchDetails, [match['match_id'] for match in matches])
    with open('dac_match_details.txt', 'w') as fo:
        fo.write(json.dumps(match_details))

## 1.5 测试获取到数据的正确性 ##
![DAC比赛场数](http://ww4.sinaimg.cn/bmiddle/00612Lottw1eq25907hrcj30cd0cataa.jpg)

可以看到共有491场比赛，应该是包括了预选赛和娱乐赛，其中队长模式477场，solo比赛9场，全阵营选择4场，死亡随机1场

分析一下fy的每分钟金钱

![fy的每分钟金钱](http://ww2.sinaimg.cn/bmiddle/00612Lottw1eq2591u79vj30fr0cowgs.jpg)

可以看到在fy的25场中每分钟金钱中最低200，最高406，平均值289