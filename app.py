from flask import Flask, render_template
import json
import pandas as pd 
import csv 
app = Flask(__name__)


csv_file = 'data/GTIN.csv'

def create_dict(csv_file):
    gtin_part = {}
    with open(csv_file, newline ='', encoding ='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            part,gtin  = row
            gtin_part[gtin] = part
    return gtin_part

dict = create_dict(csv_file)

def get_part(gtin):
    return dict.get(gtin,"No part found")

gtin = "10715001001198"
part = get_part(gtin)
print(part)


def load_Json():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    return data

def loadDf(data):
    df = pd.DataFrame(data)
    return df

def loadDataFrame(data):
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

df = loadDataFrame(data)

def levelDetails(level):
    level = str(level)
    #print a dataframe with the details of the level 
    df_level = df.loc[df['level'] == level]
    level_data = df_level.to_dict('records')
    
    return level_data

def partsInLevel(level):
    level = str(level)
    df_level = df.loc[(df['level'] == level) & (df['GTIN'] != ""), 'GTIN'].unique().tolist()
    parts = [get_part(gtin) for gtin in df_level]  # Convert GTINs to Part codes
    return parts


def calculate_gtin_counts(df):
    gtin_counts = {}
    gtin_counts['time'] = ""
    # for each unique level, count the number of non-empty GTINs
    for level in df['level'].unique().tolist():
        gtin_counts[level] = df.loc[(df['level'] == level) & (df['GTIN'] != ""), 'GTIN'].count()
    
    return gtin_counts

##function to show the GTIN counts for a specific level 
def level_unique_values(df,level):
    #Get the unique GTIN values for the level 
    unique_values = df.loc[df['level'] == level, 'GTIN'].unique().tolist()
    return unique_values

def invSummary():
    
    #Group by GTIN and LOT 
    df_inv = df.groupby(['GTIN', 'Lot'])
    sum = df_inv['QTY'].sum().reset_index()
    sum['GTIN'] = sum['GTIN'].apply(get_part)
    sum = sum.drop(sum.index[0]) #Drop the 0 index row, it contains 0 values.
    return sum

@app.route('/')
def home():
    # global df
    # data = load_Json()
    # df = loadDataFrame(data)
    #keys = df.columns.tolist() #change the keys variable to the new normalized df 
    keys = df['level'].unique().tolist()
    gtin_counts = calculate_gtin_counts(df)
    unique_gtins_per_level = {level: partsInLevel(level) for level in keys}
    sum = invSummary()
    sum = sum.to_dict(orient ='records')
    return render_template('index.html', keys=keys,gtin_counts=gtin_counts, time=data['time'], unique_gtins=unique_gtins_per_level, sum=sum)

##create a function to load the contents of each level when clicked 
@app.route('/level/<int:level>')
def level_route(level):
    level_details = levelDetails(level)
    print(level_details)
    return render_template('level.html', level_route=level,level_details=level_details)
if __name__ == '__main__':
    app.run(debug=True)
