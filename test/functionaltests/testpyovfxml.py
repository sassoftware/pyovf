
newXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References/>
  <DiskSection/>
  <NetworkSection/>
</Envelope>
"""

fileXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References>
    <File id="testFile"/>
  </References>
  <DiskSection/>
  <NetworkSection/>
</Envelope>
"""

diskXmlNoRef = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References>
    <File id="testFile0"/>
  </References>
  <DiskSection>
    <Disk fileRef="testFile0"/>
  </DiskSection>
  <NetworkSection/>
</Envelope>
"""

diskXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References>
    <File id="testFile0"/>
    <File id="testFile"/>
  </References>
  <DiskSection>
    <Disk fileRef="testFile0"/>
    <Disk fileRef="testFile"/>
  </DiskSection>
  <NetworkSection/>
</Envelope>
"""

diskWithFormatXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References>
    <File id="testFile"/>
  </References>
  <DiskSection>
    <Disk fileRef="testFile" format="http://example.com/format.html"/>
  </DiskSection>
  <NetworkSection/>
</Envelope>
"""

diskWithCompressedFormatXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References>
    <File id="testFile"/>
  </References>
  <DiskSection>
    <Disk fileRef="testFile" format="http://example.com/format.html#compressed"/>
  </DiskSection>
  <NetworkSection/>
</Envelope>
"""

systemPropertyXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References/>
  <DiskSection/>
  <VirtualSystem>
    <ProductSection>
      <Property>propertyKey</Property>
    </ProductSection>
  </VirtualSystem>
  <NetworkSection/>
</Envelope>
"""

networkXml = """<?xml version='1.0' encoding='UTF-8'?>
<Envelope>
  <References/>
  <DiskSection/>
  <NetworkSection>
    <Network id="testNetwork"/>
  </NetworkSection>
</Envelope>
"""
