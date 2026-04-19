class Book:
    def __init__(self, book_id, title):
        self.book_id = book_id
        self.title = title
        self.is_borrowed = False
    def show_book_info(self):
        borrow_status = "已借出" if self.is_borrowed else "未借出"
        print(f"图书编号：{self.book_id}")
        print(f"书名：《{self.title}》")
        print(f"借阅状态：{borrow_status}\n")
class Reader:
    def __init__(self, reader_id, name):
        self.reader_id = reader_id
        self.name = name
        self.borrowed_books = []
    def borrow_book(self, book):
        if not book.is_borrowed:
            self.borrowed_books.append(book)
            book.is_borrowed = True
            print(f"{self.name}成功借阅《{book.title}》")
        else:
            print(f"《{book.title}》已被借出，{self.name}借阅失败")
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.is_borrowed = False
            print(f"{self.name}成功归还《{book.title}》")
        else:
            print(f"{self.name}未借阅《{book.title}》，归还失败")
    def show_borrowed_books(self):
        print(f"\n{self.name}（读者编号：{self.reader_id}）的已借图书：")
        if not self.borrowed_books:
            print("暂无已借图书")
            return
        for idx, book in enumerate(self.borrowed_books, 1):
            print(f"{idx}. 图书编号：{book.book_id}，书名：《{book.title}》")
if __name__ == "__main__":
    book1 = Book("B001", "Python编程：从入门到实践")
    book2 = Book("B002", "人类简史", )
    book3 = Book("B003", "解忧杂货店")
    reader1 = Reader("R001", "张三")
    reader2 = Reader("R002", "李四")
    reader1.borrow_book(book1)
    reader1.borrow_book(book2)
    reader2.borrow_book(book2)
    reader2.borrow_book(book3)
    reader1.show_borrowed_books()
    reader2.show_borrowed_books()
    reader1.return_book(book1)
    print("\n归还后：")
    reader1.show_borrowed_books()
    print("book1当前信息：")
    book1.show_book_info()


    class Reader:
        def __init__(self, reader_id, name):
            self.reader_id = reader_id
            self.name = name
            self.borrowed_books = []
        def borrow_book(self, book):
            if not book.is_borrowed:
                self.borrowed_books.append(book)
                book.is_borrowed = True
                print(f"{self.name}成功借阅《{book.title}》")
            else:
                print(f"《{book.title}》已被借出，借阅失败")
        def return_book(self, book):
            if book in self.borrowed_books:
                self.borrowed_books.remove(book)
                book.is_borrowed = False
                print(f"{self.name}成功归还《{book.title}》")
            else:
                print(f"{self.name}未借阅《{book.title}》，归还失败")
        def show_borrowed_books(self):
            if self.borrowed_books:
                print(f"{self.name}的已借图书：")
                for book in self.borrowed_books:
                    book.show_book_info()
            else:
                print(f"{self.name}暂无已借图书")
        def information(self):
            return f"读者编号：{self.reader_id}，姓名：{self.name}"
    class Librarian(Reader):
        def __init__(self, reader_id, name, manage_id, department):
            super().__init__(reader_id, name)
            self.manage_id = manage_id
            self.department = department
        def information(self):
            print(f"管理员编号：{self.manage_id}，姓名：{self.name}，所属部门：{self.department}")
        def add_book(self, library, book):
            library.append(book)
            print(f"成功向图书馆添加图书《{book.title}》")
        def show_all_books(self, library):
            print("图书馆所有图书：")
            for book in library:
                book.show_book_info()
    class VIPReader(Reader):
        def __init__(self, reader_id, name):
            super().__init__(reader_id, name)
            self.points = 0
        def borrow_book(self, book):
            super().borrow_book(book)
            if book in self.borrowed_books:
                self.points += 10
                print(f"借阅成功，当前积分：{self.points}")
        def information(self):
            print(f"读者编号：{self.reader_id}，姓名：{self.name}，积分：{self.points}")
        def show_points(self):
            print(f"{self.name}当前积分：{self.points}")
    class Book:
        def __init__(self, book_id, title):
            self.book_id = book_id
            self.title = title
            self.is_borrowed = False
        def show_book_info(self):
            status = "已借出" if self.is_borrowed else "未借出"
            print(f"图书编号：{self.book_id}，书名：{self.title}，状态：{status}")
    if __name__ == "__main__":

        print("=== 管理员操作 ===")
        librarian = Librarian("R001", "王管理员", "M001", "图书管理部")
        librarian.information()
        library = []
        book1 = Book("B001", "Python基础")
        book2 = Book("B002", "数据结构")
        librarian.add_book(library, book1)
        librarian.add_book(library, book2)
        librarian.show_all_books(library)
        print("\n=== 普通读者操作 ===")
        reader = Reader("R002", "张三")
        print(reader.information())
        reader.borrow_book(book1)
        reader.show_borrowed_books()
        print("\n=== VIP读者操作 ===")
        vip_reader = VIPReader("R003", "李四")
        vip_reader.information()
        vip_reader.borrow_book(book2)
        vip_reader.show_points()
        vip_reader.show_borrowed_books()