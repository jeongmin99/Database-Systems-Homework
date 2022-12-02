import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import mysql.connector

import User

form_class = uic.loadUiType("main.ui")[0]
user_menu=uic.loadUiType("usermenu.ui")[0]
manager_menu=uic.loadUiType("managermenu.ui")[0]
game_list=uic.loadUiType("gamelist.ui")[0]
game_info=uic.loadUiType("gameinfo.ui")[0]
charge_warn=uic.loadUiType("chargewarn.ui")[0]
already_warn=uic.loadUiType("alreadywarn.ui")[0]
sign_class=uic.loadUiType("signclass.ui")[0]
same_id=uic.loadUiType("sameid.ui")[0]
sign_warn=uic.loadUiType("signwarn.ui")[0]
login_fail=uic.loadUiType("loginfail.ui")[0]
user_info=uic.loadUiType("userinfo.ui")[0]

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

class GameInfo(QDialog,QWidget,game_info):
     def __init__(self,gname,developer,released_date):
        super(GameInfo,self).__init__()
        self.setupUi(self)
        self.gnamev=gname
        self.developerv=developer
        self.released_datev=released_date
        self.distributorv=''
        self.pricev=''
        self.age_ratingv=''
        self.sizesv=''
        self.processorv=''
        self.memoryv=''
        self.graphicv=''
        self.storage_spacev=''
        self.directxv=''
        self.gernev=[]
        self.osv=[]
        self.considerv=[]
        self.setInfo()

     def setInfo(self):
        sql="select * from GAME where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)
        result=cur.fetchall()
        for i in result:
            self.distributorv=i[2]
            self.pricev=i[4]
            self.age_ratingv=i[5]
            self.sizesv=i[6]
            self.processorv=i[7]
            self.memoryv=i[8]
            self.graphicv=i[9]
            self.storage_spacev=i[10]
            self.directxv=''
            

        
        sql="select Gerne from GAME_GERNE where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)
        result=cur.fetchall()
        for i in result:
            self.gernev.append(i[0])

        sql="select OS from GAME_SYSTEM_REQUIREMENTS_OS where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)
        result=cur.fetchall()
        for i in result:
            self.osv.append(i[0])

        sql="select  rating_consideration from GAME_RATING_CONSIDERATIONS where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)
        result=cur.fetchall()
        for i in result:
            self.considerv.append(i[0])

        sql="select directx from GAME_GRAPHIC where graphic=%s;"
        print(self.graphicv)
        cur.execute(sql,(self.graphicv,))
        result=cur.fetchall()
        for i in result:
            self.directxv=i[0]   

        self.gname.setText(self.gnamev)
        self.developer.setText(self.developerv)
        self.distributor.setText(self.distributorv)
        self.released_date.setText(str(self.released_datev))
        self.price.setText(str(self.pricev))
        self.age.setText(str(self.age_ratingv))
        self.processor.setText(self.processorv)
        self.memory.setText(str(self.memoryv))
        self.graphic.setText(self.graphicv)
        self.sizes.setText(str(self.sizesv))
        self.storage.setText(str(self.storage_spacev))
        self.directx.setText(self.directxv)


        ger=''
        for i in self.gernev:
            ger+=i+", "
        ger=ger[:-2]
        self.gerne.setText(ger)

        o=''
        for i in self.osv:
            o+=i+", "
        o=o[:-2]
        self.os.setText(o)

        con=''
        for i in self.considerv:
            con+=i+", "
        con=con[:-2]
        self.consider.setText(con)

        self.buy.clicked.connect(self.BuyGame)
        
     def BuyGame(self):
        if int(user.charge) < int(self.pricev):
            warn=ChargeWarn()
            warn.exec()
        
        else:
            sql="select count(*) from BUYS where Uid=%s and Gname=%s and developer=%s and released_date=%s;"
            val=[user.id,self.gnamev,self.developerv,self.released_datev]
            cur.execute(sql,val)
            result=cur.fetchall()
            print(result[0][0])
            if result[0][0] >=1:
                warn=AlreadyWarn()
                warn.exec()
                

            else:
                sql="insert into BUYS values (%s,%s,%s,%s);"
                val=[user.id,self.gnamev,self.developerv,self.released_datev]
                print(val)
                cur.execute(sql,val)

                
                sql="update USER set charge=(%s-%s) where id=%s;"
                val=[int(user.charge),int(self.pricev),user.id]
                cur.execute(sql,val)
                conn.commit()
                
            

class AlreadyWarn(QDialog,QWidget,already_warn):
    def __init__(self):
        super(AlreadyWarn,self).__init__()
        self.setupUi(self)
class ChargeWarn(QDialog,QWidget,charge_warn):
    def __init__(self):
        super(ChargeWarn,self).__init__()
        self.setupUi(self)

