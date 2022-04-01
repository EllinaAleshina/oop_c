import os
import sys
import json
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QApplication, QLineEdit, QLabel,
                             QPushButton, QListWidget, QDialog,
                             QDoubleSpinBox, QMessageBox)
from PyQt5.QtGui import QFont

# Все пользователи
USERS = []


class DialogWithPercent(QDialog):
    '''Дилоговое окно с процентами'''

    def __init__(self, name, parent=None):
        '''Конструктор'''
        # Наследуем от родителя
        super().__init__(parent)
        self.parent = parent
        self.name = name

        # Устновка параметров окна
        self.setWindowTitle('Parameters')
        self.setModal(True)

        # Добавление элементов в диалоговое окно
        self.label = QLabel(name)
        self.count = QDoubleSpinBox()
        self.count.setMinimum(0.1)
        if name == 'Deposite':
            self.count.setMaximum(self.parent.user.get_balance())

        self.labelPercent = QLabel('Percent')
        self.percent = QDoubleSpinBox()
        self.percent.setMinimum(1)
        self.percent.setMaximum(100)

        self.submit = QPushButton('Add ' + name)
        self.submit.clicked.connect(self.change)

        # Разметка по grid сетке
        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.count, 0, 1)
        grid.addWidget(self.labelPercent, 1, 0)
        grid.addWidget(self.percent, 1, 1)
        grid.addWidget(self.submit, 2, 0, 1, 2)
        self.setLayout(grid)

    def change(self):
        '''Добавление вклада или кредита'''
        if self.name == 'Deposite':
            self.parent.user.addDeposite(
                self.count.value(), self.percent.value())
            self.parent.refreshDeposite()
            self.parent.deleteDepositeButton.setEnabled(True)
            self.parent.user -= self.count.value()
        else:
            self.parent.user.addCredit(
                self.count.value(), self.percent.value())
            self.parent.refreshCredit()
            self.parent.deleteCrediteButton.setEnabled(True)
            self.parent.user += self.count.value()
        self.parent.refreshBalance()
        self.close()


class DialogWithoutPercent(QDialog):
    '''Диалоговое окно без процентов'''

    def __init__(self, name, parent=None):
        '''Конструктор'''
        # Наследование от родительского окна
        super().__init__(parent)
        self.parent = parent
        self.name = name

        # Установка параметров окна
        self.setWindowTitle('Parameters')
        self.setModal(True)

        # Добавление элементов на экран диалогового окна
        self.label = QLabel('Amount:')
        self.count = QDoubleSpinBox()
        self.count.setMinimum(0.1)
        if name == 'Withdraw':
            self.count.setMaximum(self.parent.user.get_balance())
        else:
            self.count.setMaximum(10000)

        self.submit = QPushButton(name)
        self.submit.clicked.connect(self.change)

        # Разметка по grid сетке
        grid = QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.count, 0, 1)
        grid.addWidget(self.submit, 2, 0, 1, 2)
        self.setLayout(grid)

    def change(self):
        '''Снятие или пополнение счета'''
        if self.name == 'Withdraw':
            self.parent.user -= self.count.value()
        else:
            self.parent.user += self.count.value()
        self.parent.refreshBalance()
        self.close()


