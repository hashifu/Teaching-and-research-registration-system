# 面向教师的教学科研登记系统

## 1.1    系统目标

开发一个面向教师的教学科研登记系统

## 1.2 需求说明

登记发表论文情况：提供教师论文发表信息的的增、删、改、查功能；输入时要求检 查：一篇论文只能有一位通讯作者，论文的作者排名不能有重复，论文的类型和级别只 能在约定的取值集合中选取（实现时建议用下拉框）。 

登记承担项目情况：提供教师承担项目信息的增、删、改、查功能；输入时要求检查： 排名不能有重复，一个项目中所有教师的承担经费总额应等于项目的总经费，项目类型 只能在约定的取值集合中选取。 

登记主讲课程情况：提供教师主讲课程信息的增、删、改、查功能；输入时要求检查： 一门课程所有教师的主讲学时总额应等于课程的总学时，学期。

查询统计： 

**1.**实现按教师工号和给定年份范围汇总查询该教师的教学科研情况的功能；例如输入工号“01234”，“2023-2023”可以查询 01234 教师在 2023 年度的教学科研工 作情况。 

**2.**实现按教师工号和给定年份范围生成教学科研工作量统计表并导出文档的功能，导出文档格式可以是 PDF、Word、Excel 等。

## 1.3 本报告的主要贡献

​    说明本次实验的主要内容以及是如何实现实验要求的主要功能的

# 2 总体设计

## 2.1 系统模块结构

​    系统共分为五个模块，共分为主函数、控制论文的函数、控制项目的函数、控制课程的函数、实现查询统计的函数。

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)

## 2.2 系统工作流程

​    系统首先使用主函数建立最开始的交互界面，然后通过点击主函数中的各个按键来调用不同的子函数，从而实现不同的功能

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image004.jpg) 

## 2.3 数据库设计

​    数据库的ER图于实验说明PDF上的基本保持一致

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image006.jpg)

其中，发表论文的数据库采用工号和论文序号作为主键和外键且分别引用了论文的序号和教师的工号

承担项目的数据库采用工号和项目号作为主键和外键且分别引用了项目的项目号和教师的工号

主讲课程的数据库采用工号和课程号作为主键和外键且分别引用了课程的课程号和教师的工号

 

# 3 详细设计【可选】

## 3.1 主函数模块（lab3.py）

​    该模块负责将所有的其他模块串联起来，此模块没有输入也没有输出，主要是负责提供主界面来进行后续操作：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

​    流程图为：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image010.jpg)

## 3.2 控制教师发表论文模块（paper.py）

​    该模块主要有四个功能，分别实现发表论文的增删改查

​    增添数据时需要输入论文的全部属性和教师排名和是否为通讯作者，需要满足实验提供的约束条件

​    删除数据时需要输入论文号和教师号（删除该教师发表论文的记录），或者只输入论文号（删除该论文的全部记录）

​    更新数据时必须输入论文号，可以输入教师工号，输入教师工号则可以修改教师排名和是否为通讯作者（要满足约束），否则可以修改论文的记录

​    查询模块可以按照论文来查也可以按照论文号和教师工号一起查，然后输出的是论文数据和编写论文的老师的数据

流程图如下：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image012.jpg)

## 3.3  控制教师承担项目模块

​    该模块主要有四个功能，分别实现承担项目的增删改查

​    增添数据时需要输入项目的全部属性和教师排名和承担经费，需要满足实验提供的约束条件，此时对应的项目总经费会加上该教师承担的那部分经费

​    删除数据时需要输入项目号和教师号（删除该教师承担项目的记录，项目总经费会跟着修改），或者只输入项目号（删除该项目的全部记录）

​    更新数据时必须输入项目号，可以输入教师工号，输入教师工号则可以修改教师排名和承担经费（同时总经费也会跟着修改），否则可以修改项目的记录（总经费不可修改）

​    查询模块可以按照项目来查也可以按照项目号和教师工号一起查，然后输出的是项目数据和承担项目的老师的数据

流程图如下：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image014.jpg)

// 给出该模块的输入、输出和程序流程图。

## 3.4  控制教师教授课程模块

该模块主要有四个功能，分别实现教授课程的增删改查

