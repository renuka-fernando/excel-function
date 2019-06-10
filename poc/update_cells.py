import openpyxl

# make changes using openpyxl | this can also done using pandas | OR Apache POI <- JAVA
workbook = openpyxl.load_workbook("Sample1.xlsx")
sheet = workbook.active
sheet['B15'] = 4
sheet['B2'] = '=Output!B3*2'

workbook.save("Sample1.xlsx")
workbook.close()
