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


import os
from lxml import etree

from pyovf import ovf
from xobj import xobj

class OvfDocument(xobj.Document):

    nameSpaceMap = { 'ovf' : 'http://schemas.dmtf.org/ovf/envelope/1',
                     'rasd' : 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData',
                     'vssd' : 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData',
                     'cim' : 'http://schemas.dmtf.org/wbem/wscim/1/common',
                     'vmw': 'http://www.vmware.com/schema/ovf',
                   }
    schemaFile = os.path.join(os.path.dirname(__file__),
                              "schemas/ovf-envelope.xsd")
    ovf_Envelope = ovf.Ovf

    def __init__(self, *args, **kwargs):
        schemaObj = etree.XMLSchema(file = self.schemaFile)
        kwargs['schema'] = schemaObj
        xobj.Document.__init__(self, *args, **kwargs)

class NewOvf(ovf.Ovf):
    """
    Class factory to yield a new Ovf object.
    """
    def __init__(self):
        doc = OvfDocument()
        doc.ovf_Envelope = self

        self._doc = doc

        self.ovf_References = ovf.ReferencesSection()
        self.ovf_DiskSection = ovf.DiskSection()
        self.ovf_DiskSection.ovf_Info = 'Disk Section Info'
        self.ovf_NetworkSection = ovf.NetworkSection()
        self.ovf_NetworkSection.ovf_Info = 'Network Section Info'
        self.ovf_VirtualSystemCollection = ovf.VirtualSystemCollection()
        self.ovf_VirtualSystemCollection.ovf_Info = \
            'Virtual System Collection Info'
        self.ovf_VirtualSystemCollection.ovf_ResourceAllocationSection = \
            ovf.ResourceAllocationSection()
        self.ovf_VirtualSystemCollection.ovf_ResourceAllocationSection.ovf_Info = 'Resource Allocation Section Info'

        network = ovf.Network(name='Network Name')
        network.ovf_Description = 'Network Description'
        self.ovf_NetworkSection.ovf_Network.append(network)

def OvfFile(f):
    schemaPath = os.path.join(os.path.dirname(__file__),
                              "schemas/ovf-envelope.xsd")
    doc = xobj.parsef(f, documentClass=OvfDocument, schemaf=schemaPath)
    ovf = doc.ovf_Envelope
    ovf._doc = doc
    return ovf
