import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, \
    QMessageBox, QComboBox, QTextEdit
from PyQt5.QtCore import Qt
import mysql.connector


# 插入数据
def insert_class(teacherid, classnum, teachyear, semester, takehours, classname, quality):
    conn1 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM TakeCourse WHERE Classnum = %s AND TeacherID = %s", (classnum, teacherid))
    rows = cursor1.fetchall()
    if rows:
        QMessageBox.warning(None, "Error", "已经存在该老师的授课信息！")
        return
    cursor1.execute("SELECT ID FROM Teacher WHERE ID = %s", (teacherid,))
    row = cursor1.fetchone()
    if not row:
        QMessageBox.warning(None, "Error", "没有这个老师！")
        return
    cursor1.execute("SELECT Classnum FROM Class WHERE Classnum = %s", (classnum,))
    if not cursor1.fetchone():
        sql_paper = "INSERT INTO Class VALUES (%s, %s, %s, %s)"
        values = (classnum, classname, takehours, quality)
        cursor1.execute(sql_paper, values)
    else:
        cursor1.execute("SELECT * FROM Class WHERE Classnum = %s", (classnum,))
        class_row = cursor1.fetchone()
        current_time = class_row[2]
        takehours = int(takehours)
        updated_time = current_time + takehours
        sql_update = "UPDATE Class SET classhour = %s WHERE Classnum = %s"
        values = (updated_time, classnum)
        cursor1.execute(sql_update, values)
    sql = "INSERT INTO TakeCourse VALUES (%s, %s, %s, %s, %s)"
    teachyear = int(teachyear)
    takehours = int(takehours)
    values = (teacherid, classnum, teachyear, semester, takehours)
    cursor1.execute(sql, values)

    # sql = "SELECT * FROM Paper"
    # cursor1.execute(sql)
    # results = cursor1.fetchall()
    # # 处理结果集
    # if not results:
    #     print("noway")
    # for row in results:
    #     field1 = row[0]  # 第一个字段的值
    #     field2 = row[1]  # 第二个字段的值
    #
    #     # 打印字段值
    #     print("Field1:", field1)
    #     print("Field2:", field2)
    conn1.commit()
    QMessageBox.information(None, "Success", "插入成功！")
    print("Data inserted successfully.")


# 删除数据
def delete_class(teacherid, classnum):
    conn2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM TakeCourse WHERE Classnum = %s AND TeacherID = %s", (classnum, teacherid))
    rows = cursor2.fetchall()
    if not rows:
        QMessageBox.warning(None, "Error", "不存在该信息！")
        return
    cursor2.execute("SELECT takehours FROM TakeCourse WHERE Classnum = %s AND TeacherID = %s", (classnum, teacherid))
    time_now = cursor2.fetchone()
    take_hour = time_now[0]
    cursor2.execute("SELECT * FROM TakeCourse WHERE Classnum = %s", (classnum,))
    class_row = cursor2.fetchone()
    current_time = class_row[2]
    updated_time = current_time - take_hour
    sql_update = "UPDATE Class SET classhour = %s WHERE Classnum = %s"
    values = (updated_time, classnum)
    cursor2.execute(sql_update, values)
    sql = "DELETE FROM TakeCourse WHERE TeacherID = %s and Classnum = %s"
    values = (teacherid, classnum)
    cursor2.execute(sql, values)
    cursor2.execute("SELECT Classnum FROM TakeCourse WHERE Classnum = %s", (classnum,))
    row = cursor2.fetchone()
    if not row:
        sql = "DELETE FROM Class WHERE Classnum = %s"
        values = (classnum,)
        cursor2.execute(sql, values)
    conn2.commit()
    QMessageBox.information(None, "Success", "删除成功！")
    print("Data deleted successfully.")


def delete_class2(classnum):
    conn2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM Class WHERE Classnum = %s", (classnum,))
    rows = cursor2.fetchall()
    if not rows:
        QMessageBox.warning(None, "Error", "不存在该信息！")
        return
    sql = "DELETE FROM Class WHERE Classnum = %s"
    values = (classnum,)
    cursor2.execute(sql, values)
    conn2.commit()
    QMessageBox.information(None, "Success", "删除成功！")
    print("Data deleted successfully.")


