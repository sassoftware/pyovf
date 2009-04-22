#!/usr/bin/python

import os
from lxml import etree

from pyovf import ovf
from xobj import xobj

class OvfDocument(xobj.Document):

    nameSpaceMap = { 'ovf' : 'http://schemas.dmtf.org/ovf/envelope/1'}
                     # None : 'http://schemas.dmtf.org/ovf/envelope/1' }
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
        self.ovf_NetworkSection = ovf.NetworkSection()
        # self.ovf_VirtualSystem = [ { 'ovf_VirtualSystem' : ovf.VirtualSystem,
                                     # 'ovf_VirtualSystemCollection' : object } ]
        self.ovf_VirtualSystem = []

def OvfFile(f):
    schemaPath = os.path.join(os.path.dirname(__file__),
                              "schemas/ovf-envelope.xsd")
    doc = xobj.parsef(f, documentClass=OvfDocument, schemaf=schemaPath)
    ovf = doc.ovf_Envelope
    ovf._doc = doc
    return ovf
