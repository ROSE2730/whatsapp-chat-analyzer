#!/usr/bin/env python
# coding: utf-8

# In[59]:


import re
import pandas as pd


# In[60]:


f=open('WhatsApp Chat.txt','r',encoding='utf-8')


# In[61]:


data=f.read()


# In[62]:


print(data)


# In[63]:


pattern='\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'  


# In[64]:


messages=re.split(pattern,data)[1:]
messages


# In[65]:


dates=re.findall(pattern,data)
dates


# In[66]:


import pandas as pd



df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Convert the message_date to datetime
df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')

# Rename the column
df.rename(columns={'message_date': 'date'}, inplace=True)

print(df)



# In[67]:


df.shape


# In[68]:


users=[]
messages=[]
for message in df['user_message']:
    entry=re.split('([\w\W]+?):\s',message)
    if entry[1:]:
        users.append(entry[1])
        messages.append(entry[2])
    else:
        users.append('group_ notification')
        messages.append(entry[0])
        
df['users']=users
df['message']=messages
df.drop(columns=['user_message'],inplace=True)

df.head()


# In[69]:


df['year']=df['date'].dt.year
df['month']=df['date'].dt.month_name()
df['day']=df['date'].dt.day
df['hour']=df['date'].dt.hour
df['minute']=df['date'].dt.minute
df.head()


# In[70]:


df[df['users']=='Achal'].shape


# In[71]:


words=[]
for message in df['message']:
    words.extend(message.split())


# In[72]:


len(words)


# In[73]:


df[df['message']=='<Media omitted>\n'].shape[0]


# In[74]:


print(df)


# In[75]:


get_ipython().system('pip install urlextract')

from urlextract import URLExtract
extractor=URLExtract()
urls=extractor.find_urls("This is a test message with a URL: http://example.com")
urls


# In[76]:


links=[]

for message in df['message']:
    links.extend(extractor.find_urls(message))


# In[77]:


links


# In[78]:


len(links)


# In[79]:


x=df['users'].value_counts().head()


# In[80]:


import matplotlib.pyplot as plt
name=x.index
count=x.values
plt.bar(name,count)


# In[81]:


plt.bar(name,count)
plt.xticks(rotation='vertical')
plt.show()


# In[82]:


round((df['users'].value_counts()/df.shape[0])*100,2)


# In[83]:


round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})


# In[84]:


temp=df[df['users']!='group_notification']
temp=temp[temp['message']!='<Media omitted>\n']


# In[86]:


with open('english.txt', 'r', encoding='utf-8') as f:
    stop_words = f.read()
    print(stop_words)


# In[98]:


words = []
for message in temp['message']:
    for word in message.lower().split(): 
        if word not in stop_words:
            words.append(word)

   


# In[99]:


from collections import Counter
pd.DataFrame(Counter(words).most_common(20))


# In[100]:


get_ipython().system('pip install emoji')


# In[101]:


import emoji


# In[103]:


import emoji

emojis = []
for message in df['message']:
    emojis.extend([c for c in message if emoji.is_emoji(c)])


# In[104]:


pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


# In[105]:


df['month_num']=df['date'].dt.month


# In[118]:


timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
timeline


# In[119]:


time=[]
for i in range(timeline.shape[0]):
    time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))


# In[120]:


timeline['time']=time
timeline


# In[121]:


plt.plot(timeline['time'],timeline['message'])
plt.xticks(rotation='vertical')
plt.show()


# In[123]:


df['only_date']=df['date'].dt.date


# In[127]:


daily_timeline=df.groupby('only_date').count()['message'].reset_index()


# In[128]:


plt.figure(figsize=(12,10))
plt.plot(daily_timeline['only_date'],daily_timeline['message'])


# In[131]:


df['day_name']=df['date'].dt.day_name()


# In[132]:


df['day_name'].value_counts()


# In[133]:


df['month'].value_counts()


# In[134]:


df.head()


# In[135]:


period=[]
for hour in df[['day_name','hour']]['hour']:
    if hour==23:
        period.append(str(hour)+"-"+str('00'))
    elif hour==0:
        period.append(str('00')+"-"+str(hour+1))
    else:
        period.append(str(hour)+"-"+str(hour+1))


# In[136]:


df['period']=period


# In[137]:


df.sample(5)


# In[138]:


import seaborn as sns
plt.figure(figsize=(20,6))
sns.heatmap(df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0))
plt.yticks(rotation='horizontal')
plt.show()


# In[ ]:




