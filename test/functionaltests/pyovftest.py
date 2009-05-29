
import os
import types
from lxml import etree
from StringIO import StringIO

import testsuite
testsuite.setup()
from testrunner import testhelp

from pyovf import ovf
from pyovf import helper
from pyovf import item
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
    virtualSystemInfo = 'testVirtualSystemInfo'
    productInfo = 'testProductInfo'
    virtualSystemCollectionId = 'testVirtualSystemCollectionId'
    virtualHardwareSectionInfo = 'testVirtualHardwareSectionInfo'

    debug = False

    def writeXml(self, xmlName, xml):
        f = open('pyovftestxml.py', 'a')
        f.write('%s = """\\' % xmlName)
        f.write('\n')
        f.write(xml + '"""')
        f.write('\n\n')
        f.close()

    def setUp(self):
        self.ovf = helper.NewOvf()
        self.ovf.ovf_DiskSection.ovf_Info = self.diskSectionInfo
        self.ovf.ovf_NetworkSection.ovf_Info = self.networkSectionInfo
        self.ovf.ovf_VirtualSystemCollection.ovf_id = \
            self.virtualSystemCollectionId
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
        p = ovf.ProductSection()
        p.ovf_Info = self.productInfo
        s = ovf.VirtualSystem()
        s.ovf_ProductSection = p
        s.ovf_id = self.virtualSystemId
        s.ovf_Info = self.virtualSystemInfo
        self.ovf.addVirtualSystem(s)
        return s

    def addSystemProperty(self, system, key, type):
        p = ovf.Property()
        p.ovf_key = key
        p.ovf_type = type
        system.ovf_ProductSection.addProperty(p)

    def addNetwork(self):
        n = ovf.Network(id=self.networkId)
        n.ovf_name = self.networkName
        self.ovf.addNetwork(n)
        return n

    def testNewOvfXml(self):
        xml = self.ovf.toxml()
        if self.debug:
            self.writeXml('newXml', xml)
        self.assertEquals(xml, newXml)
       
    def testAddFileReference(self):
        self.addFileReference(self.fileId)
        xml = self.ovf.toxml()
        if self.debug:
            self.writeXml('fileXml', xml)
        self.assertEquals(xml, fileXml)

    def testAddDiskWithFormat(self):
        file = self.addFileReference(self.fileId)
        df = ovf.DiskFormat('http://example.com/format.html')
        self.addDisk(ovf_diskId=self.diskId, ovf_fileRef=file, 
            ovf_format=df, ovf_capacity=self.capacity)
        xml = self.ovf.toxml()
        if self.debug:
            self.writeXml('diskWithFormatXml', xml)
        self.assertEquals(xml, diskWithFormatXml)

        file2 = ovf.FileReference()
        file2.ovf_id = 'testFileId2'
        file2.ovf_href = self.fileHref
        self.addDisk(ovf_diskId=self.diskId, ovf_fileRef=file2, 
            ovf_format=df, ovf_capacity=self.capacity)
        xml = self.ovf.toxml()
        if self.debug:
            self.writeXml('diskWithFormatXml2', xml)
        self.assertEquals(xml, diskWithFormatXml2)

    def testAddDiskWithCompressedFormat(self):
        file = self.addFileReference(self.fileId)
        df = ovf.DiskFormat('http://example.com/format.html#compressed')
        self.addDisk(ovf_diskId=self.diskId, ovf_fileRef=file, 
            ovf_format=df, ovf_capacity=self.capacity)
        xml = self.ovf.toxml()
        if self.debug:
            self.writeXml('diskWithCompressedFormatXml', xml)
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
        if self.debug:
            self.writeXml('systemPropertyXml', xml)
        self.assertEquals(xml, systemPropertyXml)
        
    def testAddNetwork(self):
        n = self.addNetwork()
        xml = self.ovf.toxml()
        if self.debug:
            self.writeXml('networkXml', xml)
        self.assertEquals(xml, networkXml)

    def testOvfFile(self):
        if self.debug:
            self.write('ovfFileXml', ovfFileXml)
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

    def testNew(self):
        newOvf = helper.NewOvf()
        newOvf.NetworkSection.Info = 'network section info'
        newOvf.DiskSection.Info = 'disk section info'
        newOvf.VirtualSystemCollection.id = self.virtualSystemCollectionId

        fr = ovf.FileReference()
        fr.id = 'file1'
        fr.href = 'file'
        newOvf.addFileReference(fr)

        vhws = ovf.VirtualHardwareSection()
        vhws.Info = self.virtualHardwareSectionInfo
        cpu = item.Cpu()
        memory = item.Memory()

        vhws.addItem(cpu)
        vhws.addItem(memory)

        vs = ovf.VirtualSystem()
        vs.id = 'newId'
        vs.Info = 'newInfo'
        vs.addVirtualHardwareSection(vhws)
        newOvf.addVirtualSystem(vs)

        d = ovf.Disk()
        df = ovf.DiskFormat('http://www.vmware.com/interfaces/specifications/vmdk.html#sparse')
        d.diskId = 'vmdisk1'
        d.fileRef = fr
        d.format = df
        d.capacity = 0
        newOvf.addDisk(d)

        xml = newOvf.toxml()

        if self.debug:
            self.writeXml('newXml2', xml)
        self.assertEquals(xml, newXml2)
