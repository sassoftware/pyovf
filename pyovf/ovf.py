#!/usr/bin/python

from lxml import etree

from xobj import xobj

class OvfObject(object):

    prefix = 'ovf_'

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

    def __setattr__(self, name, value):
        if not name.startswith('_') and not name.startswith(self.prefix):
            name = self.prefix + name

        object.__setattr__(self, name, value)            
        
    def __getattr__(self, name):        
        if not name.startswith('_') and not name.startswith(self.prefix):
            name = self.prefix + name

        object.__getattribute__(self, name)            

class AbstractDiskFormat(object):

    def __str__(self):
        if self.ovf_compressed:
            return self.ovf_format + "#compressed"

        return self.ovf_format

    def __init__(self, compressed = False):
        assert(self.ovf_format)
        self.ovf_compressed = compressed

class DiskFormatVmdk(AbstractDiskFormat):

    ovf_format = "http://www.vmware.com/specifications/vmdk.html"

class DiskFormat(AbstractDiskFormat):

    def __init__(self, s, compressed = False):
        if s.endswith('#compressed'):
            # we shouldn't parse this and get it passed in
            assert(not compressed)
            compressed = True
            s = s[:-11]

        self.ovf_format = s
        AbstractDiskFormat.__init__(self, compressed)

    def __str__(self):
        if self.ovf_compressed:
            return self.ovf_format + "#compressed"

        return self.ovf_format

class Disk(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = {
                           'ovf_capacity' : long,
                           'ovf_capacityAllocationUnits' : long,
                           'ovf_diskId' : str,
                           'ovf_fileRef' : xobj.XIDREF,
                           'ovf_format' : DiskFormat,
                           'ovf_parentRef' : str,
                           'ovf_populatedSize' : long,
                         } )

class FileReference(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = {
                           "ovf_chunkSize" : long,
                           "ovf_compression" : str,
                           "ovf_href" : str,
                           "ovf_id" : str,
                           "ovf_size" : long,
                         } )

class DiskSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_Disk' ])

    ovf_Info = str
    ovf_Disk = [ Disk ]

class Network(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { "ovf_id" : str,
                           "ovf_name" : xobj.XID } )

class NetworkSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_Network' ])

    ovf_Info = str            
    ovf_Network = [ object ]

class Property(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_key' : str,
                                             'ovf_type' : str } )

class Product(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_FullVersion', 'ovf_Property' ])

    ovf_Info = str
    ovf_FullVersion = str
    ovf_Property = [ Property ]

    def addProperty(self, p):
        self.ovf_Property.append(p)

class ProductSection(OvfObject):

    ovf_Product = [ Product ]

class VirtualSystem(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_id' : str,
                                             'ovf_info' : str } )

    ovf_ProductSection = [ ProductSection ]

    def addProduct(self, p):
        self.ovf_ProductSection.append(p)

class ReferencesSection(OvfObject):

    ovf_File = [ FileReference ]

class Ovf(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_References', 'ovf_DiskSection' ] )

    ovf_References = ReferencesSection
    ovf_DiskSection = DiskSection
    ovf_NetworkSection = NetworkSection
    ovf_VirtualSystem = [ { 'ovf_VirtualSystem' : VirtualSystem,
                            'ovf_VirtualSystemCollection' : object } ]

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
        return self._doc.toxml(nsmap = self._doc.nameSpaceMap)
