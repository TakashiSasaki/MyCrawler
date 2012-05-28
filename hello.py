from __future__ import print_function, unicode_literals
from unittest import TestCase

class _Test(TestCase):
    def setUp(self):
        print("setUp")
    
    def test1(self):
        print ("test1")
        
    def tearDown(self):
        print("tearDown")

if __name__ == "__main__":
    print ("__main__")
