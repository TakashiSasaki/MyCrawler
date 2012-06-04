from config import *
import lib
import time

class TableMixin(object):

    def getTableMixin(self):
        info(self.table)
        assert issubclass(self.table, lib.DeclarativeBase.DeclarativeBase)
        assert issubclass(self.table, lib.GvizDataTableMixin.GvizDataTableMixin)
        assert issubclass(self.table, lib.TableMixin.TableMixin)
        
        if self.request.path_info == "" or self.request.path_info == "/":
            session = Session()
            try:
                data_table = self.table.getGvizDataTable(session)
                session.close()
                self.response.set_status(200)
                self.response.expires = time.time()
                self.response.out.write(data_table.ToJSonResponse())
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True

        if self.request.path_info == "/create":
            try:
                self.table.createTable()
                self.response.set_status(200)
                self.response.out.write("%s.createTable" % self.table.getTable())
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True
        
        if self.request.path_info == "/drop":
            try:
                self.table.dropTable()
                self.response.set_status(200)
                self.response.out.write("%s.dropTable" % self.table.getTable())
            except Exception,e :
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True

        if self.request.path_info == "/dummy":
            try:
                self.table.insertDummyRecords()
                self.response.set_status(200)
                self.response.out.write("%s.insertDummyRecords" % self.table.getTable())
            except Exception, e:
                self.response.set_status(500)
                self.response.out.write(e.message)
            return True
        return False
