from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame
from tkinter import filedialog, messagebox, ttk
from util.load_and_match import load_and_match_documents

def main():
    root = CTk()
    root.title("EP WhatsApp")
    root.geometry("800x700")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(2, weight=1)

    result_container = None
    tree = None

    def check_doc_entries():
        if first_doc_entry.get().strip() and second_doc_entry.get().strip():
            configure_button.configure(state="normal")
        else:
            configure_button.configure(state="disabled")

    def safe_doc_path_browse(entry_field):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            entry_field.delete(0, "end")
            entry_field.insert(0, file_path)
        check_doc_entries()

    def init_empty_table():
        nonlocal result_container, tree

        result_container = CTkFrame(root, fg_color="#2b2b2b", corner_radius=10, height=260)
        result_container.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="new")
        result_container.grid_propagate(False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=30)
        style.configure("Treeview.Heading", background="#3a3a3a", foreground="white", font=('Segoe UI', 10, 'bold'))

        tree_frame = CTkFrame(result_container, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, show="headings", height=7)
        tree["columns"] = ["Empty"]
        tree.heading("Empty", text="No Data Yet")
        tree.column("Empty", width=200, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def display_merged_data(merged_df):
        nonlocal tree

        if merged_df is None or merged_df.empty:
            messagebox.showinfo("No Matches", "No matching records found.")
            return

        tree.delete(*tree.get_children())  # Clear previous rows

        tree["columns"] = list(merged_df.columns)

        for col in merged_df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="w")

        for _, row in merged_df.iterrows():
            tree.insert("", "end", values=[row[col] for col in merged_df.columns])

    def on_configure_click():
        if first_doc_entry.get().strip() and second_doc_entry.get().strip():
            merged_df = load_and_match_documents(first_doc_entry.get(), second_doc_entry.get())
            display_merged_data(merged_df)
        else:
            messagebox.showinfo("Missing Document", "Please select both documents before continuing.")

    # === Document Entry Section ===
    doc_path_section = CTkFrame(root)
    doc_path_section.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="ew")

    CTkLabel(doc_path_section, text="First Document:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    first_doc_entry = CTkEntry(doc_path_section, width=325)
    first_doc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    first_doc_entry.bind("<KeyRelease>", lambda e: check_doc_entries())
    CTkButton(doc_path_section, text="Browse", command=lambda: safe_doc_path_browse(first_doc_entry)).grid(row=0, column=2, padx=5, pady=10)

    CTkLabel(doc_path_section, text="Second Document:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    second_doc_entry = CTkEntry(doc_path_section, width=325)
    second_doc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    second_doc_entry.bind("<KeyRelease>", lambda e: check_doc_entries())
    CTkButton(doc_path_section, text="Browse", command=lambda: safe_doc_path_browse(second_doc_entry)).grid(row=1, column=2, padx=5, pady=10)

    # === Configure Button ===
    configure_button = CTkButton(
        root,
        text="Configure\nDocuments",
        command=on_configure_click,
        state="disabled",
    )
    configure_button.grid(row=0, column=1, padx=(10, 10), pady=(30,20), sticky="nesw")

    init_empty_table()

    root.mainloop()

if __name__ == "__main__":
    main()