<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="html" version="1.0" encoding="utf-8" />
  <xsl:output doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN" />

  <xsl:template match="/" >
    <xsl:element name="html" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:element name="head">
        <link rel="stylesheet" href="style.css" type="text/css" />
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>
	  <xsl:value-of select="//dc:title"/>
        </title>
      </xsl:element>
      <xsl:element name="body" xmlns="http://www.w3.org/1999/xhtml">
        <xsl:element name="div" xmlns="http://www.w3.org/1999/xhtml">
          <xsl:attribute name="id">book-text</xsl:attribute>

          <xsl:if test="//nazwa_utworu">
            <!--h1 xmlns="http://www.w3.org/1999/xhtml"-->
              <xsl:apply-templates select="//dzielo_nadrzedne" mode="poczatek"/>
              <xsl:apply-templates select="//autor_utworu" mode="poczatek"/>
              <xsl:apply-templates select="//nazwa_utworu" mode="poczatek"/>
              <xsl:apply-templates select="//podtytul" mode="poczatek"/>
            <!--/h1-->
          </xsl:if>
          <xsl:apply-templates />
        </xsl:element>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <!--===========================================================-->
  <!-- Tagi BLOKOWE -->
  <!--===========================================================-->

  <xsl:template match="nota">
    <xsl:if test="not(@typ!='redp' or @typ!='redk')">
      <div class="note" xmlns="http://www.w3.org/1999/xhtml">
	<xsl:apply-templates />
      </div>
    </xsl:if>
  </xsl:template>

  <xsl:template match="lista_osob" >
    <div class="person-list" xmlns="http://www.w3.org/1999/xhtml">
      <div class="h3" xmlns="http://www.w3.org/1999/xhtml">
        <xsl:apply-templates select="child::naglowek_listy" />
      </div>
      <ol xmlns="http://www.w3.org/1999/xhtml">
        <xsl:apply-templates select="lista_osoba" />
      </ol>
    </div>
  </xsl:template>

  <xsl:template match="dedykacja">
    <div class="dedication" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="kwestia">
    <div class="kwestia" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates select="strofa|akapit|didaskalia|akap " />
    </div>
  </xsl:template>

  <xsl:template match="dlugi_cytat|poezja_cyt">
    <div class="block" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="motto">
    <div class="motto" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <!--===========================================================-->
  <!-- Tagi PARAGRAFOWE -->
  <!--===========================================================-->

  <xsl:template match="autor_utworu" mode="poczatek">
    <h2 class="author" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="autor_utworu" />
  <xsl:template match="autor_rozdzialu"/>

  <xsl:template match="dzielo_nadrzedne" mode="poczatek">
    <h2 class="collection" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="dzielo_nadrzedne" />

  <xsl:template match="nazwa_utworu" mode="poczatek" >
    <h2 class="intitle" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="nazwa_utworu" />

  <xsl:template match="podtytul" mode="poczatek">
    <h2 class="insubtitle" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="podtytul" />

  <xsl:template match="naglowek_czesc|srodtytul">
    <h2 class="h2" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="naglowek_akt">
    <h2 class="h2" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="naglowek_scena">
    <a xmlns="http://www.w3.org/1999/xhtml"></a>
    <h2 class="h3" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="naglowek_podrozdzial">
    <a xmlns="http://www.w3.org/1999/xhtml"></a>
    <h2 class="h4" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="naglowek_podpodrozdzial">
    <a xmlns="http://www.w3.org/1999/xhtml"></a>
    <div class="p" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  
  <xsl:template match="autor_rozdzialu">
  </xsl:template>

  <xsl:template match="naglowek_rozdzial">
    <h2 class="h2" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
    <div class="info" xmlns="http://www.w3.org/1999/xhtml">    
      <xsl:if test="name(following-sibling::*[1])='autor_rozdzialu'">
	<xsl:value-of select="following-sibling::*[1]/text()"/>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:template match="naglowek_osoba">
    <h2 class="h4" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="miejsce_czas">
    <div class="place-and-time" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="didaskalia">
    <div class="didaskalia" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="akap|akap_dialog|akap_cd">
    <p class="paragraph" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </p>
  </xsl:template>

  <xsl:template match="strofa">
    <div class="stanza" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div><div class='stanza-spacer' xmlns="http://www.w3.org/1999/xhtml">&#160;</div>
  </xsl:template>

  <xsl:template match="wers_normalny">
    <div class="verse" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    &#160;</div>
  </xsl:template>

  <xsl:template match="wers_akap">
    <div class="verse" style="margin-left: 1em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    &#160;</div>
  </xsl:template>

  <xsl:template match="wers_wciety">
    <div class="verse" style='margin-left:1em;' xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    &#160;</div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ!='']">
    <div class="verse" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:attribute name="style">
          margin-left: <xsl:value-of select="@typ" />em;
      </xsl:attribute>
      <xsl:apply-templates />
    &#160;</div>
  </xsl:template>

  <xsl:template match="wers_cd">
    <div class="verse" style="margin-left: 12em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    &#160;</div>
  </xsl:template>

  <xsl:template match="motto_podpis">
    <div class="motto_podpis" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="lista">
    <ul>
      <xsl:apply-templates />
    </ul>
  </xsl:template>

  <xsl:template match="punkt">
    <li><xsl:apply-templates /></li>
  </xsl:template>

  <xsl:template match="www">
    <a>
      <xsl:attribute name="href">
	<xsl:value-of select="text()"/>
      </xsl:attribute>
      <xsl:value-of select="text()"/>
    </a>
  </xsl:template>

  <xsl:template match="link">
    <a>
      <xsl:attribute name="href">
	<xsl:value-of select="@url"/>
      </xsl:attribute>
      <xsl:value-of select="text()"/>
    </a>
  </xsl:template>


  <!--===========================================================-->
  <!-- Tagi LINIOWE -->
  <!--===========================================================-->

  <xsl:template match="slowo_obce">
    <em class="foreign-word" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </em>
  </xsl:template>

  <xsl:template match="mat" >
    <em class="math" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </em>
  </xsl:template>

  <xsl:template match="didask_tekst" >
    <em class="didaskalia" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </em>
  </xsl:template>

  <xsl:template match="tytul_dziela" >
    <em class="book-title" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:if test="@typ = '1'" >„</xsl:if>
      <xsl:apply-templates />
      <xsl:if test="@typ = '1'">”</xsl:if>
    </em>
  </xsl:template>

  <xsl:template match="wyroznienie" >
    <em class="author-emphasis" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </em>
  </xsl:template>

  <xsl:template match="osoba" >
    <em class="person" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </em>
  </xsl:template>

  <xsl:template match="naglowek_listy"  >
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="lista_osoba" >
    <li xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </li>
  </xsl:template>

  <!--===========================================================-->
  <!-- Tagi STANDALONE -->
  <!--===========================================================-->

  <xsl:template match="sekcja_swiatlo">
    <p class="spacer" xmlns="http://www.w3.org/1999/xhtml">&#160;</p>
  </xsl:template>

  <xsl:template match="sekcja_asterysk">
    <p class="spacer-asterisk" xmlns="http://www.w3.org/1999/xhtml">*</p>
  </xsl:template>

  <xsl:template match="separator_linia">
    <hr class="spacer-line" xmlns="http://www.w3.org/1999/xhtml"></hr>
  </xsl:template>

  <!--===========================================================-->
  <!-- Tagi SPECJALNE -->
  <!--===========================================================-->

  <xsl:template match="motyw" />

  <!--===========================================================-->
  <!-- Tagi IGNOROWANE -->
  <!--===========================================================-->

  <xsl:template match="extra" />

  <xsl:template match="pe|pa|pr|pt" >
    <a id="anchor-{.}" class="anchor" href="annotations.html#annotation-{.}"
       xmlns="http://www.w3.org/1999/xhtml">[<xsl:apply-templates />]</a>
  </xsl:template>

  <xsl:template match="uwaga" />

  <xsl:template match="nota_red" />

  <!--pominięcie tych metadanych-->
  <xsl:template match="rdf:RDF" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" />

  <xsl:template match="latex" />

  <!--===========================================================-->
  <!-- Tagi TEKSTOWE -->
  <!--===========================================================-->

  <xsl:template match="text()"  >
    <xsl:value-of select="." />
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." />
  </xsl:template>

  <!--===========================================================-->
  <!-- Tagi ILUSTRACJE -->
  <!--===========================================================-->
  <xsl:template match="ilustr" >
    <img>
      <xsl:attribute name="src"><xsl:value-of select="@src"/>.<xsl:choose><xsl:when test="@extbitmap"><xsl:value-of select="@extbitmap"/></xsl:when><xsl:otherwise><xsl:value-of select="@ext"/></xsl:otherwise></xsl:choose></xsl:attribute>
    </img>
  </xsl:template>
  

</xsl:stylesheet>
