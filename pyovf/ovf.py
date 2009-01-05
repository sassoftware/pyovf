from xobj import xobj
import os

class pDisk(object):

    _xobj = xobj.XObjMetadata(
            attributes = { 'ovf_diskId' : xobj.XIDREF,
                           'ovf_capacity' : long,
                           'ovf_populatedSize' : long } )

class Disk(pDisk):

    def __init__(self, disk, capacity, format, populatedSize):
        self.ovf_diskId = disk
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

class NetworkSection(object):

    ovf_Network = [ object ]

class ProductSection(object):

    ovf_Property = [ object ]

class VirtualSystem(object):

    ovf_ProductSection = [ ProductSection ]

class ReferencesSection(object):

    ovf_File = [ pFileReference ]

class Ovf(object):

    ovf_References = ReferencesSection
    ovf_DiskSection = DiskSection
    ovf_NetworkSection = NetworkSection
    ovf_VirtualSystem = [ VirtualSystem ]

    def addDisk(self, d):
        if d.ovf_diskId not in self.ovf_References.ovf_File:
            self.addFileReference(d.ovf_diskId)
        self.ovf_DiskSection.ovf_Disk.append(d)

    def addFileReference(self, r):
        self.ovf_References.ovf_File.append(r)

    def toxml(self):
        schemaPath = os.path.join(os.path.dirname(__file__),
                                  "schemas/ovf-envelope.xsd")
        return self._doc.toxml()

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
