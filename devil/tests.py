import unittest
import tempfile
import os
import sys
import random
import string
import file 
import shutil

class LocalTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.f = file.FileController(self.tempdir)
        file.input = lambda _: randstring(6)
        file.input = lambda _: randstring(6)
        self.f.start()

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        pass

    def test_start(self):
        files = [self.f.statusfile,self.f.userfile,self.f.trackingfile]
        for i in files:
            self.assertTrue(os.path.isfile(i))
    def add(self):
        f = randfile(self.tempdir)
        self.f.add(f)
        return f 
    def test_add(self):
        f = self.add()
        fp = open(self.f.trackingfile)
        lines = fp.readlines()
        fp.close()
        self.assertEqual(lines[0],os.path.abspath(f) + ' notcommited\n')
    def commit(self):
        filestoadd = random.randint(1,10)
        added = [self.add() for i in range(filestoadd)]
        message = randstring(10)
        self.f.commit(message)
    def test_commit(self):
        self.commit()
        self.assertTrue(os.path.isdir(self.f.objectdir))


        
    

    
        
def randstring(l):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(l))

def randfile(tmpdir):
    fp = tempfile.NamedTemporaryFile(mode='w', dir=tmpdir, delete=False)
    fname = os.path.join(tmpdir,fp.name)
    nolines = random.randint(1,100)
    for i in range(nolines):
        fp.write(randstring(20)+'\n')
    fp.close()
    return fname

test_cases = (LocalTests,)

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite

if __name__ == "__main__":
    unittest.main()
