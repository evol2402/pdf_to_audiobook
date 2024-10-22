import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # For modern styled widgets
from gtts import gTTS
from PyPDF2 import PdfReader


# Function to extract text from the PDF
def extract_text_from_pdf(pdf_path, start_page=0, end_page=None):
    page_list = []
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    end_page = end_page or number_of_pages  # Default to the last page if not provided

    # Loop through the specified page range and extract text
    for page_number in range(start_page, end_page):
        page = reader.pages[page_number]
        page_list.append(page.extract_text())

    return page_list


# Function to convert text to speech and save as mp3
def convert_text_to_speech(text_list, output_name="output"):
    count = 1
    for text in text_list:
        if text.strip():  # Ensure text is not empty
            tts = gTTS(text)
            output_file = f"{output_name}_{count}.mp3"
            tts.save(output_file)
            print(f"Saved: {output_file}")
            count += 1


# Function to handle the file selection and conversion
def process_pdf():
    if not file_path.get():
        messagebox.showerror("Error", "No file selected!")
        return

    try:
        start_page = int(start_page_entry.get())
        end_page = int(end_page_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid page numbers!")
        return

    # Extract text from the PDF
    text_list = extract_text_from_pdf(file_path.get(), start_page, end_page)

    # Convert the extracted text to speech
    output_name = output_entry.get() or "output"
    convert_text_to_speech(text_list, output_name=output_name)

    # Show success message
    messagebox.showinfo("Success", f"MP3 files have been saved as '{output_name}_1.mp3', '{output_name}_2.mp3', etc.")


# Function to select the PDF file
def select_file():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

    if pdf_path:
        file_path.set(pdf_path)
        selected_file_label.config(text=f"Selected file: {pdf_path.split('/')[-1]}")


# Create the main GUI window
root = tk.Tk()
root.title("PDF to Speech Converter")
root.geometry("600x500")  # Set window size

# Make the UI elements more visually appealing with padding and styling
root.configure(bg="#ffffff")
style = ttk.Style(root)
style.configure("TButton", padding=6, relief="flat", background="#000000", foreground="blue", font=('Helvetica', 10))

file_path = tk.StringVar()

# File selection button and label
file_frame = ttk.Frame(root, padding=10)
file_frame.pack(pady=10)

select_file_button = ttk.Button(file_frame, text="Select PDF File", command=select_file)
select_file_button.pack(side="left", padx=10)

selected_file_label = tk.Label(file_frame, text="No file selected", bg="#f0f0f0", font=('Helvetica', 10))
selected_file_label.pack(side="left")

# Input fields for start and end pages
page_frame = ttk.Frame(root, padding=10)
page_frame.pack(pady=10)

tk.Label(page_frame, text="Start Page (0-based index):", bg="#f0f0f0", font=('Helvetica', 10)).grid(row=0, column=0,
                                                                                                    padx=10, pady=5,
                                                                                                    sticky='w')
start_page_entry = ttk.Entry(page_frame, width=10)
start_page_entry.grid(row=0, column=1, padx=10)

tk.Label(page_frame, text="End Page (exclusive):", bg="#f0f0f0", font=('Helvetica', 10)).grid(row=1, column=0, padx=10,
                                                                                              pady=5, sticky='w')
end_page_entry = ttk.Entry(page_frame, width=10)
end_page_entry.grid(row=1, column=1, padx=10)

# Input field for output file name
output_frame = ttk.Frame(root, padding=10)
output_frame.pack(pady=10)

tk.Label(output_frame, text="Output MP3 File Name (optional):", bg="#f0f0f0", font=('Helvetica', 10)).grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky='w')
output_entry = ttk.Entry(output_frame, width=20)
output_entry.grid(row=0, column=1, padx=10)

# Convert button
convert_button = ttk.Button(root, text="Convert to Speech", command=process_pdf)
convert_button.pack(pady=20)

# Run the application
root.mainloop()
