from xobj import xobj
import os

class AbstractDiskFormat(object):

    def __init__(self, compressed = False):
        assert(self.format)
        self.compressed = compressed

class DiskFormatVmdk(AbstractDiskFormat):

    format = "http://www.vmware.com/specifications/vmdk.html"

class DiskFormat(AbstractDiskFormat):

    def __init__(self, s, compressed = False):
        if s.endswith('#compressed'):
            # we shouldn't parse this and get it passed in
            assert(not compressed)
            compressed = True
            s = s[:-11]

        self.format = s
        AbstractDiskFormat.__init__(self, compressed)

    def __str__(self):
        if self.compressed:
            return self.format + "#compressed"

        return self.format

class pDisk(object):

    _xobj = xobj.XObjMetadata(
            attributes = { 'ovf_diskId' : str,
                           'ovf_fileRef' : xobj.XIDREF,
                           'ovf_capacity' : long,
                           'ovf_populatedSize' : long,
                           'ovf_format' : DiskFormat } )

class Disk(pDisk):

    def __init__(self, diskId, fileObj, capacity, format, populatedSize):
        self.ovf_diskId = diskId
        self.ovf_fileRef = fileObj
        self.ovf_capacity = capacity
        self.ovf_populatedSize = populatedSize
        self.ovf_format = format

class pFileReference(object):

    _xobj = xobj.XObjMetadata(
            attributes = { "ovf_id" : str,
                           "ovf_href" : str,
                           "ovf_size " : long } )

class FileReference(pFileReference):

    def __init__(self, id, href, size):
        self.ovf_id = id
        self.ovf_href = href
        self.ovf_size = size

class DiskSection(object):

    ovf_Disk = [ pDisk ]

    def __init__(self):
        self.ovf_Disk = []

class Network(object):

    _xobj = xobj.XObjMetadata(
            attributes = { "ovf_id" : str,
                           "ovf_name" : xobj.XID } )

    def __init__(self, id, name):
        self.ovf_id = id
        self.ovf_name = name
        if name is not None:
            self.ovf_name = name

class NetworkSection(object):

    ovf_Network = [ object ]

    def __init__(self):
        self.ovf_Network = []

class pProperty(object):

    pass

class Property(pProperty):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_key' : str,
                                             'ovf_type' : str } )

    def __init__(self, key, type):
        self.ovf_key = key
        self.ovf_type = type

class pProduct(object):

    ovf_info = str
    ovf_productVersion = str
    ovf_Property = [ pProperty ]

class Product(pProduct):

    def addProperty(self, p):
        self.ovf_Property.append(p)

    def __init__(self, info, version = None):
        self.ovf_Property = []
        self.ovf_info = info
        if version:
            self.ovf_productVersion = version

class ProductSection(object):

    ovf_Product = [ pProduct ]

    def __init__(self):
        self.ovf_Product = []

class pVirtualSystem(object):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_id' : str,
                                             'ovf_info' : str } )

    ovf_ProductSection = [ ProductSection ]

class VirtualSystem(object):

    def addProduct(self, p):
        self.ovf_ProductSection.append(p)

    def __init__(self, id, info):
        self.ovf_ProductSection = []
        self.ovf_id = id
        self.ovf_info = info

class ReferencesSection(object):

    ovf_File = [ pFileReference ]

    def __init__(self):
        self.ovf_File = []

class Ovf(object):

    ovf_References = ReferencesSection
    ovf_DiskSection = DiskSection
    ovf_NetworkSection = NetworkSection
    ovf_VirtualSystem = [ { 'VirtualSystem' : VirtualSystem,
                            'VirtualSystemCollection' : object } ]

    def addDisk(self, d):
        if d.ovf_fileRef not in self.ovf_References.ovf_File:
            self.addFileReference(d.ovf_fileRef)
        self.ovf_DiskSection.ovf_Disk.append(d)

    def addNetwork(self, n):
        self.ovf_NetworkSection.ovf_Network.append(n)

    def addFileReference(self, r):
        self.ovf_References.ovf_File.append(r)

    def addSystem(self, vs):
        self.ovf_VirtualSystem.append(vs)

    def toxml(self):
        schemaPath = os.path.join(os.path.dirname(__file__),
                                  "schemas/ovf-envelope.xsd")
        return self._doc.toxml(nsmap = self._doc.nameSpaceMap)

class NewOvf(Ovf):

    def __init__(self):
        doc = OvfDocument()
        doc.ovf_Envelope = self
        doc.ovf_Envelope._doc = doc

        self.ovf_References = ReferencesSection()
        self.ovf_DiskSection = DiskSection()
        self.ovf_NetworkSection = NetworkSection()
        self.ovf_VirtualSystem = []

class OvfDocument(xobj.Document):

    nameSpaceMap = { 'ovf' : 'http://schemas.dmtf.org/ovf/envelope/1',
                     None : 'http://schemas.dmtf.org/ovf/envelope/1' }
    ovf_Envelope = Ovf

def OvfFile(f):
    schemaPath = os.path.join(os.path.dirname(__file__),
                              "schemas/ovf-envelope.xsd")
    doc = xobj.parsef(f, documentClass = OvfDocument,
                      schemaf = open(schemaPath))
    ovf = doc.ovf_Envelope
    ovf._doc = doc
    return ovf
