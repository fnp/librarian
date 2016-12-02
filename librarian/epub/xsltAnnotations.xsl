<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="utf-8" />
  <xsl:output doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN" />

  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <link rel="stylesheet" href="style.css" type="text/css" />
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>
          <xsl:text>Przypisy</xsl:text>
        </title>
      </head>
      <body>
        <div id="book-text" xmlns="http://www.w3.org/1999/xhtml">
          <div id="footnotes" xmlns="http://www.w3.org/1999/xhtml">
            <h2 xmlns="http://www.w3.org/1999/xhtml">
              Przypisy:
            </h2>
            <xsl:apply-templates mode="przypis" />
          </div>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template match="pa|pe|pr|pt" mode="przypis">
    <p id="annotation-{@number}" class="annotation" xmlns="http://www.w3.org/1999/xhtml"><a href="part{@part}.html#anchor-{@number}" xmlns="http://www.w3.org/1999/xhtml"><xsl:value-of select="@number" /></a>. <xsl:apply-templates /><xsl:if test="name()='pa'"> [przypis autorski]</xsl:if><xsl:if test="name()='pt'"> [przypis tłumacza]</xsl:if><xsl:if test="name()='pr'"> [przypis redakcyjny]</xsl:if><xsl:if test="name()='pe'"> [przypis edytorski]</xsl:if></p>
    <xsl:text>&#xa;</xsl:text>
  </xsl:template>

  <xsl:template match="slowo_obce">
    <em class="foreign-word" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates select="text()" />
    </em>
  </xsl:template>

  <xsl:template match="akap|akap_cd">
    <p class="paragraph" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </p>
  </xsl:template>

  <xsl:template match="strofa">
    <div class="stanza" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="tytul_dziela" >
    <em class="book-title" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:if test="@typ = '1'" >„</xsl:if>
      <xsl:apply-templates />
      <xsl:if test="@typ = '1'">”</xsl:if>
    </em>
  </xsl:template>

  <xsl:template match="wers_normalny">
    <p class="verse" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </p>
  </xsl:template>

</xsl:stylesheet>