class Application(QWidget):
    '''Виджет для основного приложения'''

    def __init__(self, user):
        '''Конструктор'''
        # Наследование от родителя
        super().__init__()
        self.user = user
        # Инициализация интерфейса
        self.initUI()

    def initUI(self):
        '''Интерфейс'''
        # Текст
        username = QLabel(f"Username: {self.user.get_username()}")
        self.balance = QLabel(f"Balance: {self.user.get_balance()}")
        depositsLabel = QLabel(f"Deposits:")
        creditsLabel = QLabel(f"Credits:")

        # Список вкладов
        self.listDeposits = QListWidget()
        self.listDeposits.resize(100, 100)
        self.deposits = self.user.get_deposits()
        for i in range(len(self.deposits)):
            self.listDeposits.addItem(
                f'Value: {self.deposits[i][0]}, Percent: {self.deposits[i][1]}'
            )

        # Список кредитов
        self.listCredits = QListWidget()
        self.listCredits.resize(100, 100)
        self.credits = self.user.get_credits()
        for i in range(len(self.credits)):
            self.listCredits.addItem(
                f'Value: {self.credits[i][0]}, Percent: {self.credits[i][1]}'
            )

        # Кнопки
        addDeposite = QPushButton('New deposite')
        addDeposite.clicked.connect(self.addDeposite)
        addCredit = QPushButton('New credit')
        addCredit.clicked.connect(self.addCredit)
        withdraw = QPushButton('Withdraw')
        withdraw.clicked.connect(self.withdrawMoney)
        recharge = QPushButton('Recharge')
        recharge.clicked.connect(self.rechargeMoney)
        self.deleteDepositeButton = QPushButton('Delete deposite')
        self.deleteDepositeButton.clicked.connect(self.deleteDeposite)
        if len(self.deposits) == 0:
            self.deleteDepositeButton.setEnabled(False)
        self.deleteCrediteButton = QPushButton('Delete credite')
        self.deleteCrediteButton.clicked.connect(self.deleteCredite)
        if len(self.credits) == 0:
            self.deleteCrediteButton.setEnabled(False)
        exit = QPushButton('Exit')
        exit.clicked.connect(self.exit)

        # Изменение шрифта для текста
        username.setFont(QFont('Arial', 15))
        self.balance.setFont(QFont('Arial', 15))

        # Grid layout
        grid = QGridLayout()

        # Добавление виджетов в layout
        grid.addWidget(username, 0, 0)
        grid.addWidget(self.balance, 1, 0)
        grid.addWidget(depositsLabel, 2, 0)
        grid.addWidget(self.listDeposits, 2, 1)
        grid.addWidget(creditsLabel, 3, 0)
        grid.addWidget(self.listCredits, 3, 1)
        grid.addWidget(addDeposite, 4, 0)
        grid.addWidget(addCredit, 5, 0)
        grid.addWidget(withdraw, 6, 0)
        grid.addWidget(recharge, 7, 0)
        grid.addWidget(self.deleteDepositeButton, 8, 0)
        grid.addWidget(self.deleteCrediteButton, 9, 0)
        grid.addWidget(exit, 10, 0)

        # Установка layout
        self.setLayout(grid)

        # Установка размеров виджета
        self.setGeometry(300, 300, 1000, 1000)
        # Установка имени окна
        self.setWindowTitle('Application')
        self.show()

    def addDeposite(self):
        '''Вызов окна для вклада'''
        self.dialog = DialogWithPercent('Deposite', self)
        self.dialog.show()

    def addCredit(self):
        '''Вызов окна для кредита'''
        self.dialog = DialogWithPercent('Credit', self)
        self.dialog.show()

    def withdrawMoney(self):
        '''Вызов окна для снятия'''
        self.dialog = DialogWithoutPercent('Withdraw', self)
        self.dialog.show()

    def rechargeMoney(self):
        '''Вызов окна для пополнения'''
        self.dialog = DialogWithoutPercent('Recharge', self)
        self.dialog.show()

    def refreshBalance(self):
        '''Обновление баланса'''
        self.balance.setText(f"Balance: {self.user.get_balance()}")

    def refreshDeposite(self):
        '''Обновление вкладов'''
        self.listDeposits.clear()
        self.deposits = self.user.get_deposits()
        for i in range(len(self.deposits)):
            self.listDeposits.addItem(
                f'Value: {self.deposits[i][0]}, Percent: {self.deposits[i][1]}'
            )
        if len(self.deposits) == 0:
            self.deleteDepositeButton.setEnabled(False)

    def refreshCredit(self):
        '''Обновление кредитов'''
        self.listCredits.clear()
        self.credits = self.user.get_credits()
        for i in range(len(self.credits)):
            self.listCredits.addItem(
                f'Value: {self.credits[i][0]}, Percent: {self.credits[i][1]}'
            )
        if len(self.credits) == 0:
            self.deleteCrediteButton.setEnabled(False)

    def deleteDeposite(self):
        '''Удаление вклада'''
        for index in self.listDeposits.selectedIndexes():
            self.user.deleteDeposite(index.row())
        # Обновление вкладов
        self.refreshDeposite()
        # Обновление баланса
        self.refreshBalance()

    def deleteCredite(self):
        '''Удаление кредита'''
        for index in self.listCredits.selectedIndexes():
            self.user.deleteCredite(index.row())
        # Обновление кредитов
        self.refreshCredit()
        # Обновление баланса
        self.refreshBalance()

    def exit(self):
        '''Выход из приложения'''
        write_to_file()
        self.close()


class Login(QWidget):
    '''Виджет для захода в профиль пользователя'''

    def __init__(self):
        '''Изенен конструктор'''
        # Унаследовать конструктор
        super().__init__()

        # Вызов инициализации интерфейса
        self.initUI()

    def initUI(self):
        '''Интерфейс'''
        # Текст
        username = QLabel('Username:')
        password = QLabel('Password:')

        # Изменение шрифта для текста
        username.setFont(QFont('Arial', 15))
        password.setFont(QFont('Arial', 15))

        # Поля ввода
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        # Кнопки
        submit = QPushButton("Submit")
        submit.clicked.connect(self.check)

        reg = QPushButton("Registration")
        reg.clicked.connect(self.reg)

        exit = QPushButton("Exit")
        exit.clicked.connect(self.exit)

        # Grid layout
        grid = QGridLayout()

        # Добавление виджетов в layout
        grid.addWidget(username, 1, 0)
        grid.addWidget(self.usernameEdit, 1, 1, 1, 3)
        grid.addWidget(password, 2, 0)
        grid.addWidget(self.passwordEdit, 2, 1, 1, 3)
        grid.addWidget(submit, 3, 1, 1, 2)
        grid.addWidget(reg, 4, 1, 1, 2)
        grid.addWidget(exit, 5, 1, 1, 2)

        # Отступы
        grid.setContentsMargins(100, 400, 100, 500)

        # Установка layout
        self.setLayout(grid)

        # Установка размеров виджета
        self.setGeometry(300, 300, 1000, 1000)
        # Установка имени окна
        self.setWindowTitle('Login')
        self.show()

    def check(self):
        '''Проверка логина и пароля'''
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        for user in USERS:
            if user.check_user(username, password):
                self.app = Application(user)
                self.app.show()
                self.close()
                return
        QMessageBox.about(self, "Error", "Wrong username or password")

    def reg(self):
        '''Переход к виджету регистрации'''
        self.reg = Registration()
        self.reg.show()
        self.close()

    def exit(self):
        '''Выход из приложения'''
        write_to_file()
        self.close()


