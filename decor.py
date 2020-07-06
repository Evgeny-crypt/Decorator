from time import strftime, localtime

def parse_favour(favour):
    if favour:
        return 'да'
    return 'нет'


class Contact:

    def __init__(self, name, surname, phone_number, favourites=False, **kwargs):
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.favourites = favourites
        self.items = [self.name, self.surname, self.phone_number]
        self.kwargs = "\n".join(["          {} : {}".format(key, value) for key, value in kwargs.items()])

    def __str__(self):
        return 'Имя: {} \nФамилия: {} \nТелефонный номер: {} \nИзбранные контакты: {}\
         \nДополнительная информация: \n{}'.format(
            self.name, self.surname, self.phone_number, parse_favour(self.favourites), self.kwargs
                                                   )

    def __lt__(self, other):
        return self.name < other.name

    def __contains__(self, item):
        return item in self.items




def param_logger(file_patch):
    def logger(method):
        def wrapper(self, *args, **kwargs):
            res = method(self, *args, **kwargs)
            write_string = f'{strftime(f"%y-%m-%d %H.%M.%S", localtime())} {method.__name__} {args} {kwargs} {res}\n'
            with open(file_patch, 'a', encoding='utf8') as file:
                file.write(write_string)
            return res
        return wrapper
    return logger

file_patch = 'log.txt'

class PhoneBook:
    @param_logger(file_patch)
    def __init__(self, book_name, contact_list=None):
        if contact_list is None:
            contact_list = []
        self.book_name = book_name
        self.contact_list = contact_list

    @param_logger(file_patch)
    def add_contact(self, *args, **kwargs):  # добавить контакты
        self.contact_list.append(Contact(*args, **kwargs))
        self.contact_list.sort()

    @param_logger(file_patch)
    def view_favourite(self):  # избранные контакты
        for contact in self.contact_list:
            if contact.favourites:
                print(contact)

    @param_logger(file_patch)
    def view_contacts(self):  # показать контакты
        for contact in self.contact_list:
            print(contact)

    @param_logger(file_patch)
    def search_contact(self, search_string):  # поиск контакта
        for contact in self.contact_list:
            if search_string in contact:
                print(contact)

    @param_logger(file_patch)
    def delete_contact(self, phone_number):  # удалить контакт по номеру
        for contact in self.contact_list:
            if phone_number in contact:
                self.contact_list.remove(contact)


# John = Contact('John', 'Travel', '8924123456', favourites=False, telegram='@Johny', Email='vizor9@bk.ru')
# print(John)
if __name__ == '__main__':
    book = PhoneBook('<---Телефонная книга--->')
    print(book.book_name)

    book.add_contact('John', 'Travel', '+7924123456', favourites=False, telegram='@Johny', Email='vizor9@bk.ru')
    book.add_contact('Karl', 'Ratov', '+79241534248', favourites=True, telegram='@Karl', Email='Karl23@mail.ru')
    book.add_contact('Evgeny', 'Krugov', '+7914767676', favourites=False, telegram='@Evg', Email='Evg@list.ru')
    book.add_contact('Jaret', 'Letto', '+79246873349', favourites=False, telegram='@Jaret', Email='Jaret@mail.ru')
    book.add_contact('Jan', 'Clodov', '+79249875543', favourites=True, telegram='@Jan', Email='Jan@bk.ru')
    book.add_contact('Ray', 'Makov', '+79249274194', favourites=False, telegram='@Ray', Email='Ray@mail.ru')

    print('\n===Все контакты===')
    book.view_contacts()
    print('\n===Поиск===\n')
    book.search_contact('Clodov')
    print('\n===Избранные контакты===\n')
    book.view_favourite()
    print('\n===Удаление===\n')
    book.delete_contact('+79241534248')