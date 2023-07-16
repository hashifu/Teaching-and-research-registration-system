import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, \
    QMessageBox, QComboBox, QTextEdit
from PyQt5.QtCore import Qt
import mysql.connector


# 插入数据
def insert_project(teacherid, projnum, projrank, cost, projname, projsource, projtype, beginyear, endyear):
    conn1 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM TakeProj WHERE Projectnum = %s AND TeacherID = %s", (projnum, teacherid))
    rows = cursor1.fetchall()
    if rows:
        QMessageBox.warning(None, "Error", "已经存在该老师的信息！")
        return
    cursor1.execute("SELECT projrank FROM TakeProj WHERE Projectnum = %s", (projnum,))
    rows = cursor1.fetchall()
    for row in rows:
        existing_proj_rank = row[0]
        if existing_proj_rank == projrank:
            QMessageBox.warning(None, "Error", "项目负责排名不能重复！")
            return
    cursor1.execute("SELECT ID FROM Teacher WHERE ID = %s", (teacherid,))
    row = cursor1.fetchone()
    if not row:
        QMessageBox.warning(None, "Error", "没有这个老师！")
        return
    cursor1.execute("SELECT Projectnum FROM TakeProj WHERE Projectnum = %s", (projnum,))
    if not cursor1.fetchone():
        sql_paper = "INSERT INTO Project VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (projnum, projname, projsource, projtype, cost, beginyear, endyear)
        cursor1.execute(sql_paper, values)
    else:
        cursor1.execute("SELECT * FROM Project WHERE Projectnum = %s", (projnum,))
        project_row = cursor1.fetchone()
        current_budget = project_row[4]
        cost = float(cost)
        updated_budget = current_budget + cost
        sql_update = "UPDATE Project SET budget = %s WHERE Projectnum = %s"
        values = (updated_budget, projnum)
        cursor1.execute(sql_update, values)
    sql = "INSERT INTO TakeProj VALUES (%s, %s, %s, %s)"
    values = (teacherid, projnum, projrank, cost)
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
def delete_project(teacherid, projnum):
    conn2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM TakeProj WHERE Projectnum = %s AND TeacherID = %s", (projnum, teacherid))
    rows = cursor2.fetchall()
    if not rows:
        QMessageBox.warning(None, "Error", "不存在该信息！")
        return
    cursor2.execute("SELECT cost FROM TakeProj WHERE Projectnum = %s AND TeacherID = %s", (projnum, teacherid))
    cost_now = cursor2.fetchone()
    cost = cost_now[0]
    cursor2.execute("SELECT * FROM Project WHERE Projectnum = %s", (projnum,))
    project_row = cursor2.fetchone()
    current_budget = project_row[4]
    updated_budget = current_budget - cost
    sql_update = "UPDATE Project SET budget = %s WHERE Projectnum = %s"
    values = (updated_budget, projnum)
    cursor2.execute(sql_update, values)
    sql = "DELETE FROM TakeProj WHERE TeacherID = %s and Projectnum = %s"
    values = (teacherid, projnum)
    cursor2.execute(sql, values)
    cursor2.execute("SELECT Projectnum FROM TakeProj WHERE Projectnum = %s", (projnum,))
    row = cursor2.fetchone()
    if not row:
        sql = "DELETE FROM Project WHERE Projectnum = %s"
        values = (projnum,)
        cursor2.execute(sql, values)
    conn2.commit()
    QMessageBox.information(None, "Success", "删除成功！")
    print("Data deleted successfully.")


def delete_project2(projnum):
    conn2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM Project WHERE Projectnum = %s", (projnum,))
    rows = cursor2.fetchall()
    if not rows:
        QMessageBox.warning(None, "Error", "不存在该信息！")
        return
    sql = "DELETE FROM Project WHERE Projectnum = %s"
    values = (projnum,)
    cursor2.execute(sql, values)
    conn2.commit()
    QMessageBox.information(None, "Success", "删除成功！")
    print("Data deleted successfully.")


