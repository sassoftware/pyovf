
import os
import types
from lxml import etree
from StringIO import StringIO

import testsuite
testsuite.setup()
from testrunner import testhelp

from pyovf import ovf
from pyovf import helper
from xobj import xobj
from pyovftestxml import *

class TestCase(testhelp.TestCase):
    pass

class PyOvfTest(TestCase):

    fileId = 'testFileId'
    fileHref = 'testFileHref'
    networkId = 'testNetworkId'
    networkName = 'testNetworkName'
    capacity = 'testCapacity'
    diskId = 'testDiskId'
    diskSectionInfo = 'testDiskSectionInfo'
    networkSectionInfo = 'testNetworkSectionInfo'
    virtualSystemId = 'testVirtualSystemId'
    productInfo = 'testProductInfo'

    def setUp(self):
        self.ovf = helper.NewOvf()
        self.ovf.ovf_DiskSection.ovf_Info = self.diskSectionInfo
        self.ovf.ovf_NetworkSection.ovf_Info = self.networkSectionInfo
        TestCase.setUp(self)

    def addFileReference(self, id):
        f = ovf.FileReference()
        f.ovf_id = id
        f.ovf_href = self.fileHref
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
        p.ovf_Info = self.productInfo
        s = ovf.VirtualSystem()
        s.addProduct(p)
        s.ovf_id = self.virtualSystemId
        self.ovf.addSystem(s)
        return s

    def addSystemProperty(self, system, key, type):
        p = ovf.Property()
        p.ovf_key = key
        p.ovf_type = type
        system.ovf_ProductSection[0].addProperty(p)

    def addNetwork(self):
        n = ovf.Network(id=self.networkId)
        n.ovf_name = self.networkName
        self.ovf.addNetwork(n)
        return n

    def testNewOvfXml(self):
        xml = self.ovf.toxml()
        self.assertEquals(xml, newXml)
       
    def testAddFileReference(self):
        self.addFileReference(self.fileId)
        xml = self.ovf.toxml()
        self.assertEquals(xml, fileXml)

    def testAddDiskWithFormat(self):
        file = self.addFileReference(self.fileId)
        df = ovf.DiskFormat('http://example.com/format.html')
        self.addDisk(ovf_diskId=self.diskId, ovf_fileRef=file, 
            ovf_format=df, ovf_capacity=self.capacity)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskWithFormatXml)

        file2 = ovf.FileReference()
        file2.ovf_id = 'testFileId2'
        file2.ovf_href = self.fileHref
        self.addDisk(ovf_diskId=self.diskId, ovf_fileRef=file2, 
            ovf_format=df, ovf_capacity=self.capacity)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskWithFormatXml2)

    def testAddDiskWithCompressedFormat(self):
        file = self.addFileReference(self.fileId)
        df = ovf.DiskFormat('http://example.com/format.html#compressed')
        self.addDisk(ovf_diskId=self.diskId, ovf_fileRef=file, 
            ovf_format=df, ovf_capacity=self.capacity)
        xml = self.ovf.toxml()
        self.assertEquals(xml, diskWithCompressedFormatXml)

    def testAbstractDiskFormat(self):
        class FakeDiskFormat(ovf.AbstractDiskFormat):
            ovf_format = 'http://example.com/format.html'

        fdf = FakeDiskFormat(compressed=True)
        self.assertEquals(str(fdf),
            'http://example.com/format.html#compressed')

        fdf = FakeDiskFormat(compressed=False)            
        self.assertEquals(str(fdf),
            'http://example.com/format.html')

    def testSystemProperty(self):
        s = self.addSystem()
        self.addSystemProperty(s, 'propertyKey', 'string')
        xml = self.ovf.toxml()
        self.assertEquals(xml, systemPropertyXml)
        
    def testAddNetwork(self):
        n = self.addNetwork()
        xml = self.ovf.toxml()
        self.assertEquals(xml, networkXml)

    def testOvfFile(self):
        s = StringIO(ovfFileXml)
        ovfObj = helper.OvfFile(s)
        self.assertEquals(ovfObj.DiskSection.Info,
            self.diskSectionInfo)
        self.assertEquals(ovfObj.NetworkSection.Info,
            self.networkSectionInfo)
        self.assertEquals(ovfObj.NetworkSection.Network[0].id,
            self.networkId)
        self.assertEquals(ovfObj.NetworkSection.Network[0].name,
            self.networkName)

    def testUnknownConstructor(self):
        self.assertRaises(TypeError, ovf.Network, foo='foo')

    def testPrefixSetAttr(self):
        self.ovf.NetworkSection.Network = []
        self.assertTrue(hasattr(self.ovf.NetworkSection, 'ovf_Network'))
