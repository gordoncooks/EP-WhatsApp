from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkTextbox
from tkinter import filedialog, messagebox, ttk
from util.load_and_match import load_and_match_documents

def main():
    root = CTk()
    root.title("EP WhatsApp")
    root.geometry("800x495")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(3, weight=1)

    result_container = None
    tree = None
    merged_df = None  # store reference for test message

    def check_doc_entries():
        if first_doc_entry.get().strip() and second_doc_entry.get().strip():
            configure_button.configure(state="normal")
        else:
            configure_button.configure(state="disabled")

    def safe_doc_path_browse(entry_field):
        file_path = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            entry_field.delete(0, "end")
            entry_field.insert(0, file_path)
        check_doc_entries()

    def init_empty_table():
        nonlocal result_container, tree

        result_container = CTkFrame(root, fg_color="#2b2b2b", corner_radius=10, height=260)
        result_container.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(5, 20), sticky="new")
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

    def display_merged_data(dataframe):
        nonlocal tree

        if dataframe is None or dataframe.empty:
            messagebox.showinfo("No Matches", "No matching records found.")
            return

        tree.delete(*tree.get_children())
        tree["columns"] = list(dataframe.columns)

        for col in dataframe.columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="w")

        for _, row in dataframe.iterrows():
            tree.insert("", "end", values=[row[col] for col in dataframe.columns])

    def on_configure_click():
        nonlocal merged_df
        if first_doc_entry.get().strip() and second_doc_entry.get().strip():
            merged_df = load_and_match_documents(first_doc_entry.get(), second_doc_entry.get())
            display_merged_data(merged_df)
            if merged_df is not None and not merged_df.empty:
                test_message_button.configure(state="normal")
                send_button.configure(state="normal")

        else:
            messagebox.showinfo("Missing Document", "Please select both documents before continuing.")

    def insert_tag(tag):
        message_input.insert("insert", tag)

    def populate_test_message(df):
        if df is not None and not df.empty:
            row = df.iloc[0]

            # Get the message template from the textbox
            template = message_input.get("1.0", "end").strip()

            print(df.columns.tolist())

            # Replace placeholders with actual row data (use actual column names)
            replacements = {
                "{name}": str(row.get("Owner Name", "[name]")),
                "{address}": str(row.get("Street Address_x", "[address]")),
                "R" + "{price}": str(row.get("Price", "[price]")),
                "{views}": str(row.get("All Views", "[views]")),
                "{market_days}": str(row.get("List Date", "[market_days]")),
                "{enquiries}": "0",  # if you don’t have a field yet
                "{hyperlink}": str(row.get("Extracted Hyperlink", "[hyperlink]")),
            }

            # Perform the replacements
            for tag, value in replacements.items():
                template = template.replace(tag, value)

            # Show the filled message
            messagebox.showinfo("Test Message Preview", template)

    # === Document Entry Section ===
    doc_path_section = CTkFrame(root)
    doc_path_section.grid(row=0, column=0, padx=(20, 0), pady=(20, 5), sticky="ew")

    CTkLabel(doc_path_section, text="First Document:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    first_doc_entry = CTkEntry(doc_path_section, width=320)
    first_doc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    first_doc_entry.bind("<KeyRelease>", lambda e: check_doc_entries())
    CTkButton(doc_path_section, text="Browse", command=lambda: safe_doc_path_browse(first_doc_entry)).grid(row=0, column=2, padx=5, pady=10)

    CTkLabel(doc_path_section, text="Second Document:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    second_doc_entry = CTkEntry(doc_path_section, width=320)
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
    configure_button.grid(row=0, column=1, padx=(10, 20), pady=(30, 20), sticky="nesw")

    # === Tag Buttons Section ===
    messagSection = CTkFrame(root, fg_color="#2b2b2b", corner_radius=10, height=50)
    messagSection.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(5, 5), sticky="ew")
    messagSection.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

    CTkButton(messagSection, text="Name", command=lambda: insert_tag("{name}")).grid(row=0, column=0, padx=(4, 2), pady=5, sticky="ew")
    CTkButton(messagSection, text="Address", command=lambda: insert_tag("{address}")).grid(row=0, column=1, padx=2, pady=5, sticky="ew")
    CTkButton(messagSection, text="Views", command=lambda: insert_tag("{views}")).grid(row=0, column=2, padx=2, pady=5, sticky="ew")
    CTkButton(messagSection, text="Price", command=lambda: insert_tag("{price}")).grid(row=0, column=3, padx=2, pady=5, sticky="ew")
    CTkButton(messagSection, text="Market Days", command=lambda: insert_tag("{market_days}")).grid(row=0, column=4, padx=2, pady=5, sticky="ew")
    CTkButton(messagSection, text="Enquiries", command=lambda: insert_tag("{enquiries}")).grid(row=0, column=5, padx=2, pady=5, sticky="ew")
    CTkButton(messagSection, text="Hyperlink", command=lambda: insert_tag("{hyperlink}")).grid(row=0, column=6, padx=(2, 4), pady=5, sticky="ew")

    # === Message Input ===
    message_input = CTkTextbox(root, width=800, height=100, fg_color="#1e1e1e", text_color="white", wrap="word")
    message_input.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(5, 5), sticky="ew")

    default_message = (
        "Hello {name}, your property at {address} has received {views} views and {enquiries} enquiries. "
        "The current market value is estimated at {price}. It has been listed for {market_days} days.\n\n"
        "For more details, visit: {hyperlink}"
    )
    message_input.insert("1.0", default_message)

    # === Test Message Button ===
    test_message_button = CTkButton(
        root,
        text="Test Message",
        state="disabled",
        command=lambda: populate_test_message(merged_df)
    )
    test_message_button.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(0, 5), sticky="ew")

    # === Start Sending Button ===
    def on_send_click():
        print("Sending...")

    send_button = CTkButton(
        root,
        text="Start Sending",
        state="disabled",
        command=on_send_click
    )
    send_button.grid(row=5, column=0, columnspan=2, padx=(20, 20), pady=(0, 10), sticky="ew")

    init_empty_table()
    root.mainloop()

if __name__ == "__main__":
    main()
