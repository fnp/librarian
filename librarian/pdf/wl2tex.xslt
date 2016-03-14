<?xml version="1.0" encoding="utf-8"?>
<!--

   This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
   Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.

-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wl="http://wolnelektury.pl/functions"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" >

<xsl:output encoding="utf-8" indent="yes" version="2.0" />

<xsl:template match="utwor">
    <TeXML xmlns="http://getfo.sourceforge.net/texml/ns1">
        <TeXML escape="0">
        \documentclass[<xsl:value-of select="@customizations"/>]{wl}

        <!-- flags and values set on root -->

        \newif\ifflaglessadvertising
        <xsl:for-each select="@*[starts-with(name(), 'flag-')]">
            <cmd>
                <xsl:attribute name="name"><xsl:value-of select="wl:texcommand(name())" />true</xsl:attribute>
            </cmd>
        </xsl:for-each>

        <xsl:for-each select="@*[starts-with(name(), 'data-')]">
            <TeXML escape="0">
                \def\<xsl:value-of select="wl:texcommand(name())" />{<TeXML escape="1"><xsl:value-of select="."/></TeXML>}
            </TeXML>
        </xsl:for-each>
        </TeXML>

        <xsl:choose>
            <xsl:when test="@morefloats = 'new'">
                <TeXML escape="0">
                    \usepackage[maxfloats=53]{morefloats}
                </TeXML>
            </xsl:when>
            <xsl:when test="@morefloats = 'old'">
                <TeXML escape="0">
                    \usepackage{morefloats}
                </TeXML>
            </xsl:when>
            <xsl:when test="@morefloats = 'none'" />
            <xsl:otherwise>
                <TeXML escape="0">
                    \IfFileExists{morefloats.sty}{
                        \usepackage{morefloats}
                    }{}
                </TeXML>
            </xsl:otherwise>
        </xsl:choose>

        <xsl:apply-templates select="rdf:RDF" mode="titlepage" />
        <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='titlepage' />

        <env name="document">
            <xsl:if test="@data-cover-width">
                <cmd name="makecover">
                    <parm>210mm</parm>
                    <parm><xsl:value-of select="210 * @data-cover-height div @data-cover-width" />mm</parm>
                </cmd>
            </xsl:if>
                <xsl:if test="@thanks">
                    <TeXML escape="0">
                        \def\thanknote{<TeXML escape="1"><xsl:value-of select="@thanks" /></TeXML>}
                    </TeXML>
                </xsl:if>
            <cmd name="maketitle" />

            <cmd name="tytul"><parm>
              <xsl:choose>
                <xsl:when test="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/nazwa_utworu">
                    <!-- title in master -->
                    <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/autor_utworu" mode="title" />
                    <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/dzielo_nadrzedne" mode="title" />
                    <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/nazwa_utworu" mode="title" />
                    <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/podtytul" mode="title" />
                    <!-- dc in master or not -->
                    <cmd name="translatorsline" />
                </xsl:when>
                <xsl:otherwise>
                    <!-- look for author title in dc -->
                    <xsl:apply-templates select="rdf:RDF" mode="firstdctitle" />
                    <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='firstdctitle' />
                </xsl:otherwise>
              </xsl:choose>
            </parm></cmd>
            <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
            <xsl:apply-templates select="utwor" mode="part" />

            <TeXML escape="0">
                <xsl:if test="@data-cover-by">
                \def\coverby{Okładka na podstawie:
                    <xsl:choose>
                    <xsl:when test="@data-cover-source">
                        \href{\datacoversource}{\datacoverby}
                    </xsl:when>
                    <xsl:otherwise>
                        \datacoverby{}
                    </xsl:otherwise>
                    </xsl:choose>
                }
                </xsl:if>
                \def\editors{<TeXML escape="1"><xsl:call-template name="editors" /></TeXML>}
                <xsl:if test="@funders">
                    \def\funders{Publikację ufundowali i ufundowały:
                        <TeXML escape="1"><xsl:value-of select="@funders" /></TeXML>.}
                </xsl:if>

                <xsl:if test="@sponsor-note|data-sponsor">
                    \def\sponsors{
                        \scriptsize
                        <xsl:choose>
                            <xsl:when test="@sponsor-note">
                                <TeXML escape="1"><xsl:value-of select="@sponsor-note" /></TeXML>
                            </xsl:when>
                            <xsl:otherwise>
                                Sfinansowano ze~środków:
                            </xsl:otherwise>
                        </xsl:choose>

                        \vspace{1em}

                        <xsl:apply-templates select="data-sponsor" mode="sponsor" />
                    }
                </xsl:if>
            </TeXML>

            <cmd name="editorialsection" />

        </env>
    </TeXML>
</xsl:template>

