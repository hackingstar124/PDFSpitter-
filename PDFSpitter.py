
import logging
import os
from threading import Thread
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from PyPDF2 import PdfReader, PdfWriter
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()],
)

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: [20, 10]  # Adjust padding as needed
    spacing: 10

    MDBoxLayout:
        orientation: 'horizontal'
        padding: [10, 0]  # Adjust padding as needed for the MDBoxLayout
        spacing: 10

        MDLabel:
            text: ""
            halign: "center"
            valign: "center"

        MDSwitch:
            id: theme_switch
            size_hint: None, None
            size: "48dp", "48dp"
            pos_hint: {'center_y': 0.5}
            on_active: app.toggle_night_mode(*args)

    MDLabel:
        text: "Input PDF File:"
        halign: "center"

    MDBoxLayout:
        orientation: 'horizontal'
        MDTextField:
            id: input_file_input
            hint_text: "Select input PDF file"
            readonly: True
            multiline: False
            mode: "rectangle"

        MDRaisedButton:
            text: "Select File"
            on_press: app.select_file()
            pos_hint: {'center_y': 0.5}

    BoxLayout:
        size_hint_y: None
        height: dp(30)  # Reduce height
        padding: [10, 0]  # Adjust padding as needed
        BoxLayout:
            size_hint_x: None
            width: dp(150)  # Adjust width as needed
            MDLabel:
                id: page_count_label
                text: ""
                halign: "center"
                valign: "center"
                theme_text_color: "Custom"
                text_color: [0, 0.6, 1, 1]  # Sky blue color for text

    MDLabel:
        text: "Output Directory:"
        halign: "center"

    MDBoxLayout:
        orientation: 'horizontal'
        MDTextField:
            id: output_dir_input
            hint_text: "Select output directory"
            readonly: True
            multiline: False
            mode: "rectangle"

        MDRaisedButton:
            text: "Select Directory"
            on_press: app.select_output_dir()
            pos_hint: {'center_y': 0.5}

    MDLabel:
        text: "Select Page Range:"
        halign: "center"

    MDBoxLayout:
        orientation: 'horizontal'
        MDTextField:
            id: start_page_input
            hint_text: "Start Page"
            input_filter: 'int'
            multiline: False
            mode: "rectangle"

        MDLabel:
            text: "-"
            halign: "center"

        MDTextField:
            id: end_page_input
            hint_text: "End Page"
            input_filter: 'int'
            multiline: False
            mode: "rectangle"

    MDLabel:
        text: "Or"
        halign: "center"

    MDLabel:
        text: "Select Pages per Part:"
        halign: "center"

    MDBoxLayout:
        orientation: 'horizontal'
        MDLabel:
            id: pages_label
            text: "20 Pages"
            halign: "center"

        MDSlider:
            id: pages_slider
            min: 1
            max: 100
            value: 20
            on_value: app.on_pages_slider_change(*args)

    MDLabel:
        text: "Select Single Page to Split:"
        halign: "center"

    MDTextField:
        id: page_input
        hint_text: "Page Number"
        input_filter: 'int'
        multiline: False
        mode: "rectangle"

    MDRaisedButton:
        text: "Split PDF"
        on_press: app.start_split()
        pos_hint: {'center_x': 0.5}
