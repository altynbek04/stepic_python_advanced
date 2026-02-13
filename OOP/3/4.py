class Library:
    def __init__(self, books):
        self.__books = books

    def __check_availability(self, book_name):
        return book_name in self.__books

    def search_book(self, book_name):
        return self.__check_availability(book_name)

    def return_book(self, book_name):
        self.__books.append(book_name)

    def _checkout_book(self, book_name):
        if self.__check_availability(book_name):
            self.__books.remove(book_name)
            return True
        return False