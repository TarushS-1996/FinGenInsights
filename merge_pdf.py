import os
from PyPDF2 import PdfMerger

def merge_pdfs_in_folder(folder_path, output_pdf_path):
    # Create a PdfMerger object
    merger = PdfMerger()

    # Iterate over each file in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a PDF
        if file_name.lower().endswith('.pdf'):
            # Construct the full path to the PDF file
            pdf_file_path = os.path.join(folder_path, file_name)
            # Open the PDF file
            with open(pdf_file_path, 'rb') as pdf_file:
                # Add the PDF file to the merger object
                merger.append(pdf_file)

    # Write the merged PDF to the output file
    with open(output_pdf_path, 'wb') as output_pdf:
        merger.write(output_pdf)

    print(f"All PDFs in '{folder_path}' merged successfully into '{output_pdf_path}'.")


# Example usage
folder_path = '/Users/shreemoynanda/Desktop/FinGenInsights/Archive'  # Path to the ZIP file containing PDFs
output_pdf_path = '/Users/shreemoynanda/Desktop/FinGenInsights/Stock_Market_Info/Stock_Data/merged_pdf.pdf'  # Path to the output merged PDF file
merge_pdfs_in_folder(folder_path, output_pdf_path)