'''

class PDFSplitterApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_pdf_path = ""
        self.output_dir = ""
        self.start_page = None
        self.end_page = None
        self.pages_per_split = 20
        self.page_to_split = None
        self.spinner_popup = None
        self.dialog = None

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Set background to white
        Window.size = (720, 720)
        self.theme_cls.theme_style = "Light"  # Choose between 'Light' and 'Dark'
        self.theme_cls.primary_palette = "Blue"  # Choose primary color

        return Builder.load_string(KV)

    def select_file(self):
        Tk().withdraw()  # Prevents root window from appearing
        file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.input_pdf_path = file_path
            self.root.ids.input_file_input.text = self.input_pdf_path
            logging.info(f"Selected input file: {self.input_pdf_path}")

            # Update page count label
            try:
                input_pdf = PdfReader(self.input_pdf_path)
                total_pages = len(input_pdf.pages)
                self.root.ids.page_count_label.text = f"Total Pages: {total_pages}"
                logging.info(f"Total pages in input PDF: {total_pages}")
            except Exception as e:
                logging.error(f"Error counting pages: {e}")
                self.root.ids.page_count_label.text = "Error counting pages"

    def select_output_dir(self):
        Tk().withdraw()  # Prevents root window from appearing
        directory = askdirectory()
        if directory:
            self.output_dir = directory
            self.root.ids.output_dir_input.text = self.output_dir
            logging.info(f"Selected output directory: {self.output_dir}")

    def on_pages_slider_change(self, instance, value):
        self.pages_per_split = int(value)
        self.root.ids.pages_label.text = f"{self.pages_per_split} Pages"
        logging.info(f"Pages per split set to: {self.pages_per_split}")

    def start_split(self):
        if not self.input_pdf_path:
            self.show_dialog("Error", "Please select an input PDF file.")
            return
        if not os.path.isfile(self.input_pdf_path):
            self.show_dialog("Error", "Invalid input PDF file path.")
            return
        if not self.output_dir:
            self.show_dialog("Error", "Please select an output directory.")
            return

        self.start_page = self.end_page = None
        self.page_to_split = None

        try:
            self.start_page = int(self.root.ids.start_page_input.text)
            self.end_page = int(self.root.ids.end_page_input.text)
            if self.start_page < 1 or self.start_page > self.end_page:
                raise ValueError
        except ValueError:
            self.start_page = self.end_page = None

        try:
            self.page_to_split = int(self.root.ids.page_input.text)
            if self.page_to_split < 1:
                raise ValueError
        except ValueError:
            self.page_to_split = None

        if not (self.start_page and self.end_page) and not self.page_to_split and not self.pages_per_split:
            self.show_dialog("Error",
                             "Please enter a valid page range, a single page number, or specify pages per part.")
            return

        self.show_spinner()
        Thread(target=self.split_pdf).start()

    def show_spinner(self):
        self.spinner_popup = MDDialog(
            title="Processing",
            type="custom",
            content_cls=MDSpinner(size_hint=(None, None), size=(50, 50)),
        )
        self.spinner_popup.open()
        logging.info("Spinner popup shown")

    @mainthread
    def dismiss_spinner(self):
        if self.spinner_popup:
            self.spinner_popup.dismiss()
            logging.info("Spinner popup dismissed")


    def split_pdf(self):
        try:
            input_pdf = PdfReader(self.input_pdf_path)
            total_pages = len(input_pdf.pages)
            logging.info(f"Total pages in input PDF: {total_pages}")

            if self.start_page and self.end_page:
                self.start_page = max(1, min(self.start_page, total_pages))
                self.end_page = max(self.start_page, min(self.end_page, total_pages))
                logging.info(f"Page range set to: {self.start_page} - {self.end_page}")

                output_pdf = PdfWriter()
                for page_num in range(self.start_page - 1, self.end_page):  # Adjust for 0-based indexing
                    output_pdf.add_page(input_pdf.pages[page_num])

                output_filename = os.path.join(self.output_dir, "output_part.pdf")
                with open(output_filename, "wb") as output_file:
                    output_pdf.write(output_file)

                logging.info(f"PDF split by page range saved to: {output_filename}")

            if self.page_to_split:
                self.page_to_split = max(1, min(self.page_to_split, total_pages))
                logging.info(f"Splitting PDF at single page: {self.page_to_split}")

                output_pdf = PdfWriter()
                output_pdf.add_page(input_pdf.pages[self.page_to_split - 1])  # Adjust for 0-based indexing

                output_filename = os.path.join(self.output_dir, f"output_page_{self.page_to_split}.pdf")
                with open(output_filename, "wb") as output_file:
                    output_pdf.write(output_file)

                logging.info(f"PDF split at single page saved to: {output_filename}")

            if self.pages_per_split:
                logging.info(f"Splitting PDF into parts of {self.pages_per_split} pages each")
                part_num = 1
                for i in range(0, total_pages, self.pages_per_split):
                    output_pdf = PdfWriter()
                    for page_num in range(i, min(i + self.pages_per_split, total_pages)):
                        output_pdf.add_page(input_pdf.pages[page_num])

                    output_filename = os.path.join(self.output_dir, f"output_part_{part_num}.pdf")
                    with open(output_filename, "wb") as output_file:
                        output_pdf.write(output_file)

                    logging.info(f"PDF part {part_num} saved to: {output_filename}")
                    part_num += 1

            # Schedule the success dialog to be shown on the main thread
            Clock.schedule_once(lambda dt: self.show_dialog("Success", "PDF has been successfully split."))

        except Exception as e:
            logging.error(f"Error during PDF splitting: {e}")
            # Schedule the error dialog to be shown on the main thread
            Clock.schedule_once(lambda dt: self.show_dialog("Error", f"An error occurred while splitting the PDF: {e}"))
        finally:
            # Schedule the spinner to be dismissed on the main thread
            Clock.schedule_once(lambda dt: self.dismiss_spinner())

    def show_dialog(self, title, text):
        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        self.dialog = MDDialog(title=title, text=text, buttons=[close_button])
        self.dialog.open()
        logging.info(f"Dialog shown: {title} - {text}")

    def close_dialog(self, obj):
        if self.dialog:
            self.dialog.dismiss()
            logging.info("Dialog dismissed")

    def toggle_night_mode(self, switch, active):
        if active:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"
            Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"
            Window.clearcolor = (1, 1, 1, 1)  # Light background

        logging.info(f"Night mode toggled to {'on' if active else 'off'}")

    def update_button_colors(self, bg_color, text_color):
        for button in self.root.walk(restrict=True):
            if isinstance(button, MDRaisedButton):
                button.md_bg_color = bg_color
                button.text_color = text_color

    def update_label_colors(self, text_color):
        for label in self.root.walk(restrict=True):
            if isinstance(label, MDLabel) and not label.text == "Night Mode":
                label.text_color = text_color
if __name__ == "__main__":
    PDFSplitterApp().run()
