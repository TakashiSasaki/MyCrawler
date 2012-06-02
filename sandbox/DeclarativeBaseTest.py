from config import *
from sqlalchemy import  Column, String, Integer, DateTime, Boolean, ForeignKey
info("abc")
from sqlalchemy import  MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
from sqlalchemy import Column
DeclarativeBase = _declarative_base(metadata=_MetaData())

class XYZ(DeclarativeBase):
    info("XYZ start")
    __tablename__ = "XYZ"
    __table_args__ = {'sqlite_autoincrement': True}

    c1 = Column(Integer, primary_key = True)
    c2 = Column(String())
    c3 = Column(DateTime)
    c4 = Column(Boolean)

    info("dropTable")
    @classmethod
    def dropTable(cls):
        try:
            my_object_table = DeclarativeBase.metadata.tables[cls.__tablename__]
            my_object_table.drop(engine, checkfirst=True)
        except:
            pass
    
    info("createTable")
    @classmethod
    def createTable(cls):
        try:
            info("try")
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            table.create(engine, checkfirst=True)
        except:
            pass
    info("aend")

info("_Test start")
class _Test(TestCase):
    
    def setUp(self):
        info("setup start")
        #TestCase.setUp(self)
        XYZ.dropTable()
        #DeclarativeBase.metadata.create_all(engine)
        info("setup end")

        
    def tearDown(self):
        info("teardown start")
        #TestCase.tearDown(self)
        XYZ.dropTable()
        info("teardown end")
        
    def test1(self):
        info("test start")
        xyz = XYZ()
        info(XYZ.__dict__)
        pass
        info("test end")

if __name__ == "__main__":
    info("main")
    main()