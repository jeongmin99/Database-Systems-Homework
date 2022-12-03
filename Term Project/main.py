import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

import mysql.connector
import datetime
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
game_add=uic.loadUiType("gameadd.ui")[0]
game_eval=uic.loadUiType("evaluate.ui")[0]
check_eval=uic.loadUiType("checkeval.ui")[0]
game_mod=uic.loadUiType("gameupdate.ui")[0]
check_myeval=uic.loadUiType("checkmyeval.ui")[0]

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
        self.mod.clicked.connect(self.gameUpdate)
        self.info.clicked.connect(self.userInfo)
    def gameAdd(self):
        self.gadd=GameAdd()
        self.gadd.exec()
    
    def gameUpdate(self):
        self.gupdate=GameUpdate()
        self.gupdate.exec()

    def userInfo(self):
        u=UserInfo()
        u.exec()

class GameUpdate(QDialog,QWidget,game_list):
     def __init__(self):
        super(GameUpdate,self).__init__()
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
        sql="select distinct Gname,developer,released_date,age_rating,price from GAME natural join GAME_GERNE"
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
     
        index=[0,1,2,3,4]
        for row in self.res:
            for i in range(0,len(self.res)):
                k=0
                for j in index:
                    self.table.setItem(i,k,QTableWidgetItem(str(self.res[i][j])))
                    k=k+1
        
        

        
        self.table.cellDoubleClicked.connect(lambda: self.gamemod(self.res[self.table.currentRow()][0],self.res[self.table.currentRow()][1],self.res[self.table.currentRow()][2]))
           
     def gamemod(self,gn,dv,rd):
        gname=gn
        developer=dv
        released_date=rd
        gg=GameMod(gname,developer,released_date)
        gg.exec()

class GameMod(QDialog,QWidget,game_mod):
    def __init__(self, gname, developer, rdate):
        super(GameMod,self).__init__()
        self.setupUi(self)
        self.gnamev=gname
        self.developerv=developer
        self.released_datev=rdate
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

        

        self.gnametext.setText(self.gnamev)
        self.developertext.setText(self.developerv)
        self.distributortext.setText(self.distributorv)
        self.datetext.setText(str(self.released_datev))
        self.pricetext.setText(str(self.pricev))
        self.agetext.setText(str(self.age_ratingv))
        self.processortext.setText(self.processorv)
        self.memorytext.setText(str(self.memoryv))
        self.graphictext.setText(self.graphicv)
        self.sizetext.setText(str(self.sizesv))
        self.storagetext.setText(str(self.storage_spacev))
        


        ger=''
        for i in self.gernev:
            ger+=i+","
        ger=ger[:-1]
        self.gernetext.setText(ger)

        o=''
        for i in self.osv:
            o+=i+","
        o=o[:-1]
        self.ostext.setText(o)

        con=''
        for i in self.considerv:
            con+=i+","
        con=con[:-1]
        self.considertext.setText(con)
        self.modbtn.clicked.connect(self.mod)
    
    def mod(self):

        distributor=self.distributortext.text()
        price=self.pricetext.text()
        age=self.agetext.text()
        sizes=self.sizetext.text()
        processor=self.processortext.text()
        memory=self.memorytext.text()
        graphic=self.graphictext.text()
        storage=self.storagetext.text()
        gerne=self.gernetext.text()
        os=self.ostext.text()
        consider=self.considertext.text()

        sql="update GAME set distributor=%s,price=%s,age_rating=%s,size=%s,processor=%s,memory=%s,graphic=%s,storage_space=%s where Gname=%s and developer=%s and released_date=%s;"
        val=[distributor,int(price),int(age),int(sizes),processor,int(memory),graphic,int(storage),self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)

        gerne=gerne.split(',')
        os=os.split(',')
        consider=consider.split(',')

        

        sql="delete from GAME_GERNE where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)

        for i in gerne:
            sql="insert into GAME_GERNE values(%s,%s,%s,%s);"
            val=[self.gnamev,self.developerv,self.released_datev,i]
            cur.execute(sql,val)

        sql="delete from GAME_SYSTEM_REQUIREMENTS_OS where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)

        for i in os:
            sql="insert into GAME_SYSTEM_REQUIREMENTS_OS values(%s,%s,%s,%s);"
            val=[self.gnamev,self.developerv,self.released_datev,i]
            cur.execute(sql,val)


        sql="delete from GAME_RATING_CONSIDERATIONS where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gnamev,self.developerv,self.released_datev]
        cur.execute(sql,val)

        for i in consider:
            sql="insert into GAME_RATING_CONSIDERATIONS values(%s,%s,%s,%s);"
            val=[self.gnamev,self.developerv,self.released_datev,i]
            cur.execute(sql,val)

        conn.commit()
        self.hide()

        

