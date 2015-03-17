
# coding: utf-8

# In[1]:

get_ipython().magic(u'pylab inline')


# In[2]:

import pandas as pd
import numpy as np


# In[3]:

with open('dac_match_details.txt', 'r') as fi:
    data = fi.read()
import json
jsonData = json.loads(data)


# In[5]:

df = pd.DataFrame(jsonData)
print(len(df))


# In[30]:

#print(type(df.iloc[0]))
df.iloc[0]
#df.iloc[0]['players'][0]['account_id']


# In[17]:

account_id = 0
def getByAccount_id(players):
    for player in players:
        if player['account_id'] == account_id:
            return True
    return False
account_id = 101695162
player_frame = df[df['players'].map(getByAccount_id)]
player_frame['match_id']


# In[18]:

print(len(player_frame))


# In[24]:

player_frame['duration'].plot()


# In[33]:

player_frame.plot(kind='bar', x='match_id', y=['negative_votes', 'positive_votes'])


# In[43]:




# In[ ]:



