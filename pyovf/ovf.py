from xobj import xobj
import os

class OvfObject(object):

    def __init__(self, **kwargs):
        for key, val in self.__class__.__dict__.iteritems():
            if type(val) == list:
                setattr(self, key, [])

        for key, val in kwargs.iteritems():
            # ovfKey = 'ovf_' + key
            ovfKey = key
            if (hasattr(self.__class__, ovfKey) or
                (hasattr(self, '_xobj') and ovfKey in (self._xobj.attributes))):
                setattr(self, ovfKey, val)
            else:
                raise TypeError, 'unknown constructor parameter %s' % key

def OvfFile(f):
    schemaPath = os.path.join(os.path.dirname(__file__),
                              "schemas/ovf-envelope.xsd")
    doc = xobj.parsef(f, documentClass = OvfDocument,
                      schemaf = open(schemaPath))
    ovf = doc.Envelope
    ovf._doc = doc
    return ovf

class AbstractDiskFormat(object):

    def __str__(self):
        if self.compressed:
            return self.format + "#compressed"

        return self.format

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
            attributes = {
                           'capacity' : long,
                           'capacityAllocationUnits' : long,
                           'diskId' : str,
                           'fileRef' : xobj.XIDREF,
                           'format' : DiskFormat,
                           'parentRef' : str,
                           'populatedSize' : long,
                         } )

class FileReference(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = {
                           "chunkSize" : long,
                           "compression" : str,
                           "href" : str,
                           "id" : str,
                           "size" : long,
                         } )

class DiskSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'Info', 'Disk' ])

    Disk = [ Disk ]
    Info = str

class Network(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { "id" : str,
                           "name" : xobj.XID } )

class NetworkSection(OvfObject):

    Network = [ object ]

class Property(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'key' : str,
                                             'type' : str } )

class Product(OvfObject):

    info = str
    productVersion = str
    Property = [ Property ]

    def addProperty(self, p):
        self.Property.append(p)

class ProductSection(OvfObject):

    Product = [ Product ]

class VirtualSystem(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'id' : str,
                                             'info' : str } )

    ProductSection = [ ProductSection ]

    def addProduct(self, p):
        self.ProductSection.append(p)

class ReferencesSection(OvfObject):

    File = [ FileReference ]

class Ovf(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'References', 'DiskSection' ] )

    References = ReferencesSection
    DiskSection = DiskSection
    NetworkSection = NetworkSection
    VirtualSystem = [ { 'VirtualSystem' : VirtualSystem,
                            'VirtualSystemCollection' : object } ]

    def addDisk(self, d):
        if d.fileRef not in self.References.File:
            self.addFileReference(d.fileRef)
        self.DiskSection.Disk.append(d)

    def addNetwork(self, n):
        self.NetworkSection.Network.append(n)

    def addFileReference(self, r):
        self.References.File.append(r)

    def addSystem(self, vs):
        self.VirtualSystem.append(vs)

    def toxml(self):
        schemaPath = os.path.join(os.path.dirname(__file__),
                                  "schemas/ovf-envelope.xsd")
        return self._doc.toxml(nsmap = self._doc.nameSpaceMap)

class OvfDocument(xobj.Document):

    nameSpaceMap = { 'ovf' : 'http://schemas.dmtf.org/ovf/envelope/1',
                     None : 'http://schemas.dmtf.org/ovf/envelope/1' }
    Envelope = Ovf

class NewOvf(Ovf):
    """
    Class factory to yield a new Ovf object.
    """
    def __init__(self):
        doc = OvfDocument()
        doc.Envelope = self

        self._doc = doc

        self.References = ReferencesSection()
        self.DiskSection = DiskSection()
        self.NetworkSection = NetworkSection()
        self.VirtualSystem = []

