<?xml version="1.0" encoding="utf-8"?>
<!--
#
#    This file is part of Librarian.
#
#    Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>
#    
#    For full list of contributors see AUTHORS file. 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wl="http://wolnelektury.pl/functions" >

<xsl:output encoding="utf-8" method="text" />

<xsl:param name="wrapping" select="0" />

<!-- ============================================================================== -->
<!-- = MASTER TAG                                                                 = -->
<!-- = (can contain block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ============================================================================== -->
<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny">
<xsl:if test="nazwa_utworu"><xsl:apply-templates select="autor_utworu|dzielo_nadrzedne|nazwa_utworu|podtytul" mode="header" /></xsl:if>
<xsl:text>

</xsl:text>
<xsl:apply-templates />
</xsl:template>


<!-- ==================================================================================== -->
<!-- = BLOCK TAGS                                                                       = -->
<!-- = (can contain other block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ==================================================================================== -->
<xsl:template match="nota">
<xsl:apply-templates />
</xsl:template>

<xsl:template match="lista_osob">
<xsl:text>


</xsl:text>
<xsl:value-of select="naglowek_listy" />
<xsl:apply-templates select="lista_osoba" />
<xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="dedykacja">
<xsl:text>

</xsl:text>
<xsl:apply-templates />
</xsl:template>

<xsl:template match="kwestia">
<xsl:apply-templates select="strofa|akap|didaskalia" />
</xsl:template>

<xsl:template match="dlugi_cytat|poezja_cyt">
<xsl:text>
</xsl:text>
<xsl:apply-templates />
</xsl:template>

<xsl:template match="motto">
<xsl:text>



</xsl:text>
<xsl:apply-templates /><xsl:text>

</xsl:text>
</xsl:template>


<!-- ========================================== -->
<!-- = PARAGRAPH TAGS                         = -->
<!-- = (can contain inline and special tags)  = -->
<!-- ========================================== -->
<!-- Title page -->
<xsl:template match="autor_utworu" mode="header">
<xsl:text>

</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="nazwa_utworu" mode="header">
<xsl:text>

</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="dzielo_nadrzedne" mode="header">
<xsl:text>
    
</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="podtytul" mode="header">
<xsl:text>
</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<!-- Section headers (included in index)-->
<xsl:template match="naglowek_akt|naglowek_czesc|srodtytul">
<xsl:text>




</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="naglowek_scena|naglowek_rozdzial">
<xsl:text>



</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="naglowek_osoba|naglowek_podrozdzial">
<xsl:text>


</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<!-- Other paragraph tags -->
<xsl:template match="miejsce_czas">
<xsl:text>



</xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="didaskalia">
<xsl:variable name="content">
    <xsl:apply-templates select="*|text()" mode="inline" />
</xsl:variable>
<xsl:text>
    
/ </xsl:text><xsl:value-of select="wl:wrap_words(wl:strip($content), $wrapping)" /><xsl:text> /</xsl:text>
</xsl:template>

<xsl:template match="lista_osoba">
<xsl:text>
 * </xsl:text>
<xsl:apply-templates mode="inline" />
</xsl:template>

<xsl:template match="akap|akap_dialog|akap_cd">
<xsl:variable name="content">
    <xsl:apply-templates select="*|text()" mode="inline" />
</xsl:variable>
<xsl:text>

</xsl:text>
<xsl:value-of select="wl:wrap_words(wl:strip($content), $wrapping)" />
</xsl:template>

<xsl:template match="strofa">
<xsl:text>
</xsl:text>
    <xsl:choose>
        <xsl:when test="count(br) > 0">     
            <xsl:call-template name="verse">
                <xsl:with-param name="verse-content" select="br[1]/preceding-sibling::text() | br[1]/preceding-sibling::node()" />
                <xsl:with-param name="verse-type" select="br[1]/preceding-sibling::*[name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd'][1]" />
            </xsl:call-template>    
            <xsl:for-each select="br">		
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
</xsl:template>

<xsl:template name="verse">
    <xsl:param name="verse-content" />
    <xsl:param name="verse-type" />
<xsl:text>
</xsl:text>
    <xsl:variable name="content">
        <xsl:apply-templates select="$verse-content" mode="inline" />
    </xsl:variable>
    <xsl:choose>
        <xsl:when test="name($verse-type) = 'wers_akap'">
            <xsl:text>  </xsl:text>
        </xsl:when>
        <xsl:when test="name($verse-type) = 'wers_wciety'">
            <xsl:choose>
                <xsl:when test="$verse-content/@typ">
                    <xsl:text>    </xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>  </xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:when>
        <xsl:when test="name($verse-type) = 'wers_cd'">
            <xsl:text>                        </xsl:text>
        </xsl:when>
    </xsl:choose>
<xsl:value-of select="wl:strip($content)" />
</xsl:template>

<xsl:template match="motto_podpis">
<xsl:apply-templates mode="inline" />
</xsl:template>


<!-- ================================================ -->
<!-- = INLINE TAGS                                  = -->
<!-- = (contain other inline tags and special tags) = -->
<!-- ================================================ -->
<!-- Annotations -->
<xsl:template match="pa|pe|pr|pt" mode="inline" />

<!-- Other inline tags -->
<xsl:template match="mat" mode="inline"><xsl:apply-templates mode="inline" /></xsl:template>

<xsl:template match="didask_tekst" mode="inline"><xsl:apply-templates mode="inline" /></xsl:template>

<xsl:template match="slowo_obce" mode="inline"><xsl:apply-templates mode="inline" /></xsl:template>

<xsl:template match="tytul_dziela" mode="inline">
<xsl:if test="@typ = '1'">„</xsl:if><xsl:apply-templates mode="inline" /><xsl:if test="@typ = '1'">”</xsl:if>
</xsl:template>

<xsl:template match="wyroznienie" mode="inline">
<xsl:text>*</xsl:text><xsl:apply-templates mode="inline" /><xsl:text>*</xsl:text>
</xsl:template>

<xsl:template match="osoba" mode="inline">
<xsl:apply-templates mode="inline" />
</xsl:template>


<!-- ============================================== -->
<!-- = STANDALONE TAGS                            = -->
<!-- = (cannot contain any other tags)            = -->
<!-- ============================================== -->
<xsl:template match="sekcja_swiatlo">
<xsl:text>



</xsl:text>
</xsl:template>

<xsl:template match="sekcja_asterysk">
<xsl:text>

*

</xsl:text>
</xsl:template>

<xsl:template match="separator_linia">
<xsl:text>

------------------------------------------------

</xsl:text>
</xsl:template>


<!-- ================ -->
<!-- = SPECIAL TAGS = -->
<!-- ================ -->
<!-- Themes -->
<xsl:template match="begin" mode="inline" />

<xsl:template match="end" mode="inline" />

<xsl:template match="begin|end" />

<xsl:template match="motyw" mode="inline" />


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

