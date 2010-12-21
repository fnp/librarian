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
        \documentclass[a4paper, oneside, 11pt]{book}
        \usepackage{wl}
        </TeXML>

        <xsl:choose>
            <xsl:when test="@old-morefloats">
                <TeXML escape="0">
                    \IfFileExists{morefloats.sty}{
                        \usepackage{morefloats}
                    }{}
                </TeXML>
            </xsl:when>
            <xsl:otherwise>
                <TeXML escape="0">
                    \usepackage[maxfloats=64]{morefloats}
                </TeXML>
            </xsl:otherwise>
        </xsl:choose>

        <xsl:apply-templates select="rdf:RDF" mode="titlepage" />
        <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='titlepage' />

        <env name="document">
            <cmd name="maketitle" />

            <xsl:choose>
                <xsl:when test="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/nazwa_utworu">
                    <xsl:apply-templates select="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/autor_utworu" mode="title" />
                    <!-- title in master -->
                </xsl:when>
                <xsl:otherwise>
                    <!-- look for author title in dc -->
                    <xsl:apply-templates select="rdf:RDF" mode="firstdctitle" />
                    <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='firstdctitle' />
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
            <xsl:apply-templates select="utwor" mode="part" />
        </env>
    </TeXML>
</xsl:template>

<xsl:template match="utwor" mode="part">
    <!-- title for empty dc -->
    <xsl:choose>
        <xsl:when test="(powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny)/nazwa_utworu">
            <!-- title in master -->
        </xsl:when>
        <xsl:otherwise>
            <!-- look for title in dc -->
            <xsl:apply-templates select="rdf:RDF" mode="dctitle" />
            <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='dctitle' />
        </xsl:otherwise>
    </xsl:choose>

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
    <cmd name='title'><parm>
        <xsl:apply-templates select=".//dc:title/node()" mode="inline" />
    </parm></cmd>
    <cmd name='author'><parm>
        <xsl:apply-templates select=".//dc:creator_parsed/node()" mode="inline" />
    </parm></cmd>
    <TeXML escape="0">
        \def\sourceinfo{<TeXML escape="1"><xsl:apply-templates select=".//dc:source/node()" mode="inline" /></TeXML>}
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
    <cmd name="section*"><parm>
        <xsl:apply-templates select=".//dc:title/node()" mode="inline" />
    </parm></cmd>
</xsl:template>


<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode="firstdctitle">
    <xsl:apply-templates select="rdf:RDF" mode="firstdctitle" />
</xsl:template>

<xsl:template match="rdf:RDF" mode="firstdctitle">
    <cmd name="subsection*"><parm>
        <xsl:apply-templates select=".//dc:creator_parsed/node()" mode="inline" />
    </parm></cmd>
    <cmd name="section*"><parm>
        <xsl:apply-templates select=".//dc:title/node()" mode="inline" />
    </parm></cmd>
</xsl:template>


