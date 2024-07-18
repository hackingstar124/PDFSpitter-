# PDFSpitter-
This program is a Python GUI application designed to split PDF documents. It uses the Kivy framework to create a user-friendly interface and the PyPDF2 library to handle the PDF manipulation.  Here's a breakdown of the functionalities: 
The program uses the PyPDF2 library to read and write PDF files.
Based on user input, it can split the PDF in three ways:
By page range: Extracts a specific range of pages from the original PDF.
By single page: Creates a new PDF containing only the specified page.
By page parts: Splits the PDF into multiple PDFs, each containing a user-defined number of pages.
Before run this install those 
pip install kivy 
pip instaal tkinter
pip install kivymd 
pip install PyPDF2

![Screenshot (923)](https://github.com/user-attachments/assets/9d8cc9bf-648e-4fbe-93af-520cbc46d69d)
![Screenshot (922)](https://github.com/user-attachments/assets/c7572127-19e0-4491-afde-5fa31417afea)
![Screenshot (924)](https://github.com/user-attachments/assets/d50b27b3-e163-4661-ae61-909f0952a21f)

Select File: This button allows you to browse and select a PDF file you want to split.

Select Directory: This button lets you choose a directory (folder) where the program will save the split PDFs.

The slider in this program allows you to define the number of pages you want to include in each split PDF file. By dragging the slider or entering a value, you set the "pages per part" for the splitting process.

Split PDF: This is the main action button. Clicking this button initiates the process of splitting the PDF based on the options you've chosen.


