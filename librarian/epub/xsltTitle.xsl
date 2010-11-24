<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wl="http://wolnelektury.pl/functions">
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
            <xsl:choose>
              <xsl:when test="//autor_utworu | //nazwa_utworu">
                <xsl:apply-templates select="//autor_utworu" mode="poczatek"/>
                <xsl:apply-templates select="//nazwa_utworu | //podtytul | //dzielo_nadrzedne" mode="poczatek"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:apply-templates select="//dc:creator" mode="poczatek"/>
                <xsl:apply-templates select="//dc:title | //podtytul | //dzielo_nadrzedne" mode="poczatek"/>
              </xsl:otherwise>
            </xsl:choose>
          </div>
          <p class="info">Publikacja zrealizowana w ramach projektu WolneLektury.pl</p>
          <xsl:if test="//dc:source" >
            <p class="info">Na podstawie: <xsl:value-of select="//dc:source" /></p>
          </xsl:if>
          <p class="info">
            <img src="logo_wolnelektury.png" alt="WolneLektury.pl" />
          </p>
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

  <xsl:template match="dc:creator" mode="poczatek">
    <div class="author" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="dc:creator/text()">
    <div class="author" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:value-of select="wl:person_name(.)" />
    </div>
  </xsl:template>

  <xsl:template match="autor_utworu" mode="poczatek">
    <div class="author" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="dzielo_nadrzedne" mode="poczatek">
    <div class="collection" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="nazwa_utworu" mode="poczatek" >
    <h1 class="title" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h1>
  </xsl:template>

  <xsl:template match="dc:title" mode="poczatek" >
    <h1 class="title" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h1>
  </xsl:template>

  <xsl:template match="podtytul" mode="poczatek">
    <div class="subtitle" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="pe|pa|pr|pt" />

  <xsl:template match="extra" />

  <xsl:template match="pe|pa|pr|pt" />

  <xsl:template match="extra" />

  <xsl:template match="motyw" />

</xsl:stylesheet>