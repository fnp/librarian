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
        \usepackage[MeX]{polski}
        \usepackage[utf8]{inputenc}
        \pagestyle{plain}
        \usepackage{antpolt}
        \usepackage[bottom]{footmisc}

        \usepackage{color}
        \definecolor{theme-gray}{gray}{.3}


        \setlength{\marginparsep}{2em}
        \setlength{\marginparwidth}{8.5em}
        \setlength{\oddsidemargin}{0pt}
        \clubpenalty=10000
        \widowpenalty=10000 
        </TeXML>

        <xsl:apply-templates select="rdf:RDF" mode='title' />
        <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='title' />

        <env name="document">
            <cmd name="maketitle" />
            <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
            <xsl:apply-templates select="utwor" mode="part" />
        </env>
    </TeXML>
</xsl:template>

<xsl:template match="utwor" mode="part">
    <xsl:if test="utwor">
        <xsl:apply-templates select="rdf:RDF" mode='subtitle' />
        <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode='subtitle' />
    </xsl:if>
    <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
    <xsl:apply-templates select="utwor" mode="part" />
</xsl:template>


<!-- ============================================================================== -->
<!-- = MASTER TAG                                                                 = -->
<!-- = (can contain block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ============================================================================== -->

<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode="title">
    <xsl:apply-templates select="rdf:RDF" mode='title' />
</xsl:template>

<xsl:template match="rdf:RDF" mode="title">

<!-- TODO!
            <cmd name='title'><parm>
                <xsl:apply-templates select="dzielo_nadrzedne|podtytul" mode="header" />
            </parm></cmd>
            czytanie z tagów nazwa_utworu, autor_utworu
-->

                <cmd name='title'><parm>
                    <xsl:apply-templates select=".//dc:title" mode="header" />
                </parm></cmd>
                <cmd name='author'><parm>
                    <xsl:apply-templates select=".//dc:author" mode="header" />
                </parm></cmd>
</xsl:template>

<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" mode="subtitle">
    <xsl:apply-templates select="rdf:RDF" mode='subtitle' />
</xsl:template>

<xsl:template match="rdf:RDF" mode="subtitle">
                <cmd name='part*'><parm>
                    <xsl:apply-templates select=".//dc:title" mode="header" />
                </parm></cmd>
</xsl:template>



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
    <cmd name="par">
        <cmd name="textbf">
            <parm><xsl:value-of select="naglowek_listy" /></parm>
        </cmd>
        <env name="itemize">
            <xsl:apply-templates select="lista_osoba" />
        </env>
    </cmd>
</xsl:template>

<xsl:template match="dedykacja">
    <cmd name="raggedleft"><parm>
        <env name="em">
            <xsl:apply-templates />
        </env>
    </parm></cmd>
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
<!-- Title page -->
<xsl:template match="autor_utworu" mode="header">
    <xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="nazwa_utworu" mode="header">
    <xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="dzielo_nadrzedne" mode="header">
    <xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="podtytul" mode="header">
    <xsl:apply-templates mode="inline" />
</xsl:template>


<xsl:template match="nazwa_utworu">
    <cmd name="pagebreak" />
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
    <cmd name="paragraph*">
        <parm><xsl:apply-templates mode="inline" /></parm>
    </cmd>
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
                    <cmd name="newline" />
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
        <xsl:choose><xsl:when test="name($verse-type) = 'wers_akap'"><cmd name="hspace" ><parm><xsl:value-of select="$firet" />pt</parm></cmd></xsl:when>
            <xsl:when test="name($verse-type) = 'wers_wciety'">
                <xsl:choose>
                    <xsl:when test="$verse-content/@typ">
                        <cmd name="hspace" ><parm><xsl:value-of select="$verse-content/@typ" />em</parm></cmd>
                    </xsl:when>
                    <xsl:otherwise>
                        <cmd name="hspace" ><parm>1em</parm></cmd>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_cd'">
                <cmd name="hspace" ><parm>12em</parm></cmd>
            </xsl:when>
        </xsl:choose>
        <xsl:apply-templates select="$verse-content" mode="inline" />
</xsl:template>

<xsl:template match="motto_podpis">
    <cmd name="raggedleft"><parm>
        <xsl:apply-templates mode="inline" />
    </parm></cmd>
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
    <!-- TODO: letterspacing 1pt -->
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


<xsl:template match="begin" mode="inline">
    <xsl:variable name="mnum" select="concat('m', substring(@id, 2))" />
    <cmd name="mbox" />
    <cmd name="marginpar">
        <parm><cmd name="raggedright"><parm>
            <cmd name="hspace"><parm>0pt</parm></cmd>
            <cmd name="footnotesize"><parm>
                <cmd name="color"><parm>theme-gray</parm><parm>
                    <xsl:value-of select="string(following::motyw[@id=$mnum]/text())" />
                </parm></cmd>
            </parm></cmd>
        </parm></cmd></parm>
    </cmd>
</xsl:template>

<xsl:template match="begin|end">
    <xsl:apply-templates select='.' mode="inline" />
</xsl:template>

<xsl:template match="end" mode="inline" />
<xsl:template match="motyw" mode="inline" />


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


<!-- ======== -->
<!-- = TEXT = -->
<!-- ======== -->
<xsl:template match="text()" />
<xsl:template match="text()" mode="inline">
    <xsl:value-of select="wl:substitute_entities(.)" />
</xsl:template>


</xsl:stylesheet>