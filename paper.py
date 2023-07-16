import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, \
    QMessageBox, QComboBox, QTextEdit
from PyQt5.QtCore import Qt
import mysql.connector


# 插入数据
def insert_data(teacherid, paperid, papername, publisher, pubyear, pubtype, level, pubrank, iscoauthor):
    conn1 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM Publication WHERE PaperID = %s AND TeacherID = %s", (paperid, teacherid))
    rows = cursor1.fetchall()
    if rows:
        QMessageBox.warning(None, "Error", "已经存在该作者的信息！")
        return
    cursor1.execute("SELECT pubrank, iscoauthor FROM Publication WHERE PaperID = %s", (paperid,))
    rows = cursor1.fetchall()
    for row in rows:
        existing_pub_rank = row[0]
        existing_is_coauthor = row[1]
        if existing_pub_rank == pubrank:
            QMessageBox.warning(None, "Error", "论文作者排名不能重复！")
            return
        if existing_is_coauthor == 1 and iscoauthor == "1":
            QMessageBox.warning(None, "Error", "一篇论文只能有一位通讯作者！")
            return
    cursor1.execute("SELECT ID FROM Teacher WHERE ID = %s", (teacherid,))
    row = cursor1.fetchone()
    if not row:
        QMessageBox.warning(None, "Error", "没有这个老师！")
        return
    cursor1.execute("SELECT PaperID FROM Paper WHERE PaperID = %s", (paperid,))
    if not cursor1.fetchone():
        sql_paper = "INSERT INTO Paper VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            values = (paperid, papername, publisher, pubyear, pubtype, level)
            cursor1.execute(sql_paper, values)
        except:
            QMessageBox.warning(None, "Error", "数据非法！")
            return
    sql = "INSERT INTO Publication VALUES (%s, %s, %s, %s)"
    values = (teacherid, paperid, pubrank, iscoauthor)
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
def delete_data(teacherid, paperid):
    conn2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM Publication WHERE PaperID = %s AND TeacherID = %s", (paperid, teacherid))
    rows = cursor2.fetchall()
    if not rows:
        QMessageBox.warning(None, "Error", "不存在该信息！")
        return
    sql = "DELETE FROM Publication WHERE TeacherID = %s and PaperID = %s"
    values = (teacherid, paperid)
    cursor2.execute(sql, values)
    cursor2.execute("SELECT PaperID FROM Publication WHERE PaperID = %s", (paperid,))
    row = cursor2.fetchone()
    if not row:
        sql = "DELETE FROM Paper WHERE PaperID = %s"
        values = (paperid,)
        cursor2.execute(sql, values)
    conn2.commit()
    QMessageBox.information(None, "Success", "删除成功！")
    print("Data deleted successfully.")


def delete_paper(paperid):
    conn2 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT * FROM Paper WHERE PaperID = %s", (paperid,))
    rows = cursor2.fetchall()
    if not rows:
        QMessageBox.warning(None, "Error", "不存在该信息！")
        return
    sql = "DELETE FROM Paper WHERE PaperID = %s"
    values = (paperid,)
    cursor2.execute(sql, values)
    conn2.commit()
    QMessageBox.information(None, "Success", "删除成功！")
    print("Data deleted successfully.")


