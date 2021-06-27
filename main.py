import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5
from ssis import Ui_AttendanceSystem
import sqlite3
import db

connect = sqlite3.connect('ssis.db')
cursor = connect.cursor()


class MainWin(QtWidgets.QMainWindow, Ui_AttendanceSystem):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.ui = Ui_AttendanceSystem()
        self.setupUi(self)
        self.show()
        self.load_data()
        self.add_button()
        self.del_button()
        self.update_btn()
        self.sel_btn()

    def load_data(self):
        result = cursor.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_button(self):
        self.pushButton.clicked.connect(lambda: self.add_student())

    def add_student(self):
        connect = sqlite3.connect('ssis.db')
        cursor = connect.cursor()

        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        course = self.lineEdit_3.text()
        gender = str(self.comboBox.currentText())
        year = str(self.comboBox_2.currentText())
        student_info = [(id, name, gender, year, course)]
        with connect:
            print('pushed')

            cursor.executemany("INSERT INTO student VALUES(?,?,?,?,?)", student_info)

        result = cursor.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connect.commit()
        connect.close()

    def del_button(self):
        self.pushButton_2.clicked.connect(lambda: self.del_student())

    def del_student(self):
        print("pushed del")
        test = str(self.tableWidget.currentItem().text())
        connect = sqlite3.connect('ssis.db')
        cursor = connect.cursor()
        print(test)
        cursor.execute('DELETE from student WHERE student_id = (?)', (test,))
        print(cursor.fetchall())

        result = cursor.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print(cursor.fetchall())
        connect.commit()
        connect.close()

    def search_btn(self):
        self.pushButton_3.clicked.connect(lambda: self.search())

    def sel_btn(self):
        self.pushButton_4.clicked.connect(lambda: self.sel())


    def update_btn(self):
        self.pushButton_5.clicked.connect(lambda: self.updtdb())

    def updtdb(self):
        connect = sqlite3.connect('ssis.db')
        cursor = connect.cursor()

        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        course = self.lineEdit_3.text()
        gender = str(self.comboBox.currentText())
        year = str(self.comboBox_2.currentText())
        student_info = [(id, name, gender, year, course)]

        with connect:
            print('pushed')

            cursor.executemany("INSERT INTO student VALUES(?,?,?,?,?)", student_info)

        result = cursor.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connect.commit()
        connect.close()

    def sel(self):
        connect = sqlite3.connect('ssis.db')
        cursor = connect.cursor()
        select = str(self.tableWidget.currentItem().text())
        x = []

        cursor.execute("SELECT* FROM student WHERE student_id = (?)", (select,))
        values = cursor.fetchall()

        self.lineEdit.setText(values[0][0])
        self.lineEdit_2.setText(values[0][1])
        self.lineEdit_3.setText(values[0][4])
        self.comboBox.setCurrentText(values[0][3])
        self.comboBox_2.setCurrentText(values[0][2])

        print("pushed del")
        test = str(self.tableWidget.currentItem().text())
        connect = sqlite3.connect('ssis.db')
        cursor = connect.cursor()
        print(test)
        cursor.execute('DELETE from student WHERE student_id = (?)', (test,))
        print("deleted")
        connect.commit()
        connect.close()

app = QtWidgets.QApplication(sys.argv)
win = MainWin()
sys.exit(app.exec())
