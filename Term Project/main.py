import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import mysql.connector

import User

form_class = uic.loadUiType("main.ui")[0]
user_menu=uic.loadUiType("usermenu.ui")[0]
manager_menu=uic.loadUiType("managermenu.ui")[0]
game_list=uic.loadUiType("gamelist.ui")[0]

conn = mysql.connector.connect( #접속 정보
            host="192.168.56.101",#ip
            port="4567",#포트
            user="leejm",#사용자명
            passwd="1234",#비밀번호
            database="term"#데이터베이스
        )

cur=conn.cursor()#cursor 객체 생성

class ManagerMenu(QDialog,QWidget,manager_menu):
    def __init__(self):
        super(ManagerMenu,self).__init__()
        self.setupUi(self)

        self.add.clicked.connect(self.gameAdd)
        self.remove.clicked.connect(self.gameRemove)
        self.update.clicked.connect(self.gameUpdate)


class GameList(QDialog,QWidget,game_list):
    def __init__(self):
        super(GameList,self).__init__()
        self.setupUi(self)

        gname=self.gamename.text()
        developer=self.developer.text()
        minprice=self.minprice.text()
        maxprice=self.maxprice.text()
        sql="select name from GAME;"
        cur.execute(sql)
        result=cur.fetchall()
        for i in result:
            self.gerne.addItem(i[0])
        

        


class UserMenu(QDialog,QWidget,user_menu):
    def __init__(self):
        super(UserMenu,self).__init__()
        self.setupUi(self)

        self.find.clicked.connect(self.findGame)
        #self.recommand.clicked.connect(self.recommandGame)
        #self.info.clicked.connect(self.info)

    def findGame(self):
        self.hide()
        self.gamelist=GameList()
        self.gamelist.exec()
    
    def recommandGame(self):
        pass

    def info(self):
        pass

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.login.clicked.connect(self.loginFunc)
        self.sign.clicked.connect(self.signFunc)


        

    def loginFunc(self):
        id=self.idbox.text()
        password=self.passwdbox.text()

        sql="select *,count(*) from USER where id=%s and password=%s;"
        val=[id,password]
        cur.execute(sql,val)
        result=cur.fetchall()
        if result[0][7]==1:
            user=User.User(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6])
            if(user.type=='u'):
                self.hide()
                self.usermenu=UserMenu()
                self.usermenu.exec()
            else:
                self.hide()
                self.managermenu=ManagerMenu()
                self.managermenu.exec()


        

    def signFunc(self):
        pass


if __name__ == "__main__" :
    
    app = QApplication(sys.argv) 

    myWindow = WindowClass() 

    myWindow.show()

    app.exec_()