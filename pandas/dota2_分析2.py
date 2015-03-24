
# coding: utf-8

# In[1]:

get_ipython().magic(u'pylab inline')


# In[2]:

import pandas as pd
import numpy as np


# In[3]:

import json


# In[59]:

with open('dac_match_details.txt', 'r') as fi:
    buf = fi.read()
data = json.loads(buf)


# In[60]:

df = pd.DataFrame(data)


# In[14]:

df[df['radiant_name'].map(lambda x:x=='Vici Gaming')]


# In[26]:

print(type(df['radiant_name']))
print(type(df[['radiant_name', 'dire_name']]))
#使用Boolean index结合any方法，选择参赛队伍名称为Vici Gaming的比赛
team_frame = df[(df[['radiant_name', 'dire_name']]=='Vici Gaming').any(1)]


# In[29]:

print(type(team_frame))
team_frame['match_id']


# In[48]:

account_id = 101695162
def getKAD(row):
    for x in row['players']:
        if x['account_id']==account_id:
            if x['deaths']==0:
                return (x['kills']+x['assists'])/1.0
            else:
                return (x['kills']+x['assists'])*1.0/x['deaths']
#使用DataFrame的
kads = [getKAD(row) for index, row in team_frame.iterrows()]
print(kads)


# In[61]:

#参赛人数为10的队长模式的比赛
cap_frame = df[(df['players'].map(lambda x:len(x)==10))&(df['game_mode']==2)]
len(cap_frame)


# In[94]:

#使用reduce方法计算队伍的总击杀数
players = cap_frame.iloc[0]['players'][:5]
def add(x, y):
    if isinstance(x, dict):
        return x['kills']+y['kills']
    return x+y['kills']
reduce(add, players)


# In[100]:

#计算kad和参战率
def getTeamKills(x, y):
    return x+y['kills']
for index, row in cap_frame.iterrows():
    players = row['players']
    radiant_kills = reduce(getTeamKills, players[:5], 0)
    dire_kills = reduce(getTeamKills, players[5:], 0)
    for player in players:
        ka = (player['kills']+player['assists'])*1.0
        #计算kad
        if player['deaths']==0:
            player['kad'] = ka
        else:
            player['kad'] = ka/player['deaths']
        #计算参战率    
        if player['player_slot']<5:
            if radiant_kills==0:
                player['rate'] = 0
            else:
                player['rate'] = ka/radiant_kills
        else:
            if dire_kills==0:
                player['rate'] = 0
            else:
                player['rate'] = ka/dire_kills


# In[101]:

cap_frame['players'][0]


# In[ ]:



