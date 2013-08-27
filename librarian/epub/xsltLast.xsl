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
          <xsl:text>Credits</xsl:text>
        </title>
      </head>
      <body>
        <div id="book-text" >
	  

<p>The Future of Copyright 2.0 Contest is a~part of Future of Copyright Project supported by Trust for Civil Society in Central and Eastern Europe</p>

<!-- \includegraphics[scale=.2]<p>trust.eps} -->

<p>This book is available under the terms of Creative Commons Attribution-ShareAlike 3.0 Unported License (read more:
<a href="http://creativecommons.org/licenses/by-sa/3.0/">http://creativecommons.org/licenses/by-sa/3.0/</a>) <br/>
Published by Modern Poland Foundation, Warsaw 2013 </p>

<p>Technical editor: Paulina Choromańska <br/>
Book design: Jakub Waluchowski<br/>
Typography: Marcin Koziej </p>

<p>Modern Poland Fundation <br/>
Marszalkowska St. 84/92 app. 125 <br/>
00-514 Warsaw <br/>
tel/fax: +48 22 621-30-17 <br/>
email: fundacja@nowoczesnapolska.org.pl <br/> 
</p>

 
<p>If you wish to support our projects, feel free to make a~donation via our secure online payment service: 
<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&amp;hosted_button_id=L2CLCXHZCWYJN">PLN</a> or <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&amp;hosted_button_id=XVC8XD7DBGV6N">USD</a>
 or direct payment account number: 59 1030 0019 0109 8530 0040 5685 </p>

<p> Thank you for your support.</p>





<!--          <div class="info">
          <img src="jedenprocent.png" alt="Logo 1%" />
          <div>Przekaż 1% podatku na rozwój Wolnych Lektur.</div>
          <div>Nazwa organizacji: Fundacja Nowoczesna Polska</div>
          <div>KRS 0000070056</div>
          </div>-->

          <p class="info">&#160;</p>
          <p class="minor info">
              Generated on <span id="file_date"><xsl:value-of select="substring(date:date(), 1, 10)" /></span>.
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

  <xsl:template match="dc:contributor.editor|dc:contributor.technical_editor">
      <br /><xsl:apply-templates mode='person' />
  </xsl:template>

  <xsl:template match="text()" mode="person">
    <xsl:value-of select="wl:person_name(.)" />
  </xsl:template>
</xsl:stylesheet>