<xsl:template match="utwor" mode="part">
    <cmd name="tytul"><parm>
      <xsl:choose>
        <xsl:when test="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/nazwa_utworu">
            <!-- title in master -->
            <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/nazwa_utworu" mode="title" />
            <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/podtytul" mode="title" />
        </xsl:when>
        <xsl:otherwise>
            <!-- look for title in dc -->
            <xsl:apply-templates select="rdf:RDF" mode="dctitle" />
            <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='dctitle' />
        </xsl:otherwise>
      </xsl:choose>
    </parm></cmd>

    <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
    <xsl:apply-templates select="utwor" mode="part" />
</xsl:template>

<!-- =================== -->
<!-- = MAIN TITLE PAGE = -->
<!-- = (from DC)       = -->
<!-- =================== -->

<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode="titlepage">
    <xsl:apply-templates select="rdf:RDF" mode="titlepage" />
</xsl:template>

<xsl:template match="rdf:RDF" mode="titlepage">
    <TeXML escape="0">
        \def\authors{<TeXML escape="1"><xsl:call-template name="authors" /></TeXML>}
        \author{\authors}
        \title{<TeXML escape="1"><xsl:apply-templates select=".//dc:title" mode="inline" /></TeXML>}
        \def\translatorsline{<TeXML escape="1"><xsl:call-template name="translators" /></TeXML>}

        \def\bookurl{<TeXML escape="1"><xsl:value-of select=".//dc:identifier.url" /></TeXML>}

        \def\rightsinfo{Ten utwór nie jest objęty majątkowym prawem autorskim i~znajduje się w~domenie
            publicznej, co oznacza że możesz go swobodnie wykorzystywać, publikować
            i~rozpowszechniać. Jeśli utwór opatrzony jest dodatkowymi materiałami
            (przypisy, motywy literackie etc.), które podlegają prawu autorskiemu, to
            te dodatkowe materiały udostępnione są na licencji
            \href{http://creativecommons.org/licenses/by-sa/3.0/}{Creative Commons
            Uznanie Autorstwa – Na Tych Samych Warunkach 3.0 PL}.}
        <xsl:if test=".//dc:rights.license">
            \def\rightsinfo{Ten utwór jest udostepniony na licencji
            \href{<xsl:value-of select=".//dc:rights.license" />}{<TeXML escape="1"><xsl:apply-templates select=".//dc:rights" mode="inline" /></TeXML>}.}
        </xsl:if>

        \def\sourceinfo{
            <xsl:if test=".//dc:source">
                Tekst opracowany na podstawie: <TeXML escape="1"><xsl:apply-templates select=".//dc:source" mode="inline" /></TeXML>
                \vspace{.6em}
            </xsl:if>}
        \def\description{<TeXML escape="1"><xsl:apply-templates select=".//dc:description" mode="inline" /></TeXML>}
    </TeXML>
</xsl:template>


<!-- ============== -->
<!-- = BOOK TITLE = -->
<!-- = (from DC)  = -->
<!-- ============== -->

<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode="dctitle">
    <xsl:apply-templates select="rdf:RDF" mode="dctitle" />
</xsl:template>

<xsl:template match="rdf:RDF" mode="dctitle">
    <cmd name="nazwapodutworu"><parm>
        <xsl:apply-templates select=".//dc:title/node()" mode="inline" />
    </parm></cmd>
</xsl:template>

<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode="firstdctitle">
    <xsl:apply-templates select="rdf:RDF" mode="firstdctitle" />
</xsl:template>

<xsl:template match="rdf:RDF" mode="firstdctitle">
    <cmd name="autorutworu"><parm><cmd name="authors"/></parm></cmd>
    <cmd name="nazwautworu"><parm>
        <xsl:apply-templates select=".//dc:title/node()" mode="inline" />
    </parm></cmd>
    <cmd name="translatorsline" />
</xsl:template>