class GameAdd(QDialog,QWidget,game_add):
    def __init__(self):
        super(GameAdd,self).__init__()
        self.setupUi(self)

        self.addbutton.clicked.connect(self.addgame)
    
    def addgame(self):
        gname=self.gnametext.text()
        developer=self.developertext.text()
        distributor=self.distributortext.text()
        price=self.pricetext.text()
        age=self.agetext.text()
        sizes=self.sizetext.text()
        processor=self.processortext.text()
        memory=self.memorytext.text()
        graphic=self.graphictext.text()
        storage=self.storagetext.text()
        released_date=self.datetext.text()
        gerne=self.gernetext.text()
        os=self.ostext.text()
        consider=self.considertext.text()

        released_date = datetime.datetime.strptime(released_date, '%Y-%m-%d')
        sql="insert into GAME values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val=[gname,developer,distributor,released_date,int(price),int(age),int(sizes),processor,int(memory),graphic,int(storage)]
        val2=[gname,developer,released_date,gerne]
        val3=[gname,developer,released_date,os]
        val4=[gname,developer,released_date,consider]
        if '' in val or '' in val2 or '' in val3 or '' in val4:
            pass
        else:
            cur.execute(sql,val)
            gerne=gerne.split(',')
            os=os.split(',')
            consider=consider.split(',')
            for i in gerne:
                sql="insert into GAME_GERNE values(%s,%s,%s,%s);"
                val=[gname,developer,released_date,i]
                cur.execute(sql,val)
            
            for i in os:
                sql="insert into GAME_SYSTEM_REQUIREMENTS_OS values (%s,%s,%s,%s);"
                val=[gname,developer,released_date,i]
                cur.execute(sql,val)

            for i in consider:
                sql="insert into GAME_RATING_CONSIDERATIONS values (%s,%s,%s,%s);"
                val=[gname,developer,released_date,i]
                cur.execute(sql,val)

            conn.commit()
            self.hide()
        
        


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
            ger+=i+","
        ger=ger[:-1]
        self.gerne.setText(ger)

        o=''
        for i in self.osv:
            o+=i+","
        o=o[:-1]
        self.os.setText(o)

        con=''
        for i in self.considerv:
            con+=i+","
        con=con[:-1]
        self.consider.setText(con)

        self.buy.clicked.connect(self.BuyGame)
        self.eval.clicked.connect(lambda:self.checkeval(self.gnamev,self.developerv,self.released_datev))

     def checkeval(self,gname,developer,rdate):
        e=CheckEval(gname,developer,rdate)
        e.exec()

      
        
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
                self.hide()
                
class CheckEval(QDialog,QWidget,check_eval):
     def __init__(self,gname,developer,rdate):
        super(CheckEval,self).__init__()
        self.setupUi(self)
        
        self.gname=gname
        self.developer=developer
        self.rdate=rdate
        
        sql="select Writer_id,Gname,developer,released_date,level,context from GAME_EVALUATION where Gname=%s and developer=%s and released_date=%s;"
        val=[self.gname,self.developer,self.rdate]
        cur.execute(sql,val)
        self.result=cur.fetchall()

        self.table.setRowCount(len(self.result))
        self.table.setColumnCount(6)
     

        for i in range(0,len(self.result)):
            
            for j in range(0,len(self.result[i])):

                if j==4:
                    if self.result[i][4]=='g':
                        self.table.setItem(i,j,QTableWidgetItem(str('추천함')))
                    else:
                        self.table.setItem(i,j,QTableWidgetItem(str('추천하지 않음')))
                else:
                    self.table.setItem(i,j,QTableWidgetItem(str(self.result[i][j])))
                   
        
        self.eval.clicked.connect(lambda: self.gameeval(self.gname,self.developer,self.rdate))

     def gameeval(self,gname,developer,rdate):
        e=GameEval(gname,developer,rdate)
        e.exec()

