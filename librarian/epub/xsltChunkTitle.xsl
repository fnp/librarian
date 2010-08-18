<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="html" version="1.0" encoding="utf-8" />
  <xsl:output doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN" />

  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <link rel="stylesheet" href="style.css" type="text/css" />
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>
          <xsl:text>Strona tytułowa</xsl:text>
        </title>
      </head>
      <body>
        <div id="book-text" xmlns="http://www.w3.org/1999/xhtml">
          <div class='title-page'>
            <xsl:apply-templates select="//dc:title" mode="poczatek"/>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." disable-output-escaping="yes" />
  </xsl:template>

  <xsl:template match="node()" mode="poczatek">
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template match="dc:title" mode="poczatek" >
    <h1 class="title" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h1>
  </xsl:template>

</xsl:stylesheet>