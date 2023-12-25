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
    for column in df.columns:
        # Assuming each cell in the column is a list of dictionaries
        counts = df[column].apply(lambda x: sum(1 for item in x if item.get('GTIN', '') != ''))
        gtin_counts[column] = counts.sum()
    return gtin_counts

@app.route('/')
def home():
    data = load_Json()
    df = loadDf(data)
    keys = df.columns.tolist()
    
    return render_template('index.html', keys=keys)

if __name__ == '__main__':
    app.run(debug=True)