# 更新数据
def update_data(teacherid, paperid, papername, publisher, pubyear, pubtype, level, pubrank, iscoauthor):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    if teacherid and paperid:
        check_key_sql = "SELECT COUNT(*) FROM Publication WHERE TeacherID = %s AND PaperID = %s"
        check_key_values = (teacherid, paperid)
        cursor3.execute(check_key_sql, check_key_values)
        count = cursor3.fetchone()[0]
        if count == 0:
            QMessageBox.warning(None, "Error", "数据非法！请检查你的工号和论文序号！")
            return
    else:
        check_key_sql = "SELECT COUNT(*) FROM Publication WHERE PaperID = %s"
        check_key_values = (paperid,)
        cursor3.execute(check_key_sql, check_key_values)
        count = cursor3.fetchone()[0]
        if count == 0:
            QMessageBox.warning(None, "Error", "数据非法！请检查你的论文序号！")
            return
    if teacherid:
        if pubrank != -1:
            check_pubrank_sql = "SELECT COUNT(*) FROM Publication WHERE PaperID = %s AND pubrank = %s"
            check_pubrank_values = (paperid, pubrank)
            cursor3.execute(check_pubrank_sql, check_pubrank_values)
            count = cursor3.fetchone()[0]
            if count > 0:
                QMessageBox.warning(None, "Error", "论文作者排名不能重复！")
                return
            sql = "UPDATE Publication SET pubrank = %s WHERE PaperID = %s AND TeacherID = %s"
            values = (pubrank, paperid, teacherid)
            cursor3.execute(sql, values)

        # 如果修改后的iscoauthor为1，检查相同PaperID但是iscoauthor也为1的记录
        if iscoauthor:
            if iscoauthor == 1:
                check_iscoauthor_sql = "SELECT COUNT(*) FROM Publication WHERE PaperID = %s AND iscoauthor = 1"
                check_iscoauthor_values = (paperid,)
                cursor3.execute(check_iscoauthor_sql, check_iscoauthor_values)
                count = cursor3.fetchone()[0]
                if count > 0:
                    QMessageBox.warning(None, "Error", "一篇论文只能有一位通讯作者！")
                    return
        sql = "UPDATE Publication SET iscoauthor = %s WHERE PaperID = %s AND TeacherID = %s"
        values = (iscoauthor, paperid, teacherid)
        cursor3.execute(sql, values)

    if papername:
        sql = "UPDATE Paper SET papername = %s WHERE PaperID = %s"
        values = (papername, paperid)
        cursor3.execute(sql, values)
    if publisher:
        sql = "UPDATE Paper SET publisher = %s WHERE PaperID = %s"
        values = (publisher, paperid)
        cursor3.execute(sql, values)
    if pubyear:
        sql = "UPDATE Paper SET pubyear = %s WHERE PaperID = %s"
        values = (pubyear, paperid)
        cursor3.execute(sql, values)
    if pubtype:
        sql = "UPDATE Paper SET type = %s WHERE PaperID = %s"
        values = (pubtype, paperid)
        cursor3.execute(sql, values)
    if level:
        sql = "UPDATE Paper SET level = %s WHERE PaperID = %s"
        values = (level, paperid)
        cursor3.execute(sql, values)

    conn3.commit()
    QMessageBox.information(None, "Success", "更新成功！")
    print("Data updated successfully.")


