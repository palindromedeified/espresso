import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QTableWidgetItem
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(f"SELECT * FROM Coffee ").fetchall()
        con.close()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(len(result)):
            for j in range(len(result[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
