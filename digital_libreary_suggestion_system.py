import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# ---------------------------
# File paths
# ---------------------------
CATALOG_FILE = "catalog.json"
BORROWED_FILE = "borrowed.json"

# ---------------------------
# Helper functions
# ---------------------------
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Initialize data
catalog = load_data(CATALOG_FILE)
borrowed = load_data(BORROWED_FILE)

# ---------------------------
# GUI App
# ---------------------------
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Digital Library Suggestion System")
        self.root.geometry("700x500")
        self.root.configure(bg="#1d9d50")

        # Buttons
        tk.Button(root, background="#DC9517",text="📘 View Available Books", width=25, command=self.view_books).pack(pady=5)
        tk.Button(root, background="#DC9517",text="➕ Add New Book", width=25, command=self.add_book).pack(pady=5)
        tk.Button(root, background="#DC9517",text="📖 Borrow Book", width=25, command=self.borrow_book).pack(pady=5)
        tk.Button(root, background="#DC9517",text="🔙 Return Book", width=25, command=self.return_book).pack(pady=5)
        tk.Button(root, background="#DC9517",text="💡 Recommend Books", width=25, command=self.recommend_books).pack(pady=5)

        # Output area
        self.output = tk.Text(root,background="#1DA5DB", width=80, height=20, wrap="word")
        self.output.pack(pady=10)

    # ---------------------------
    # Functions
    # ---------------------------
    def view_books(self):
        """Show all available books subject-wise."""
        self.output.delete(1.0, tk.END)
        if not catalog:
            self.output.insert(tk.END, "No books available in the catalog.\n")
            return

        for subject, books in catalog.items():
            self.output.insert(tk.END, f"\n📚 {subject}:\n")
            for b in books:
                self.output.insert(tk.END, f"   - {b}\n")

    def add_book(self):
        """Add a new book to the catalog."""
        subject = simpledialog.askstring("Subject", "Enter subject name:")
        if not subject:
            return
        subject = subject.capitalize()

        book = simpledialog.askstring("Book Title", "Enter book title:")
        if not book:
            return

        catalog.setdefault(subject, [])
        if book in catalog[subject]:
            messagebox.showwarning("Warning", "Book already exists in catalog.")
            return

        catalog[subject].append(book)
        save_data(CATALOG_FILE, catalog)
        messagebox.showinfo("Success", f"'{book}' added under '{subject}'.")

    def borrow_book(self):
        """Remove book from catalog and record who borrowed it."""
        subject = simpledialog.askstring("Subject", "Enter subject of the book:")
        if not subject:
            return
        subject = subject.capitalize()

        if subject not in catalog or not catalog[subject]:
            messagebox.showerror("Unavailable", f"No books available under '{subject}'.")
            return

        book = simpledialog.askstring("Book Title", f"Enter book title from {subject}:")
        if not book or book not in catalog[subject]:
            messagebox.showerror("Not Found", f"'{book}' not found in '{subject}' category.")
            return

        borrower = simpledialog.askstring("Borrower Name", "Enter student's name:")
        if not borrower:
            return

        catalog[subject].remove(book)
        borrowed.setdefault(subject, []).append({"title": book, "borrower": borrower})

        save_data(CATALOG_FILE, catalog)
        save_data(BORROWED_FILE, borrowed)

        messagebox.showinfo("Borrowed", f"'{book}' borrowed by {borrower}.")

    def return_book(self):
        """Return borrowed book and re-add to catalog."""
        subject = simpledialog.askstring("Subject", "Enter subject of the book:")
        if not subject:
            return
        subject = subject.capitalize()

        if subject not in borrowed or not borrowed[subject]:
            messagebox.showinfo("Info", f"No borrowed books under '{subject}'.")
            return

        book = simpledialog.askstring("Book Title", "Enter title of the returning book:")
        if not book:
            return

        for entry in borrowed[subject]:
            if entry["title"] == book:
                borrowed[subject].remove(entry)
                catalog.setdefault(subject, []).append(book)
                save_data(CATALOG_FILE, catalog)
                save_data(BORROWED_FILE, borrowed)
                messagebox.showinfo("Returned", f"'{book}' returned successfully.")
                return

        messagebox.showerror("Error", f"No record found for '{book}' under '{subject}'.")

    def recommend_books(self):
        """Recommend books for a given subject."""
        subject = simpledialog.askstring("Subject", "Enter subject for recommendation:")
        if not subject:
            return
        subject = subject.capitalize()

        self.output.delete(1.0, tk.END)
        if subject not in catalog or not catalog[subject]:
            self.output.insert(tk.END, f"⚠️ No books available under '{subject}'.\n")
        else:
            self.output.insert(tk.END, f"📚 Recommended books for '{subject}':\n")
            for book in catalog[subject]:
                self.output.insert(tk.END, f"   - {book}\n")

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
