import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

# Determine the base directory where the script is running
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # If running as a PyInstaller exe
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # If running as a script

# Set paths for QPDF and Poppler
QPDF_PATH = os.path.join(BASE_DIR, "qpdf-10.6.3", "bin", "qpdf.exe")
PDFTOCAIRO_PATH = os.path.join(BASE_DIR, "poppler-0.68.0", "bin", "pdftocairo.exe")

def decrypt_and_convert_pdf(files, output_text):
    for file in files:
        directory = os.path.dirname(file)  # Get the directory of the input file
        decrypted_file = os.path.join(directory, "decrypted_temp_file.pdf")
        converted_file = os.path.splitext(file)[0] + " DECRYPTED.pdf"

        # Construct the command to decrypt the PDF using qpdf
        qpdf_command = [QPDF_PATH, '--decrypt', file, decrypted_file]

        try:
            # Execute the qpdf command
            subprocess.run(qpdf_command, check=True)

            output_text.insert(tk.END, "PDF decryption successful!\n")

            # Construct the command to convert the decrypted PDF using pdftocairo
            pdftocairo_command = [PDFTOCAIRO_PATH, '-pdf', decrypted_file, converted_file]

            # Execute the pdftocairo command
            subprocess.run(pdftocairo_command, check=True)

            output_text.insert(tk.END, "PDF conversion successful!\n")

            # Delete the decrypted file after conversion
            os.remove(decrypted_file)
            output_text.insert(tk.END, "Temporary file deleted!\n")
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f"PDF decryption or conversion failed for file: {file}. Error: {e}\n")

    output_text.insert(tk.END, "Finished!")

def confirm_files(output_text):
    files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
    if files:
        confirmation = messagebox.askquestion("Confirmation", f"Are you sure you want to decrypt the following files?\n\n{', '.join(files)}")
        if confirmation == "yes":
            decrypt_and_convert_pdf(files, output_text)

def select_folder(output_text):
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".pdf")]
        confirmation = messagebox.askquestion("Confirmation", f"Are you sure you want to decrypt all the PDF files in the following folder?\n\n{folder}")
        if confirmation == "yes":
            decrypt_and_convert_pdf(files, output_text)

window = tk.Tk()
window.title("PDF Decryption Program")
window.geometry("400x300")  # Set window size to 400x300

title_label = tk.Label(window, text="Please select which PDFs need their security/encryption removed")
title_label.pack(pady=10)

select_frame = tk.Frame(window)
select_frame.pack()

select_files_button = tk.Button(select_frame, text="Select Files", command=lambda: confirm_files(output_text))
select_files_button.pack(side=tk.LEFT)

select_folder_button = tk.Button(select_frame, text="Select Folder", command=lambda: select_folder(output_text))
select_folder_button.pack(side=tk.LEFT, padx=10)

output_text = tk.Text(window, height=10, width=40)
output_text.pack(padx=10, pady=10)  # Add padding of 10 pixels on all sides

window.mainloop()
