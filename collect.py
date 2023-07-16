import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QLabel, QLineEdit, \
    QMessageBox, QComboBox, QTextEdit
from PyQt5.QtCore import Qt
import mysql.connector
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def select_data(teacherid, year):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()

    sql = "SELECT * FROM Teacher " \
          "JOIN Publication ON Teacher.ID = Publication.TeacherID " \
          "JOIN Paper ON Publication.PaperID = Paper.PaperID AND EXTRACT(YEAR FROM Paper.pubyear) = %s " \
          "WHERE Teacher.ID = %s"
    values = (year, teacherid)
    cursor3.execute(sql, values)
    rows = cursor3.fetchall()
    print("Data selected successfully.")
    return rows


def select_project(teacherid, year):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    sql = "SELECT * FROM Teacher " \
          "JOIN TakeProj ON Teacher.ID = TakeProj.TeacherID " \
          "JOIN Project ON TakeProj.Projectnum = Project.Projectnum AND Project.beginyear = %s " \
          "WHERE Teacher.ID = %s"
    values = (year, teacherid)
    cursor3.execute(sql, values)
    rows = cursor3.fetchall()
    print("Data selected successfully.")
    return rows


def select_class(teacherid, year):
    conn3 = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="lab3"
    )

    # 创建游标对象
    cursor3 = conn3.cursor()
    sql = "SELECT * FROM Teacher " \
          "JOIN TakeCourse ON Teacher.ID = TakeCourse.TeacherID " \
          "JOIN Class ON TakeCourse.Classnum = Class.Classnum AND TakeCourse.teachyear = %s " \
          "WHERE Teacher.ID = %s"
    values = (year, teacherid)
    cursor3.execute(sql, values)
    rows = cursor3.fetchall()
    print("Data selected successfully.")
    return rows


class ResultColDialog(QDialog):
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


def generate_pdf(result_str0, result_str1, result_str2, result_str3, result_str4, result_str5, result_str6, result_str7,
                 height, width, beginyear, endyear):
    # 创建PDF文件
    pdfmetrics.registerFont(TTFont('tencent', 'tencent.TTF'))
    pdf_file = "result.pdf"
    if not height:
        height = 1000
    else:
        height = int(height)
    if not width:
        width = 1000
    else:
        width = int(width)
    pagesize = (width, height)
    c = canvas.Canvas(pdf_file, pagesize=pagesize)
    line_height = 20  # 行高
    y = height - line_height - 50  # 初始纵坐标位置

    result_str = "教师教学工作科研统计（" + str(beginyear) + "-" + str(endyear) + "）\n"
    c.setFont("tencent", 50)
    c.setFillColor(colors.red)
    c.drawString((width - 825) / 2, y, result_str)
    y -= 80

    # 设置字体样式和大小
    c.setFont("tencent", 30)
    c.setFillColor(colors.red)
    c.drawString(50, y, result_str0)
    y -= 30
    c.setFont("tencent", 15)
    c.setFillColor(colors.black)
    # 在PDF中添加文本内容
    for line in result_str1.split("\n"):
        c.drawString(50, y, line)
        y -= line_height

    c.setFont("tencent", 30)
    c.setFillColor(colors.red)
    c.drawString(50, y, result_str2)
    y -= 30
    c.setFont("tencent", 15)
    c.setFillColor(colors.black)
    for line in result_str3.split("\n"):
        c.drawString(50, y, line)
        y -= line_height

    c.setFont("tencent", 30)
    c.setFillColor(colors.red)
    c.drawString(50, y, result_str4)
    y -= 30
    c.setFont("tencent", 15)
    c.setFillColor(colors.black)
    for line in result_str5.split("\n"):
        c.drawString(50, y, line)
        y -= line_height

    c.setFont("tencent", 30)
    c.setFillColor(colors.red)
    c.drawString(50, y, result_str6)
    y -= 30
    c.setFont("tencent", 15)
    c.setFillColor(colors.black)
    for line in result_str7.split("\n"):
        c.drawString(50, y, line)
        y -= line_height
    # 保存并关闭PDF文件
    c.save()
    print(f"PDF生成成功: {pdf_file}")


class SearchColDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("查询项目")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("按教师工号、起止年查询:"))
        teacher_id_label = QLabel("教师工号:")
        self.teacher_id_input = QLineEdit()
        layout.addWidget(teacher_id_label)
        layout.addWidget(self.teacher_id_input)

        paper_begin_label = QLabel("从这一年开始:")
        self.paper_begin_input = QLineEdit()
        layout.addWidget(paper_begin_label)
        layout.addWidget(self.paper_begin_input)

        paper_end_label = QLabel("从这一年结束:")
        self.paper_end_input = QLineEdit()
        layout.addWidget(paper_end_label)
        layout.addWidget(self.paper_end_input)

        paper_height_label = QLabel("生成pdf长度（默认为1000）:")
        self.paper_height_input = QLineEdit()
        layout.addWidget(paper_height_label)
        layout.addWidget(self.paper_height_input)

        paper_width_label = QLabel("生成pdf宽度（默认为1000）:")
        self.paper_width_input = QLineEdit()
        layout.addWidget(paper_width_label)
        layout.addWidget(self.paper_width_input)

        submit_btn = QPushButton("提交")
        submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):
        conn0 = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="lab3"
        )

        # 创建游标对象
        cursor0 = conn0.cursor()
        teacherid = self.teacher_id_input.text()
        beginyear = self.paper_begin_input.text()
        endyear = self.paper_end_input.text()
        height = self.paper_height_input.text()
        width = self.paper_width_input.text()
        if not teacherid or not beginyear or not endyear:
            QMessageBox.warning(self, "错误的输入", "请输入完整！")
            return
        if beginyear > endyear:
            QMessageBox.warning(self, "错误的输入", "输入不合法！")
            return
        result_str = ""
        result_str0 = f"教师信息:\n"
        result_str1 = ""
        cursor0.execute("SELECT * FROM Teacher WHERE ID = %s", (teacherid,))
        row0 = cursor0.fetchone()
        if not row0:
            QMessageBox.warning(self, "错误的输入", "没有找到该老师！")
            return
        if row0[2] == 1:
            tsex = "男"
        else:
            tsex = "女"
        if row0[3] == 1:
            title = "博士后"
        elif row0[3] == 2:
            title = "助教"
        elif row0[3] == 3:
            title = "讲师"
        elif row0[3] == 4:
            title = "副教授"
        elif row0[3] == 5:
            title = "特任教授"
        else:
            title = "教授"
        result_str1 += f"工号: {row0[0]}, 教师姓名: {row0[1]}, 教师性别: {tsex}, 教师职称: {title}\n"

        beginyear = int(beginyear)
        endyear = int(endyear)
        result_str2 = f"发表论文信息:\n"
        result_str3 = ""
        for year in range(beginyear, endyear + 1):
            row10 = select_data(teacherid, year)
            if not row10:
                continue
            for row1 in row10:
                if row1[7] == 0:
                    ifcoauthor = "否"
                else:
                    ifcoauthor = "是"
                if row1[12] == 1:
                    papertype = "full paper"
                elif row1[12] == 2:
                    papertype = "short paper"
                elif row1[12] == 3:
                    papertype = "poster paper"
                else:
                    papertype = "demo paper"
                if row1[13] == 1:
                    paperlevel = "CCF-A"
                elif row1[13] == 2:
                    paperlevel = "CCF-B"
                elif row1[13] == 3:
                    paperlevel = "CCF-C"
                elif row1[13] == 4:
                    paperlevel = "中文CCF-A"
                elif row1[13] == 5:
                    paperlevel = "中文CCF-B"
                else:
                    paperlevel = "无级别"
                result_str3 += f"论文号: {row1[5]}, 教师排名: {row1[6]}, 是否为通讯作者: {ifcoauthor}, 论文名称: {row1[9]}, " \
                               f"发表源: {row1[10]}, 发表时间: {row1[11]}, 论文类型: {papertype}, 论文级别: {paperlevel}\n"

        result_str4 = f"承担项目信息:\n"
        result_str5 = ""
        for year in range(beginyear, endyear + 1):
            row20 = select_project(teacherid, year)
            if not row20:
                continue
            for row2 in row20:
                if row2[11] == 1:
                    projtype = "国家级项目"
                elif row2[11] == 2:
                    projtype = "省部级项目"
                elif row2[11] == 3:
                    projtype = "市厅级项目"
                elif row2[11] == 4:
                    projtype = "企业合作项目"
                else:
                    projtype = "其他类型项目"
                result_str5 += f"项目号: {row2[5]}, 教师排名: {row2[6]}, 承担费用: {row2[7]}, 项目名称: {row2[9]}, " \
                               f"项目来源: {row2[10]}, 项目类型: {projtype}, 项目预算: {row2[12]}, 起始年份: {row2[13]}, 结束年份: {row2[14]}\n"

        result_str6 = f"教授课程信息:\n"
        result_str7 = ""
        for year in range(beginyear, endyear + 1):
            row30 = select_project(teacherid, year)
            if not row30:
                continue
            for row3 in row30:
                if row3[7] == 1:
                    classsem = "春季学期"
                elif row3[7] == 2:
                    classsem = "夏季学期"
                else:
                    classsem = "秋季学期"
                if row3[12] == 1:
                    classtype = "本科生课程"
                else:
                    classtype = "研究生课程"
                result_str7 += f"课程号: {row3[5]}, 教学年份: {row3[6]}, 教学学期: {classsem}, 承担学时: {row3[8]}, " \
                               f"课程名称: {row3[10]}, 课程总学时: {row3[11]}, 课程性质: {classtype}\n"
        result_str = result_str0 + result_str1 + result_str2 + result_str3 + result_str4 + result_str5 + result_str6 + result_str7
        generate_pdf(result_str0, result_str1, result_str2, result_str3, result_str4, result_str5, result_str6,
                     result_str7, height, width, beginyear, endyear)
        # 显示结果窗口
        dialog = ResultColDialog(result_str)
        dialog.exec_()
        self.close()
