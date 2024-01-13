import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QTableWidgetItem, QAbstractItemView, QDialog
from untitled import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("main.ui", self)
        self.setupUi(self)
        self.from_db_to_table()
        self.item = -1
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tableWidget.cellClicked.connect(self.get_cell_last_clicked)
        self.changeButton.clicked.connect(self.run)
        self.addButton.clicked.connect(self.run)

    def get_cell_last_clicked(self, item):
        self.item = item

    def run(self):
        flag = True if self.sender().text() == 'Изменить' else False
        if self.item > -1 and flag:
            app = AddEditCoffeeForm(flag=flag, lst=self.result[self.item])
            app.exec_()
        elif not flag:
            app = AddEditCoffeeForm(flag=flag)
            app.exec_()
        self.from_db_to_table()

    def from_db_to_table(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        self.result = cur.execute(f"SELECT * FROM Coffee ").fetchall()
        con.close()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(len(self.result)):
            for j in range(len(self.result[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))


class AddEditCoffeeForm(QDialog, Ui_Form):
    def __init__(self, flag, lst=None):
        super(AddEditCoffeeForm, self).__init__()
        self.setupUi(self)
        # uic.loadUi("addEditCoffeeForm.ui", self)
        self.lineEdits = [self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5,
                          self.lineEdit_6]
        self.flag = flag
        self.lst = lst
        self.some_func()
        self.pushButton.clicked.connect(self.ok_func)

    def ok_func(self):
        texts = [i.text() for i in self.lineEdits]
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        if self.flag:
            texts = [self.lst[i + 1] if texts[i] == '' else texts[i] for i in range(6)]
            cur.execute(
                f"UPDATE coffee SET sort_name = '{texts[0]}', roasting = '{texts[1]}', ground_grains = '{texts[2]}', taste_desc = '{texts[3]}', price = '{texts[4]}', volume = '{texts[5]}' WHERE id = '{self.lst[0]}'").fetchall()
        else:
            texts = ['Null' if texts[i] == '' else texts[i] for i in range(6)]
            cur.execute(
                f"INSERT INTO coffee(sort_name, roasting, ground_grains, taste_desc, price, volume) VALUES('{texts[0]}', '{texts[1]}', '{texts[2]}','{texts[3]}', '{texts[4]}', '{texts[5]}')").fetchall()
        con.commit()
        con.close()
        self.close()

    def some_func(self):
        if self.flag:
            for i in range(len(self.lineEdits)):
                self.lineEdits[i].setPlaceholderText(self.lst[i + 1])


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
