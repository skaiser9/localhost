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
        # Count non-empty 'GTIN' entries in each column
        count = sum(1 for item in df[column] if item.get('GTIN', '') != '')
        gtin_counts[column] = count
    return gtin_counts





@app.route('/')
def home():
    data = load_Json()
    df = loadDf(data)
    keys = df.columns.tolist()

    gtin_counts = calculate_gtin_counts(df)
    print(gtin_counts)
    return render_template('index.html', keys=keys,gtin_counts=gtin_counts)

if __name__ == '__main__':
    app.run(debug=True)
