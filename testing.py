import json
import pandas as pd 

def load_Json():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    return data

def loadDf(data):
    dfs = []
    
    for level, level_data in data.items():
        if level.startswith('level'):
            # Normalize the level data
            df_level = pd.json_normalize(level_data)
            lvlnum = level[5:]
            df_level['level'] = lvlnum
            dfs.append(df_level)
            
    df = pd.concat(dfs, ignore_index=True)
    return df


data = load_Json()
df = loadDf(data)

print(df)