# 查询数据
def select_data(teacherid, paperid):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    if paperid and not teacherid:
        sql = "SELECT * FROM Paper " \
              "INNER JOIN Publication ON Publication.PaperID = Paper.PaperID " \
              "INNER JOIN Teacher ON Teacher.ID = Publication.TeacherID " \
              "WHERE Paper.PaperID = %s"
        values = (paperid,)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    elif teacherid and not paperid:
        sql = "SELECT * FROM Teacher " \
              "INNER JOIN Publication ON Publication.TeacherID = Teacher.ID " \
              "INNER JOIN Paper ON Publication.PaperID = Paper.PaperID " \
              "WHERE Teacher.ID = %s"
        values = (teacherid,)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    elif teacherid and paperid:
        sql = "SELECT * FROM Publication " \
              "INNER JOIN Teacher ON Teacher.ID = Publication.TeacherID " \
              "INNER JOIN Paper ON Publication.PaperID = Paper.PaperID " \
              "WHERE Teacher.ID = %s AND Paper.PaperID = %s"
        values = (teacherid, paperid)
        cursor3.execute(sql, values)
        rows = cursor3.fetchall()
    else:
        rows = None
    print("Data selected successfully.")
    return rows


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("插入论文")

        layout = QVBoxLayout()

        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("论文编号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        paper_name_label = QLabel("论文名称:")
        self.paper_name_input = QLineEdit()
        layout.addWidget(paper_name_label)
        layout.addWidget(self.paper_name_input)

        publisher_label = QLabel("发表源:")
        self.publisher_input = QLineEdit()
        layout.addWidget(publisher_label)
        layout.addWidget(self.publisher_input)

        publish_year_label = QLabel("发表年份（年-月-日）:")
        self.publish_year_input = QLineEdit()
        layout.addWidget(publish_year_label)
        layout.addWidget(self.publish_year_input)

        publish_type_label = QLabel("论文类型:")
        self.publish_type_input = QComboBox()
        self.publish_type_input.addItem("full paper")
        self.publish_type_input.addItem("short paper")
        self.publish_type_input.addItem("poster paper")
        self.publish_type_input.addItem("demo paper")
        layout.addWidget(publish_type_label)
        layout.addWidget(self.publish_type_input)

        publish_level_label = QLabel("论文级别:")
        self.publish_level_input = QComboBox()
        self.publish_level_input.addItem("CCF-A")
        self.publish_level_input.addItem("CCF-B")
        self.publish_level_input.addItem("CCF-C")
        self.publish_level_input.addItem("中文CCF-A")
        self.publish_level_input.addItem("中文CCF-B")
        self.publish_level_input.addItem("其他类型")
        layout.addWidget(publish_level_label)
        layout.addWidget(self.publish_level_input)

        pub_rank_label = QLabel("排名:")
        self.pub_rank_input = QLineEdit()
        layout.addWidget(pub_rank_label)
        layout.addWidget(self.pub_rank_input)

        coauthor_label = QLabel("是否为通讯作者:")
        self.coauthor_input = QComboBox()
        self.coauthor_input.addItem("否")
        self.coauthor_input.addItem("是")
        layout.addWidget(coauthor_label)
        layout.addWidget(self.coauthor_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        paperid = self.paper_id_input.text()
        pub_rank = self.pub_rank_input.text()
        is_coauthor = self.coauthor_input.currentText()
        papername = self.paper_name_input.text()
        publisher = self.publisher_input.text()
        pubyear = self.publish_year_input.text()
        what_type = self.publish_type_input.currentText()
        what_level = self.publish_level_input.currentText()

        coauthor_mapping = {"否": 0, "是": 1}
        iscoauthor = coauthor_mapping.get(is_coauthor, None)
        type_mapping = {"full paper": 1, "short paper": 2, "poster paper": 3, "demo paper": 4}
        pubtype = type_mapping.get(what_type, None)
        level_mapping = {"CCF-A": 1, "CCF-B": 2, "CCF-C": 3, "中文CCF-A": 4, "中文CCF-B": 5, "其他类型": 6}
        level = level_mapping.get(what_level, None)

        if not teacherid or not paperid or not pub_rank or not papername or not publisher or not \
                pubyear or not pubtype or not level:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        pubrank = int(pub_rank)
        insert_data(teacherid, paperid, papername, publisher, pubyear, pubtype, level, pubrank, iscoauthor)
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("删除论文")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("删除论文发表记录:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("论文编号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        layout.addWidget(QLabel("直接删除论文:"))

        paper_label = QLabel("论文编号:")
        self.paper_input = QLineEdit()
        layout.addWidget(paper_label)
        layout.addWidget(self.paper_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        paperid = self.paper_id_input.text()
        paperid2 = self.paper_input.text()
        if not teacherid and not paperid and not paperid2:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        if paperid2:
            delete_paper(paperid2)
        else:
            if not teacherid or not paperid:
                QMessageBox.warning(self, "错误的输入", "请输入完整！")
                return
            else:
                delete_data(teacherid, paperid)
        self.close()


class UpdateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("更新论文")

        layout = QVBoxLayout()

        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("论文编号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        paper_name_label = QLabel("论文名称:")
        self.paper_name_input = QLineEdit()
        layout.addWidget(paper_name_label)
        layout.addWidget(self.paper_name_input)

        publisher_label = QLabel("发表源:")
        self.publisher_input = QLineEdit()
        layout.addWidget(publisher_label)
        layout.addWidget(self.publisher_input)

        publish_year_label = QLabel("发表年份:")
        self.publish_year_input = QLineEdit()
        layout.addWidget(publish_year_label)
        layout.addWidget(self.publish_year_input)

        publish_type_label = QLabel("论文类型:")
        self.publish_type_input = QComboBox()
        self.publish_type_input.addItem("full paper")
        self.publish_type_input.addItem("short paper")
        self.publish_type_input.addItem("poster paper")
        self.publish_type_input.addItem("demo paper")
        layout.addWidget(publish_type_label)
        layout.addWidget(self.publish_type_input)

        publish_level_label = QLabel("论文级别:")
        self.publish_level_input = QComboBox()
        self.publish_level_input.addItem("CCF-A")
        self.publish_level_input.addItem("CCF-B")
        self.publish_level_input.addItem("CCF-C")
        self.publish_level_input.addItem("中文CCF-A")
        self.publish_level_input.addItem("中文CCF-B")
        self.publish_level_input.addItem("其他类型")
        layout.addWidget(publish_level_label)
        layout.addWidget(self.publish_level_input)

        pub_rank_label = QLabel("排名:")
        self.pub_rank_input = QLineEdit()
        layout.addWidget(pub_rank_label)
        layout.addWidget(self.pub_rank_input)

        coauthor_label = QLabel("是否为通讯作者:")
        self.coauthor_input = QComboBox()
        self.coauthor_input.addItem("否")
        self.coauthor_input.addItem("是")
        layout.addWidget(coauthor_label)
        layout.addWidget(self.coauthor_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        paperid = self.paper_id_input.text()
        pub_rank = self.pub_rank_input.text()
        is_coauthor = self.coauthor_input.currentText()
        papername = self.paper_name_input.text()
        publisher = self.publisher_input.text()
        pubyear = self.publish_year_input.text()
        what_type = self.publish_type_input.currentText()
        what_level = self.publish_level_input.currentText()

        coauthor_mapping = {"否": 0, "是": 1}
        iscoauthor = coauthor_mapping.get(is_coauthor, None)
        type_mapping = {"full paper": 1, "short paper": 2, "poster paper": 3, "demo paper": 4}
        pubtype = type_mapping.get(what_type, None)
        level_mapping = {"CCF-A": 1, "CCF-B": 2, "CCF-C": 3, "中文CCF-A": 4, "中文CCF-B": 5, "其他类型": 6}
        level = level_mapping.get(what_level, None)

        if not paperid:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        if pub_rank:
            pubrank = int(pub_rank)
        else:
            pubrank = -1
        update_data(teacherid, paperid, papername, publisher, pubyear, pubtype, level, pubrank, iscoauthor)
        self.close()


class ResultDialog(QDialog):
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


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("查询论文")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("按教师工号、论文编号或一起查询:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_id_label = QLabel("论文编号:")
        self.paper_id_input = QLineEdit()
        layout.addWidget(paper_id_label)
        layout.addWidget(self.paper_id_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        teacherid = self.teacher_id_input.text()
        paperid = self.paper_id_input.text()
        if not teacherid and not paperid:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        rows = select_data(teacherid, paperid)
        if not rows:
            QMessageBox.warning(self, "结果", "未找到搜索结果！")
            return
        result_str = ""
        if paperid and not teacherid:
            for row in rows:
                if row[9] == 0:
                    ifcoauthor = "否"
                else:
                    ifcoauthor = "是"
                if row[12] == 1:
                    tsex = "男"
                else:
                    tsex = "女"
                if row[13] == 1:
                    title = "博士后"
                elif row[13] == 2:
                    title = "助教"
                elif row[13] == 3:
                    title = "讲师"
                elif row[13] == 4:
                    title = "副教授"
                elif row[13] == 5:
                    title = "特任教授"
                else:
                    title = "教授"
                if row[4] == 1:
                    papertype = "full paper"
                elif row[4] == 2:
                    papertype = "short paper"
                elif row[4] == 3:
                    papertype = "poster paper"
                else:
                    papertype = "demo paper"
                if row[5] == 1:
                    paperlevel = "CCF-A"
                elif row[5] == 2:
                    paperlevel = "CCF-B"
                elif row[5] == 3:
                    paperlevel = "CCF-C"
                elif row[5] == 4:
                    paperlevel = "中文CCF-A"
                elif row[5] == 5:
                    paperlevel = "中文CCF-B"
                else:
                    paperlevel = "无级别"
                result_str += f"论文序号: {row[0]}, 论文名称: {row[1]}, 发表源: {row[2]}, 发表日期: {row[3]}, " \
                              f"论文类型: {papertype}, 论文等级: {paperlevel}, 工号: {row[6]}, 教师排名: {row[8]}, " \
                              f"是否为通讯作者: {ifcoauthor}, 教师名称: {row[11]}, 教师性别: {tsex}, 教师职称: {title}\n"
        elif teacherid and not paperid:
            for row in rows:
                if row[7] == 0:
                    ifcoauthor = "否"
                else:
                    ifcoauthor = "是"
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
                if row[12] == 1:
                    papertype = "full paper"
                elif row[12] == 2:
                    papertype = "short paper"
                elif row[12] == 3:
                    papertype = "poster paper"
                else:
                    papertype = "demo paper"
                if row[13] == 1:
                    paperlevel = "CCF-A"
                elif row[13] == 2:
                    paperlevel = "CCF-B"
                elif row[13] == 3:
                    paperlevel = "CCF-C"
                elif row[13] == 4:
                    paperlevel = "中文CCF-A"
                elif row[13] == 5:
                    paperlevel = "中文CCF-B"
                else:
                    paperlevel = "无级别"
                result_str += f"工号: {row[0]}, 教师名称: {row[1]}, 教师性别: {tsex}, 教师职称: {title}, " \
                              f"论文序号: {row[5]}, 在该论文中的排名: {row[6]}, 是否为通讯作者: {ifcoauthor}, 论文名称: {row[9]}, " \
                              f"发表源: {row[10]}, 发表日期: {row[11]}, 论文类型: {papertype}, 论文等级: {paperlevel}\n"
        elif teacherid and paperid:
            for row in rows:
                if row[3] == 0:
                    ifcoauthor = "否"
                else:
                    ifcoauthor = "是"
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
                    papertype = "full paper"
                elif row[11] == 2:
                    papertype = "short paper"
                elif row[11] == 3:
                    papertype = "poster paper"
                else:
                    papertype = "demo paper"
                if row[12] == 1:
                    paperlevel = "CCF-A"
                elif row[12] == 2:
                    paperlevel = "CCF-B"
                elif row[12] == 3:
                    paperlevel = "CCF-C"
                elif row[12] == 4:
                    paperlevel = "中文CCF-A"
                elif row[12] == 5:
                    paperlevel = "中文CCF-B"
                else:
                    paperlevel = "无级别"
                result_str += f"工号: {row[0]}, 论文序号: {row[1]}, 在该论文中的排名: {row[2]}, 是否为通讯作者: {ifcoauthor}, " \
                              f"教师姓名: {row[5]}, 教师性别: {tsex}, 教师职称: {title}, 论文名称: {row[9]}, " \
                              f"发表日期: {row[10]}, 论文类型: {papertype}, 论文等级: {paperlevel}\n"
        else:
            result_str = ""

        # 显示结果窗口
        dialog = ResultDialog(result_str)
        dialog.exec_()
        self.close()
