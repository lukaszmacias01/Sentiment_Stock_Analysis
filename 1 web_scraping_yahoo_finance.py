
import requests 
import json 
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np

url = 'https://finance.yahoo.com/quote/TSLA/community/'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'})

soup = BeautifulSoup(response.text)

def get_comments(count, offset):
    
    try:

        data = json.loads(soup.select_one('#spotim-config').get_text(strip=True))['config']
        
        url = "https://api-2-0.spot.im/v1.0.0/conversation/read"
        payload = json.dumps({
          "conversation_id": data['spotId'] + data['uuid'].replace('_', '$'),
          "count": count,
          "offset": offset
        })
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
          'Content-Type': 'application/json',
          'x-spot-id': data['spotId'],
          'x-post-id': data['uuid'].replace('_', '$'),
        }
        
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
          
        comments = data['conversation']['comments']
          
        df = pd.DataFrame(comments)
        
        # df = df[['time', 'content']]
        
        df = df[['time', 'content']]
        
        df['content'] = df['content'].apply(lambda x: x[0])
        
        content_expanded = df['content'].apply(pd.Series)
        
        df = pd.concat([df.drop(columns=['content']), content_expanded], axis=1)
        
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        return df 

    except KeyError as e1:
        print(f"Key error occurred: {e1}")
        return None
    except Exception as e2:
        print(f"An unexpected error occurred: {e2}")
        return None

# ---------------------------------------------------------------------------------------

offsets = []   

for i in range(1, 100000, 100):
    offsets.append(i)

for i in offsets:
    df = get_comments(100, i)
    print(i)
    
print('I am done!')

df.to_excel('tesla_comments.xlsx')


 

