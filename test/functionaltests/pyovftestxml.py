
newXml = """<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
  </ovf:NetworkSection>
</ovf:Envelope>
"""

fileXml = """<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
  </ovf:NetworkSection>
</ovf:Envelope>
"""

diskWithFormatXml = """<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
    <ovf:Disk ovf:diskId="testDiskId" ovf:capacity="testCapacity" ovf:fileRef="testFileId" ovf:format="http://example.com/format.html"/>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
  </ovf:NetworkSection>
</ovf:Envelope>
"""

diskWithCompressedFormatXml = """<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References>
    <ovf:File ovf:href="testFileHref" ovf:id="testFileId"/>
  </ovf:References>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
    <ovf:Disk ovf:diskId="testDiskId" ovf:capacity="testCapacity" ovf:fileRef="testFileId" ovf:format="http://example.com/format.html#compressed"/>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
  </ovf:NetworkSection>
</ovf:Envelope>
"""

systemPropertyXml = """<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
  </ovf:NetworkSection>
  <ovf:VirtualSystem ovf:id="testVirtualSystemId">
    <ovf:ProductSection>
      <ovf:Info>testProductInfo</ovf:Info>
      <ovf:Property ovf:key="propertyKey" ovf:type="string"/>
    </ovf:ProductSection>
  </ovf:VirtualSystem>
</ovf:Envelope>
"""

networkXml = """<?xml version='1.0' encoding='UTF-8'?>
<ovf:Envelope xmlns:ovf="http://schemas.dmtf.org/ovf/envelope/1">
  <ovf:References/>
  <ovf:DiskSection>
    <ovf:Info>testDiskSectionInfo</ovf:Info>
  </ovf:DiskSection>
  <ovf:NetworkSection>
    <ovf:Info>testNetworkSectionInfo</ovf:Info>
    <ovf:Network ovf:id="testNetworkId" ovf:name="testNetworkName"/>
  </ovf:NetworkSection>
</ovf:Envelope>
"""
