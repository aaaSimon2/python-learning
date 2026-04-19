class Book:
    def __init__(self, book_id, title, is_borrowed=False):
        self.book_id = book_id
        self.title = title
        self.is_borrowed = is_borrowed
    def show_book_info(self):
        borrow_status = "已借出" if self.is_borrowed else "未借出"
        print(f"图书编号：{self.book_id}，书名：{self.title}，借阅状态：{borrow_status}")
class Reader:
    def __init__(self, reader_id, name, borrowed_books=None):
        self.reader_id = reader_id
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books else []
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
if __name__ == "__main__":
    book1 = Book("B001", "Python编程基础")
    book2 = Book("B002", "数据结构与算法")
    book3 = Book("B003", "机器学习实战")
    reader1 = Reader("R001", "张三")
    reader2 = Reader("R002", "李四")
    reader1.borrow_book(book1)
    reader1.borrow_book(book2)
    reader2.borrow_book(book1)
    reader2.borrow_book(book3)
    print("\n--- 读者已借图书列表 ---")
    reader1.show_borrowed_books()
    reader2.show_borrowed_books()
    print("\n--- 归还图书后 ---")
    reader1.return_book(book1)
    reader1.show_borrowed_books()
    book1.show_book_info()