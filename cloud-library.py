import os

CRED_FILE = r"c:\Users\Akshaj Agarwal\pyprog002\credentials.txt"
BOOKS_FILE = r"c:\Users\Akshaj Agarwal\pyprog002\books\available_books.txt"
LOG_FOLDER, TRIES_FOLDER, MAX_TRIES = "book_logs", "user_tries", 5

os.makedirs(LOG_FOLDER, exist_ok=True)
os.makedirs(TRIES_FOLDER, exist_ok=True)

def get_books():
    try:
        with open(BOOKS_FILE) as f:
            return [l.strip() for l in f if l.strip() and l[0].isdigit()]
    except: return []

def get_tries(name):
    try:
        with open(os.path.join(TRIES_FOLDER, f"{name}_tries.txt")) as f: return int(f.read())
    except: return 0

def save_tries(name, n):
    try:
        with open(os.path.join(TRIES_FOLDER, f"{name}_tries.txt"), "w") as f: f.write(str(n))
    except: pass

def check_pwd(name, pwd):
    try:
        with open(CRED_FILE) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if f"USERNAME: {name}" in line and i+1 < len(lines) and f"PASSWORD: {pwd}" in lines[i+1]:
                return True
    except: pass
    return False

def make_account(name, pwd):
    try:
        with open(CRED_FILE) as f:
            if f"USERNAME: {name}" in f.read(): print("Already exists!"); return
    except: pass
    try:
        with open(CRED_FILE, "a") as f:
            f.write(f"\nUSERNAME: {name}\nPASSWORD: {pwd}\n" + "="*40 + "\n")
        print("Account created!"); save_tries(name, 0)
    except: print("Error creating account.")

def log_book(name, book, fully_read):
    try:
        with open(os.path.join(LOG_FOLDER, f"{name}_books.txt"), "a") as f:
            f.write(f"{book} - {'Fully' if fully_read else 'Partially'} Read\n")
        print("Book saved!")
    except: print("Could not save.")

def show_menu(name, books):
    while True:
        print("\n" + "="*40 + "\n1. See All Books\n2. Log a Book\n3. See My Books\n4. Exit\n" + "="*40)
        pick = input("Pick (1-4): ").strip()
        if pick == "1":
            for b in books: print(b)
        elif pick == "2":
            for i, b in enumerate(books, 1): print(f"{i}. {b}")
            try:
                n = int(input("Pick number: ")) - 1
                if 0 <= n < len(books):
                    log_book(name, books[n], input("Read fully? (yes/no): ").lower().strip() in ["yes","y"])
                else: print("Wrong number!")
            except: print("Enter a number!")
        elif pick == "3":
            try:
                with open(os.path.join(LOG_FOLDER, f"{name}_books.txt")) as f:
                    data = f.read(); print(data if data else "No books yet!")
            except: print("No books logged yet!")
        elif pick == "4": print("Goodbye!"); break
        else: print("Wrong choice!")

def main():
    print("="*40 + "\nONLINE LIBRARY\n" + "="*40)
    pick = input("(1) Login or (2) Create Account? ").strip()
    if pick not in ["1","2"]: print("Wrong choice!"); return
    name = input("Username: ").strip()
    pwd  = input("Password: ").strip()
    if not name or not pwd: print("Cannot be empty!"); return
    if pick == "2": make_account(name, pwd); return

    tries = get_tries(name)
    if tries >= MAX_TRIES: print("Account locked!"); return
    if check_pwd(name, pwd):
        print("Login OK!"); save_tries(name, 0)
        books = get_books()
        show_menu(name, books) if books else print("Could not load books!")
    else:
        tries += 1; save_tries(name, tries)
        print(f"Wrong password! Tries left: {MAX_TRIES - tries}")
        if tries >= MAX_TRIES: print("Account locked!")

if __name__ == "__main__": main()
