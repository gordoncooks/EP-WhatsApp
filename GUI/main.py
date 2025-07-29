from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame
from tkinter import messagebox
from util.doc_path_finder import browse_and_insert  # You must ensure this calls .set() or triggers validation

def main():
    root = CTk()
    root.title("EP WhatsApp")
    root.geometry("800x600")

    # Function to check if both document entries are filled
    def check_doc_entries():
        if first_doc_entry.get().strip() and second_doc_entry.get().strip():
            configure_button.configure(state="normal")
        else:
            configure_button.configure(state="disabled")

    # Function to safely browse and insert document paths this also checks entries
    # to ensure the button state is updated accordingly
    def safe_doc_path_browse(entry_field):
        browse_and_insert(entry_field)
        check_doc_entries()

    # Function to handle the configure button click
    def on_configure_click():
        if first_doc_entry.get().strip() and second_doc_entry.get().strip():
            print("Configure Documents Clicked")
        else:
            messagebox.showinfo("Missing Document", "Please select both documents before continuing.")

    # === Document Entry Section ===
    doc_path_section = CTkFrame(root)
    doc_path_section.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="w")

    CTkLabel(doc_path_section, text="First Document:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    first_doc_entry = CTkEntry(doc_path_section, width=300)
    first_doc_entry.grid(row=0, column=1, padx=5, pady=5)
    first_doc_entry.bind("<KeyRelease>", lambda e: check_doc_entries())
    CTkButton(doc_path_section, text="Browse", command=lambda: safe_doc_path_browse(first_doc_entry)).grid(row=0, column=2, padx=5, pady=10)

    CTkLabel(doc_path_section, text="Second Document:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    second_doc_entry = CTkEntry(doc_path_section, width=300)
    second_doc_entry.grid(row=1, column=1, padx=5, pady=5)
    second_doc_entry.bind("<KeyRelease>", lambda e: check_doc_entries())
    CTkButton(doc_path_section, text="Browse", command=lambda: safe_doc_path_browse(second_doc_entry)).grid(row=1, column=2, padx=5, pady=10)

    # === Configure Button ===
    configure_button = CTkButton(
        root,
        text="Configure\nDocuments",
        command=on_configure_click,
        state="disabled"
    )
    configure_button.grid(row=0, column=1, padx=(10, 10), pady=20, sticky="nesw")

    root.mainloop()

if __name__ == "__main__":
    main()