from xobj import xobj
import os

class OvfObject(object):

    def __init__(self, **kwargs):
        for key, val in self.__class__.__dict__.iteritems():
            if type(val) == list:
                setattr(self, key, [])

        for key, val in kwargs.iteritems():
            ovfKey = 'ovf_' + key
            if (hasattr(self.__class__, ovfKey) or
                (hasattr(self, '_xobj') and ovfKey in (self._xobj.attributes))):
                setattr(self, ovfKey, val)
            else:
                raise TypeError, 'unknown constructor parameter %s' % key

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

class Disk(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { 'ovf_diskId' : str,
                           'ovf_fileRef' : xobj.XIDREF,
                           'ovf_capacity' : long,
                           'ovf_populatedSize' : long,
                           'ovf_format' : DiskFormat } )

class FileReference(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { "ovf_id" : str,
                           "ovf_href" : str,
                           "ovf_size" : long } )

class DiskSection(object):

    ovf_Disk = [ Disk ]

class Network(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { "ovf_id" : str,
                           "ovf_name" : xobj.XID } )

class NetworkSection(object):

    ovf_Network = [ object ]

class Property(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_key' : str,
                                             'ovf_type' : str } )

class Product(OvfObject):

    ovf_info = str
    ovf_productVersion = str
    ovf_Property = [ Property ]

    def addProperty(self, p):
        self.ovf_Property.append(p)

class ProductSection(object):

    ovf_Product = [ Product ]

class VirtualSystem(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_id' : str,
                                             'ovf_info' : str } )

    ovf_ProductSection = [ ProductSection ]

    def addProduct(self, p):
        self.ovf_ProductSection.append(p)

class ReferencesSection(object):

    ovf_File = [ FileReference ]

class Ovf(OvfObject):

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
