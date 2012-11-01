import unittest
import tempfile
import os
import sys
import random
import string
import file 
import shutil
import filecmp

class LocalTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.tempdir2 = tempfile.mkdtemp()
        self.f = file.FileController(self.tempdir)
        file.raw_input = lambda _: randstring(6)
        file.raw_input = lambda _: randstring(6)
        self.f.start()
        self.g = None

    def tearDown(self):
        #shutil.rmtree(self.tempdir)
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
        filestoadd = random.randint(0,3)
        added = [self.add() for i in range(filestoadd)]
        message = randstring(10)
        self.f.commit(message)
        return added

    def test_commit(self):
        added = self.commit()
        self.assertTrue(os.path.isdir(self.f.objectdir))
        fp = open(self.f.trackingfile)
        lines = fp.readlines()
        fp.close()
        for i,f in enumerate(added):
            self.assertEqual(lines[i],os.path.abspath(f) + ' commited\n')
        fp = open(self.f.statusfile)
        lns = fp.readlines()
        fp.close()
        committag = lns[0].split()[1]
        # check objectdir 
        cdir = os.path.join(self.f.commitfiles)
        self.assertTrue(os.path.isdir(cdir))
        # check hashmapfile 
        hfile = os.path.join(self.f.objectdir,committag)
        print hfile
        self.assertTrue(os.path.isfile(hfile))
        # check all files copied 

        fp = open(hfile)
        lines = fp.readlines()
        fp.close()
        for line in lines:
            sp = line.split()
            self.assertTrue(os.path.isfile(os.path.join(cdir,sp[1])))

    def test_merge(self):
        file.raw_input = lambda _: randstring(6)
        file.raw_input = lambda _: randstring(6)
        self.g =  file.FileController(self.tempdir2)
        self.g.start()
        self.commit()
        self.g.merge(self.tempdir)
        compareObj = filecmp.dircmp(self.f.commitfiles,self.g.commitfiles)
        self.assertTrue(compareObj.left_only == [])
        self.assertTrue(compareObj.right_only == [])
        shutil.rmtree(self.tempdir2)


    
        



def randstring(l):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(l))

def randfile(tmpdir):
    fp = tempfile.NamedTemporaryFile(mode='w', dir=tmpdir, delete=False)
    fname = os.path.join(tmpdir,fp.name)
    nolines = random.randint(0,10)
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