<!-- ============================================================================== -->
<!-- = MASTER TAG                                                                 = -->
<!-- = (can contain block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ============================================================================== -->

<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny">
    <xsl:apply-templates />
</xsl:template>



<!-- ==================================================================================== -->
<!-- = BLOCK TAGS                                                                       = -->
<!-- = (can contain other block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ==================================================================================== -->
<xsl:template match="nota">
    <cmd name="par">
        <parm><xsl:apply-templates /></parm>
    </cmd>
</xsl:template>

<xsl:template match="lista_osob">
    <cmd name="par"><parm>
        <cmd name="textbf">
            <parm><xsl:apply-templates select="naglowek_listy" mode="inline" /></parm>
        </cmd>
        <env name="itemize">
            <xsl:apply-templates select="lista_osoba" />
        </env>
    </parm></cmd>
</xsl:template>

<xsl:template match="dedykacja">
    <env name="em">
        <env name="flushright">
            <xsl:apply-templates/>
        </env>
    </env>
</xsl:template>

<xsl:template match="kwestia">
    <cmd name="par">
        <parm><xsl:apply-templates select="strofa|akap|didaskalia" /></parm>
    </cmd>
</xsl:template>

<xsl:template match="dlugi_cytat">
    <env name="quotation">
        <xsl:apply-templates />
    </env>
</xsl:template>

<xsl:template match="poezja_cyt">
    <env name="verse">
        <xsl:apply-templates />
    </env>
</xsl:template>

<xsl:template match="motto">
    <env name="em">
        <xsl:apply-templates mode="inline" />
    </env>
</xsl:template>


<!-- ========================================== -->
<!-- = PARAGRAPH TAGS                         = -->
<!-- = (can contain inline and special tags)  = -->
<!-- ========================================== -->

<!-- only in root -->
<xsl:template match="autor_utworu" mode="title">
    <cmd name="subsection*"><parm>
        <xsl:apply-templates mode="inline" />
    </parm></cmd>
</xsl:template>

<xsl:template match="nazwa_utworu">
    <cmd name="section*"><parm>
        <xsl:apply-templates mode="inline" />
    </parm></cmd>
</xsl:template>

<!-- Section headers (included in index)-->
<xsl:template match="naglowek_akt|naglowek_czesc|srodtytul">
    <cmd name="subsection*">
        <parm><xsl:apply-templates mode="inline" /></parm>
    </cmd>
</xsl:template>

<xsl:template match="naglowek_scena|naglowek_rozdzial">
    <cmd name="subsubsection*">
        <parm><xsl:apply-templates mode="inline" /></parm>
    </cmd>
</xsl:template>

<xsl:template match="naglowek_osoba|naglowek_podrozdzial">
    <cmd name="par">
        <parm><xsl:apply-templates mode="inline" /></parm>
    </cmd><cmd name="nopagebreak" />
</xsl:template>

<!-- Other paragraph tags -->
<xsl:template match="miejsce_czas">
    <cmd name="par"><parm>
        <cmd name="emph">
            <parm><xsl:apply-templates mode="inline" /></parm>
        </cmd>
    </parm></cmd>
</xsl:template>

<xsl:template match="didaskalia">
    <cmd name="par"><parm>
        <cmd name="emph">
            <parm><xsl:apply-templates mode="inline" /></parm>
        </cmd>
    </parm></cmd>
</xsl:template>

<xsl:template match="lista_osoba">
    <cmd name="item"><parm>
        <xsl:apply-templates mode="inline" />
    </parm></cmd>
</xsl:template>

<xsl:template match="akap|akap_dialog|akap_cd">
    <cmd name="par"><parm>
        <xsl:apply-templates mode="inline" />
    </parm></cmd>
</xsl:template>

<xsl:template match="strofa">
<cmd name="par"><parm><cmd name="noindent"><parm>
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
    <cmd name="vspace"><parm>1em</parm></cmd>
</parm></cmd></parm></cmd>
</xsl:template>


<xsl:template name="verse">
    <xsl:param name="verse-content" />
    <xsl:param name="verse-type" />
        <xsl:choose><xsl:when test="name($verse-type) = 'wers_akap'"><cmd name="hspace" ><parm>1em</parm></cmd></xsl:when>
            <xsl:when test="name($verse-type) = 'wers_wciety'">
                <xsl:choose>
                    <xsl:when test="string($verse-content/@typ)">
                        <cmd name="hspace" ><parm><xsl:value-of select="$verse-content/@typ" />em</parm></cmd>
                    </xsl:when>
                    <xsl:otherwise>
                        <cmd name="hspace" ><parm>1em</parm></cmd>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_cd'">
                <cmd name="hspace" ><parm>8em</parm></cmd>
            </xsl:when>
        </xsl:choose>
        <xsl:apply-templates select="$verse-content" mode="inline" />
</xsl:template>

<xsl:template match="motto_podpis">
    <env name="em">
        <env name="flushright">
            <xsl:apply-templates mode="inline"/>
        </env>
    </env>
</xsl:template>

<!-- ================================================ -->
<!-- = INLINE TAGS                                  = -->
<!-- = (contain other inline tags and special tags) = -->
<!-- ================================================ -->

<!-- Annotations -->
<xsl:template match="pa|pe|pr|pt" mode="inline">
    <cmd name="footnote"><parm><xsl:apply-templates mode="inline" /></parm></cmd>
</xsl:template>

<!-- Other inline tags -->
<xsl:template match="mat" mode="inline">
    <math><xsl:apply-templates mode="inline" /></math>
</xsl:template>

<xsl:template match="didask_tekst" mode="inline">
    <cmd name="emph"><parm><xsl:apply-templates mode="inline" /></parm></cmd>
</xsl:template>

<xsl:template match="slowo_obce" mode="inline">
    <cmd name="emph"><parm><xsl:apply-templates mode="inline" /></parm></cmd>
</xsl:template>

<xsl:template match="tytul_dziela" mode="inline">
    <cmd name="emph"><parm>
        <xsl:if test="@typ = '1'">„</xsl:if><xsl:apply-templates mode="inline" /><xsl:if test="@typ = '1'">”</xsl:if>
    </parm></cmd>
</xsl:template>

<xsl:template match="wyroznienie" mode="inline">
    <cmd name="emph"><parm><xsl:apply-templates mode="inline" /></parm></cmd>
</xsl:template>

<xsl:template match="osoba" mode="inline">
    <cmd name="textsc"><parm><xsl:apply-templates mode="inline" /></parm></cmd>
</xsl:template>


<!-- ============================================== -->
<!-- = STANDALONE TAGS                            = -->
<!-- = (cannot contain any other tags)            = -->
<!-- ============================================== -->
<xsl:template match="sekcja_swiatlo">
    <cmd name="hspace"><parm>30pt</parm></cmd>
</xsl:template>

<xsl:template match="sekcja_asterysk">
    <!-- TODO: padding? -->
    <cmd name="par"><parm>*</parm></cmd>
</xsl:template>

<xsl:template match="separator_linia">
    <cmd name="hrule" />
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
    <cmd name="mbox" />
    <cmd name="marginpar">
        <parm>
            <cmd name="vspace"><parm>-8pt</parm></cmd>
            <xsl:if test="@moved">
                <cmd name="vspace"><parm>-<xsl:value-of select="@moved" /><cmd name="baselineskip" /></parm></cmd>
            </xsl:if>
            <cmd name="raggedright"><parm>
                <cmd name="hspace"><parm>0pt</parm></cmd>
                <cmd name="footnotesize"><parm>
                    <cmd name="color"><parm>theme</parm><parm>
                        <xsl:apply-templates mode="inline" />
                    </parm></cmd>
                </parm></cmd>
            </parm></cmd>
            <cmd name="vspace"><parm><cmd name="baselineskip" /></parm></cmd>
        </parm>
    </cmd>
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

<!-- ================ -->
<!-- = IGNORED TAGS = -->
<!-- ================ -->
<xsl:template match="extra|uwaga" />
<xsl:template match="extra|uwaga" mode="inline" />

<xsl:template match="nota_red" />

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