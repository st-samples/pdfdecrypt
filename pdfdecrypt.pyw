import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

def decrypt_and_convert_pdf(files, output_text):
    for file in files:
        directory = os.path.dirname(file)  # Get the directory of the input file
        decrypted_file = os.path.join(directory, "decrypted temp file.pdf")
        converted_file = os.path.splitext(file)[0] + " DECRYPTED.pdf"

        # Construct the command to decrypt the PDF using qpdf
        qpdf_command = ['qpdf', '--decrypt', file, decrypted_file]

        try:
            # Execute the qpdf command without showing the command prompt window
            subprocess.run(qpdf_command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            output_text.insert(tk.END, "PDF decryption successful!\n")

            # Construct the command to convert the decrypted PDF using pdftocairo
            pdftocairo_command = ['pdftocairo', '-pdf', decrypted_file, converted_file]

            # Execute the pdftocairo command without showing the command prompt window
            subprocess.run(pdftocairo_command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

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
