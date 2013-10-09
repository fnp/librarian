<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wl="http://wolnelektury.pl/functions">
  <xsl:output method="html" version="1.0" encoding="utf-8" />
  <xsl:output doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN" />

  <xsl:template match="/">
    <html>
      <head>
        <link rel="stylesheet" href="style.css" type="text/css" />
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>
          <xsl:text>Strona tytułowa</xsl:text>
        </title>
      </head>
      <body>
        <div id="book-text" >
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

          <p class="info">&#160;</p>

          <xsl:call-template name="translators" />

          <xsl:if test="utwor/@working-copy">
            <p class="info">[Kopia robocza]</p>
          </xsl:if>

          <xsl:if test="not(utwor/@less-advertising)">
            <p class="info">
              <a>
                  <xsl:attribute name="href">
                      <xsl:value-of select="//dc:identifier.url" />
                  </xsl:attribute>
                  Ta lektura</a>,
              podobnie jak tysiące innych, jest dostępna on-line na stronie
              <a href="http://www.wolnelektury.pl/">wolnelektury.pl</a>.
            </p>
          </xsl:if>

          <xsl:if test="utwor/@thanks">
            <p class="info"><xsl:value-of select="utwor/@thanks" /></p>
          </xsl:if>

          <p class="info">
            Utwór opracowany został w&#160;ramach projektu<a href="http://www.wolnelektury.pl/"> Wolne Lektury</a> przez<a href="http://www.nowoczesnapolska.org.pl/"> fundację Nowoczesna Polska</a>.
          </p>

          <p class="footer info">
            <a href="http://www.wolnelektury.pl/"><img src="logo_wolnelektury.png" alt="WolneLektury.pl" /></a>
          </p>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template match="node()" mode="poczatek">
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template match="dc:creator" mode="poczatek">
    <h2 class="author">
      <xsl:apply-templates mode='person' />
    </h2>
  </xsl:template>

  <xsl:template match="dc:creator/text()">
    <h2 class="author" >
      <xsl:apply-templates mode='person' />
    </h2>
  </xsl:template>

  <xsl:template name="translators">
    <xsl:if test="//dc:contributor.translator">
        <p class="info">
            <xsl:text>tłum. </xsl:text>
            <xsl:for-each select="//dc:contributor.translator">
                <xsl:if test="position() != 1">, </xsl:if>
                <xsl:apply-templates mode="person" />
            </xsl:for-each>
        </p>
    </xsl:if>
  </xsl:template>

  <xsl:template match="text()" mode="person">
    <xsl:value-of select="wl:person_name(.)" />
  </xsl:template>

  <xsl:template match="autor_utworu" mode="poczatek">
    <h2 class="author" >
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="dzielo_nadrzedne" mode="poczatek">
    <h2 class="collection" >
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="nazwa_utworu" mode="poczatek" >
    <h1 class="title" >
      <xsl:apply-templates />
    </h1>
  </xsl:template>

  <xsl:template match="dc:title" mode="poczatek" >
    <h1 class="title" >
      <xsl:apply-templates />
    </h1>
  </xsl:template>

  <xsl:template match="podtytul" mode="poczatek">
    <h2 class="subtitle" >
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="pe|pa|pr|pt" />

  <xsl:template match="extra" />

  <xsl:template match="motyw" />

</xsl:stylesheet>
