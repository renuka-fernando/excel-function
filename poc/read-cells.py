import pandas as pd

# update the worksheet Sample1.xlsx using Apache POI.
# Output is the worksheet Sample1-out.xlsx.
# Open it using Pandas -> read values | this can also done using Apache POI or openpyxl

df = pd.read_excel('Sample1.xlsx', 0, header=None)
print(df)

df = pd.read_excel('Sample1.xlsx', 1, header=None)
print(df)