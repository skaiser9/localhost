from flask import Flask, render_template
import json
import pandas as pd 

app = Flask(__name__)

def load_Json():
    with open('data/data.json', 'r') as f:
        data = json.load(f)
    return data

def loadDf(data):
    df = pd.DataFrame(data)
    return df

    
def calculate_gtin_counts(df):
    gtin_counts = {}
    gtin_counts['time'] = df['time']

    return gtin_counts

##function to show the GTIN counts for a specific level 
def level_unique_values(df,level):
    #Get the unique GTIN values for the level 
    unique_values = df.loc[df['level'] == level, 'GTIN'].unique().tolist()
    return unique_values


##create a function to load the contents of each level when clicked 
@app.route('/level/<level>')
def level_route(level):
    return render_template('level.html', level_route=level)

@app.route('/')
def home():
    data = load_Json()
    df = loadDf(data)
    keys = df.columns.tolist() #change the keys variable to the new normalized df 

    gtin_counts = calculate_gtin_counts(df)
    return render_template('index.html', keys=keys,gtin_counts=gtin_counts, time=data['time'])

if __name__ == '__main__':
    app.run(debug=True)