# 更新数据
def update_class(teacherid, classnum, teachyear, semester, takehours, classname, quality):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    if teacherid and classnum:
        check_key_sql = "SELECT COUNT(*) FROM TakeCourse WHERE TeacherID = %s AND Classnum = %s"
        check_key_values = (teacherid, classnum)
        cursor3.execute(check_key_sql, check_key_values)
        count = cursor3.fetchone()[0]
        if count == 0:
            QMessageBox.warning(None, "Error", "数据非法！请检查你的工号和课程号！")
            return
    else:
        check_key_sql = "SELECT COUNT(*) FROM TakeCourse WHERE Classnum = %s"
        check_key_values = (classnum,)
        cursor3.execute(check_key_sql, check_key_values)
        count = cursor3.fetchone()[0]
        if count == 0:
            QMessageBox.warning(None, "Error", "数据非法！请检查你的课程号！")
            return
    if teacherid:
        if takehours:
            cursor3.execute("SELECT takehours FROM TakeCourse WHERE Classnum = %s AND TeacherID = %s", (classnum, teacherid))
            time_now = cursor3.fetchone()
            cost_delete = time_now[0]
            cursor3.execute("SELECT * FROM Class WHERE Classnum = %s", (classnum,))
            class_row = cursor3.fetchone()
            current_time = class_row[2]
            takehours = int(takehours)
            updated_time = current_time - cost_delete + takehours
            sql_update = "UPDATE Class SET classhour = %s WHERE Classnum = %s"
            values = (updated_time, classnum)
            cursor3.execute(sql_update, values)
            sql_update = "UPDATE TakeCourse SET takehours = %s WHERE Classnum = %s AND TeacherID = %s"
            values = (takehours, classnum, teacherid)
            cursor3.execute(sql_update, values)
        if teachyear:
            sql = "UPDATE TakeCourse SET teachyear = %s WHERE Classnum = %s AND TeacherID = %s"
            values = (teachyear, classnum, teacherid)
            cursor3.execute(sql, values)
        if semester:
            sql = "UPDATE TakeCourse SET semester = %s WHERE Classnum = %s AND TeacherID = %s"
            values = (semester, classnum, teacherid)
            cursor3.execute(sql, values)


    if classname:
        sql = "UPDATE Class SET classname = %s WHERE Classnum = %s"
        values = (classname, classnum)
        cursor3.execute(sql, values)
    if quality:
        sql = "UPDATE Class SET quality = %s WHERE Classnum = %s"
        values = (quality, classnum)
        cursor3.execute(sql, values)

    conn3.commit()
    QMessageBox.information(None, "Success", "更新成功！")
    print("Data updated successfully.")


# 查询数据
def select_class(teacherid, classnum):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    if classnum and not teacherid:
        sql = "SELECT * FROM Class " \
              "INNER JOIN TakeCourse ON Class.Classnum = TakeCourse.Classnum " \
              "INNER JOIN Teacher ON Teacher.ID = TakeCourse.TeacherID " \
              "WHERE Class.Classnum = %s"
        values = (classnum,)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    elif teacherid and not classnum:
        sql = "SELECT * FROM Teacher " \
              "INNER JOIN TakeCourse ON Teacher.ID = TakeCourse.TeacherID " \
              "INNER JOIN Class ON TakeCourse.Classnum = Class.Classnum " \
              "WHERE Teacher.ID = %s"
        values = (teacherid,)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    elif teacherid and classnum:
        sql = "SELECT * FROM TakeCourse " \
              "INNER JOIN Teacher ON Teacher.ID = TakeCourse.TeacherID " \
              "INNER JOIN Class ON TakeCourse.Classnum = Class.Classnum " \
              "WHERE Teacher.ID = %s AND Class.Classnum = %s"
        values = (teacherid, classnum)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    else:
        rows = None
    print("Data selected successfully.")
    return rows


class InsertClaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("插入课程")

        layout = QVBoxLayout()

        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("课程号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        paper_name_label = QLabel("课程名称:")
        self.paper_name_input = QLineEdit()
        layout.addWidget(paper_name_label)
        layout.addWidget(self.paper_name_input)

        type_label = QLabel("课程性质:")
        self.type_input = QComboBox()
        self.type_input.addItem("本科生课程")
        self.type_input.addItem("研究生课程")
        layout.addWidget(type_label)
        layout.addWidget(self.type_input)

        publish_begin_label = QLabel("年份:")
        self.publish_begin_input = QLineEdit()
        layout.addWidget(publish_begin_label)
        layout.addWidget(self.publish_begin_input)

        publish_semester_label = QLabel("学期:")
        self.publish_semester_input = QComboBox()
        self.publish_semester_input.addItem("春季学期")
        self.publish_semester_input.addItem("夏季学期")
        self.publish_semester_input.addItem("秋季学期")
        layout.addWidget(publish_semester_label)
        layout.addWidget(self.publish_semester_input)

        pub_hour_label = QLabel("承担学时:")
        self.pub_hour_input = QLineEdit()
        layout.addWidget(pub_hour_label)
        layout.addWidget(self.pub_hour_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        classnum = self.paper_id_input.text()
        classname = self.paper_name_input.text()
        what_type = self.type_input.currentText()
        teachyear = self.publish_begin_input.text()
        what_semester = self.publish_semester_input.currentText()
        takehours = self.pub_hour_input.text()

        type_mapping = {"本科生课程": 1, "研究生课程": 2}
        quality = type_mapping.get(what_type, None)

        semester_mapping = {"春季学期": 1, "夏季学期": 2, "秋季学期": 3}
        semester = semester_mapping.get(what_semester, None)

        if not teacherid or not classnum or not classname or not quality or not teachyear or not \
                semester or not takehours:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        insert_class(teacherid, classnum, teachyear, semester, takehours, classname, quality)
        self.close()


class DeleteClaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("删除课程")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("删除授课记录:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("课程号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        layout.addWidget(QLabel("直接删除课程:"))

        paper_label = QLabel("课程号:")
        self.paper_input = QLineEdit()
        layout.addWidget(paper_label)
        layout.addWidget(self.paper_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        classnum = self.paper_id_input.text()
        classnum2 = self.paper_input.text()
        if not teacherid and not classnum and not classnum2:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        if classnum2:
            delete_class2(classnum2)
        else:
            if not teacherid or not classnum:
                QMessageBox.warning(self, "错误的输入", "请输入完整！")
                return
            else:
                delete_class(teacherid, classnum)
        self.close()


class UpdateClaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("插入课程")

        layout = QVBoxLayout()

        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("课程号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        paper_name_label = QLabel("课程名称:")
        self.paper_name_input = QLineEdit()
        layout.addWidget(paper_name_label)
        layout.addWidget(self.paper_name_input)

        type_label = QLabel("课程性质:")
        self.type_input = QComboBox()
        self.type_input.addItem("本科生课程")
        self.type_input.addItem("研究生课程")
        layout.addWidget(type_label)
        layout.addWidget(self.type_input)

        publish_begin_label = QLabel("年份:")
        self.publish_begin_input = QLineEdit()
        layout.addWidget(publish_begin_label)
        layout.addWidget(self.publish_begin_input)

        publish_semester_label = QLabel("学期:")
        self.publish_semester_input = QComboBox()
        self.publish_semester_input.addItem("春季学期")
        self.publish_semester_input.addItem("夏季学期")
        self.publish_semester_input.addItem("秋季学期")
        layout.addWidget(publish_semester_label)
        layout.addWidget(self.publish_semester_input)

        pub_hour_label = QLabel("承担学时:")
        self.pub_hour_input = QLineEdit()
        layout.addWidget(pub_hour_label)
        layout.addWidget(self.pub_hour_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        classnum = self.paper_id_input.text()
        classname = self.paper_name_input.text()
        what_type = self.type_input.currentText()
        teachyear = self.publish_begin_input.text()
        what_semester = self.publish_semester_input.currentText()
        takehours = self.pub_hour_input.text()

        type_mapping = {"本科生课程": 1, "研究生课程": 2}
        quality = type_mapping.get(what_type, None)

        semester_mapping = {"春季学期": 1, "夏季学期": 2, "秋季学期": 3}
        semester = semester_mapping.get(what_semester, None)

        if not classnum:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return

        update_class(teacherid, classnum, teachyear, semester, takehours, classname, quality)
        self.close()


class ResultClaDialog(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("查询结果")
        self.layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setText(data)
        self.layout.addWidget(self.result_text)

        self.setLayout(self.layout)
        self.setFixedSize(1000, 800)


class SearchClaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("查询课程")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("按教师工号、课程号或一起查询:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("课程号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        classnum = self.paper_id_input.text()
        if not teacherid and not classnum:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        rows = select_class(teacherid, classnum)
        if not rows:
            QMessageBox.warning(self, "结果", "未找到搜索结果！")
            return
        result_str = ""
        if teacherid and not classnum:
            for row in rows:
                if row[2] == 1:
                    tsex = "男"
                else:
                    tsex = "女"
                if row[3] == 1:
                    title = "博士后"
                elif row[3] == 2:
                    title = "助教"
                elif row[3] == 3:
                    title = "讲师"
                elif row[3] == 4:
                    title = "副教授"
                elif row[3] == 5:
                    title = "特任教授"
                else:
                    title = "教授"
                if row[7] == 1:
                    classsem = "春季学期"
                elif row[7] == 2:
                    classsem = "夏季学期"
                else:
                    classsem = "秋季学期"
                if row[12] == 1:
                    classtype = "本科生课程"
                else:
                    classtype = "研究生课程"
                result_str += f"工号: {row[0]}, 教师姓名: {row[1]}, 教师性别: {tsex}, 教师职称: {title}, " \
                              f"课程号: {row[5]}, 教学年份: {row[6]}, 教学学期: {classsem}, 承担学时: {row[8]}, " \
                              f"课程名称: {row[10]}, 课程总学时: {row[11]}, 课程性质: {classtype}\n"
        elif classnum and not teacherid:
            for row in rows:
                if row[11] == 1:
                    tsex = "男"
                else:
                    tsex = "女"
                if row[12] == 1:
                    title = "博士后"
                elif row[12] == 2:
                    title = "助教"
                elif row[12] == 3:
                    title = "讲师"
                elif row[12] == 4:
                    title = "副教授"
                elif row[12] == 5:
                    title = "特任教授"
                else:
                    title = "教授"
                if row[7] == 1:
                    classsem = "春季学期"
                elif row[7] == 2:
                    classsem = "夏季学期"
                else:
                    classsem = "秋季学期"
                if row[3] == 1:
                    classtype = "本科生课程"
                else:
                    classtype = "研究生课程"
                result_str += f"课程号: {row[0]}, 课程名称: {row[1]}, 课程总学时: {row[2]}, 课程性质: {classtype}, " \
                              f"工号: {row[4]}, 教学年份: {row[6]}, 教学学期: {classsem}, 承担学时: {row[8]}, " \
                              f"教师姓名: {row[10]}, 教师性别: {tsex}, 教师职称: {title}\n"
        elif teacherid and classnum:
            for row in rows:
                if row[7] == 1:
                    tsex = "男"
                else:
                    tsex = "女"
                if row[8] == 1:
                    title = "博士后"
                elif row[8] == 2:
                    title = "助教"
                elif row[8] == 3:
                    title = "讲师"
                elif row[8] == 4:
                    title = "副教授"
                elif row[8] == 5:
                    title = "特任教授"
                else:
                    title = "教授"
                if row[3] == 1:
                    classsem = "春季学期"
                elif row[3] == 2:
                    classsem = "夏季学期"
                else:
                    classsem = "秋季学期"
                if row[12] == 1:
                    classtype = "本科生课程"
                else:
                    classtype = "研究生课程"
                result_str += f"工号: {row[0]}, 课程号: {row[1]}, 教学年份: {row[2]}, 教学学期: {classsem}, " \
                              f"承担学时: {row[4]}, 教师姓名: {row[6]}, 教师性别: {tsex}, 教师职称: {title}, 课程名称: {row[10]}, " \
                              f"课程总学时: {row[11]}, 课程性质: {classtype}\n"
        else:
            result_str = ""

        # 显示结果窗口
        dialog = ResultClaDialog(result_str)
        dialog.exec_()
        self.close()
