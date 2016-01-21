<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://wolnelektury.pl/functions">
  <xsl:output method="html" version="1.0" omit-xml-declaration="no" />

  <xsl:template match="/">
    <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
      <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:opf="http://www.idpf.org/2007/opf">
        <xsl:apply-templates select="//dc:title" />
        <dc:language>
          <xsl:apply-templates select="//dc:language" mode="language" />
        </dc:language>
        <dc:identifier id="BookId" opf:scheme="URI">
          <xsl:apply-templates select="//dc:identifier.url" />
        </dc:identifier>
        <dc:subject>
          <xsl:apply-templates select="//dc:identifier.url" />
        </dc:subject>
        <dc:creator opf:role="aut">
          <xsl:attribute name="opf:file-as">
            <xsl:value-of select="//dc:creator" />
          </xsl:attribute>
          <xsl:for-each select="//dc:creator/text()">
              <xsl:value-of select="wl:person_name(.)"/>
              <xsl:if test="not(position() = last())">, </xsl:if>
          </xsl:for-each>
        </dc:creator>
        <dc:publisher>
          <xsl:apply-templates select="//dc:publisher" />
        </dc:publisher>
        <dc:date opf:event="publication">
          <xsl:apply-templates select="//dc:date" />
        </dc:date>
      </metadata>
      <manifest>
        <item id="toc" href="toc.ncx" media-type="application/x-dtbncx+xml" />
        <item id="style" href="style.css" media-type="text/css" />
        <item id="titlePage" href="title.html" media-type="application/xhtml+xml" />
        <item id="logo_wolnelektury" href="logo_wolnelektury.png" media-type="image/png" />
        <item id="jedenprocent" href="jedenprocent.png" media-type="image/png" />
      </manifest>
      <spine toc="toc">
        <itemref idref="titlePage" />
      </spine>
      <guide>
        <reference type="text" title="Początek" href="part1.html" />
      </guide>
    </package>
  </xsl:template>

  <xsl:template match="dc:title" >
    <dc:title>
      <xsl:value-of select="." />
    </dc:title>
  </xsl:template>
  
  <xsl:template match="text()" mode="person">
    <xsl:value-of select="wl:person_name(.)" />
  </xsl:template>
  
  <xsl:template match="text()" mode="language">
    <xsl:value-of select="wl:lang_code_3to2(.)" />
  </xsl:template>

</xsl:stylesheet>
