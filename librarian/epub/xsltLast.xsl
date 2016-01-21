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

  <xsl:template match="utwor">
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
                    Ten utwór nie jest objęty majątkowym prawem autorskim i znajduje się w domenie
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
                  <xsl:for-each select="//dc:creator/text()"><xsl:value-of select="wl:person_name(.)"/>, </xsl:for-each><xsl:value-of select="//dc:title" />
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

          <xsl:call-template name="funders" />

          <xsl:if test="@data-cover-by">
            <p class="info">Okładka na podstawie: 
            <xsl:choose>
            <xsl:when test="@data-cover-source">
                <a>
                <xsl:attribute name="href">
                  <xsl:value-of select="@data-cover-source" />
                </xsl:attribute>
                <xsl:value-of select="@data-cover-by" />
                </a>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="@data-cover-by" />
            </xsl:otherwise>
            </xsl:choose>
            </p>
          </xsl:if>

          <p class="info">&#160;</p>
          <p class="minor-info">
              Plik wygenerowany dnia <span id="file_date"><xsl:value-of select="substring(date:date(), 1, 10)" /></span>.
          </p>

        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template name="editors">
    <xsl:if test="@editors">
        <p class="info">
            <xsl:text>Opracowanie redakcyjne i przypisy: </xsl:text>
            <xsl:value-of select="@editors" />.</p>
    </xsl:if>
  </xsl:template>

  <xsl:template name="funders">
    <xsl:if test="@funders">
        <p class="minor-info">Publikację ufundowali i ufundowały:
            <xsl:value-of select="@funders" />.</p>
    </xsl:if>
  </xsl:template>

  <xsl:template match="text()" mode="person">
    <xsl:value-of select="wl:person_name(.)" />
  </xsl:template>
</xsl:stylesheet>
