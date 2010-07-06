<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="utf-8" />
  <xsl:output doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.1//EN" />

  <xsl:template match="/" >
    <xsl:element name="html" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:element name="head">
        <link rel="stylesheet" href="style.css" type="text/css" />
        <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
        <title>
          WolneLektury.pl
        </title>
      </xsl:element>
      <xsl:element name="body" xmlns="http://www.w3.org/1999/xhtml">
        <xsl:element name="div" xmlns="http://www.w3.org/1999/xhtml">
          <xsl:attribute name="id">book-text</xsl:attribute>
          <xsl:if test="//nazwa_utworu">
            <!--h1 xmlns="http://www.w3.org/1999/xhtml"-->
              <xsl:apply-templates select=" //nazwa_utworu" mode="poczatek"/>
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
    <div class="note" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
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

  <xsl:template match="dzielo_nadrzedne" mode="poczatek">
    <h2 class="collection" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="dzielo_nadrzedne" />

  <xsl:template match="nazwa_utworu" mode="poczatek" >
    <h2 class="author" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="nazwa_utworu" />

  <xsl:template match="podtytul" mode="poczatek">
    <h2 class="subtitle" xmlns="http://www.w3.org/1999/xhtml">
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
    <a id="sub{@sub}" xmlns="http://www.w3.org/1999/xhtml"></a>
    <h2 class="h3" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="naglowek_podrozdzial">
    <a id="sub{@sub}" xmlns="http://www.w3.org/1999/xhtml"></a>
    <h2 class="h4" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
  </xsl:template>

  <xsl:template match="naglowek_rozdzial">
    <h2 class="h3" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </h2>
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
    <div class="paragraph" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="strofa">
    <div class="stanza" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_normalny">
    <div class="verse" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety">
    <div class="verse" style="padding-left: 1em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ='1']">
    <div class="verse" style="padding-left: 1em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ='2']">
    <div class="verse" style="padding-left: 2em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ='3']">
    <div class="verse" style="padding-left: 3em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ='4']">
    <div class="verse" style="padding-left: 4em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ='5']">
    <div class="verse" style="padding-left: 5em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_wciety[@typ='6']">
    <div class="verse" style="padding-left: 6em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="wers_cd">
    <div class="verse" style="padding-left: 12em;" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="motto_podpis">
    <div class="motto_podpis" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates />
    </div>
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
    <hr class="spacer" xmlns="http://www.w3.org/1999/xhtml"></hr>
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

  <!--xsl:template match="motyw" >
    <a class="theme-begin" xmlns="http://www.w3.org/1999/xhtml">
      <xsl:apply-templates select="text()" />
    </a>
  </xsl:template-->
  <xsl:template match="motyw" />

  <!--===========================================================-->
  <!-- Tagi IGNOROWANE -->
  <!--===========================================================-->

  <xsl:template match="pe|pa|pr|pt" />

  <xsl:template match="extra" />

  <xsl:template match="pe|pa|pr|pt" >
    <a id="anchor-{.}" class="anchor" href="annotations.html#annotation-{.}" 
       xmlns="http://www.w3.org/1999/xhtml">[<xsl:apply-templates />]</a>
  </xsl:template>

  <xsl:template match="uwaga" />

  <!--pominięcie tych metadanych-->
  <xsl:template match="rdf:RDF" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" />

  <!--===========================================================-->
  <!-- Tagi TEKSTOWE -->
  <!--===========================================================-->

  <xsl:template match="text()"  >
    <xsl:value-of select="." disable-output-escaping="yes"/>
  </xsl:template>

  <xsl:template match="text()" >
    <xsl:value-of select="." disable-output-escaping="yes"/>
  </xsl:template>

</xsl:stylesheet>