class GameList(QDialog,QWidget,game_list):
    def __init__(self):
        super(GameList,self).__init__()
        self.setupUi(self)
        
        self.res=''
        sql="select distinct Gerne from GAME_GERNE;"
        cur.execute(sql)
        result=cur.fetchall()
        self.gerne.addItem('')
        for i in result:
            self.gerne.addItem(str(i[0]))
        
        sql="select distinct age_rating from GAME;"
        cur.execute(sql)
        result=cur.fetchall()
        self.age.addItem('')
        for i in result:
            self.age.addItem(str(i[0]))

        
        self.search.clicked.connect(self.Searching)
    

    def Searching(self):
        sql="select * from GAME natural join GAME_GERNE"
        val=[]
        st=" where GAME.Gname=GAME_GERNE.Gname and"
        sql+=st
        stri=""
       
        gname=self.gamename.text()
        developer=self.developer.text()
        minprice=self.minprice.text()
        maxprice=self.maxprice.text()
        gerne=self.gerne.currentText()
        age=self.age.currentText()

        if gname!='':
            val.append(gname)
            stri+=" Gname=%s and"
        if gerne!='':
            val.append(gerne)
            stri+=" Gerne=%s and"
        if developer!='':
            val.append(developer)
            stri+=" developer=%s and"
        if minprice!='':
            val.append(int(minprice))
        else:
            val.append(0)
        if maxprice!='':
            val.append(int(maxprice))
        else:
            val.append(999999999)
        
        sql+=stri

        stri=" price >= %s and price <= %s and"
        if age!="":
            val.append(int(age))
            stri+=" age_rating=%s and"
        
        sql+=stri[:len(stri)-4]
        sql+=";"
        print(sql)
        print(val)
        cur.execute(sql,val)
        self.res=cur.fetchall()

       
        self.table.setRowCount(len(self.res))
        self.table.setColumnCount(5)
     
        index=[0,1,2,5,4]
        for row in self.res:
            for i in range(0,len(self.res)):
                k=0
                for j in index:
                    self.table.setItem(i,k,QTableWidgetItem(str(self.res[i][j])))
                    k=k+1
        
        self.selectGame()

    def selectGame(self):
        num=self.table.currentRow()
        self.table.cellDoubleClicked.connect(lambda: self.gameinfo(self.res[num][0],self.res[num][1],self.res[num][2]))
           
        

        
        

    def gameinfo(self,gn,dv,rd):
        gname=gn
        developer=dv
        released_date=rd
        self.Gameinfo=GameInfo(gname,developer,released_date)
        self.Gameinfo.exec()


class UserMenu(QDialog,QWidget,user_menu):
    def __init__(self):
        super(UserMenu,self).__init__()
        self.setupUi(self)

        self.find.clicked.connect(self.findGame)
        #self.recommand.clicked.connect(self.recommandGame)
        self.info.clicked.connect(self.infod)

    def findGame(self):
        self.gamelist=GameList()
        self.gamelist.exec()
    
    def recommandGame(self):
        pass

    def infod(self):
        self.info=UserInfo()
        self.info.exec()

class UserInfo(QDialog,QWidget,user_info):
    def __init__(self) :
        super(UserInfo,self).__init__()
        self.setupUi(self)

        self.idtext.setText(user.id)
        self.typetext.setText(user.type)
        self.nametext.setText(user.name)
        self.agetext.setText(str(user.age))
        self.chargetext.setText(str(user.charge))
        self.mod.clicked.connect(self.modify)
    
    def modify(self):
        sql="update USER set password=%s and name=%s and age=%s and charge=%s;"
        val=[self.pwtext.text(),self.nametext.text(),self.agetext.text(),self.chargetext.text()]
        if '' in val:
            sw=SignWarn()
            sw.exec()
        else:
            val[2]=int(val[2])
            val[3]=int(val[3])
            cur.execute(sql,val)
            conn.commit()
        

class signClass(QDialog,QWidget,sign_class):
    def __init__(self) :
        super(signClass,self).__init__()
        self.setupUi(self)

        

        self.signbutton.clicked.connect(self.goSign)

        

    def goSign(self):

        self.id=self.idtext.text()
        self.pw=self.pwtext.text()
        self.name=self.nametext.text()
        if self.typebox.currentText()=="일반 사용자":
            self.type='u'
        else:
            self.type='m'
        
        if self.genderbox.currentText()=="남자":
            self.gender='m'
        else:
            self.gender='f'
        
        self.age=self.agetext.text()
        self.charge=self.chargetext.text()
        sql="select count(*) from USER where id=%s;"
        val=(self.id,)
        cur.execute(sql,val)
        result=cur.fetchall()

        if result[0][0]>0:
            self.same=SameId()
            self.same.exec()

        else:

            sql="insert into USER value (%s,%s,%s,%s,%s,%s,%s)"
            val=[self.id,self.pw,self.name,self.type,self.gender,self.age,self.charge]
            if '' in val:
                warn=SignWarn()
                warn.exec()

            else:
                val[5]=int(val[5])
                val[6]=int(val[6])
                cur.execute(sql,val)
                conn.commit()
                self.hide() 

class SignWarn(QDialog,QWidget,sign_warn):
    def __init__(self) :
        super(SignWarn,self).__init__()
        self.setupUi(self)
class SameId(QDialog,QWidget,same_id):
    def __init__(self) :
        super(SameId,self).__init__()
        self.setupUi(self)

class loginFail(QDialog,QWidget,login_fail):
    def __init__(self) :
        super(loginFail,self).__init__()
        self.setupUi(self)

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        
        self.login.clicked.connect(self.loginFunc)
        self.sign.clicked.connect(self.signFunc)


        

    def loginFunc(self):
        id=self.idbox.text()
        password=self.passwdbox.text()
        global user
        sql="select *,count(*) from USER where id=%s and password=%s;"
        val=[id,password]
        cur.execute(sql,val)
        result=cur.fetchall()

        if result[0][7]==1:
            user = User.User(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6])
            if(user.type=='u'):
                self.hide()
                self.usermenu=UserMenu()
                self.usermenu.exec()
            else:
                self.hide()
                self.managermenu=ManagerMenu()
                self.managermenu.exec()
        else:
            loginfail=loginFail()
            loginfail.exec()

        

    def signFunc(self):
        self.hide()
        sign=signClass()
        sign.exec()
        self.show()


if __name__ == "__main__" :
    
    app = QApplication(sys.argv) 

    myWindow = WindowClass() 

    myWindow.show()

    app.exec_()