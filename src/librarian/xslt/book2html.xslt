<?xml version="1.0" encoding="utf-8"?>
<!--

   This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
   Copyright © Fundacja Wolne Lektury. See NOTICE for more information.

-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wl="http://wolnelektury.pl/functions"
    xmlns:dc="http://purl.org/dc/elements/1.1/" >

<xsl:output encoding="utf-8" indent="yes" omit-xml-declaration = "yes" version="2.0" />
<xsl:strip-space  elements="opowiadanie powiesc dramat_wierszowany_l dramat_wierszowany_lp dramat_wspolczesny liryka_l liryka_lp wywiad"/>
<xsl:template match="utwor">
    <xsl:choose>
        <xsl:when test="@full-page">
            <html>
            <head>
                <title>Książka z serwisu WolneLektury.pl</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
		<link rel="stylesheet" type="text/css">
			<xsl:attribute name="href">
				<xsl:value-of select="$css" />
			</xsl:attribute>
		</link>
		<style>
		  .ilustr.prawo img {
		  float: right;
		  }
		  .ilustr.lewo img {
  		  float: left;
		  }
		  .ilustr.srodek {
		  text-align: center;
		  }
		  .ilustr .stop {
		  clear: both;
		  }
		  .ilustr.oblew .stop {
		  clear: none;
		  }

                  .ilustr.oblew img {
                    margin-bottom: 1em;
                  }
                  .ilustr.oblew.lewo img {
                    margin-right: 2em;
                    }
                    .ilustr.oblew.prawo img {
                    margin-left: 2em;
                    }


                    .ilustr img {
                    min-width: 200px !important;
                    }
                    @media screen and (max-width: 320px) {
                    .ilustr img {
                    width: 100% !important;
                    min-width: auto !important;
                    }
                    .ilustr.lewo img {
                    float: none;
                    }
                    .ilustr.prawo img {
                    float:none;
                    }
                    .ilustr.oblew.prawo img {
                    margin-left: 0;
                    }
                    .ilustr.oblew.lewo img{
                    margin-right: 0;
                    }
                    .ilustr .stop {
		    clear: none;
                    }

                    }
		</style>
	    </head>
            <body>
              <xsl:call-template name="book-text" />

	      <script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
	      <script src="http://malsup.github.io/min/jquery.cycle2.min.js"></script>
            </body>
            </html>
        </xsl:when>
        <xsl:otherwise>
            <xsl:call-template name="book-text" />
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="book-text">
    <div id="book-text">
        <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
        <xsl:if test="count(descendant::*[self::pe or self::pa or self::pr or self::pt or self::ptrad][not(parent::extra)])">
            <div id="footnotes">
                <h3>Przypisy</h3>
                <xsl:for-each select="descendant::*[self::pe or self::pa or self::pr or self::pt or self::ptrad][not(parent::extra)]">
                    <div>
                        <xsl:attribute name="class">fn-<xsl:value-of select="name()" /></xsl:attribute>
                        <a name="{concat('footnote-', generate-id(.))}" />
                        <a href="{concat('#anchor-', generate-id(.))}" class="annotation">[<xsl:number value="count(preceding::*[self::pa or self::pe or self::pr or self::pt or self::ptrad]) + 1" />]</a>
                        <xsl:choose>
                            <xsl:when test="count(akap|akap_cd|strofa) = 0">
                                <p><xsl:apply-templates select="text()|*" mode="inline" />
                                <xsl:if test="name()='pa'"> [przypis autorski]</xsl:if>
                                <xsl:if test="name()='pt'"> [przypis tłumacza]</xsl:if>
                                <xsl:if test="name()='pr'"> [przypis redakcyjny]</xsl:if>
                                <xsl:if test="name()='pe'"> [przypis edytorski]</xsl:if>
                                <xsl:if test="name()='ptrad'"> [przypis tradycyjny]</xsl:if>
                                </p>
                            </xsl:when>
                            <xsl:otherwise>
                              <xsl:apply-templates />
                              <p>
                                <xsl:if test="name()='pa'"> [przypis autorski]</xsl:if>
                                <xsl:if test="name()='pt'"> [przypis tłumacza]</xsl:if>
                                <xsl:if test="name()='pr'"> [przypis redakcyjny]</xsl:if>
                                <xsl:if test="name()='pe'"> [przypis edytorski]</xsl:if>
                                <xsl:if test="name()='ptrad'"> [przypis tradycyjny]</xsl:if>
                              </p>
                            </xsl:otherwise>
                        </xsl:choose>
                    </div>
                </xsl:for-each>
            </div>
        </xsl:if>
    </div>
