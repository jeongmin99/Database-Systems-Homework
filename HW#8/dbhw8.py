import mysql.connector

conn = mysql.connector.connect( #접속 정보
    host="192.168.56.101",#ip
    port="4567",#포트
    user="leejm",#사용자명
    passwd="1234",#비밀번호
    database="madang"#데이터베이스
)

cur=conn.cursor()#cursor 객체 생성

def insert_Book():#insert 함수
    bookid=input("bookid: ") #bookid 입력
    bookname=input("bookname: ") #bookname 입력
    publisher=input("publisher: ")#publisher 입력
    price=input("price: ")#price 입력


    sql="INSERT INTO Book VALUES (%s,%s,%s,%s);" #데이터 삽입 sql문
    val=(bookid,bookname,publisher,price) #입력값을 튜플로
    cur.execute(sql,val)#쿼리 실행
    conn.commit()#commit
    

def delete_Book(): #delete 함수
    bookid=input("bookid: ") #bookid 입력
    bookname=input("bookname: ") #bookname 입력
    publisher=input("publisher: ")#publisher 입력
    price=input("price: ")#price 입력

    sql="DELETE FROM Book" #sql 쿼리
    val=[] # 입력값 리스트 초기화

    """각 condition 별 연결할 문자열 초기화"""
    bid="" 
    bn=""
    pub=""
    pr=""

    """입력한 condition에 따른 문자열 생성 및 입력값 저장"""
    if bookid!="":
        val.append(bookid)
        bid=" bookid=%s,"
    if bookname!="":
        val.append(bookname)
        bn=" bookname=%s,"
    if publisher!="":
        val.append(publisher)
        pub=" publisher=%s,"
    if price!="":
        val.append(price)
        pr=" price=%s,"


    val=tuple(val)#튜플로 타입 캐스팅

    if len(val)!=0:#입력값이 하나라도 있으면
        sql+=" WHERE"#where 절 추가
        sql=sql+bid+bn+pub+pr#입력한 문자열 연결
        sql=sql[:-1]#마지막 , 제거
    
    sql+=";"# ; 연결
    print(sql)#sql문 출력
    cur.execute(sql,val)#쿼리 실행
    conn.commit()#commit

def select_Book():#select 함수
    bookid=input("bookid: ") #bookid 입력
    bookname=input("bookname: ") #bookname 입력
    publisher=input("publisher: ")#publisher 입력
    price=input("price: ")#price 입력

    sql="SELECT * FROM Book" #sql 쿼리
    val=[] #입력값 리스트 초기화

    """각 condition 별 연결할 문자열 초기화"""
    bid=""
    bn=""
    pub=""
    pr=""

    """입력한 condition에 따른 문자열 생성 및 입력값 저장"""
    if bookid!="":
        val.append(bookid)
        bid=" bookid=%s,"
    if bookname!="":
        val.append(bookname)
        bn=" bookname=%s,"
    if publisher!="":
        val.append(publisher)
        pub=" publisher=%s,"
    if price!="":
        val.append(price)
        pr=" price=%s,"

    val=tuple(val)#튜플로 형변환

    if len(val)!=0:#입력값이 하나라도 있으면
        sql+=" WHERE"#where 절 추가
        sql=sql+bid+bn+pub+pr#입력한 문자열 연결
        sql=sql[:-1]#마지막 , 제거
    
    sql+=";" #; 연결
    print(sql)#sql문 출력
    cur.execute(sql,val)#쿼리 실행
    result=cur.fetchall()#결과 가져오기

    for i in result:#결과 출력
        print(i)
    



while True:
    menu=int(input("insert: 1, delete: 2, select: 3 ==>"))#메뉴 선택

    if menu==1:
        insert_Book()
    elif menu==2:
        delete_Book()
    elif menu==3:
        select_Book()
    else:
        break

    conn.close()#접속 종료



