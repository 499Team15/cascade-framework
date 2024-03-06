import pandas as pd
from lib.twitterdata import load_data

data = load_data()
x = data.head()
print(x)