# 更新数据
def update_project(teacherid, projnum, projrank, cost, projname, projsource, projtype, beginyear, endyear):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    if teacherid and projnum:
        check_key_sql = "SELECT COUNT(*) FROM TakeProj WHERE TeacherID = %s AND Projectnum = %s"
        check_key_values = (teacherid, projnum)
        cursor3.execute(check_key_sql, check_key_values)
        count = cursor3.fetchone()[0]
        if count == 0:
            QMessageBox.warning(None, "Error", "数据非法！请检查你的工号和项目号！")
            return
    else:
        check_key_sql = "SELECT COUNT(*) FROM TakeProj WHERE Projectnum = %s"
        check_key_values = (projnum,)
        cursor3.execute(check_key_sql, check_key_values)
        count = cursor3.fetchone()[0]
        if count == 0:
            QMessageBox.warning(None, "Error", "数据非法！请检查你的项目号！")
            return
    if teacherid:
        if projrank != -1:
            check_pubrank_sql = "SELECT COUNT(*) FROM TakeProj WHERE Projectnum = %s AND projrank = %s"
            check_pubrank_values = (projnum, projrank)
            cursor3.execute(check_pubrank_sql, check_pubrank_values)
            count = cursor3.fetchone()[0]
            if count > 0:
                QMessageBox.warning(None, "Error", "承担项目排名不能重复！")
                return
            sql = "UPDATE TakeProj SET projrank = %s WHERE Projectnum = %s AND TeacherID = %s"
            values = (projrank, projnum, teacherid)
            cursor3.execute(sql, values)
        if cost:
            cursor3.execute("SELECT cost FROM TakeProj WHERE Projectnum = %s AND TeacherID = %s", (projnum, teacherid))
            cost_now = cursor3.fetchone()
            cost_delete = cost_now[0]
            cursor3.execute("SELECT * FROM Project WHERE Projectnum = %s", (projnum,))
            project_row = cursor3.fetchone()
            current_budget = project_row[4]
            cost = float(cost)
            updated_budget = current_budget - cost_delete + cost
            sql_update = "UPDATE Project SET budget = %s WHERE Projectnum = %s"
            values = (updated_budget, projnum)
            cursor3.execute(sql_update, values)
            sql_update = "UPDATE TakeProj SET cost = %s WHERE Projectnum = %s AND TeacherID = %s"
            values = (cost, projnum, teacherid)
            cursor3.execute(sql_update, values)

    if projname:
        sql = "UPDATE Project SET projname = %s WHERE Projectnum = %s"
        values = (projname, projnum)
        cursor3.execute(sql, values)
    if projsource:
        sql = "UPDATE Project SET projsource = %s WHERE Projectnum = %s"
        values = (projsource, projnum)
        cursor3.execute(sql, values)
    if projtype:
        sql = "UPDATE Project SET projtype = %s WHERE Projectnum = %s"
        values = (projtype, projnum)
        cursor3.execute(sql, values)
    if beginyear:
        sql = "UPDATE Project SET beginyear = %s WHERE Projectnum = %s"
        values = (beginyear, projnum)
        cursor3.execute(sql, values)
    if endyear:
        sql = "UPDATE Project SET endyear = %s WHERE Projectnum = %s"
        values = (endyear, projnum)
        cursor3.execute(sql, values)

    conn3.commit()
    QMessageBox.information(None, "Success", "更新成功！")
    print("Data updated successfully.")


# 查询数据
def select_project(teacherid, projnum):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    if projnum and not teacherid:
        sql = "SELECT * FROM Project " \
              "INNER JOIN TakeProj ON Project.Projectnum = TakeProj.Projectnum " \
              "INNER JOIN Teacher ON Teacher.ID = TakeProj.TeacherID " \
              "WHERE Project.Projectnum = %s"
        values = (projnum,)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    elif teacherid and not projnum:
        sql = "SELECT * FROM Teacher " \
              "INNER JOIN TakeProj ON Teacher.ID = TakeProj.TeacherID " \
              "INNER JOIN Project ON TakeProj.Projectnum = Project.Projectnum " \
              "WHERE Teacher.ID = %s"
        values = (teacherid,)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    elif teacherid and projnum:
        sql = "SELECT * FROM TakeProj " \
              "INNER JOIN Teacher ON Teacher.ID = TakeProj.TeacherID " \
              "INNER JOIN Project ON TakeProj.Projectnum = Project.Projectnum " \
              "WHERE Teacher.ID = %s AND Project.Projectnum = %s"
        values = (teacherid, projnum)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    else:
        rows = None
    print("Data selected successfully.")
    return rows


class InsertProDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("插入项目")

        layout = QVBoxLayout()

        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("项目号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        paper_name_label = QLabel("项目名称:")
        self.paper_name_input = QLineEdit()
        layout.addWidget(paper_name_label)
        layout.addWidget(self.paper_name_input)

        publisher_label = QLabel("项目来源:")
        self.publisher_input = QLineEdit()
        layout.addWidget(publisher_label)
        layout.addWidget(self.publisher_input)

        publish_type_label = QLabel("项目类型:")
        self.publish_type_input = QComboBox()
        self.publish_type_input.addItem("国家级项目")
        self.publish_type_input.addItem("省部级项目")
        self.publish_type_input.addItem("市厅级项目")
        self.publish_type_input.addItem("企业合作项目")
        self.publish_type_input.addItem("其他类型项目")
        layout.addWidget(publish_type_label)
        layout.addWidget(self.publish_type_input)

        pub_rank_label = QLabel("排名:")
        self.pub_rank_input = QLineEdit()
        layout.addWidget(pub_rank_label)
        layout.addWidget(self.pub_rank_input)

        publish_cost_label = QLabel("承担经费:")
        self.publish_cost_input = QLineEdit()
        layout.addWidget(publish_cost_label)
        layout.addWidget(self.publish_cost_input)

        publish_begin_label = QLabel("开始年份:")
        self.publish_begin_input = QLineEdit()
        layout.addWidget(publish_begin_label)
        layout.addWidget(self.publish_begin_input)

        publish_end_label = QLabel("结束年份:")
        self.publish_end_input = QLineEdit()
        layout.addWidget(publish_end_label)
        layout.addWidget(self.publish_end_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        projnum = self.paper_id_input.text()
        proj_rank = self.pub_rank_input.text()
        projname = self.paper_name_input.text()
        projsource = self.publisher_input.text()
        cost = self.publish_cost_input.text()
        beginyear = self.publish_begin_input.text()
        endyear = self.publish_end_input.text()
        what_type = self.publish_type_input.currentText()

        type_mapping = {"国家级项目": 1, "省部级项目": 2, "市厅级项目": 3, "企业合作项目": 4, "其他类型项目": 5}
        projtype = type_mapping.get(what_type, None)

        if not teacherid or not projnum or not proj_rank or not projname or not projsource or not \
                cost or not beginyear or not endyear or not projtype:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        projrank = int(proj_rank)
        insert_project(teacherid, projnum, projrank, cost, projname, projsource, projtype, beginyear, endyear)
        self.close()


class DeleteProDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("删除项目")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("删除项目承担记录:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("项目号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        layout.addWidget(QLabel("直接删除项目:"))

        paper_label = QLabel("项目号:")
        self.paper_input = QLineEdit()
        layout.addWidget(paper_label)
        layout.addWidget(self.paper_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        projnum = self.paper_id_input.text()
        projnum2 = self.paper_input.text()
        if not teacherid and not projnum and not projnum2:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        if projnum2:
            delete_project2(projnum2)
        else:
            if not teacherid or not projnum:
                QMessageBox.warning(self, "错误的输入", "请输入完整！")
                return
            else:
                delete_project(teacherid, projnum)
        self.close()


class UpdateProDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("更新项目")

        layout = QVBoxLayout()

        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("项目号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        paper_name_label = QLabel("项目名称:")
        self.paper_name_input = QLineEdit()
        layout.addWidget(paper_name_label)
        layout.addWidget(self.paper_name_input)

        publisher_label = QLabel("项目来源:")
        self.publisher_input = QLineEdit()
        layout.addWidget(publisher_label)
        layout.addWidget(self.publisher_input)

        publish_type_label = QLabel("项目类型:")
        self.publish_type_input = QComboBox()
        self.publish_type_input.addItem("国家级项目")
        self.publish_type_input.addItem("省部级项目")
        self.publish_type_input.addItem("市厅级项目")
        self.publish_type_input.addItem("企业合作项目")
        self.publish_type_input.addItem("其他类型项目")
        layout.addWidget(publish_type_label)
        layout.addWidget(self.publish_type_input)

        pub_rank_label = QLabel("排名:")
        self.pub_rank_input = QLineEdit()
        layout.addWidget(pub_rank_label)
        layout.addWidget(self.pub_rank_input)

        publish_cost_label = QLabel("承担经费:")
        self.publish_cost_input = QLineEdit()
        layout.addWidget(publish_cost_label)
        layout.addWidget(self.publish_cost_input)

        publish_begin_label = QLabel("开始年份:")
        self.publish_begin_input = QLineEdit()
        layout.addWidget(publish_begin_label)
        layout.addWidget(self.publish_begin_input)

        publish_end_label = QLabel("结束年份:")
        self.publish_end_input = QLineEdit()
        layout.addWidget(publish_end_label)
        layout.addWidget(self.publish_end_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        projnum = self.paper_id_input.text()
        proj_rank = self.pub_rank_input.text()
        projname = self.paper_name_input.text()
        projsource = self.publisher_input.text()
        cost = self.publish_cost_input.text()
        beginyear = self.publish_begin_input.text()
        endyear = self.publish_end_input.text()
        what_type = self.publish_type_input.currentText()

        type_mapping = {"国家级项目": 1, "省部级项目": 2, "市厅级项目": 3, "企业合作项目": 4, "其他类型项目": 5}
        projtype = type_mapping.get(what_type, None)

        if not projnum:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        if proj_rank:
            projrank = int(proj_rank)
        else:
            projrank = -1
        update_project(teacherid, projnum, projrank, cost, projname, projsource, projtype, beginyear, endyear)
        self.close()


class ResultProDialog(QDialog):
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


class SearchProDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("查询项目")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("按教师工号、项目号或一起查询:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("项目号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        projnum = self.paper_id_input.text()
        if not teacherid and not projnum:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        rows = select_project(teacherid, projnum)
        if not rows:
            QMessageBox.warning(self, "结果", "未找到搜索结果！")
            return
        result_str = ""
        if teacherid and not projnum:
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
                if row[11] == 1:
                    projtype = "国家级项目"
                elif row[11] == 2:
                    projtype = "省部级项目"
                elif row[11] == 3:
                    projtype = "市厅级项目"
                elif row[11] == 4:
                    projtype = "企业合作项目"
                else:
                    projtype = "其他类型项目"
                result_str += f"工号: {row[0]}, 教师姓名: {row[1]}, 教师性别: {tsex}, 教师职称: {title}, " \
                              f"项目号: {row[5]}, 教师排名: {row[6]}, 承担费用: {row[7]}, 项目名称: {row[9]}, " \
                              f"项目来源: {row[10]}, 项目类型: {projtype}, 项目预算: {row[12]}, 起始年份: {row[13]}, 结束年份: {row[14]}\n"
        elif projnum and not teacherid:
            for row in rows:
                if row[13] == 1:
                    tsex = "男"
                else:
                    tsex = "女"
                if row[14] == 1:
                    title = "博士后"
                elif row[14] == 2:
                    title = "助教"
                elif row[14] == 3:
                    title = "讲师"
                elif row[14] == 4:
                    title = "副教授"
                elif row[14] == 5:
                    title = "特任教授"
                else:
                    title = "教授"
                if row[3] == 1:
                    projtype = "国家级项目"
                elif row[3] == 2:
                    projtype = "省部级项目"
                elif row[3] == 3:
                    projtype = "市厅级项目"
                elif row[3] == 4:
                    projtype = "企业合作项目"
                else:
                    projtype = "其他类型项目"
                result_str += f"项目号: {row[0]}, 项目名称: {row[1]}, 项目来源: {row[2]}, 项目类型: {projtype}, " \
                              f"项目预算: {row[4]}, 开始年份: {row[5]}, 结束年份: {row[6]}, 工号: {row[7]}, " \
                              f"教师排名: {row[9]}, 承担费用: {row[10]}, 教师姓名: {row[12]}, 教师性别: {tsex}, 教师职称: {title}\n"
        elif teacherid and projnum:
            for row in rows:
                if row[6] == 1:
                    tsex = "男"
                else:
                    tsex = "女"
                if row[7] == 1:
                    title = "博士后"
                elif row[7] == 2:
                    title = "助教"
                elif row[7] == 3:
                    title = "讲师"
                elif row[7] == 4:
                    title = "副教授"
                elif row[7] == 5:
                    title = "特任教授"
                else:
                    title = "教授"
                if row[11] == 1:
                    projtype = "国家级项目"
                elif row[11] == 2:
                    projtype = "省部级项目"
                elif row[11] == 3:
                    projtype = "市厅级项目"
                elif row[11] == 4:
                    projtype = "企业合作项目"
                else:
                    projtype = "其他类型项目"
                result_str += f"工号: {row[0]}, 项目号: {row[1]}, 教师排名: {row[2]}, 承担费用: {row[3]}, " \
                              f"教师姓名: {row[5]}, 教师性别: {tsex}, 教师职称: {title}, 项目名称: {row[9]}, " \
                              f"项目来源: {row[10]}, 项目类型: {projtype}, 项目预算: {row[12]}, 起始年份: {row[13]}, 结束年份: {row[14]}\n"
        else:
            result_str = ""

        # 显示结果窗口
        dialog = ResultProDialog(result_str)
        dialog.exec_()
        self.close()
