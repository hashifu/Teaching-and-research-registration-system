use lab3;

insert into teacher values ('10001', 'Hashifu', 1, 1);
insert into teacher values ('10002', 'jpq', 2, 3);
insert into teacher values ('10003', 'xulinli', 2, 1);
insert into teacher values ('10004', 'nihao', 1, 2);

insert into paper values (1, '第一篇论文', 'lunwen', '2023-11-1', 1, 1);
insert into paper values (2, '第二篇论文', '22222', '1999-10-23', 2, 2);
insert into paper values (3, '3rd', 'XQTD', '2022-1-1', 1, 1);

insert into class values ('MATH1001', '数学分析 1', 120, 1);
insert into class values ('COMP4001', '计算方法 A', 100, 1);
insert into class values ('CS1234', 'ICS A', 80, 1);
insert into class values ('CS1235', 'ICS B', 60, 1);
insert into class values ('CS6666', '软件工程', 60, 2);

insert into project values ('PROJECT-X', 'X', 'MHY', 1, 5000, 2019, 2024);
insert into project values ('TOUHOU', '东方', 'Alice', 2, 1000, 2002, 9999);

insert into publication values ('10001', 1, 1, true);
insert into publication values ('10002', 1, 2, false);
insert into publication values ('10002', 2, 1, false);
insert into publication values ('10001', 2, 2, false);
insert into publication values ('10003', 2, 3, true);
insert into publication values ('10003', 1, 3, false);
insert into publication values ('10001', 3, 1, true);
insert into publication values ('10002', 3, 2, false);
insert into publication values ('10003', 3, 3, false);
insert into publication values ('10004', 1, 4, false);
insert into publication values ('10004', 2, 4, false);
insert into publication values ('10004', 3, 4, false);

insert into TakeCourse values ('10003', 'MATH1001', 2020, 1, 100);
insert into TakeCourse values ('10001', 'MATH1001', 2020, 1, 20);
insert into TakeCourse values ('10002', 'CS1234', 1999, 3, 70);
insert into TakeCourse values ('10003', 'CS1234', 1999, 3, 10);
insert into TakeCourse values ('10002', 'CS1235', 1999, 3, 60);
insert into TakeCourse values ('10002', 'CS6666', 2021, 2, 60);

insert into TakeProj values ('10001', 'PROJECT-X', 1, 1234);
insert into TakeProj values ('10003', 'PROJECT-X', 2, 3766);
insert into TakeProj values ('10002', 'TOUHOU', 1, 999.9);
insert into TakeProj values ('10001', 'TOUHOU', 2, 0.1);