</xsl:template>


<!-- ============================================================================== -->
<!-- = MASTER TAG                                                                 = -->
<!-- = (can contain block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ============================================================================== -->
<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny">
    <xsl:apply-templates select="nota_red" mode="special" />
    <xsl:if test="nazwa_utworu">
        <h1>
            <xsl:apply-templates select="autor_utworu|dzielo_nadrzedne|nazwa_utworu|podtytul" mode="header" />
            <xsl:call-template name="translators" />
        </h1>
    </xsl:if>
    <xsl:apply-templates />
</xsl:template>


<!-- ==================================================================================== -->
<!-- = BLOCK TAGS                                                                       = -->
<!-- = (can contain other block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ==================================================================================== -->
<xsl:template match="nota">
    <div class="note"><xsl:apply-templates /></div>
</xsl:template>

<xsl:template match="lista_osob">
    <xsl:call-template name="section-anchor"/>
    <div class="person-list">
        <h3><xsl:value-of select="naglowek_listy" /></h3>
        <ol>
            <xsl:apply-templates select="lista_osoba" />
        </ol>
    </div>
</xsl:template>

<xsl:template match="dedykacja">
    <div class="dedication"><xsl:apply-templates /></div>
</xsl:template>

<xsl:template match="ramka">
    <div class="frame"><xsl:apply-templates /></div>
</xsl:template>

<xsl:template match="kwestia">
    <div class="kwestia">
        <xsl:apply-templates select="strofa|akap|didaskalia" />
    </div>
</xsl:template>

<xsl:template match="dlugi_cytat|poezja_cyt">
    <blockquote><xsl:apply-templates /></blockquote>
</xsl:template>

<xsl:template match="motto">
    <xsl:call-template name="section-anchor"/>
    <div class="motto">
      <xsl:call-template name="block-args" />
      <xsl:apply-templates />
    </div>
</xsl:template>

<xsl:template match="ilustr" mode="inline">
    <xsl:apply-templates select="."/>
</xsl:template>

<xsl:template match="ilustr">
  <div>
    <xsl:call-template name="block-args" />

    <xsl:attribute name="class">
      <xsl:text>ilustr </xsl:text>
      <xsl:value-of select="@wyrownanie"/>
      <xsl:if test="@oblew">
        <xsl:text> oblew</xsl:text>
      </xsl:if>
    </xsl:attribute>
    
    <img>
      <xsl:attribute name="src">
        <xsl:value-of select="@src" />
      </xsl:attribute>
      <xsl:attribute name="srcset">
        <xsl:value-of select="@srcset" />
      </xsl:attribute>
      <xsl:attribute name="sizes">
        (min-width: 718px) 600px,
        (min-width: 600px) calc(100vw - 118px),
        (min-width: 320px) calc(100vw - 75px),
        (min-width: 15em) calc(100wv - 60px),
        calc(100wv - 40px)
      </xsl:attribute>
      <xsl:attribute name="alt">
        <xsl:value-of select="@alt" />
      </xsl:attribute>
      <xsl:attribute name="title">
        <xsl:value-of select="@alt" />
      </xsl:attribute>

      <xsl:if test="@szer">
        <xsl:attribute name="style">
          <xsl:text>width: </xsl:text>
          <xsl:value-of select="@szer"/>
        </xsl:attribute>
      </xsl:if>
    </img>

    <div class="stop"></div>
  </div>
</xsl:template>

<xsl:template match="animacja">
  <div class="animacja cycle-slideshow" data-cycle-pause-on-hover="true" data-cycle-next="> img" data-cycle-fx="fadeout" data-cycle-paused="true">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates/>
  </div>
</xsl:template>


<!-- ========================================== -->
<!-- = PARAGRAPH TAGS                         = -->
<!-- = (can contain inline and special tags)  = -->
<!-- ========================================== -->
<!-- Title page -->
<xsl:template match="autor_utworu" mode="header">
  <span class="author">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </span>
</xsl:template>

<xsl:template match="nazwa_utworu" mode="header">
  <span class="title">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </span>
</xsl:template>

<xsl:template match="dzielo_nadrzedne" mode="header">
  <span class="collection">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </span>
</xsl:template>

<xsl:template match="podtytul" mode="header">
  <span class="subtitle">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </span>
</xsl:template>

<!-- Section headers (included in index)-->
<xsl:template match="naglowek_akt|naglowek_czesc|srodtytul">
  <xsl:call-template name="section-anchor"/>
  <h2>
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </h2>
</xsl:template>

<xsl:template match="podtytul_akt|podtytul_czesc">
  <div class="subtitle2">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </div>
</xsl:template>

<xsl:template match="naglowek_scena|naglowek_rozdzial">
    <xsl:call-template name="section-anchor"/>
    <h3>
      <xsl:call-template name="block-args" />
      <xsl:apply-templates mode="inline" />
    </h3>
</xsl:template>

<xsl:template match="podtytul_scena|podtytul_rozdzial">
  <div class="subtitle3">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </div>
</xsl:template>

<xsl:template match="naglowek_osoba|naglowek_podrozdzial">
  <xsl:call-template name="section-anchor"/>
  <h4>
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </h4>
</xsl:template>

<xsl:template match="podtytul_podrozdzial">
  <div class="subtitle4">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </div>
</xsl:template>

<!-- Other paragraph tags -->
<xsl:template match="miejsce_czas">
  <xsl:call-template name="section-anchor"/>
  <p class="place-and-time">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </p>
</xsl:template>

<xsl:template match="didaskalia">
  <xsl:call-template name="section-anchor"/>
  <div class="didaskalia">
    <xsl:call-template name="block-args" />
    <xsl:apply-templates mode="inline" />
  </div>
</xsl:template>

<xsl:template match="lista_osoba">
    <li><xsl:apply-templates mode="inline" /></li>
</xsl:template>

<xsl:template match="akap|akap_dialog|akap_cd">
    <p class="paragraph">
      <xsl:call-template name="block-args" />
      <xsl:call-template name="section-anchor"/>
	<xsl:apply-templates mode="inline" />
    </p>
</xsl:template>

<xsl:template match="list">
    <blockquote class="letter"><xsl:apply-templates /></blockquote>
</xsl:template>
<xsl:template match="adresat">
  <p class="paragraph adresat">
    <xsl:call-template name="block-args" />
    <xsl:call-template name="section-anchor"/>
    <xsl:apply-templates mode="inline" />
  </p>
</xsl:template>
<xsl:template match="miejsce_data">
  <p class="paragraph miejsce_data">
    <xsl:call-template name="block-args" />
    <xsl:call-template name="section-anchor"/>
    <xsl:apply-templates mode="inline" />
  </p>
</xsl:template>
<xsl:template match="naglowek_listu">
  <p class="paragraph naglowek_listu">
    <xsl:call-template name="block-args" />
    <xsl:call-template name="section-anchor"/>
    <xsl:apply-templates mode="inline" />
  </p>
</xsl:template>
<xsl:template match="pozdrowienie">
  <p class="paragraph pozdrowienie">
    <xsl:call-template name="block-args" />
    <xsl:call-template name="section-anchor"/>
    <xsl:apply-templates mode="inline" />
  </p>
</xsl:template>
<xsl:template match="podpis">
  <p class="paragraph podpis">
    <xsl:call-template name="block-args" />
    <xsl:call-template name="section-anchor"/>
    <xsl:apply-templates mode="inline" />
  </p>
</xsl:template>

<xsl:template match="strofa" mode="inline">
    <xsl:apply-templates select="." />
</xsl:template>

<xsl:template match="strofa">
  <div class="stanza">
    <xsl:call-template name="block-args" />
      <xsl:call-template name="section-anchor"/>
        <xsl:choose>
            <xsl:when test="count(br) > 0">
                <xsl:call-template name="verse">
                    <xsl:with-param name="verse-content" select="br[1]/preceding-sibling::text() | br[1]/preceding-sibling::node()" />
                    <xsl:with-param name="verse-type" select="br[1]/preceding-sibling::*[name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd' or name() = 'wers_do_prawej' or name() = 'wers_srodek'][1]" />
                </xsl:call-template>
                <xsl:for-each select="br">		
        			<!-- Each BR tag "consumes" text after it -->
                    <xsl:variable name="lnum" select="count(preceding-sibling::br)" />
                    <xsl:call-template name="verse">
                        <xsl:with-param name="verse-content"
                            select="following-sibling::text()[count(preceding-sibling::br) = $lnum+1] | following-sibling::node()[count(preceding-sibling::br) = $lnum+1]" />
                        <xsl:with-param name="verse-type" select="following-sibling::*[count(preceding-sibling::br) = $lnum+1 and (name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd' or name() = 'wers_do_prawej' or name() = 'wers_srodek')][1]" />
                    </xsl:call-template>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="verse">
                    <xsl:with-param name="verse-content" select="text() | node()" />
                    <xsl:with-param name="verse-type" select="wers_wciety|wers_akap|wers_cd|wers_do_prawej|wers_srodek[1]" />
                 </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </div>
</xsl:template>

<xsl:template name="verse">
    <xsl:param name="verse-content" />
    <xsl:param name="verse-type" />
    <div class="verse">
      <xsl:attribute name="class">
        <xsl:text>verse</xsl:text>
        <xsl:choose>
            <xsl:when test="name($verse-type) = 'wers_akap'">
              <xsl:text> verse-p</xsl:text>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_wciety'">
              <xsl:text> verse-indent</xsl:text>
              <xsl:if test="$verse-content/@typ">
                <xsl:text> verse-indent-</xsl:text>
                <xsl:value-of select="$verse-content/@typ" />
              </xsl:if>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_cd'">
              <xsl:text> verse-cont</xsl:text>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_do_prawej'">
              <xsl:text> verse-right</xsl:text>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_srodek'">
              <xsl:text> verse-center</xsl:text>
            </xsl:when>
        </xsl:choose>
      </xsl:attribute>
      <xsl:apply-templates select="$verse-content" mode="inline" />
    </div>
</xsl:template>

<xsl:template match="motto_podpis">
    <xsl:call-template name="section-anchor"/>
    <p class="motto_podpis">
      <xsl:call-template name="block-args" />
      <xsl:apply-templates mode="inline" />
    </p>
</xsl:template>

<xsl:template match="tabela|tabelka">
    <xsl:call-template name="section-anchor"/>
    <xsl:choose>
        <xsl:when test="@ramka = '1'">
          <table class="border">
            <xsl:call-template name="block-args" />
            <xsl:apply-templates />
          </table>
        </xsl:when>
        <xsl:otherwise>
          <table>
            <xsl:call-template name="block-args" />
            <xsl:apply-templates />
          </table>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
<xsl:template match="wiersz">
    <tr><xsl:apply-templates /></tr>
</xsl:template>
<xsl:template match="kol">
    <td><xsl:apply-templates mode="inline" /></td>
</xsl:template>

<xsl:template match="mat">
    <math xmlns="http://www.w3.org/1998/Math/MathML"><xsl:copy-of select="*" /></math>
</xsl:template>


<!-- ================================================ -->
<!-- = INLINE TAGS                                  = -->
<!-- = (contain other inline tags and special tags) = -->
<!-- ================================================ -->
<!-- Annotations -->
<xsl:template match="pa|pe|pr|pt|ptrad" mode="inline">
    <a name="{concat('anchor-', generate-id(.))}" />
    <a href="{concat('#footnote-', generate-id(.))}" class="annotation">[<xsl:number value="count(preceding::*[self::pa or self::pe or self::pr or self::pt or self::ptrad]) + 1" />]</a>
</xsl:template>

<xsl:template match="ref" mode="inline">
  <a class="reference" data-uri="">
    <xsl:attribute name="data-uri">
      <xsl:value-of select="@href"/>
    </xsl:attribute>
  </a>
</xsl:template>

<!-- Other inline tags -->
<xsl:template match="mat" mode="inline">
    <math xmlns="http://www.w3.org/1998/Math/MathML"><xsl:copy-of select="*|text()" /></math>
</xsl:template>

<xsl:template match="didask_tekst" mode="inline">
    <em class="didaskalia"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="slowo_obce" mode="inline">
  <em>
    <xsl:attribute name="class">
      <xsl:text>foreign-word</xsl:text>
      <xsl:if test="@protect">
	<xsl:text> foreign-word-protected</xsl:text>
      </xsl:if>
    </xsl:attribute>
    <xsl:apply-templates mode="inline" />
  </em>
</xsl:template>

<xsl:template match="tytul_dziela" mode="inline">
    <em class="book-title">
        <xsl:if test="@typ = '1'">„</xsl:if><xsl:apply-templates mode="inline" /><xsl:if test="@typ = '1'">”</xsl:if>
    </em>
</xsl:template>

<xsl:template match="wyroznienie" mode="inline">
    <em class="author-emphasis"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="wieksze_odstepy" mode="inline">
    <em class="wieksze-odstepy"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="indeks_dolny" mode="inline">
    <sub><xsl:apply-templates mode="inline" /></sub>
</xsl:template>

<xsl:template match="osoba" mode="inline">
    <em class="person"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="www" mode="inline">
    <a target="_blank">
        <xsl:attribute name="href">
            <xsl:value-of select="text()"/>
        </xsl:attribute>
        <xsl:apply-templates mode="inline" />
    </a>
</xsl:template>

<!-- ============================================== -->
<!-- = STANDALONE TAGS                            = -->
<!-- = (cannot contain any other tags)            = -->
<!-- ============================================== -->
<xsl:template match="sekcja_swiatlo">
    <hr class="spacer" />
</xsl:template>

<xsl:template match="sekcja_asterysk">
    <p class="spacer-asterisk">*</p>
</xsl:template>

<xsl:template match="separator_linia">
    <hr class="spacer-line" />
</xsl:template>


<!-- ================ -->
<!-- = SPECIAL TAGS = -->
<!-- ================ -->
<!-- Themes -->
<xsl:template match="begin" mode="inline">
    <xsl:variable name="mnum" select="concat('m', substring(@id, 2))" />
    <a name="m{substring(@id, 2)}" class="theme-begin" fid="{substring(@id, 2)}">
        <xsl:value-of select="string(following::motyw[@id=$mnum]/text())" />
    </a>
</xsl:template>

<xsl:template match="end" mode="inline">
    <span class="theme-end" fid="{substring(@id, 2)}"> </span>
</xsl:template>

<xsl:template match="begin|end">
    <xsl:apply-templates select='.' mode="inline" />
</xsl:template>

<xsl:template match="motyw" mode="inline" />


<xsl:template match="nota_red" mode="special">
    <div id="nota_red">
        <xsl:apply-templates />
    </div>
</xsl:template>


<xsl:template name="translators">
    <xsl:if test="//dc:contributor.translator">
        <span class="translator">
            <xsl:text>tłum. </xsl:text>
            <xsl:for-each select="//dc:contributor.translator">
                <xsl:if test="position() != 1">, </xsl:if>
                <xsl:apply-templates mode="person" />
            </xsl:for-each>
        </span>
    </xsl:if>
</xsl:template>

<xsl:template match="text()" mode="person">
    <xsl:value-of select="wl:person_name(.)" />
</xsl:template>

<xsl:template match="rownolegle">
    <xsl:apply-templates mode="rownolegle" />
</xsl:template>
<xsl:template match="*" mode="rownolegle">
  <!-- is it last? -->
  <div>
    <xsl:attribute name="class">
      <xsl:text>rownolegly-blok</xsl:text>
      <xsl:if test="not(following-sibling::*)">
        <xsl:text> last</xsl:text>
      </xsl:if>
      <xsl:if test="not(preceding-sibling::*)">
        <xsl:text> first</xsl:text>
      </xsl:if>
    </xsl:attribute>
    <xsl:attribute name="style">
      <xsl:text>border-left: 2px solid red; padding-left: .5em;</xsl:text>
      <xsl:if test="not(following-sibling::*)">
        <xsl:text> border-radius: 0 0 0 .75em;</xsl:text>
      </xsl:if>
      <xsl:if test="not(preceding-sibling::*)">
        <xsl:text> border-radius: .75em 0 0 0;</xsl:text>
      </xsl:if>
    </xsl:attribute>
    <xsl:apply-templates match="." />
  </div>
</xsl:template>

<xsl:template match="tab" mode="inline">
  <span>
    <xsl:choose>
      <xsl:when test="@szer">
        <xsl:attribute name="style">display: inline-block; width: <xsl:value-of select="@szer" />em</xsl:attribute>
      </xsl:when>
      <xsl:otherwise>
        <xsl:attribute name="style">display: inline-block; width: 1em</xsl:attribute>
      </xsl:otherwise>
    </xsl:choose>
  </span>
</xsl:template>


<xsl:template match="werset">
    <p class="werset paragraph">
      <xsl:call-template name="block-args" />
      <xsl:call-template name="section-anchor"/>
	<xsl:apply-templates mode="inline" />
    </p>
</xsl:template>


<!-- ================ -->
<!-- = IGNORED TAGS = -->
<!-- ================ -->
<xsl:template match="extra|uwaga" />
<xsl:template match="extra|uwaga" mode="inline" />

<xsl:template match="nota_red" />
<xsl:template match="abstrakt" />

<!-- ======== -->
<!-- = TEXT = -->
<!-- ======== -->
<xsl:template match="text()" />
<xsl:template match="text()" mode="inline">
    <xsl:value-of select="wl:substitute_entities(.)" />
</xsl:template>

<!-- ========= -->
<!-- = utils = -->
<!-- ========= -->
<xsl:template name="section-anchor">
  <!-- 
       this formula works as follows:
       - get all ancestors including self
       - choose the header (third one from root): utwor/book-type/header
       - get all preceding siblings
       - count them
       - create an <a name="sec123"/> tag.
  -->
        <a name="{concat('sec', count(ancestor-or-self::*[last()-2]/preceding-sibling::*) + 1)}" />
</xsl:template>

<xsl:template name="block-args">
  <xsl:if test="@id">
    <xsl:attribute name="id">
      <xsl:text>wl-</xsl:text>
      <xsl:value-of select="@id"/>
    </xsl:attribute>
  </xsl:if>
</xsl:template>

<xsl:template match="numeracja">
	<span class="numeracja">
		<xsl:attribute name="data-start">
			<xsl:value-of select="@start" />
		</xsl:attribute>
		<xsl:attribute name="data-link">
			<xsl:value-of select="@link" />
		</xsl:attribute>
	</span>
</xsl:template>

</xsl:stylesheet>
