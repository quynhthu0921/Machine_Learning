import mysql.connector

server = "localhost"
port = 3306
database = "studentmanagement"
username = "root"
password = "@Obama123"

conn = mysql.connector.connect(
    host=server,
    port=port,
    database=database,
    user=username,
    password=password,
    use_pure=True
)

cursor = conn.cursor()

# Truy vấn toàn bộ Sinh viên
sql = "select * from student"
cursor.execute(sql)
dataset = cursor.fetchall()

align = '{0:<3} {1:<6} {2:<15} {3:<10}'
print(align.format('ID', 'Code', 'Name', "Age"))
for item in dataset:
    print(align.format(item[0], item[1], item[2], item[3]))

cursor.close()

# Truy vấn các Sinh viên có độ tuổi từ 22 tới 26
sql = "SELECT * FROM student WHERE Age >= 22 AND Age <= 26"
cursor.execute(sql)
dataset = cursor.fetchall()

print("\nSinh viên có Age từ 22-26:")
print(align.format('ID', 'Code', 'Name', "Age"))
for item in dataset:
    print(align.format(item[0], item[1], item[2], item[3]))

cursor.close()

# Truy vấn toàn bộ sinh viên và sắp xếp theo tuổi tăng dần
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "order by Age asc"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print("\nSinh viên có Age tăng dần:")
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

# Truy vấn các Sinh viên có độ tuổi từ 22 tới 26 và sắp xếp theo tuổi giảm dần
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "where Age>=22 and Age<=26 " \
    "order by Age desc "
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print("\nSinh viên có Age từ 22-26 và giảm dần:")
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

# Truy vấn chi tiết thông tin Sinh viên khi biết Id
cursor = conn.cursor()
sql="SELECT * FROM student " \
    "where ID=1 "

cursor.execute(sql)

dataset=cursor.fetchone()
if dataset!=None:
    id,code,name,age,avatar,intro=dataset
    print("\nSinh viên khi biết ID=1:")
    print("Id=",id)
    print("code=",code)
    print("name=",name)
    print("age=",age)

cursor.close()

# Truy vấn dạng phân trang Student
cursor = conn.cursor()
sql="SELECT * FROM student LIMIT 3 OFFSET 0"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print("\n")
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

cursor = conn.cursor()
sql="SELECT * FROM student LIMIT 3 OFFSET 3"
cursor.execute(sql)

dataset=cursor.fetchall()
align='{0:<3} {1:<6} {2:<15} {3:<10}'
print("\n")
print(align.format('ID', 'Code','Name',"Age"))
for item in dataset:
    id=item[0]
    code=item[1]
    name=item[2]
    age=item[3]
    avatar=item[4]
    intro=item[5]
    print(align.format(id,code,name,age))

cursor.close()

print("\PAGING!!!!!")
cursor = conn.cursor()
sql="SELECT count(*) FROM student"
cursor.execute(sql)
dataset=cursor.fetchone()
rowcount=dataset[0]

limit=3
step=3
for offset in range(0,rowcount,step):
    sql=f"SELECT * FROM student LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql)

    dataset=cursor.fetchall()
    align='{0:<3} {1:<6} {2:<15} {3:<10}'
    print(align.format('ID', 'Code','Name',"Age"))
    for item in dataset:
        id=item[0]
        code=item[1]
        name=item[2]
        age=item[3]
        avatar=item[4]
        intro=item[5]
        print(align.format(id,code,name,age))

cursor.close()

# Thêm mới 1 Student
cursor = conn.cursor()

sql="insert into student (code,name,age) values (%s,%s,%s)"

val=("sv07","Trần Duy Thanh",45)

cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()

# Thêm mới nhiều Student
cursor = conn.cursor()

sql="insert into student (code,name,age) values (%s,%s,%s)"

val=[
    ("sv08","Trần Quyết Chiến",19),
    ("sv09","Hồ Thắng",22),
    ("sv10","Hoàng Hà",25),
     ]

cursor.executemany(sql,val)

conn.commit()

print(cursor.rowcount," record inserted")

cursor.close()

# Cập nhật tên Sinh viên có Code=’sv09′ thành tên mới “Hoàng Lão Tà”
cursor = conn.cursor()
sql="update student set name='Hoàng Lão Tà' where Code='sv09'"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")

# Cập nhật tên Sinh viên có Code=’sv09′ thành tên mới “Hoàng Lão Tà” như viết dạng SQL Injection:
cursor = conn.cursor()
sql="update student set name=%s where Code=%s"
val=('Hoàng Lão Tà','sv09')

cursor.execute(sql,val)

conn.commit()

print(cursor.rowcount," record(s) affected")

# Xóa Student có ID=14
conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
cursor = conn.cursor()
sql="DELETE from student where ID=14"
cursor.execute(sql)

conn.commit()

print(cursor.rowcount," record(s) affected")

# Xóa Student có ID=13 với SQL Injection
conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
cursor = conn.cursor()
sql = "DELETE from student where ID=%s"
val = (13,)

cursor.execute(sql, val)

conn.commit()

print(cursor.rowcount," record(s) affected")