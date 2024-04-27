import pandas as pd
from fpdf import FPDF

def xlsx_to_pdf(input_file, output_file):
    # Read Excel file
    try:
        xls = pd.ExcelFile(input_file)
        sheets = xls.sheet_names
    except FileNotFoundError:
        print("Error: Input file not found.")
        return
    
    # Combine data from all sheets into one DataFrame
    all_data = pd.DataFrame()
    for sheet_name in sheets:
        df = pd.read_excel(xls, sheet_name)
        all_data = pd.concat([all_data, df], ignore_index=True)
    
    # Initialize PDF with landscape orientation
    pdf = FPDF(orientation='L')
    pdf.add_page()

    # Set font for the header
    pdf.set_font("Arial", size=12)

    # Write header with specified column order
    columns = ['Date', 'Ticker', 'Name', 'Current Price', 'High', 'Low', 'Volume']
    for col in columns:
        pdf.cell(40, 10, str(col), border=1)
    pdf.ln()

    # Set font for the data
    pdf.set_font("Arial", size=10)

    # Write data
    for _, row in all_data.iterrows():
        for col in columns:
            pdf.cell(40, 10, str(row[col]), border=1)
        pdf.ln()

    # Output PDF
    pdf.output(output_file)

if __name__ == "__main__":
    input_file = "Airflow Scripts/Data/stock_info.xlsx"
    output_file = "Airflow Scripts/Data/stock_info.pdf"
    xlsx_to_pdf(input_file, output_file)