class CheckMyEval(QDialog,QWidget,check_myeval):
     def __init__(self,id):
        super(CheckMyEval,self).__init__()
        self.setupUi(self)
        
       
        
        sql="select Writer_id,Gname,developer,released_date,level,context from GAME_EVALUATION where Writer_id=%s;"
        val=[user.id]
        cur.execute(sql,val)
        self.result=cur.fetchall()

        self.table.setRowCount(len(self.result))
        self.table.setColumnCount(6)
     

        for i in range(0,len(self.result)):
            
            for j in range(0,len(self.result[i])):

                if j==4:
                    if self.result[i][4]=='g':
                        self.table.setItem(i,j,QTableWidgetItem(str('추천함')))
                    else:
                        self.table.setItem(i,j,QTableWidgetItem(str('추천하지 않음')))
                else:
                    self.table.setItem(i,j,QTableWidgetItem(str(self.result[i][j])))
                   

class GameEval(QDialog,QWidget,game_eval):
    def __init__(self,gname,developer,rdate):
        super(GameEval,self).__init__()
        self.setupUi(self)
        self.reg.clicked.connect(self.register)
        self.gname=gname
        self.developer=developer
        self.rdate=rdate

    def register(self):
        level=self.level.currentText()
        contexts=self.context.toPlainText()
        if level=='추천함':
            level='g'
        else:
            level='b'
        sql="insert into GAME_EVALUATION values (%s,%s,%s,%s,%s,%s);"
        val=[self.gname,self.developer,self.rdate,user.id,level,contexts]
        cur.execute(sql,val)
        sql="insert into EVALUATES values (%s,%s,%s,%s);"
        val=[user.id,self.gname,self.developer,self.rdate]
        cur.execute(sql,val)
        conn.commit()
        self.hide()

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
        sql="select DISTINCT Gname,developer,released_date,age_rating,price from GAME natural join GAME_GERNE"
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
     
        index=[0,1,2,3,4]
        for row in self.res:
            for i in range(0,len(self.res)):
                k=0
                for j in index:
                    self.table.setItem(i,k,QTableWidgetItem(str(self.res[i][j])))
                    k=k+1
        
      
       
        self.table.cellDoubleClicked.connect(lambda: self.gameinfo(self.res[self.table.currentRow()][0],self.res[self.table.currentRow()][1],self.res[self.table.currentRow()][2]))
           
        

        
        

    def gameinfo(self,gn,dv,rd):
        gname=gn
        developer=dv
        released_date=rd
        self.Gameinfo=GameInfo(gname,developer,released_date)
        self.Gameinfo.exec()

class HaveGame(QDialog,QWidget,game_list):
     def __init__(self):
        super(HaveGame,self).__init__()
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
        sql="select distinct Gname,developer,released_date,age_rating,price from GAME  natural join GAME_GERNE natural join BUYS"
        val=[user.id]
        st=" where GAME.Gname=GAME_GERNE.Gname and BUYS.Uid=%s and"
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
     
        index=[0,1,2,3,4]
        for row in self.res:
            for i in range(0,len(self.res)):
                k=0
                for j in index:
                    self.table.setItem(i,k,QTableWidgetItem(str(self.res[i][j])))
                    k=k+1


class UserMenu(QDialog,QWidget,user_menu):
    def __init__(self):
        super(UserMenu,self).__init__()
        self.setupUi(self)

        self.find.clicked.connect(self.findGame)
        self.check.clicked.connect(self.checkGame)
        self.info.clicked.connect(self.infod)
        self.evaluates.clicked.connect(self.evals)

    def findGame(self):
        self.gamelist=GameList()
        self.gamelist.exec()
    
    def checkGame(self):
        c=HaveGame()
        c.exec()

    def infod(self):
        self.info=UserInfo()
        self.info.exec()
    def evals(self):
        e=CheckMyEval(user.id)
        e.exec()

class UserInfo(QDialog,QWidget,user_info):
    def __init__(self) :
        super(UserInfo,self).__init__()
        self.setupUi(self)

        self.idtext.setText(user.id)
        if user.type=='u':
            self.typetext.setText('일반 사용자')
        else:
            self.typetext.setText('관리자')

        self.nametext.setText(user.name)
        self.agetext.setText(str(user.age))
        self.chargetext.setText(str(user.charge))
        self.mod.clicked.connect(self.modify)
    
    def modify(self):
        
        sql="update USER set password=%s, name=%s, age=%s, charge=%s where id=%s;"
        val=[self.pwtext.text(),self.nametext.text(),self.agetext.text(),self.chargetext.text(),user.id]
        if '' in val:
            sw=SignWarn()
            sw.exec()
        else:
            val[2]=int(val[2])
            val[3]=int(val[3])
            cur.execute(sql,val)
            conn.commit()
            user.password=self.pwtext.text()
            user.name=self.nametext.text()
            user.age=val[2]
            user.charge=val[3]
            self.hide()
        

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