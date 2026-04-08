# Digital Library Suggestion System
catalog = {}
borrowed = {}
history = {}

def add_book():
    subject = input("Enter subject: ").capitalize()
    book = input("Enter book title: ")
    catalog.setdefault(subject, []).append(book)
    print(f"'{book}' added under '{subject}'.")

def view_books():
    if not catalog:
        print("No books available.")
        return
    for subject, books in catalog.items():
        print(f"\n{subject}:")
        for b in books:
            print(f" - {b}")

def borrow_book():
    student = input("Enter student name: ").capitalize()
    if not catalog:
        print("No books available to borrow.")
        return
    print("\nAvailable subjects:")
    view_books()
    subject = input("Enter subject: ").capitalize()
    if subject not in catalog or not catalog[subject]:
        print("Invalid or empty subject.")
        return
    print(f"\nBooks in {subject}:")
    for b in catalog[subject]:
        print(f" - {b}")
    book = input("Enter book name: ")
    if book not in catalog[subject]:
        print("Book not found.")
        return
    catalog[subject].remove(book)
    borrowed.setdefault(student, []).append(book)
    history.setdefault(student, []).append(subject)
    print(f"{student} borrowed '{book}' from {subject} section.")

def view_borrowed():
    if not borrowed:
        print("No borrowed books.")
        return
    print("\nBorrowed Books:")
    for student, books in borrowed.items():
        print(f"{student}:")
        for b in books:
            print(f" - {b}")

def recommend_books():
    student = input("Enter student name: ").capitalize()
    if student not in history or not history[student]:
        print("No borrowing history for this student.")
        return
    subjects = history[student]
    fav_subject = max(set(subjects), key=subjects.count)
    if fav_subject not in catalog or not catalog[fav_subject]:
        print(f"No available books in {fav_subject} currently{student}.")
        return
    print(f"\nRecommended books for {student} (based on '{fav_subject}'):")
    for book in catalog[fav_subject]:
        print(f" - {book}")

while True:
    print("-----------------------------------------")
    print("\n1. Add Book")
    print("2. View Books")
    print("3. Borrow Book")
    print("4. History ")
    print("5. Recommend Books")
    print("6. Exit")
    print("-----------------------------------------")
    choice = input("Enter your choice: ")
    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        borrow_book()
    elif choice == "4":
        view_borrowed()
    elif choice == "5":
        recommend_books()
    elif choice == "6":
        print("Exiting program.")
        break
    else:
        print("Invalid choice.")
