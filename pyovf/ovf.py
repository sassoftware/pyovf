#!/usr/bin/python
#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from lxml import etree
from xobj import xobj

class AbstractOvfObject(object):
    prefix = ''

    def __init__(self, **kwargs):
        for key, val in self.__class__.__dict__.iteritems():
            if type(val) == list:
                setattr(self, key, [])
            elif type(val) == str:
                setattr(self, key, val)
                

        for key, val in kwargs.iteritems():
            ovfKey = self.prefix + key
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

        return object.__getattribute__(self, name)            

class RasdObject(AbstractOvfObject):
    prefix = 'rasd_'

class OvfObject(AbstractOvfObject):
    prefix = 'ovf_'

class VssdObject(AbstractOvfObject):
    prefix = 'vssd_'

class Item(RasdObject):
    pass

class System(VssdObject):
    _xobj = xobj.XObjMetadata(
            elements = [ 'vssd_ElementName', 'vssd_InstanceID', 
                         'vssd_VirtualSystemType' ] )

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
            elements = [ 'ovf_Description' ],
            attributes = { "ovf_id" : str,
                           "ovf_name" : xobj.XID } )

class NetworkSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_Network' ])

    ovf_Info = str            
    ovf_Network = [ Network ]

class VirtualHardwareSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_System' , 'ovf_Item'])

    ovf_Info = str
    ovf_System = System
    ovf_Item = [ Item ]

    def addItem(self, item):
        self.ovf_Item.append(item)

class Property(OvfObject):

    _xobj = xobj.XObjMetadata(attributes = { 'ovf_key' : str,
                                             'ovf_type' : str } )

class Category(OvfObject):
    pass

class ProductSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_Product', 'ovf_Vendor',
                         'ovf_Version', 'ovf_FullVersion',
                         'ovf_ProductUrl', 'ovf_VendorUrl',
                         'ovf_Icon', 'ovf_Category', 'ovf_Property'])

    ovf_Category = [ Category ]
    ovf_Property = [ Property ]

    def addProperty(self, property):
        self.ovf_Property.append(property)

class EulaSection(OvfObject):
    
    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_License' ])

class OperatingSystemSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { 'ovf_id' : str, 'ovf_version' : str, 'vmw_osType' : str },
            elements = [ 'ovf_Info', 
                         'ovf_Description' ] )

class VirtualSystem(OvfObject):

    _xobj = xobj.XObjMetadata(
            attributes = { 'ovf_id' : str, },
            elements = [ 'ovf_Info', 
                         'ovf_EulaSection',
                         'ovf_ProductSection',
                         'ovf_OperatingSystemSection',
                         'ovf_VirtualHardwareSection', ] )

    ovf_EulaSection = EulaSection
    ovf_ProductSection = ProductSection
    ovf_OperatingSystemSection = OperatingSystemSection
    ovf_VirtualHardwareSection = [ VirtualHardwareSection ] 

    def addVirtualHardwareSection(self, vhws):
        self.ovf_VirtualHardwareSection.append(vhws)

class ResourceAllocationSection(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_Item' ])

    ovf_Item = [ Item ]            

    def addItem(self, item):
        self.ovf_Item.append(item)

class VirtualSystemCollection(OvfObject):
    
    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_Info', 'ovf_ResourceAllocationSection', 
                         'ovf_VirtualSystem' ],
            attributes = { 'ovf_id' : str})

    ovf_Info = str
    ovf_ResourceAllocationSection = ResourceAllocationSection
    ovf_VirtualSystem = [ VirtualSystem ]

    def addVirtualSystem(self, vs):
        self.ovf_VirtualSystem.append(vs)

class ReferencesSection(OvfObject):

    ovf_File = [ FileReference ]

class Ovf(OvfObject):

    _xobj = xobj.XObjMetadata(
            elements = [ 'ovf_References', 
                         'ovf_DiskSection',
                         'ovf_NetworkSection',
                         'ovf_VirtualSystemCollection'
                         ] )

    ovf_References = ReferencesSection
    ovf_DiskSection = DiskSection
    ovf_NetworkSection = NetworkSection
    ovf_VirtualSystemCollection = VirtualSystemCollection

    def addDisk(self, d):
        if d.ovf_fileRef not in self.ovf_References.ovf_File:
            self.addFileReference(d.ovf_fileRef)
        self.ovf_DiskSection.ovf_Disk.append(d)

    def addNetwork(self, n):
        self.ovf_NetworkSection.ovf_Network.append(n)

    def addFileReference(self, r):
        self.ovf_References.ovf_File.append(r)

    def addVirtualSystem(self, vs):
        self.ovf_VirtualSystemCollection.ovf_VirtualSystem.append(vs)

    def toxml(self):
        return self._doc.toxml(nsmap = self._doc.nameSpaceMap)
