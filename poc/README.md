## Update existing `Sample1.xlsx` file

Existing sheet: [`Sample1.xlsx`](Sample1.xlsx)
Sheet: `input`

|     | A                     | B         |
|-----|-----------------------|-----------|
| 1   | ASSETVALUE            | 8,000,000 |
| 2   | ALLOCATIONFLAG        | DETAILED  |
| ... | ...                   | ...       |
| 15  | ClientLiabilityValue  | 1         |
| 16  | ClientPSLiabilityPV01 | 2         |
| 17  | ClientPSLiabilityIE01 | 3         |

Sheet: `output`

|     | A           | B                               |
|-----|-------------|---------------------------------|
| ... | ...         | ...                             |
| 3   | OUTPUT_VAL3 | `=AVERAGE(Input!B15:Input!B17)` |

### 1. Update cells

Update can be a value change or formula change. It is possible to use `openpyxl`, Apache POI.

Run `python update_cells.py`

```py
import openpyxl

# make changes using openpyxl | this can also done using pandas | OR Apache POI <- JAVA
workbook = openpyxl.load_workbook("Sample1.xlsx")
sheet = workbook.active
sheet['B15'] = 4
sheet['B2'] = '=Output!B3*2'

workbook.save("Sample1.xlsx")
workbook.close()
```

### 2. Recalculate all formulas

Run `java -jar exceltest-1.0-SNAPSHOT.jar`

```java
XSSFWorkbook workbook;

try (InputStream inputStream = new FileInputStream("Sample1.xlsx")){
    workbook = new XSSFWorkbook(inputStream);
    XSSFFormulaEvaluator.evaluateAllFormulaCells(workbook);
}

try(OutputStream outputStream = new FileOutputStream("Sample1.xlsx")){
    workbook.write(outputStream);
}
```

Now average on `Output!B3` and `Input!B2` should be updated.

### 3. Read file

This cal also done using Apache POI.
Run the file `python read-cells.py`

```py
import pandas as pd

df = pd.read_excel('Sample1.xlsx', 0, header=None)
print(df)

df = pd.read_excel('Sample1.xlsx', 1, header=None)
print(df)
```

#### Outputs

| 0 | 1              | B       |
|---|----------------|---------|
| 0 | ASSETVALUE     | 8000000 |
| 1 | ALLOCATIONFLAG | 6       |

| 0 | 1                    | B     |
|---|----------------------|-------|
| 0 | OUTPUT_VAL1          | 16000 |
| 1 | OUTPUT_VAL2 -7999996 | 6     |
| 2 | OUTPUT_VAL3          | 3     |

`Output!B3` is updated with `3` and `Input!B2` updated with `6`.