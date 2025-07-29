from tkinter import filedialog

def browse_and_insert(entry_field):
    file_path = filedialog.askopenfilename(
        title="Select a document",
        filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("Word Documents", "*.docx")]
    )
    if file_path:
        entry_field.delete(0, "end")  # Clear existing text
        entry_field.insert(0, file_path)