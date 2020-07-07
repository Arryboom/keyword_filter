#coding:utf-8
####by arryboom
####https://github.com/arryboom

from fastapi import FastAPI
#import 
import json
from enum import Enum
from pydantic import BaseModel
import time,datetime
from typing import Optional
from sqlalchemy import Column, String,Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import jieba

# ##init
# class BadKeyWord(BaseModel):
    # keyword: str
    # description: Optional[str] = "Null"
    # date: Optional[str]="1970-01-01 15:30"
    # main_type: Optional[str]="normall"
    
# class UserIn(BaseModel):
    # username: str
    # password: str=None
    # email: str=None
    # full_name: str = None

# ###structure

# app = FastAPI()

# @app.get("/")
# async def root():
    # return {"message": "Hello World"}

# @app.post("/putkeyword")
# async def putkeyword(kwdobj: BadKeyWord):
    # if (kwdobj.keyword!="Null"):
        # nowtime=time.strftime('%Y-%m-%d %H:%M:%S')
        # kwdobj.date=nowtime
        # return {kwdobj}
    # else:
        # return {"success":"no"}
    
# @app.post("/xputkeyword",response_model=BadKeyWord)
# async def putkeyword(kwdobj: BadKeyWord):
    # if (kwdobj.keyword!="Null"):
        # nowtime=time.strftime('%Y-%m-%d %H:%M:%S')
        # kwdobj.date=str(nowtime)
        # return {kwdobj}
    # else:
        # return {"success":"no"}


# # Don't do this in production!
# @app.post("/user/", response_model=UserIn) 
# async def create_user(*, user: UserIn):
    # return user
    
   
   
###----------------------------------------------------------------------------------------------------------.
###db init###
Base = declarative_base()
engine = create_engine('sqlite:///words.db?check_same_thread=False', echo=True)
DBSession = sessionmaker(bind=engine)
#from sqlalchemy import Column, Integer, String

# 定义映射类User，其继承上一步创建的Base
class Words(Base):
    # 指定本类映射到users表
    __tablename__ = 'words'
    # 如果有多个类指向同一张表，那么在后边的类需要把extend_existing设为True，表示在已有列基础上进行扩展
    # 或者换句话说，sqlalchemy允许类是表的字集
    # __table_args__ = {'extend_existing': True}
    # 如果表在同一个数据库服务（datebase）的不同数据库中（schema），可使用schema参数进一步指定数据库
    # __table_args__ = {'schema': 'test_database'}
    
    # 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系
    # 从语法上说，各变量类型和表的类型可以不完全一致，如表字段是String(64)，但我就定义成String(32)
    # 但为了避免造成不必要的错误，变量的类型和其对应的表的字段的类型还是要相一致
    # sqlalchemy强制要求必须要有主键字段不然会报错，如果要映射一张已存在且没有主键的表，那么可行的做法是将所有字段都设为primary_key=True
    # 不要看随便将一个非主键字段设为primary_key，然后似乎就没报错就能使用了，sqlalchemy在接收到查询结果后还会自己根据主键进行一次去重
    # 指定id映射到id字段; id字段为整型，为主键，自动增长（其实整型主键默认就自动增长）
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 指定name映射到name字段; name字段为字符串类形，
    word = Column(String(40))
    description = Column(String(256))
    time = Column(String(64))
    maintype = Column(String(64))

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    # def __repr__(self):
        # return "<User(name='%s', fullname='%s', password='%s')>" % (
                   # self.name, self.fullname, self.password)
###
Base.metadata.create_all(engine, checkfirst=True)
# 创建session对象:
session = DBSession()
# 创建新User对象:
# new_user = User(id='5', name='Bob')
# # 添加到session:
# session.add(new_user)
# # 提交即保存到数据库:
# session.commit()
# # 关闭session:
# session.close()

##################################################################DB#####
class Keyword(BaseModel):
    keyword: str
    description: Optional[str] = None
    time: Optional[str] = "1970-01-01 15:00"
    maintype: Optional[str] = "common"
class XText(BaseModel):
    text: str
def checkrepeat(item: Keyword):
    result=session.query(Words).filter_by(word=item.keyword).first()
    if result:
        return False
    else:
        return True
def insertKWD(item: Keyword):
    db_item=Words(word=item.keyword,description=item.description,time=item.time,maintype=item.maintype)
    session.add(db_item)
    session.commit()
def deleteKWD(item: Keyword):
    result=session.query(Words).filter_by(word=item.keyword).first()
    if result:
        id=result.id
        session.delete(result)
        session.commit()
        return True
    else:
        return False
