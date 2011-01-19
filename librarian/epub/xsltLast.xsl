<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wl="http://wolnelektury.pl/functions"
    xmlns:date="http://exslt.org/dates-and-times">
  <xsl:output method="html" version="1.0" encoding="utf-8" />
  <xsl:output doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN" />

  <xsl:template match="/">
    <html>
      <head>
        <link rel="stylesheet" href="style.css" type="text/css" />
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>
          <xsl:text>Strona redakcyjna</xsl:text>
        </title>
      </head>
      <body>
        <div id="book-text" >
          <p class="info">
              <xsl:choose>
                  <xsl:when test="//dc:rights.license">
                      Ten utwór jest udostepniony na licencji
                      <a>
                          <xsl:attribute name="href">
                              <xsl:value-of select="//dc:rights.license" />
                          </xsl:attribute>
                          <xsl:value-of select="//dc:rights" />
                      </a>
                  </xsl:when>
                  <xsl:otherwise>
                    Ten utwór nie jest chroniony prawem autorskim i znajduje się w domenie
                    publicznej, co oznacza że możesz go swobodnie wykorzystywać, publikować
                    i rozpowszechniać. Jeśli utwór opatrzony jest dodatkowymi materiałami
                    (przypisy, motywy literackie etc.), które podlegają prawu autorskiemu, to
                    te dodatkowe materiały udostępnione są na licencji
                    <a href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons
                    Uznanie Autorstwa – Na Tych Samych Warunkach 3.0 PL</a>.
                  </xsl:otherwise>
              </xsl:choose>
          </p>

          <p class="info">Źródło: <a>
              <xsl:attribute name="href">
                  <xsl:value-of select="//dc:identifier.url" />
              </xsl:attribute>
              <xsl:attribute name="title">
                  <xsl:value-of select="wl:person_name(//dc:creator/text())" />, <xsl:value-of select="//dc:title" />
              </xsl:attribute>
              <xsl:value-of select="//dc:identifier.url" />
          </a></p>

          <xsl:if test="//dc:source" >
            <p class="info">Tekst opracowany na podstawie: <xsl:value-of select="//dc:source" /></p>
          </xsl:if>

          <xsl:if test="//dc:description" >
            <p class="info"><xsl:value-of select="//dc:description" /></p>
          </xsl:if>

          <xsl:call-template name="editors" />

          <p class="info">&#160;</p>
          <p class="minor info">
              Plik wygenerowany dnia <span id="file_date"><xsl:value-of select="substring(date:date(), 1, 10)" /></span>.
          </p>

        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." disable-output-escaping="yes" />
  </xsl:template>

  <xsl:template name="editors">
    <xsl:if test="//dc:contributor.editor|//dc:contributor.technical_editor">
        <p class="info">
            <xsl:text>Opracowanie redakcyjne i przypisy: </xsl:text>
            <xsl:for-each select="//dc:contributor.editor|//dc:contributor.technical_editor">
                <xsl:if test="position() != 1">, </xsl:if>
                <xsl:apply-templates mode="person" />
            </xsl:for-each>.
        </p>
    </xsl:if>
  </xsl:template>

  <xsl:template match="dc:contributor.editor|dc:contributor.technical_editor">
      <br /><xsl:apply-templates mode='person' />
  </xsl:template>

  <xsl:template match="text()" mode="person">
    <xsl:value-of select="wl:person_name(.)" />
  </xsl:template>
</xsl:stylesheet>