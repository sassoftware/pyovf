diskWithCompressedFormatXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
    <ovf:Disk ovf:diskId="testDiskId" ovf:capacity="testCapacity" ovf:fileRef="testFileId" ovf:format="http://example.com/format.html#compressed"/>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

diskWithFormatXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
    <ovf:Disk ovf:diskId="testDiskId" ovf:capacity="testCapacity" ovf:fileRef="testFileId" ovf:format="http://example.com/format.html"/>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

diskWithFormatXml2 = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId2"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
    <ovf:Disk ovf:diskId="testDiskId" ovf:capacity="testCapacity" ovf:fileRef="testFileId" ovf:format="http://example.com/format.html"/>
    <ovf:Disk ovf:diskId="testDiskId" ovf:capacity="testCapacity" ovf:fileRef="testFileId2" ovf:format="http://example.com/format.html"/>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

fileXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

networkXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
    <ovf:Network ovf:id="testNetworkId" ovf:name="testNetworkName"/>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

newXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

systemPropertyXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
    <ovf:VirtualSystem ovf:id="testVirtualSystemId">
      <ovf:Info>testVirtualSystemInfo</ovf:Info>
      <ovf:ProductSection>
        <ovf:Info>testProductInfo</ovf:Info>
        <ovf:Property ovf:key="propertyKey" ovf:type="string"/>
      </ovf:ProductSection>
    </ovf:VirtualSystem>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

ovfFileXml = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:id="testNetworkId" ovf:name="testNetworkName"/>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>testVirtualSystemCollectionInfo</ovf:Info>
    <ovf:VirtualSystem ovf:id="testVirtualSystemId">
      <ovf:Info>testVirtualSystemInfo</ovf:Info>
      <ovf:ProductSection>
        <ovf:Info>testProductInfo</ovf:Info>
        <ovf:Property ovf:key="propertyKey" ovf:type="string"/>
      </ovf:ProductSection>
    </ovf:VirtualSystem>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""

newXml2 = """\
<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:vssd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData" xmlns:rasd="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData" xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1" xmlns:cim="http://schemas.dmtf.org/wbem/wscim/1/common">
  <ovf:References>
    <ovf:File ovf:href="file" ovf:id="file1"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>disk section info</ovf:Info>
    <ovf:Disk ovf:diskId="vmdisk1" ovf:capacity="0" ovf:fileRef="file1" ovf:format="http://www.vmware.com/interfaces/specifications/vmdk.html#sparse"/>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>network section info</ovf:Info>
    <ovf:Network ovf:name="Network Name">
      <ovf:Description>Network Description</ovf:Description>
    </ovf:Network>
  </ovf:NetworkSection>
  <ovf:VirtualSystemCollection ovf:id="testVirtualSystemCollectionId">
    <ovf:Info>Virtual System Collection Info</ovf:Info>
    <ovf:ResourceAllocationSection>
      <ovf:Info>Resource Allocation Section Info</ovf:Info>
    </ovf:ResourceAllocationSection>
    <ovf:VirtualSystem ovf:id="newId">
      <ovf:Info>newInfo</ovf:Info>
      <ovf:VirtualHardwareSection>
        <ovf:Info>testVirtualHardwareSectionInfo</ovf:Info>
        <ovf:System>
          <vssd:ElementName>testElementName</vssd:ElementName>
          <vssd:InstanceID>testInstanceID</vssd:InstanceID>
          <vssd:VirtualSystemType>testVirtualSystemType</vssd:VirtualSystemType>
        </ovf:System>
        <ovf:Item>
          <rasd:Caption>Virtual CPU</rasd:Caption>
          <rasd:Description>Number of virtual CPUs</rasd:Description>
          <rasd:ElementName>some virt cpu</rasd:ElementName>
          <rasd:InstanceID>1</rasd:InstanceID>
          <rasd:ResourceType>3</rasd:ResourceType>
          <rasd:VirtualQuantity>1</rasd:VirtualQuantity>
        </ovf:Item>
        <ovf:Item>
          <rasd:AllocationUnits>MegaBytes</rasd:AllocationUnits>
          <rasd:Caption>256 MB of memory</rasd:Caption>
          <rasd:Description>Memory Size</rasd:Description>
          <rasd:ElementName>some mem size</rasd:ElementName>
          <rasd:InstanceID>2</rasd:InstanceID>
          <rasd:ResourceType>4</rasd:ResourceType>
          <rasd:VirtualQuantity>256</rasd:VirtualQuantity>
        </ovf:Item>
      </ovf:VirtualHardwareSection>
    </ovf:VirtualSystem>
  </ovf:VirtualSystemCollection>
</ovf:Envelope>
"""