​    增添数据时需要输入课程的全部属性和教师的主讲年份、主讲学期和承担学时，需要满足实验提供的约束条件，此时对应的课程总学时会加上该教师教授的那部分学时

​    删除数据时需要输入课程号和教师号（删除该教师教授课程的记录，课程总承担学时会跟着修改），或者只输入课程号（删除该课程的全部记录）

​    更新数据时必须输入课程号，可以输入教师工号，输入教师工号则可以修改教师的主讲年份、主讲学期和承担学时（同时总学时也会跟着修改），否则可以修改课程的记录（总学时不可修改）

​    查询模块可以按照课程来查也可以按照课程号和教师工号一起查，然后输出的是课程数据和教授课程的老师的数据

流程图如下：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image016.jpg)

## 3.5  查询统计模块

该模块仅有查询统计这一个功能

  查询时需要输入教师的工号和查询起始年份和终止年份，程序会根据你输入的起始年份和终止年份查询教师在这期间的所有活动，输出所有查找过的数据并且会生成一个pdf文件。同时为了更好的生成pdf文件，我们提供用户可以自定义输出的pdf的长宽，默认为1000 * 1000

流程图如下：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image018.jpg)

# 4 实现与测试

## 4.1 实现结果

首先是初始界面：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image020.jpg)

添加界面（由于各个功能的增删改查界面几乎一致，这里只演示发表论文部分，下同）：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image022.jpg)

删除页面：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image024.jpg)

修改页面：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image026.jpg)

查询页面：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image028.jpg)

查询统计页面：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image030.jpg)

## 4.2 测试结果

测试时首先在数据库中增加了几条初始数据

首先给10001的老师增添一条论文数据：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image032.jpg)

再查询其所有论文，发现确实已经有了这条记录：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image034.jpg)

试着更改一下论文2的名字然后删除论文1，再进行查询：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image036.jpg) ![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image038.jpg)

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image040.jpg)

为10001添加一个新的承担项目：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image042.jpg)

查询其所有承担项目：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image044.jpg)

修改10001在“TOUHOU”中承担的经费，然后删除PROJECT-X项目，再查找TOUHOU：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image046.jpg) ![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image048.jpg)

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image050.jpg)

为10001在添加一个新课：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image052.jpg)

查询其所有授课记录：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image054.jpg)

删除刚才添加的课程，然后将10001在数学分析1的承担学时改为2，然后查询数学分析1：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image056.jpg) ![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image058.jpg)

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image060.jpg)

最最后，我们对10001的1998年~2023年的所有成就查询一下，并设置输出pdf画框宽度为2000，高度仍为默认：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image062.jpg)

输出的可视查询窗口：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image064.jpg)

输出的pdf：

![img](file:///C:/Users/Hashifu/AppData/Local/Temp/msohtmlclip1/01/clip_image066.jpg)

综上所述，都很好的满足了实验的要求。

## 4.3 实现中的难点问题及解决【可选】

1.问题描述：在输出pdf文件时不知道该怎么输出

2.难点分析：选择合适的输出pdf的字体和效果

3.已有方法的局限性：使用了canvas库，但是该库仅支持英文输出，中文输出时便会输出一些黑块。

4.我采取的方法：下载了一个新的支持中文的字体并且在运行canvas之前先注册该字体，然后就可以输出了。

5.实现效果：参考前一部分的输出pdf的样式，我通过这样不仅做到了可以改变字体、大小、间距、还可以改变画框的大小

# 5 总结与讨论

​    本次实验当中，我们主要学习了数据库访问编程，将数据库与python代码联系了起来，并且第一次学会使用QT这一工具实现了C/S架构的编写，学会了使用canvas输出pdf，对数据库访问编程有了进一步的认识，也学会了如何将前端与数据库进行连接，同时也增强了我编写python代码的本领。但是本次实验当中仍然存在一些过分依赖前端的问题，许多诸如通讯作者仅有一位以及排名不能重复的问题我都是通过前端python代码部分来实现规避，这可能会导致数据库安全性的问题，同时由于是第一次使用QT，因此交互界面也设计的比较简陋，这也是打磨时间不够长造成的。