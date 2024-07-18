# PDFSpitter-
This program is a Python GUI application designed to split PDF documents. It uses the Kivy framework to create a user-friendly interface and the 

PyPDF2 library to handle the PDF manipulation.  Here's a breakdown of the functionalities: 

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

 ![Screenshot (924)](https://github.com/user-attachments/assets/4268ed8d-b506-4fb1-9937-7f6d2571e80f)
![Screenshot (923)](https://github.com/user-attachments/assets/b03bff85-9081-4cbf-8a4b-7defd69fac7e)
![Screenshot (922)](https://github.com/user-attachments/assets/f6c4ac77-7c57-4a73-b186-0de61ad40e03)


Select File: This button allows you to browse and select a PDF file you want to split.

Select Directory: This button lets you choose a directory (folder) where the program will save the split PDFs.

The slider in this program allows you to define the number of pages you want to include in each split PDF file. By dragging the slider or entering a value, you set the "pages per part" for the splitting process.

Split PDF: This is the main action button. Clicking this button initiates the process of splitting the PDF based on the options you've chosen.


