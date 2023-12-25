   
import pandas as pd
import numpy as np


#create a new dataframe 
# Create a new dataframe
df = pd.DataFrame()

#add random numbers to the dataframe
df['rand'] = np.random.rand(100)

#print the dataframe 
print(df.head())
