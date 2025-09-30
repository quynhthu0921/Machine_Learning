from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([[1., 6.5, 3.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 3.],
                     [4, 6.5, 3.],
                     [3, 7.5, 5.5]])

print(data)
print("-"*10)
cleaned = data.fillna(data.mean())
print(cleaned)