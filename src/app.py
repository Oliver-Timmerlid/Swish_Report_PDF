from tkinter import Tk, filedialog, messagebox
import customtkinter as ctk
from utils.drag_and_drop import DragAndDrop
from utils.csv_to_pdf import convert_csv_to_pdf
from tkinterdnd2 import TkinterDnD

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV to PDF Converter")
        self.root.geometry("400x300")

        self.drag_and_drop = DragAndDrop(self.root, self.on_file_drop)

        self.label = ctk.CTkLabel(self.root, text="Drag and drop a CSV file here")
        self.label.pack(pady=20)

        self.convert_button = ctk.CTkButton(self.root, text="Convert to PDF", command=self.convert_to_pdf)
        self.convert_button.pack(pady=10)

        self.csv_file_path = None

    def on_file_drop(self, file_path):
        self.csv_file_path = file_path
        self.label.configure(text=f"Selected file: {file_path}")

    def convert_to_pdf(self):
        if not self.csv_file_path:
            messagebox.showerror("Error", "Please drop a CSV file first.")
            return

        pdf_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_file_path:
            try:
                convert_csv_to_pdf(self.csv_file_path, pdf_file_path)
                messagebox.showinfo("Success", "PDF file created successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert CSV to PDF: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = TkinterDnD.Tk()  # Use TkinterDnD.Tk for drag-and-drop support
    app = App(root)
    root.mainloop()