class Registration(Login):
    '''Виджет для регистрации'''

    def __init__(self):
        '''Конструктор'''
        # Наследование конструктора
        super().__init__()

    def initUI(self):
        '''Создание интерфейса'''
        # Текст
        username = QLabel('Username:')
        password = QLabel('Password:')

        # Изменение шрифта для текста
        username.setFont(QFont('Arial', 15))
        password.setFont(QFont('Arial', 15))

        # Поля ввода
        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        # Кнопка регистрации
        submit = QPushButton("Submit")
        submit.clicked.connect(self.reg)

        # Выход
        exit = QPushButton("Exit")
        exit.clicked.connect(self.exit)

        # Сетка
        grid = QGridLayout()

        grid.addWidget(username, 1, 0)
        grid.addWidget(self.usernameEdit, 1, 1, 1, 3)

        grid.addWidget(password, 2, 0)
        grid.addWidget(self.passwordEdit, 2, 1, 1, 3)

        grid.addWidget(submit, 3, 1, 1, 2)

        grid.addWidget(exit, 4, 1, 1, 2)

        grid.setContentsMargins(100, 400, 100, 500)

        self.setLayout(grid)

        # Установка параметров окна
        self.setGeometry(300, 300, 1000, 1000)
        self.setWindowTitle('Registraion')
        self.show()

    def reg(self):
        '''Регистрация пользователя'''
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        if not username or not password:
            QMessageBox.about(self, "Error", "Empty field")
            return
        # Проверка что такого пользователя не существует
        for user in USERS:
            if user.get_username() == username:
                QMessageBox.about(self, "Error", "User already exists")
                return
        # Регистрация
        user = Account(username, password)
        USERS.append(user)

        QMessageBox.about(self, "Success", "User created")

        self.login = Login()
        self.login.show()
        self.close()


class Account(object):
    '''Класс для пользователя'''

    def __init__(self, username, password):
        '''Инициализация класса'''
        self.__username = username
        self.__password = password
        self.__balance = 0
        self.__deposits = []
        self.__credits = []

    def get_username(self):
        '''Получение usernamd'''
        return self.__username

    def get_password(self):
        '''Получение пароля'''
        return self.__password

    def get_balance(self):
        '''Получение баланса'''
        return self.__balance

    def get_deposits(self):
        '''Получение вкладов'''
        return self.__deposits

    def get_credits(self):
        '''Получение кредитов'''
        return self.__credits

    def check_user(self, username, password):
        '''Проверка логина и пароля пользователя'''
        if self.__username == username and self.__password == password:
            return True
        return False

    def addDeposite(self, value, percent):
        '''Добавление вклада'''
        self.__deposits.append((value, percent))

    def addCredit(self, value, percent):
        '''Добавление кредита'''
        self.__credits.append((value, percent))

    def __add__(self, other):
        '''Перегрузка оператора + '''
        self.__balance += other
        self.fixBalance()
        return self

    def __iadd__(self, other):
        '''Перегрузка оператора += '''
        self.__balance += other
        self.fixBalance()
        return self

    def __sub__(self, other):
        '''Перегрузка оператора - '''
        self.__balance -= other
        self.fixBalance()
        return self

    def __isub__(self, other):
        '''Перегрузка оператора -= '''
        self.__balance -= other
        self.fixBalance()
        return self

    def fixBalance(self):
        '''Округление баланса до сотых '''
        self.__balance = round(self.__balance, 2)

    def deleteDeposite(self, index):
        '''Удаление депозита'''
        self.__balance += self.__deposits[index][0]
        self.fixBalance()
        del self.__deposits[index]

    def deleteCredite(self, index):
        '''Удаление кредита'''
        self.__balance -= self.__credits[index][0]
        self.fixBalance()
        del self.__credits[index]


def read_from_file():
    '''Чтение пользователей из файла'''
    if not os.path.exists('data.json'):
        return
    with open('data.json') as f:
        users = json.load(f)
        for user in users:
            a = Account(user['username'], user['password'])
            a += user['balance']
            for deposite in user['deposits']:
                a.addDeposite(deposite[0], deposite[1])
            for credit in user['credits']:
                a.addCredit(credit[0], credit[1])
            USERS.append(a)


def write_to_file():
    '''Запись пользователей в файл'''
    data = []
    for user in USERS:
        data.append(
            {
                'username': user.get_username(),
                'password': user.get_password(),
                'balance': user.get_balance(),
                'deposits': user.get_deposits(),
                'credits': user.get_credits()
            }
        )
    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    read_from_file()
    login = Login()

    sys.exit(app.exec_())
