
import os
import types

import testsuite
testsuite.setup()
from testrunner import testhelp
from lxml import etree

from pyovf import ovf
from xobj import xobj
from StringIO import StringIO

from testpyovfxml import *

class TestCase(testhelp.TestCase):
    pass

class PyOvfTest(TestCase):

    fileId = 'testFile'
    networkId = 'testNetwork'

    def setUp(self):
        self.ovf = ovf.NewOvf()
        TestCase.setUp(self)

    def addFileReference(self, id):
        f = ovf.FileReference()
        f.id = id
        self.ovf.addFileReference(f)
        return f

    def addDisk(self, **kwargs):
        d = ovf.Disk()
    
        for attr in d._xobj.attributes.keys():
            if kwargs.has_key(attr):
                setattr(d, attr, kwargs[attr])

        self.ovf.addDisk(d)

    def addSystem(self):
        p = ovf.Product()
        s = ovf.VirtualSystem()
        s.addProduct(p)
        self.ovf.addSystem(s)
        return s

    def addSystemProperty(self, system, key):
        system.ProductSection[0].addProperty(key)

    def addNetwork(self):
        n = ovf.Network(id=self.networkId)
        self.ovf.addNetwork(n)
        return n

    def testNewOvfXml(self):
        new = ovf.NewOvf()
        xml = new.toxml()
        self.assertEquals(xml, newXml)
       
    def testAddFileReference(self):
        self.addFileReference(self.fileId)
        xml = self.ovf.toxml()
        self.assertEquals(xml, fileXml)

    def testAddDisk(self):
        fr = ovf.FileReference()
        fr.id = 'testFile0'
        self.addDisk(fileRef=fr)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskXmlNoRef)

        file = self.addFileReference(self.fileId)
        self.addDisk(fileRef=file)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskXml)

    def testAddDiskWithFormat(self):
        file = self.addFileReference(self.fileId)
        df = ovf.DiskFormat('http://example.com/format.html')
        self.addDisk(fileRef=file, format=df)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskWithFormatXml)

    def testAddDiskWithCompressedFormat(self):
        file = self.addFileReference(self.fileId)
        df = ovf.DiskFormat('http://example.com/format.html#compressed')
        self.addDisk(fileRef=file, format=df)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskWithCompressedFormatXml)

    def testAbstractDiskFormat(self):
        class FakeDiskFormat(ovf.AbstractDiskFormat):
            format = 'http://example.com/format.html'

        fdf = FakeDiskFormat(compressed=True)
        self.assertEquals(str(fdf),
            'http://example.com/format.html#compressed')

        fdf = FakeDiskFormat(compressed=False)            
        self.assertEquals(str(fdf),
            'http://example.com/format.html')

    def testSystemProperty(self):
        s = self.addSystem()
        self.addSystemProperty(s, 'propertyKey')
        xml = self.ovf.toxml()
        self.assertEquals(xml, systemPropertyXml)
        
    def testAddNetwork(self):
        n = self.addNetwork()
        xml = self.ovf.toxml()
        self.assertEquals(xml, networkXml)
