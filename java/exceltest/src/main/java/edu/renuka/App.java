package edu.renuka;

import org.apache.poi.xssf.usermodel.XSSFFormulaEvaluator;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.*;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) throws IOException {
        XSSFWorkbook workbook;

        try (InputStream inputStream = new FileInputStream("Sample1.xlsx")){
            workbook = new XSSFWorkbook(inputStream);
            XSSFFormulaEvaluator.evaluateAllFormulaCells(workbook);
        }

        try(OutputStream outputStream = new FileOutputStream("Sample1.xlsx")){
            workbook.write(outputStream);
        }
    }
}
