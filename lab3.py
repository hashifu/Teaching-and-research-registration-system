from paper import *
from project import *
from classal import *
from collect import *

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="sanshiyi",
    password="USTCdb@3202.",
    database="lab3"
)

cursor = conn.cursor()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据库增删改查系统")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)

        self.row1_layout = QHBoxLayout()
        self.row2_layout = QHBoxLayout()
        self.row3_layout = QHBoxLayout()
        self.row4_layout = QHBoxLayout()

        self.btn1_insert = QPushButton("发表论文添加")
        self.btn1_delete = QPushButton("发表论文删除")
        self.btn1_update = QPushButton("发表论文更新")
        self.btn1_select = QPushButton("发表论文查询")

        self.btn2_insert = QPushButton("承担项目添加")
        self.btn2_delete = QPushButton("承担项目删除")
        self.btn2_update = QPushButton("承担项目更新")
        self.btn2_select = QPushButton("承担项目查询")

        self.btn3_insert = QPushButton("主讲课程添加")
        self.btn3_delete = QPushButton("主讲课程删除")
        self.btn3_update = QPushButton("主讲课程更新")
        self.btn3_select = QPushButton("主讲课程查询")

        self.btn4 = QPushButton("查询统计")

        self.btn1_insert.clicked.connect(self.insert_clicked)
        self.btn1_delete.clicked.connect(self.delete_clicked)
        self.btn1_update.clicked.connect(self.update_clicked)
        self.btn1_select.clicked.connect(self.select_clicked)

        self.btn2_insert.clicked.connect(self.insert_clicked2)
        self.btn2_delete.clicked.connect(self.delete_clicked2)
        self.btn2_update.clicked.connect(self.update_clicked2)
        self.btn2_select.clicked.connect(self.select_clicked2)

        self.btn3_insert.clicked.connect(self.insert_clicked3)
        self.btn3_delete.clicked.connect(self.delete_clicked3)
        self.btn3_update.clicked.connect(self.update_clicked3)
        self.btn3_select.clicked.connect(self.select_clicked3)

        self.btn4.clicked.connect(self.collect_clicked)

        self.btn1_insert.setFixedSize(120, 70)
        self.btn1_delete.setFixedSize(120, 70)
        self.btn1_update.setFixedSize(120, 70)
        self.btn1_select.setFixedSize(120, 70)
        self.btn2_insert.setFixedSize(120, 70)
        self.btn2_delete.setFixedSize(120, 70)
        self.btn2_update.setFixedSize(120, 70)
        self.btn2_select.setFixedSize(120, 70)
        self.btn3_insert.setFixedSize(120, 70)
        self.btn3_delete.setFixedSize(120, 70)
        self.btn3_update.setFixedSize(120, 70)
        self.btn3_select.setFixedSize(120, 70)
        self.btn4.setFixedSize(200, 60)

        self.row1_layout.addWidget(self.btn1_insert)
        self.row1_layout.addWidget(self.btn1_delete)
        self.row1_layout.addWidget(self.btn1_update)
        self.row1_layout.addWidget(self.btn1_select)

        self.row2_layout.addWidget(self.btn2_insert)
        self.row2_layout.addWidget(self.btn2_delete)
        self.row2_layout.addWidget(self.btn2_update)
        self.row2_layout.addWidget(self.btn2_select)

        self.row3_layout.addWidget(self.btn3_insert)
        self.row3_layout.addWidget(self.btn3_delete)
        self.row3_layout.addWidget(self.btn3_update)
        self.row3_layout.addWidget(self.btn3_select)

        self.row4_layout.addWidget(self.btn4)

        self.layout.addLayout(self.row1_layout)
        self.layout.addLayout(self.row2_layout)
        self.layout.addLayout(self.row3_layout)
        self.layout.addLayout(self.row4_layout)

        self.setLayout(self.layout)
        self.setFixedSize(600, 400)

    def insert_clicked(self):
        dialog = InsertDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data inserted successfully.")

    def delete_clicked(self):
        dialog = DeleteDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data deleted successfully.")

    def update_clicked(self):
        dialog = UpdateDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Updated successfully.")

    def select_clicked(self):
        dialog = SearchDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Searched successfully.")

    def insert_clicked2(self):
        dialog = InsertProDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data inserted successfully.")

    def delete_clicked2(self):
        dialog = DeleteProDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data deleted successfully.")

    def update_clicked2(self):
        dialog = UpdateProDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Updated successfully.")

    def select_clicked2(self):
        dialog = SearchProDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Searched successfully.")

    def insert_clicked3(self):
        dialog = InsertClaDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data inserted successfully.")

    def delete_clicked3(self):
        dialog = DeleteClaDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data deleted successfully.")

    def update_clicked3(self):
        dialog = UpdateClaDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Updated successfully.")

    def select_clicked3(self):
        dialog = SearchClaDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Searched successfully.")

    def collect_clicked(self):
        dialog = SearchColDialog()
        if dialog.exec_() == QDialog.Accepted:
            print("Data Searched successfully.")


# 关闭连接
def close_connection():
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# 关闭连接
close_connection()

# 关闭游标和连接
cursor.close()
conn.close()
