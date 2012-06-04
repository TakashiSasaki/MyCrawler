from config import *
from sqlalchemy import Column, Integer, String, DateTime
from lib.DeclarativeBase import DeclarativeBase
from lib.GvizDataTableMixin import GvizDataTableMixin
from lib.TableMixin import TableMixin
from uuid import uuid1

class SyncState(DeclarativeBase, GvizDataTableMixin, TableMixin):
    __tablename__ = "SyncState" 
    stateUuid = Column(String, primary_key=True, index=True, nullable=False)
    lockBegin = Column(DateTime, nullable = False)
    lockEnd = Column(DateTime, nullable = True)
    stateBeforeLock = Column(String, nullable = False)
    stateAfterLock = Column(String, nullable = True)
    agetnId = Column(String, nullable = True)
    userName = Column(String, nullable = True)
    userDomain = Column(String, nullable = True)

    def __init__(self):
        self.stateUuid = uuid1.get_hex()
    
    def setLockBegin(self, lock_begin = None):
        if lock_begin is None:
            lock_begin = utcnow()
        self.lockBegin = lock_begin
    
    def setLockEnd(self, lock_end = None):
        if lock_end is None:
            lock_end = utcnow()
        self.lockEnd = lock_end
    
    def setStateBeforeLock(self, state_before_lock):
        assert isinstance(state_before_lock, str)
        self.stateBeforeLock = state_before_lock
        
    def setStateAfterLock(self, state_after_lock):
        assert isinstance(state_after_lock, str)
        self.stateAfterLock = state_after_lock

class _Test(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        
    def tearDown(self):
        TestCase.tearDown(self)
