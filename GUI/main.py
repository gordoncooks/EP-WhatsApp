from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame
from util.doc_path_finder import browse_and_insert

def main():
    root = CTk()
    root.title("EP WhatsApp")
    root.geometry("800x600")

    # Create a section for document paths collection
    doc_path_section = CTkFrame(root)
    doc_path_section.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="w")

    CTkLabel(doc_path_section, text="First Document:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    first_doc_entry = CTkEntry(doc_path_section, width=300)
    first_doc_entry.grid(row=0, column=1, padx=5, pady=5)
    CTkButton(doc_path_section, text="Browse", command=lambda: browse_and_insert(first_doc_entry)).grid(row=0, column=2, padx=5, pady=10)

    CTkLabel(doc_path_section, text="Second Document:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    second_doc_entry = CTkEntry(doc_path_section, width=300)
    second_doc_entry.grid(row=1, column=1, padx=5, pady=5)
    CTkButton(doc_path_section, text="Browse", command=lambda: browse_and_insert(second_doc_entry)).grid(row=1, column=2, padx=5, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
