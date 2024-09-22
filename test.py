import PyPDF2
import fitz  # PyMuPDF
from pathlib import Path


def combine_pdfs(pdf_list, output_path):
    # Create a PDF writer object to merge PDFs
    pdf_writer = PyPDF2.PdfWriter()

    # Loop through all the PDF files
    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)

        # Add all pages from this PDF to the writer object
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.compress_content_streams()
            pdf_writer.add_page(page)

    # Write the combined PDF to the output file
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Combined PDF saved to {output_path}")

    # compress_pdf(output_path, output_path.rsplit(".",1)[0] + " - LQ.pdf")

def compress_pdf(input_pdf, output_pdf, quality=20):
    """ Compress the input PDF and save it to output_pdf.
        Quality defines the level of compression (lower is more compression).
    """
    doc = fitz.open(input_pdf)  # Open the PDF file
    # Iterate through pages and compress
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)
        pix.set_dpi(quality, quality)

    doc.save(output_pdf, deflate=True)
    print(f"Compressed PDF saved to {output_pdf}")


if __name__ == "__main__":
    # Example usage
    pdf_files = [
        "G:\\My Drive\\Cloud2\\MiscFiles\\tax\\Hua2019.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\tax\\Hua2020.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\tax\\Hua2021.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\tax\\Hua2022.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\tax\\Hua2023.pdf",

        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\January 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\February 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\March 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\April 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\May 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\June 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\July 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\August 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\September 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\October 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\November 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2019\\December 2019 e-statement.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\1.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\2.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\3.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\4.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\5.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\6.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\7.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\8.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\9.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\10.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\11.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2020\\12.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2021\\2021_combined.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2022\\2022_combined.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2023\\2023_combined.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\2024\\2024_combined.pdf",
        "G:\\My Drive\\Cloud2\\MiscFiles\\bank\\Account Details _ Scotiabank - 2022-2024.pdf",
    ]  # List of PDF files to combine
    output_file = "G:\\My Drive\\Cloud2\\MiscFiles\\pr\\Han - Hua - Proof of residency - 1.pdf"  # Output file path

    combine_pdfs(pdf_files, output_file)
