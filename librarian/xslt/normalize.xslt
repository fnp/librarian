<?xml version="1.0" encoding="utf-8"?>
<!--
 
   This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
   Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
  
-->
<xsl:stylesheet version="1.0"
    xmlns="http://nowoczesnapolska.org.pl/ML/Lektury/1.1"
        
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wlf="http://wolnelektury.pl/functions"

    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
    xmlns:dc="http://purl.org/dc/elements/1.1/"

    exclude-result-prefixes="wlf xsl"
>

    <!-- Normalization Stylsheet for Wolne Lektury XML -->
    <xsl:output method="xml" encoding="utf-8" indent="yes" />
     
    <xsl:strip-space elements="rdf:RDF rdf:Description meta doc main-text strofa stanza drama-line wlml:*" />

    <xsl:param name="normalize-text" select="boolean(1)" />

    <!-- Main entry point -->
    <xsl:template match="/">
        <doc>
            <meta>
                <xsl:apply-templates select="//rdf:RDF" mode="meta"/>
            </meta>

            <xsl:variable name="body" select="/utwor/*[local-name() = name()]" />

            <main-text class="{name($body)}">
                <xsl:apply-templates select="$body/node()" />
            </main-text>

            <annotations>
                <xsl:apply-templates select="//pr|pt|pe|pa" mode="annotations" />              
            </annotations>
        </doc>
    </xsl:template>    

    <xsl:template match="strofa">
        <xsl:element name="stanza" namespace="http://nowoczesnapolska.org.pl/ML/Lektury/1.1">
            <!-- normalize verses -->
            <xsl:choose>
                <xsl:when test="count(br) > 0">
                    <!-- First, collect all the tags up to first BR -->
                    <xsl:call-template name="verse">
                        <xsl:with-param name="verse-content" select="br[1]/preceding-sibling::node()" />
                        <xsl:with-param name="verse-type" select="br[1]/preceding-sibling::*[name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd'][1]" />
                    </xsl:call-template>

                    <!-- Collect the rest of verses -->
                    <xsl:for-each select="br">
        			<!-- Each BR tag "consumes" text after it -->
                        <xsl:variable name="lnum" select="count(preceding-sibling::br)" />
                        <xsl:call-template name="verse">
                            <xsl:with-param name="verse-content"
                                select="following-sibling::node()[count(preceding-sibling::br) = $lnum+1 and name() != 'br']" />
                            <xsl:with-param name="verse-type" select="following-sibling::*[count(preceding-sibling::br) = $lnum+1 and (name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd')][1]" />
                        </xsl:call-template>
                    </xsl:for-each>
                </xsl:when>

                <!-- No BR's - collect the whole content -->
                <xsl:otherwise>
                    <xsl:call-template name="verse">
                        <xsl:with-param name="verse-content" select="child::node()" />
                        <xsl:with-param name="verse-type" select="wers_wciety|wers_akap|wers_cd[1]" />
                    </xsl:call-template>
                </xsl:otherwise>

            </xsl:choose>
        </xsl:element>
    </xsl:template>

    <xsl:template name="verse">
        <xsl:param name="verse-content" />
        <xsl:param name="verse-type" />

        <xsl:choose>
            <xsl:when test="not($verse-type)">
                <xsl:element name="v" namespace="http://nowoczesnapolska.org.pl/ML/Lektury/1.1">
                    <xsl:apply-templates select="$verse-content" />
                </xsl:element>
            </xsl:when>

            <xsl:otherwise>
                <xsl:apply-templates select="$verse-content" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <!-- akapity -->
    <xsl:template match="akap">
        <xsl:element name="p">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="akap_cd">
        <xsl:element name="pc">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="akap_dialog">
        <xsl:element name="pd">
            <xsl:variable name="prolog" select="./text()[1]" />            
            <xsl:value-of select="wlf:fix-dialog-line($prolog)" />
            <xsl:apply-templates select="@*|*|text()[. != $prolog]" />
        </xsl:element>
    </xsl:template>

    <!-- wersy -->
    <xsl:template match="wers_cd">
        <xsl:element name="vc">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="wers_akap">
        <xsl:element name="vi">
            <xsl:attribute name="size">p</xsl:attribute>
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="wers_wciety">
        <xsl:element name="vi">
            <xsl:if test="@typ">
            <xsl:attribute name="size"><xsl:value-of select="@typ" /></xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="@*[name() != 'typ']|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="zastepnik_wersu">
        <xsl:element name="verse-skip">
            <xsl:choose>
                <xsl:when test="starts-with(., '.')">
                    <xsl:attribute name="type">dot</xsl:attribute>
                </xsl:when>
            </xsl:choose> 
        </xsl:element>
    </xsl:template>

    <!-- Przypisy i motywy -->
    <xsl:template match="begin">
        <xsl:element name="mark">
            <xsl:attribute name="starts">
                <xsl:value-of select="substring(@id, 2)" />
            </xsl:attribute>
            <xsl:attribute name="themes">
                <xsl:value-of select="following-sibling::motyw[1]/text()" />
            </xsl:attribute>
        </xsl:element>
    </xsl:template>

    <xsl:template match="motyw" />

    <xsl:template match="end">
        <xsl:element name="mark">
            <xsl:attribute name="ends">
                <xsl:value-of select="substring(@id, 2)" />
            </xsl:attribute>
        </xsl:element>
    </xsl:template>

    <xsl:template match="pa|pe|pr|pt">
        <mark id="{generate-id(.)}" />
    </xsl:template>


    <xsl:template match="pa|pe|pr|pt" mode="annotations">
        <annotation refs="{generate-id(.)}" type="{name(.)}">
            <xsl:apply-templates select="@*|node()" />
        </annotation>
    </xsl:template>


    <!-- Tytuły -->
    <xsl:template match="autor_utworu">
        <xsl:element name="author">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="nazwa_utworu">
        <xsl:element name="title">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="naglowek_czesc">
        <chapter>
            <xsl:apply-templates select="@*|node()" />
        </chapter>
    </xsl:template>

    <xsl:template match="naglowek_akt">
        <act>
            <xsl:apply-templates select="@*|node()" />
        </act>
    </xsl:template>

    <xsl:template match="naglowek_scena">
        <scene>
            <xsl:apply-templates select="@*|node()" />
        </scene>
    </xsl:template>

    <xsl:template match="podtytul">
        <second-title>
            <xsl:apply-templates select="@*|node()" />
        </second-title>
    </xsl:template>

    <xsl:template match="srodtytul">
        <part-title>
            <xsl:apply-templates select="@*|node()" />
        </part-title>
    </xsl:template>

    <!-- elementy dramatu -->
    <xsl:template match="miejsce_czas">
        <xsl:element name="time-and-date">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>


    <xsl:template match="didaskalia|didask_tekst">
        <xsl:element name="stage-directions">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="motto">
        <xsl:element name="motto">
            <xsl:apply-templates select="@*|node()" />
        
        <xsl:variable name="sign" select="following-sibling::*[1][name() = 'motto_podpis']" />
        <signature>
            <xsl:apply-templates select="$sign/node()" />
        </signature>
        </xsl:element>
    </xsl:template>

    <xsl:template match="motto_podpis[preceding-sibling::*[1][name() = 'motto']]" />
        
    <xsl:template match="lista_osob">
        <person-list>
            <xsl:apply-templates select="@*|node()" />
        </person-list>
    </xsl:template>

    <xsl:template match="naglowek_listy">
        <caption>
            <xsl:apply-templates select="@*|node()" />
        </caption>
    </xsl:template>

    <xsl:template match="lista_osoba">
        <person>
            <xsl:apply-templates select="@*|node()" />
        </person>
    </xsl:template>

    <!-- Odstępy i prześwity -->
    <xsl:template match="sekcja_swiatlo">
        <vertical-space />
    </xsl:template>
    
    <xsl:template match="sekcja_asterysk">
        <vertical-space type="asterisk" />
    </xsl:template>

    <xsl:template match="sekcja_asterysk">
        <vertical-space type="line" />
    </xsl:template>

    <!-- pozostałe elementy blokowe -->
    <xsl:template match="dlugi_cytat">
        <block-quote>
            <xsl:apply-templates select="@*|node()" />
        </block-quote>`
    </xsl:template>

    <xsl:template match="poezja_cyt">
        <block-quote>
            <xsl:apply-templates select="@*|node()" />
        </block-quote>`
    </xsl:template>

    <xsl:template match="kwestia">
        <xsl:variable name="person" select="preceding-sibling::*[1][name() = 'naglowek_osoba']" />
        <drama-line>
            <person>
                <xsl:apply-templates select="$person/node()" />
            </person>
            <xsl:apply-templates select="node()[. != $person]" />
        </drama-line>
    </xsl:template>

    <xsl:template match="naglowek_osoba[following-sibling::*[1][name() = 'kwestia']]" />
        
    <!-- Inne -->
    <xsl:template match="osoba">
        <xsl:element name="person-ref">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="slowo_obce">
        <xsl:element name="df">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="wyroznienie">
        <xsl:element name="em">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="mat">
        <xsl:element name="math">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <!-- oznaczenie tytulu innego utworu, wymienionego w tym -->
    <xsl:template match="tytul_dziela">
        <xsl:element name="book-ref">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="extra">
        <xsl:element name="comment">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <xsl:template match="uwaga">
        <xsl:element name="edit-comment">
            <xsl:apply-templates select="@*|node()" />
        </xsl:element>
    </xsl:template>

    <!-- Copy attributes -->
    <xsl:template match="@*|comment()">
        <xsl:copy />
    </xsl:template>    

    <!-- Inside RDF meta-data, leave the text unchanged -->
    <xsl:template match="rdf:RDF//text()">
        <xsl:value-of select="." />
    </xsl:template>

    <!-- Normalize text in other nodes -->
    <xsl:template match="text()">
        <xsl:choose>
            <xsl:when test="$normalize-text">
                <xsl:value-of select="wlf:normalize-text(.)" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="." />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- Ignoruj RDF poza meta -->
    <xsl:template match="rdf:*|dc:*" />
   
    <xsl:template match="@*|node()" mode="meta">
        <xsl:copy>
            <xsl:apply-templates match="@*|node()" mode="meta" />
        </xsl:copy>
    </xsl:template>

    <!-- Warn about non-matched elements -->
    <xsl:template match="node()">
        <xsl:message>
            <xsl:text>Nieprzetworzony węzeł:</xsl:text>
            <xsl:value-of select="." />           
        </xsl:message>
        <unparsed-node>
            <xsl:copy-of select="." />
        </unparsed-node>
    </xsl:template>
    
</xsl:stylesheet>