<!-- ============================================================================== -->
<!-- = MASTER TAG                                                                 = -->
<!-- = (can contain block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ============================================================================== -->
<!-- ==================================================================================== -->
<!-- = BLOCK TAGS                                                                       = -->
<!-- = (can contain other block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ==================================================================================== -->

<xsl:template
    match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny|nota|dedykacja|dlugi_cytat|poezja_cyt|motto">
    <cmd>
        <xsl:attribute name="name">
            <xsl:value-of select="wl:texcommand(name())" />
        </xsl:attribute>
        <parm><xsl:apply-templates/></parm>
    </cmd>
</xsl:template>

<xsl:template match="lista_osob">
    <cmd name="listaosob">
        <parm><xsl:apply-templates select="naglowek_listy" /></parm>
        <parm><xsl:apply-templates select="lista_osoba" /></parm>
    </cmd>
</xsl:template>

<xsl:template match="kwestia">
    <cmd name="kwestia">
        <parm><xsl:apply-templates select="strofa|akap|didaskalia" /></parm>
    </cmd>
</xsl:template>

<xsl:template match="ilustr">
    <cmd name="ilustr">
        <parm><xsl:value-of select="@src" /></parm>
        <parm><xsl:value-of select="@alt" /></parm>
    </cmd>
</xsl:template>

<!-- ========================================== -->
<!-- = PARAGRAPH TAGS                         = -->
<!-- = (can contain inline and special tags)  = -->
<!-- ========================================== -->

<!-- only in root -->
<xsl:template
    match="autor_utworu|dzielo_nadrzedne|nazwa_utworu|podtytul"
    mode="title">
    <cmd>
        <xsl:attribute name="name">
            <xsl:value-of select="wl:texcommand(name())" />
        </xsl:attribute>
        <parm><xsl:apply-templates mode="inline"/></parm>
    </cmd>
</xsl:template>


<xsl:template
    match="naglowek_akt|naglowek_czesc|srodtytul|naglowek_osoba|naglowek_podrozdzial|naglowek_scena|naglowek_rozdzial|miejsce_czas|didaskalia|lista_osoba|akap|akap_dialog|akap_cd|motto_podpis|naglowek_listy">
    <cmd>
        <xsl:attribute name="name">
            <xsl:value-of select="wl:texcommand(name())" />
        </xsl:attribute>
        <parm><xsl:apply-templates mode="inline"/></parm>
    </cmd>
</xsl:template>

<xsl:template match="strofa">
  <cmd name="strofa"><parm>
    <xsl:choose>
        <xsl:when test="count(br) > 0">
            <xsl:call-template name="verse">
                <xsl:with-param name="verse-content" select="br[1]/preceding-sibling::text() | br[1]/preceding-sibling::node()" />
                <xsl:with-param name="verse-type" select="br[1]/preceding-sibling::*[name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd'][1]" />
            </xsl:call-template>
            <xsl:for-each select="br">
                <TeXML escape="0">\\{}</TeXML>
                <!-- Each BR tag "consumes" text after it -->
                <xsl:variable name="lnum" select="count(preceding-sibling::br)" />
                <xsl:call-template name="verse">
                    <xsl:with-param name="verse-content"
                        select="following-sibling::text()[count(preceding-sibling::br) = $lnum+1] | following-sibling::node()[count(preceding-sibling::br) = $lnum+1]" />
                    <xsl:with-param name="verse-type" select="following-sibling::*[count(preceding-sibling::br) = $lnum+1 and (name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd')][1]" />
                </xsl:call-template>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:call-template name="verse">
                <xsl:with-param name="verse-content" select="text() | node()" />
                <xsl:with-param name="verse-type" select="wers_wciety|wers_akap|wers_cd[1]" />
            </xsl:call-template>
        </xsl:otherwise>
    </xsl:choose>
  </parm></cmd>
</xsl:template>


<xsl:template name="verse">
    <xsl:param name="verse-content" />
    <xsl:param name="verse-type" />

    <cmd>
        <xsl:attribute name="name">
            <xsl:choose>
                <xsl:when test="$verse-type != ''">
                    <xsl:value-of select='wl:texcommand(name($verse-type))' />
                </xsl:when>
                <xsl:otherwise>wers</xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
        <xsl:if test="string($verse-content/@typ)">
            <opt><xsl:value-of select="$verse-content/@typ" />em</opt>
        </xsl:if>
        <parm><xsl:apply-templates select="$verse-content" mode="inline"/></parm>
    </cmd>
</xsl:template>

<!-- ================================================ -->
<!-- = INLINE TAGS                                  = -->
<!-- = (contain other inline tags and special tags) = -->
<!-- ================================================ -->

<xsl:template mode="inline"
    match="pa|pe|pr|pt|mat|didask_tekst|slowo_obce|wyroznienie|osoba">
    <cmd>
        <xsl:attribute name="name">
            <xsl:value-of select="wl:texcommand(name())" />
        </xsl:attribute>
        <parm><xsl:apply-templates mode="inline"/></parm>
    </cmd>
</xsl:template>



<xsl:template match="tytul_dziela" mode="inline">
    <cmd name="tytuldziela"><parm>
        <xsl:if test="@typ = '1'">„</xsl:if><xsl:apply-templates mode="inline" /><xsl:if test="@typ = '1'">”</xsl:if>
    </parm></cmd>
</xsl:template>



<!-- ============================================== -->
<!-- = STANDALONE TAGS                            = -->
<!-- = (cannot contain any other tags)            = -->
<!-- ============================================== -->
<xsl:template
    match="sekcja_swiatlo|sekcja_asterysk|separator_linia">
    <cmd>
        <xsl:attribute name="name">
            <xsl:value-of select="wl:texcommand(name())" />
        </xsl:attribute>
    </cmd>
</xsl:template>


<!-- ================ -->
<!-- = SPECIAL TAGS = -->
<!-- ================ -->
<!-- Themes -->


<xsl:template match="begin|end|motyw">
    <xsl:apply-templates select='.' mode="inline" />
</xsl:template>

<xsl:template match="begin" mode="inline" />
<xsl:template match="end" mode="inline" />

<xsl:template match="motyw" mode="inline">
    <cmd name="motyw">
        <xsl:if test="@moved">
            <opt name="moved"><xsl:value-of select="@moved" /></opt>
        </xsl:if>
        <parm><xsl:apply-templates mode="inline" /></parm>
    </cmd>
</xsl:template>

<xsl:template name="authors">
    <xsl:for-each select=".//dc:creator_parsed">
        <xsl:if test="position() != 1">, </xsl:if>
        <xsl:apply-templates mode="inline" />
    </xsl:for-each>
</xsl:template>

<xsl:template name="editors">
    <xsl:if test="@editors">
        <xsl:text>Opracowanie redakcyjne i przypisy: </xsl:text>
        <xsl:value-of select="@editors" />
        <xsl:text>.</xsl:text>
    </xsl:if>
</xsl:template>

<xsl:template name="translators">
    <xsl:if test=".//dc:contributor.translator_parsed">
        <cmd name='translator'><parm>
            <xsl:for-each select=".//dc:contributor.translator_parsed">
                <xsl:if test="position() != 1">, </xsl:if>
                <xsl:apply-templates mode="inline" />
            </xsl:for-each>
        </parm></cmd>
    </xsl:if>
</xsl:template>

<xsl:template match="data-sponsor" mode="sponsor">
    <cmd name="par"><parm>
    <xsl:choose>
        <xsl:when test="@src">
            \includegraphics[height=0.25\textwidth,width=0.25\textwidth,keepaspectratio]{<xsl:value-of select="@src" />}
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="@name" />
        </xsl:otherwise>
    </xsl:choose>
    </parm></cmd>
</xsl:template>

<xsl:template match="mat" mode="inline">
    <TeXML escape="0">
        <xsl:text>$</xsl:text>
        <xsl:value-of select="wl:mathml_latex(.)" />
        <xsl:text>$</xsl:text>
    </TeXML>
</xsl:template>

<xsl:template match="mat">
    <TeXML escape="0">
        <xsl:text>$$</xsl:text>
        <xsl:value-of select="wl:mathml_latex(.)" />
        <xsl:text>$$</xsl:text>
    </TeXML>
</xsl:template>

<xsl:template match="tabela|tabelka">
    <cmd name="par" />
    <cmd name="vspace"><parm>1em</parm></cmd>
    <group><cmd name="raggedright" />
    <env name="longtabu"> to <TeXML escape="0">\textwidth </TeXML>
      <!--parm><cmd name="textwidth"/></parm-->
      <parm><TeXML escape="0"><xsl:value-of select="@_format" /></TeXML></parm>
        <xsl:choose>
        <xsl:when test="@ramka='1' or @ramki='1'">
          <cmd name="hline" />
          <xsl:apply-templates mode="wiersze-ramki"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates/>
        </xsl:otherwise>
        </xsl:choose>
    </env>
    </group>
    <cmd name="vspace"><parm>1em</parm></cmd>
</xsl:template>
<xsl:template match="wiersz" mode="wiersze-ramki">
    <xsl:apply-templates />
    <spec cat="esc"/><spec cat="esc"/>
    <cmd name="hline" gr="0" />
</xsl:template>
<xsl:template match="wiersz">
    <xsl:apply-templates />
    <spec cat="esc"/><spec cat="esc"/>
</xsl:template>
<xsl:template match="kol">
    <xsl:apply-templates mode="inline"/>
    <xsl:if test="position() &lt; last()">
    <spec cat="align"/>
    </xsl:if>
</xsl:template>


<!-- ============== -->
<!-- = ADDED TAGS = -->
<!-- ============== -->


<xsl:template match="dywiz" mode="inline">
    <cmd name="dywiz" />
</xsl:template>

<xsl:template match="nbsp" mode="inline">
    <spec cat="tilde" />
</xsl:template>

<xsl:template match="alien" mode="inline">
    <group>
        <cmd name="alien" />
        <xsl:apply-templates mode="inline" />
    </group>
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
    <xsl:if test="preceding-sibling::node() and wl:starts_white(.)">
      <xsl:text> </xsl:text>
    </xsl:if>

    <xsl:value-of select="wl:substitute_entities(wl:strip(.))" />

    <xsl:if test="following-sibling::node() and wl:ends_white(.)">
      <xsl:text> </xsl:text>
    </xsl:if>
</xsl:template>


</xsl:stylesheet>