def getall():
    all_res={}
    counter=0
    holder=[]
    for word in session.query(Words):
        # tempx=[]
        # tempx.append(word.word)
        # tempx.append(word.description)
        # tempx.append(word.time)
        # tempx.append(word.maintype)
        # holder.append(tempx)
        tempx={}
        tempx['id']=word.id
        tempx['keyword']=word.word
        tempx['description']=word.description
        tempx['time']=word.time
        tempx['type']=word.maintype
        holder.append(tempx)
        #print(user)
        counter+=1
    all_res["count"]=counter
    all_res["result"]=holder
    return all_res

def clearall():
    # all_res={}
    # counter=0
    # holder=[]
    # for word in session.query(Words):
        # tempx=[]
        # tempx.append(word.word)
        # tempx.append(word.description)
        # tempx.append(word.time)
        # tempx.append(word.maintype)
        # holder.append(tempx)
        # #print(user)
        # counter+=1
    # all_res["count"]=counter
    # all_res["result"]=holder
    # return all_res
    # for word in session.query(Words):
        # session.delete(word)
        
        # #print(user)
        # #counter+=1
    #session.commit()
    session.execute('DELETE FROM words;')
    #session.execute("DELETE FROM sqlite_sequence WHERE name = 'words'")
    session.commit()
    # print("hehre")
    res={}
    res["success"]="true"
    return res
    #pass
#    db_item=Words(words=item.keyword,description=item.description,time=item.time,maintype=item.maintype)
#our_user = session.query(User).filter_by(name='ed').first()
###################################################################################################################check uppon##########
def ck1(text):
    #check for "人民群众吃屎？自媒体才吃！" /"突发!自媒体天天吃屎" /"自媒体吃屎？确实不假" type
    if ("!" in text) or ("！" in text) or ("?" in text) or ("？" in text):
        as_mark_pos=text.find("!")
        cn_mark_pos=text.find("！")
        as_qu_pos=text.find("?")
        cn_qu_pos=text.find("？")
        if (cn_qu_pos!=-1):
            if ((as_mark_pos!=-1)or(cn_mark_pos!=-1))and((cn_qu_pos<as_mark_pos)or(cn_qu_pos<cn_mark_pos)):
                return True
            elif(cn_qu_pos<len(text)-1):
                #if "?" not in the end
                return True
        if (as_qu_pos!=-1):
            if ((as_mark_pos!=-1)or(cn_mark_pos!=-1))and((as_qu_pos<as_mark_pos)or(as_qu_pos<cn_mark_pos)):
                return True
            elif(as_qu_pos<len(text)-1):
            #if "?" not in the end
                return True
        if ((as_mark_pos!=-1)or(cn_mark_pos!=-1)):
            return True
    else:
        return False
def ck2(text):
    #check for "网友：自媒体都是天使" type
    if ((":" in text)or("：" in text)):
        return True


###############################################################################################################################################

def checkit(text: XText):
    for word in session.query(Words):
        if (word.word in text.text)or(ck1(text.text))or(ck2(text.text)):
            return True
    return False
def split_sentence(text: XText):
    all_res={}
    counter=0
    holder=[]
    xvgroup=jieba.cut_for_search(text.text)
    #vgrpu=",".join(xvgroup)
    for x in xvgroup:
        holder.append(x)
        counter+=1
    all_res["count"]=counter
    all_res["result"]=holder
    return all_res


###--------------------------------------------------------------------------------------------------------------





app = FastAPI()

###CORS
from fastapi.middleware.cors import CORSMiddleware
# origins = [
    # "http://localhost",
    # "http://localhost:8080",
    # "http://localhost:8080",
# ]
# origins = [
    # "http://localhost",
    # "http://127.0.0.1:32768",
    # "http://127.0.0.1:61112"
# ]
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####


@app.post("/putkwd/")
async def create_item(item: Keyword):
    nowtime=time.strftime('%Y-%m-%d %H:%M:%S')
    item.time=str(nowtime)
    item_dict = item.dict()
    item_dict["repeat"]=checkrepeat(item)
    if (checkrepeat(item) and item.keyword):
        insertKWD(item)
    return item_dict
@app.post("/getkwds/")
async def getkwds():
    return getall()
@app.post("/clearall/")
async def clearxall():
    return clearall()
@app.post("/checkjunk/")
async def checkxit(text: XText):
    if checkit(text):
       return "True"
    return "False"
@app.post("/split_sts/")
async def splitsz(text: XText):
    return split_sentence(text)
@app.post("/delkwd/")
async def delzx(xitem: Keyword):
    return deleteKWD(xitem)