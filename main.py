import sqlite3
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from course import Ui_course
from ssis import Ui_AttendanceSystem

global course_code
course_code = ''
conn = sqlite3.connect('ssis.db')
c = conn.cursor()


class MainWin(QtWidgets.QMainWindow, Ui_AttendanceSystem):
    def __init__(self):
        super(MainWin, self).__init__()
        self.ui = Ui_AttendanceSystem()
        self.setupUi(self)
        self.show()
        self.load_data()
        self.add_button()
        self.del_button()
        self.update_btn()
        self.sel_btn()
        self.new_btn()

    def new_btn(self):
        self.pushButton_6.clicked.connect(self.courses)

    def courses(self):
        self.newWin = course()
        self.newWin.show()

    def load_data(self):
        result = c.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_button(self):
        self.pushButton.clicked.connect(self.add_student)

    def add_student(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()

        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        course = course_code
        gender = str(self.comboBox.currentText())
        year = str(self.comboBox_2.currentText())
        student_info = [(id, name, gender, year, course)]
        with conn:
            print('pushed')

            c.executemany("INSERT INTO student VALUES(?,?,?,?,?)", student_info)

        result = c.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.commit()
        conn.close()

    def del_button(self):
        self.pushButton_2.clicked.connect(self.del_student)

    def del_student(self):
        print("pushed del")
        test = str(self.tableWidget.currentItem().text())
        connect = sqlite3.connect('ssis.db')
        c = connect.cursor()
        print(test)
        c.execute('DELETE from student WHERE student_id = (?)', (test,))
        print(c.fetchall())

        result = c.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print(c.fetchall())
        connect.commit()
        connect.close()

    def search_btn(self):
        self.pushButton_3.clicked.connect(self.search)

    def sel_btn(self):
        self.pushButton_4.clicked.connect(self.sel)

    def update_btn(self):
        self.pushButton_5.clicked.connect(self.updtdb)

    def updtdb(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()

        id = self.lineEdit.text()
        name = self.lineEdit_2.text()
        course = self.lineEdit_3.text()
        gender = str(self.comboBox.currentText())
        year = str(self.comboBox_2.currentText())
        student_info = [(id, name, gender, year, course)]

        with conn:
            print('pushed')

            c.executemany("INSERT INTO student VALUES(?,?,?,?,?)", student_info)

        result = c.execute("SELECT* FROM student")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.commit()
        conn.close()

    def sel(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        select = str(self.tableWidget.currentItem().text())
        x = []

        c.execute("SELECT* FROM student WHERE student_id = (?)", (select,))
        values = c.fetchall()

        self.lineEdit.setText(values[0][0])
        self.lineEdit_2.setText(values[0][1])
        self.lineEdit_3.setText(values[0][4])
        self.comboBox.setCurrentText(values[0][3])
        self.comboBox_2.setCurrentText(values[0][2])

        print("pushed del")
        test = str(self.tableWidget.currentItem().text())
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        print(test)
        c.execute('DELETE from student WHERE student_id = (?)', (test,))
        print("deleted")
        conn.commit()
        conn.close()


class course(QtWidgets.QMainWindow, Ui_course):
    def __init__(self):
        super().__init__()
        self.ui = Ui_course()
        self.setupUi(self)
        self.show()
        self.load()
        self.add_btn()
        self.del_btn()
        self.confirm_btn()
        self.sel_btn()
        self.update_btn()

    def confirm_btn(self):
        self.pushButton_5.clicked.connect(self.confirm)

    def confirm(self):
        global course_code
        course_code = self.tableWidget.currentItem().text()
        print(course_code)

    def add_btn(self):
        self.pushButton.clicked.connect(self.add)

    def load(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()

        result = c.execute("SELECT* FROM course")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.commit()
        conn.close()

    def del_btn(self):
        self.pushButton_2.clicked.connect(self.del_course)

    def add(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        course_code = ''
        course_name = self.lineEdit.text()
        course_code += course_name[0]
        final_code = ''

        hey = course_name.replace(' of', '', 1)
        print(hey)

        for name in range(0, len(hey)):
            if hey[name] == ' ':
                course_code += hey[name + 1]
        c.execute("SELECT course_id FROM course")
        test = c.fetchall()
        CC = course_code.upper()
        final_code = CC
        for t in test:
            tes = t[0]
            if t[0] == CC:
                tes = t[0] + 'S'
                final_code = tes
                print(final_code)
        print(final_code)
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        CC = course_code.upper()
        print("pass")
        courses = [(final_code, hey)]
        print(courses)
        with conn:
            c.executemany("INSERT INTO course VALUES(?,?)", courses)
        print("pass")

        result = c.execute("SELECT* FROM course")
        print("pass")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print("pass")
        conn.commit()
        conn.close()

    def del_course(self):
        print("pushed del")
        test = str(self.tableWidget.currentItem().text())
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        print(test)
        c.execute('DELETE from course WHERE course_id = (?)', (test,))
        conn.commit()
        c.close()
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        result = c.execute("SELECT* FROM course")

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def sel_btn(self):
        self.pushButton_3.clicked.connect(self.sel)

    def update_btn(self):
        self.pushButton_4.clicked.connect(self.updtdb)

    def updtdb(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        course_code = ''
        course_name = self.lineEdit.text()
        course_code += course_name[0]
        final_code = ''

        hey = course_name.replace(' of', '', 1)
        print(hey)

        for name in range(0, len(hey)):
            if hey[name] == ' ':
                course_code += hey[name + 1]
        c.execute("SELECT course_id FROM course")
        test = c.fetchall()
        CC = course_code.upper()
        final_code = CC
        for t in test:
            tes = t[0]
            if t[0] == CC:
                tes = t[0] + 'S'
                final_code = tes
                print(final_code)
        print(final_code)
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        CC = course_code.upper()
        print("pass")
        courses = [(final_code, hey)]
        print(courses)
        with conn:
            c.executemany("INSERT INTO course VALUES(?,?)", courses)
        print("pass")

        result = c.execute("SELECT* FROM course")
        print("pass")
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print("pass")
        conn.commit()
        conn.close()

    def sel(self):
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        select = str(self.tableWidget.currentItem().text())

        c.execute("SELECT* FROM student WHERE student_id = (?)", (select,))
        values = c.fetchall()

        self.lineEdit.setText(values[0][0])

        print("pushed del")
        test = str(self.tableWidget.currentItem().text())
        conn = sqlite3.connect('ssis.db')
        c = conn.cursor()
        print(test)
        c.execute('DELETE from course WHERE course_id = (?)', (test,))
        print("deleted")
        conn.commit()
        conn.close()


app = QtWidgets.QApplication(sys.argv)
win = MainWin()
sys.exit(app.exec())
