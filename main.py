from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont
import sys
import calculate
import os
import subprocess
import time


class ThreadShow(QThread):
    def __init__(self, result, text):
        super(ThreadShow, self).__init__()
        self.text = text
        self.result = result

    def run(self):

        result = self.result
        with open(self.text + ".txt", "w", encoding='utf-8') as f:
            f.write(self.text + "\n")
            f.write(str(time.asctime(time.localtime(time.time()))) + "\n")
            if result.success:
                f.write(result.mean + "\n")
                f.write("计算成功, 均值类型为" + result.mean_type + "， 均值为" + result.mean + "， 均方差为" + result.std + "\n")
                if len(result.abnormal_list) > 0:
                    f.write("存在粗大误差：\n")
                    f.write(str(result.abnormal_list) + '\n')
                else:
                    f.write("不存在粗大误差\n")
                f.write("生成数据：\n")
                f.write(str(result.generated_data) + "\n")
            else:
                f.write("\n")
                f.write(result.string)


class ThreadCal(QThread):
    trigger = pyqtSignal(calculate.Result)

    def __init__(self, file_name, sheet_num, row_num, alpha, num, output):
        super(ThreadCal, self).__init__()
        self.fileName = file_name
        self.sheet_num = sheet_num
        self.row_num = row_num
        self.alpha = alpha
        self.num = num
        self.output = output

    def run(self):
        result = calculate.calculate(self.fileName, self.sheet_num, self.row_num, self.alpha, self.num, self.output)
        self.trigger.emit(result)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        self.alpha = 0.01
        self.output = None
        self.sheet_num = 0
        self.row_num = 0
        self.fileName = ""
        self.num = 100
        self.result = None
        self.work_thread = None
        self.show_thread = None

        super(Ui, self).__init__()
        uic.loadUi('work.ui', self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time_out)

        self.tabWeight = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.stackedWeight = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.stackedWeight.setCurrentIndex(0)

        self.page1 = self.stackedWeight.findChild(QtWidgets.QWidget, "page")
        self.page1_lineEdit = self.page1.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.page1_next_pushButton = self.page1.findChild(QtWidgets.QPushButton, "pushButton")
        self.page1_next_pushButton.clicked.connect(self.next_button_clicked)

        self.page2 = self.stackedWeight.findChild(QtWidgets.QWidget, "page_2")
        self.page2_next_pushButton = self.page2.findChild(QtWidgets.QPushButton, "pushButton_5")
        self.page2_next_pushButton.clicked.connect(self.next_button_clicked)
        self.page2_last_pushButton = self.page2.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.page2_last_pushButton.clicked.connect(self.last_button_clicked)
        self.page2_choose_pushButton = self.page2.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.page2_choose_pushButton.clicked.connect(self.file_choose_button_clicked)
        self.page2_spinBox_sheet = self.page2.findChild(QtWidgets.QSpinBox, "spinBox")
        self.page2_spinBox_sheet.valueChanged.connect(self.spin_box_sheet_changed)
        self.page2_spinBox_row = self.page2.findChild(QtWidgets.QSpinBox, "spinBox_2")
        self.page2_spinBox_row.valueChanged.connect(self.spin_box_row_changed)
        self.page2_choose_lineEdit = self.page2.findChild(QtWidgets.QLineEdit, "lineEdit_2")

        self.page3 = self.stackedWeight.findChild(QtWidgets.QWidget, "page_3")
        self.page3_next_pushButton = self.page3.findChild(QtWidgets.QPushButton, "pushButton_7")
        self.page3_next_pushButton.clicked.connect(self.page_3_next_button_clicked)
        self.page3_last_pushButton = self.page3.findChild(QtWidgets.QPushButton, "pushButton_6")
        self.page3_last_pushButton.clicked.connect(self.last_button_clicked)
        self.page3_radioButton_1 = self.page3.findChild(QtWidgets.QRadioButton, "radioButton")
        self.page3_radioButton_1.clicked.connect(self.radio_button_1_clicked)
        self.page3_radioButton_2 = self.page3.findChild(QtWidgets.QRadioButton, "radioButton_2")
        self.page3_radioButton_2.clicked.connect(self.radio_button_2_clicked)
        self.page3_lineEdit = self.page3.findChild(QtWidgets.QLineEdit, "lineEdit_3")
        self.page3_radio_widget = self.page3.findChild(QtWidgets.QWidget, "widget")
        self.page3_widget_radioButton_3 = self.page3_radio_widget.findChild(QtWidgets.QRadioButton, "radioButton_3")
        self.page3_widget_radioButton_3.clicked.connect(self.radio_button_3_clicked)
        self.page3_widget_radioButton_4 = self.page3_radio_widget.findChild(QtWidgets.QRadioButton, "radioButton_4")
        self.page3_widget_radioButton_4.clicked.connect(self.radio_button_4_clicked)
        self.page3_widget_radioButton_5 = self.page3_radio_widget.findChild(QtWidgets.QRadioButton, "radioButton_5")
        self.page3_widget_radioButton_5.clicked.connect(self.radio_button_5_clicked)

        self.page4 = self.stackedWeight.findChild(QtWidgets.QWidget, "page_4")
        self.page4_progressBar = self.page4.findChild(QtWidgets.QProgressBar, "progressBar")
        self.page4_progressBar.setMinimum(0)
        self.page4_progressBar.setMaximum(0)

        self.page5 = self.stackedWeight.findChild(QtWidgets.QWidget, "page_5")
        self.page5_result_label = self.page5.findChild(QtWidgets.QLabel, "label_43")
        self.page5_result_label.setScaledContents(True)
        self.page5_reset = self.page5.findChild(QtWidgets.QPushButton, "pushButton_11")
        self.page5_reset.clicked.connect(self.reset_clicked)
        self.page5_show_more = self.page5.findChild(QtWidgets.QPushButton, "pushButton_10")
        self.page5_show_more.clicked.connect(self.current_show_more)

        self.table = self.tabWeight.findChild(QtWidgets.QTableWidget, "tableWidget")
        font = QFont('微软雅黑', 10)
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['名称', '时间', '计算结果', '  '])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)  # 设置第五列宽度自动调整，充满屏幕
        self.table.horizontalHeader().setStretchLastSection(True)  ##设置最后一列拉伸至最大
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        # self.table.setRo
        self.table.horizontalHeader().resizeSection(0, 160)
        self.table.horizontalHeader().resizeSection(1, 160)
        self.table.horizontalHeader().resizeSection(2, 160)
        rootdir = os.path.join('./')
        self.txt_list = []
        for (dirpaths, dirnames, filenames) in os.walk(rootdir):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.txt':
                    self.txt_list.append(filename)

        # self.table.setRowCount(len(self.txt_list))

        for filename in self.txt_list:
            self.table_add_line(filename)
        self.show()

    def table_add_line(self, filename):
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        with open(filename, 'r', encoding='utf-8') as f:
            for i in range(3):
                text = f.readline().strip()
                self.table.setItem(row, i, QtWidgets.QTableWidgetItem(text))
            pb = QtWidgets.QPushButton("详情")
            pb.clicked.connect(self.table_show_more)
            pb2 = QtWidgets.QPushButton("删除")
            pb2.clicked.connect(self.table_delete_clicked)
            h = QtWidgets.QHBoxLayout()
            h.setAlignment(Qt.AlignCenter)
            h.addWidget(pb)
            h.addWidget(pb2)
            w = QtWidgets.QWidget()
            w.setLayout(h)
            self.table.setCellWidget(row, 3, w)
            self.table.setRowHeight(row, 40)

    def next_button_clicked(self):
        self.stackedWeight.setCurrentIndex(self.stackedWeight.currentIndex() + 1)

    def last_button_clicked(self):
        self.stackedWeight.setCurrentIndex(self.stackedWeight.currentIndex() - 1)

    def file_choose_button_clicked(self):
        self.fileName = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "/", "*.xlsx")[0]
        self.page2_choose_lineEdit.setText(str(self.fileName))

    def spin_box_sheet_changed(self):
        self.sheet_num = self.page2_spinBox_sheet.value()

    def spin_box_row_changed(self):
        self.row_num = self.page2_spinBox_row.value()

    def radio_button_1_clicked(self):
        self.alpha = 0.05

    def radio_button_2_clicked(self):
        self.alpha = 0.01

    def radio_button_3_clicked(self):
        self.output = 1

    def radio_button_4_clicked(self):
        self.output = 2

    def radio_button_5_clicked(self):
        self.output = 3

    def page_3_next_button_clicked(self):
        self.next_button_clicked()
        self.timer.start(5000)
        self.num = int(self.page3_lineEdit.text())

    def time_out(self):
        self.work_thread = ThreadCal(self.fileName, self.sheet_num, self.row_num, self.alpha, self.num, self.output)
        self.work_thread.trigger.connect(self.show_result)
        self.work_thread.start()
        self.next_button_clicked()
        self.timer.stop()

    def show_result(self, result):
        self.page5_result_label.setText(result.string)
        self.show_thread = ThreadShow(result, str(self.page1_lineEdit.text()))
        self.show_thread.start()
        self.txt_list.append(str(self.page1_lineEdit.text())+".txt")
        # self.table_add_line(str(self.page1_lineEdit.text())+".txt")

    def reset_clicked(self):
        self.stackedWeight.setCurrentIndex(0)

    def current_show_more(self):
        open_file(str(self.page1_lineEdit.text()) + ".txt")

    def table_delete_clicked(self):
        button = self.sender()
        if button:
            item = button.parent()
            row = self.table.indexAt(item.pos()).row()
            os.remove(self.txt_list[row])
            self.table.removeRow(row)
            self.txt_list.pop(row)

    def table_show_more(self):
        button = self.sender()
        if button:
            item = button.parent()
            row = self.table.indexAt(item.pos()).row()
            open_file(self.txt_list[row])


def open_file(file_name):
    if sys.platform == 'linux2':
        subprocess.call(["xdg-open", file_name])
    else:
        os.startfile(file_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Ui()
    app.exec_()
