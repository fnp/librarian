<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wl="http://wolnelektury.pl/functions" >

<xsl:output encoding="utf-8" indent="yes" omit-xml-declaration = "yes" version="2.0" />


<xsl:template match="utwor">
    <!-- <html>
        <head>
            <title>Książka z serwisu WolneLektury.pl</title>
            <meta http-equiv="content-type" content="text/html;charset=utf-8"/>
        </head>
        <style>
            body {
                font-size: 16px;
                font: Georgia, "Times New Roman", serif;
                line-height: 1.5em;
                margin: 0;
            }

            a {
                color: blue;
                text-decoration: none;
            }

            #book-text {
                margin: 3em;
                max-width: 36em;
            }

            /* ================================== */
            /* = Header with logo and menu      = */
            /* ================================== */
            #header {
                margin: 3.4em 0 0 1.4em;
            }

            img {
                border: none;
            }


            #menu {
                position: fixed;
                left: 0em;
                top: 0em;
                width: 100%;
                height: 1.5em;
                background: #333;
                color: #FFF;
                opacity: 0.9;
            }

            #menu ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            #menu li a {
                display: block;
                float: left;
                width: 7.5em;
                height: 1.5em;
                margin-left: 0.5em;
                text-align: center;
                color: #FFF;
            }

            #menu li a:hover, #menu li a:active {
                color: #000;
                background: #FFF url(/media/img/arrow-down.png) no-repeat center right;
            }

            #menu li a.selected {
                color: #000;
                background: #FFF url(/media/img/arrow-up.png) no-repeat center right;
            }

            #toc, #themes {
                position: fixed;
                left: 0em;
                top: 1.5em;
                width: 37em;
                padding: 1.5em;
                background: #FFF;
                border-bottom: 0.25em solid #DDD;
                border-right: 0.25em solid #DDD;
                display: none;
                height: 16em;
                overflow-x: hidden;
                overflow-y: auto;
                opacity: 0.9;
            }

            #toc ol, #themes ol {
                list-style: none;
                padding: 0;
                margin: 0;
            }

            #toc ol li {
                font-weight: bold;
            }

            #toc ol ol {
                padding: 0 0 1.5em 1.5em;
                margin: 0;
            }

            #toc ol ol li {
                font-weight: normal;
            }

            #toc h2 {
                display: none;
            }

            #toc .anchor {
                float: none;
                margin: 0;
                color: blue;
                font-size: 16px;
                position: inherit;
            }

            /* =================================================== */
            /* = Common elements: headings, paragraphs and lines = */
            /* =================================================== */
            h1 {
                font-size: 3em;
                margin: 1.5em 0;
                text-align: center;
                line-height: 1.5em;
                font-weight: bold;
            }

            h2 {
                font-size: 2em;
                margin: 1.5em 0 0;
                font-weight: bold;
                line-height: 1.5em;
            }

            h3 {
                font-size: 1.5em;
                margin: 1.5em 0 0;
                font-weight: normal;
                line-height: 1.5em;
            }

            h4 {
                font-size: 1em;
                margin: 1.5em 0 0;
                line-height: 1.5em;
            }

            p {
                margin: 0;
            }

            /* ======================== */
            /* = Footnotes and themes = */
            /* ======================== */
            .theme-begin {
                border-left: 0.1em solid #DDDDDD;
                color: #777;
                padding: 0 0.5em;
                width: 7.5em;
                font-style: normal;
                font-weight: normal;
                font-size: 16px;
                float: right;
                margin-right: -9.5em;
                clear: both;
                left: 40em;
                line-height: 1.5em;
                text-align: left;
            }

            .annotation {
                font-style: normal;
                font-weight: normal;
                font-size: 12px;
            }

            #footnotes .annotation {
                display: block;
                float: left;
                width: 2.5em;
                clear: both;
            }

            #footnotes div {
                margin: 1.5em 0 0 0;
            }

            #footnotes p {
                margin-left: 2.5em;
                font-size: 0.875em;
            }

            blockquote {
                font-size: 0.875em;
            }

            /* ============= */
            /* = Numbering = */
            /* ============= */
            .anchor {
                position: absolute;
                margin: -0.25em -0.5em;
                left: 1em;
                color: #777;
                font-size: 12px;
                width: 2em;
                text-align: center;
                padding: 0.25em 0.5em;
                line-height: 1.5em;
            }

            .anchor:hover, #book-text .anchor:active {
                color: #FFF;
                background-color: #CCC;
            }

            /* =================== */
            /* = Custom elements = */
            /* =================== */
            span.author {
                font-size: 0.5em;
                display: block;
                line-height: 1.5em;
                margin-bottom: 0.25em;
            }

            span.collection {
                font-size: 0.375em;
                display: block;
                line-height: 1.5em;
                margin-bottom: -0.25em;
            }

            span.subtitle {
                font-size: 0.5em;
                display: block;
                line-height: 1.5em;
                margin-top: -0.25em;
            }

            div.didaskalia {
                font-style: italic;
                margin: 0.5em 0 0 1.5em;
            }

            div.kwestia {
                margin: 0.5em 0 0;
            }

            div.stanza {
                margin: 1.5em 0 0;
            }

            div.kwestia div.stanza {
                margin: 0;
            }

            p.paragraph {
                text-align: justify;
                margin: 1.5em 0 0;
            }

            p.motto {
                text-align: justify;
                font-style: italic;
                margin: 1.5em 0 0;
            }

            p.motto_podpis {
                font-size: 0.875em;
                text-align: right;
            }

            div.fragment {
                border-bottom: 0.1em solid #999;
                padding-bottom: 1.5em;
            }

            div.note p, div.dedication p, div.note p.paragraph, div.dedication p.paragraph {
                text-align: right;
                font-style: italic;
            }

            hr.spacer {
                height: 3em;
                visibility: hidden;
            }

            hr.spacer-line {
                margin: 1.5em 0;
                border: none;
                border-bottom: 0.1em solid #000;
            }

            p.spacer-asterisk {
                padding: 0;
                margin: 1.5em 0;
                text-align: center;
            }

            div.person-list ol {
                list-style: none;
                padding: 0 0 0 1.5em;
            }

            p.place-and-time {
                font-style: italic;
            }

            em.math, em.foreign-word, em.book-title, em.didaskalia {
                font-style: italic;
            }

            em.author-emphasis {
                letter-spacing: 0.1em;
            }

            em.person {
                font-style: normal;
                font-variant: small-caps;
            }
        </style>
        <body> -->
        <div id="book-text">
            <xsl:apply-templates select="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny" />
            <xsl:if test="count(descendant::*[self::pe or self::pa or self::pr or self::pt][not(parent::extra)])">
                <div id="footnotes">
                    <h3>Przypisy</h3>
                    <xsl:for-each select="descendant::*[self::pe or self::pa or self::pr or self::pt][not(parent::extra)]">
                        <div>
                            <a name="{concat('footnote-', generate-id(.))}" />
                            <a href="{concat('#anchor-', generate-id(.))}" class="annotation">[<xsl:number value="count(preceding::*[self::pa or self::pe or self::pr or self::pt]) + 1" />]</a>
                            <xsl:choose>
                                <xsl:when test="count(akap|akap_cd|strofa) = 0">
                                    <p><xsl:apply-templates select="text()|*" mode="inline" /></p>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:apply-templates select="text()|*" mode="inline" />
                                </xsl:otherwise>
                            </xsl:choose>
                        </div>
                    </xsl:for-each>
                </div>
            </xsl:if>
        </div>
        <!-- </body>
    </html> -->
</xsl:template>


<!-- ============================================================================== -->
<!-- = MASTER TAG                                                                 = -->
<!-- = (can contain block tags, paragraph tags, standalone tags and special tags) = -->
<!-- ============================================================================== -->
<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp|dramat_wspolczesny">
    <xsl:if test="nazwa_utworu">
        <h1>
            <xsl:apply-templates select="autor_utworu|dzielo_nadrzedne|nazwa_utworu|podtytul" mode="header" />
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

<xsl:template match="kwestia">
    <div class="kwestia">
        <xsl:apply-templates select="strofa|akap|didaskalia" />
    </div>
</xsl:template>

<xsl:template match="dlugi_cytat|poezja_cyt">
    <blockquote><xsl:apply-templates /></blockquote>
</xsl:template>

<xsl:template match="motto">
    <div class="motto"><xsl:apply-templates mode="inline" /></div>
</xsl:template>


<!-- ========================================== -->
<!-- = PARAGRAPH TAGS                         = -->
<!-- = (can contain inline and special tags)  = -->
<!-- ========================================== -->
<!-- Title page -->
<xsl:template match="autor_utworu" mode="header">
    <span class="author"><xsl:apply-templates mode="inline" /></span>
</xsl:template>

<xsl:template match="nazwa_utworu" mode="header">
    <span class="title"><xsl:apply-templates mode="inline" /></span>
</xsl:template>

<xsl:template match="dzielo_nadrzedne" mode="header">
    <span class="collection"><xsl:apply-templates mode="inline" /></span>
</xsl:template>

<xsl:template match="podtytul" mode="header">
    <span class="subtitle"><xsl:apply-templates mode="inline" /></span>
</xsl:template>

<!-- Section headers (included in index)-->
<xsl:template match="naglowek_akt|naglowek_czesc|srodtytul">
    <h2><xsl:apply-templates mode="inline" /></h2>
</xsl:template>

<xsl:template match="naglowek_scena|naglowek_rozdzial">
    <h3><xsl:apply-templates mode="inline" /></h3>
</xsl:template>

<xsl:template match="naglowek_osoba|naglowek_podrozdzial">
    <h4><xsl:apply-templates mode="inline" /></h4>
</xsl:template>

<!-- Other paragraph tags -->
<xsl:template match="miejsce_czas">
    <p class="place-and-time"><xsl:apply-templates mode="inline" /></p>
</xsl:template>

<xsl:template match="didaskalia">
    <div class="didaskalia"><xsl:apply-templates mode="inline" /></div>
</xsl:template>

<xsl:template match="lista_osoba">
    <li><xsl:apply-templates mode="inline" /></li>
</xsl:template>

<xsl:template match="akap|akap_dialog|akap_cd">
    <p class="paragraph"><xsl:apply-templates mode="inline" /></p>
</xsl:template>

<xsl:template match="strofa">
    <div class="stanza">
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
    </div>
</xsl:template>

<xsl:template name="verse">
    <xsl:param name="verse-content" />
    <xsl:param name="verse-type" />
    <p class="verse">
        <xsl:choose>
            <xsl:when test="name($verse-type) = 'wers_akap'">
                <xsl:attribute name="style">padding-left: 1em</xsl:attribute>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_wciety'">
                <xsl:choose>
                    <xsl:when test="$verse-content/@typ">
                        <xsl:attribute name="style">padding-left: <xsl:value-of select="$verse-content/@typ" />em</xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="style">padding-left: 1em</xsl:attribute>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:when test="name($verse-type) = 'wers_cd'">
                <xsl:attribute name="style">padding-left: 12em</xsl:attribute>
            </xsl:when>
        </xsl:choose>
        <xsl:apply-templates select="$verse-content" mode="inline" />
    </p>
</xsl:template>

<xsl:template match="motto_podpis">
    <p class="motto_podpis"><xsl:apply-templates mode="inline" /></p>
</xsl:template>


<!-- ================================================ -->
<!-- = INLINE TAGS                                  = -->
<!-- = (contain other inline tags and special tags) = -->
<!-- ================================================ -->
<!-- Annotations -->
<xsl:template match="pa|pe|pr|pt" mode="inline">
    <a name="{concat('anchor-', generate-id(.))}" />
    <a href="{concat('#footnote-', generate-id(.))}" class="annotation">[<xsl:number value="count(preceding::*[self::pa or self::pe or self::pr or self::pt]) + 1" />]</a>
</xsl:template>

<!-- Other inline tags -->
<xsl:template match="mat" mode="inline">
    <em class="math"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="didask_tekst" mode="inline">
    <em class="didaskalia"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="slowo_obce" mode="inline">
    <em class="foreign-word"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="tytul_dziela" mode="inline">
    <em class="book-title">
        <xsl:if test="@typ = '1'">„</xsl:if><xsl:apply-templates mode="inline" /><xsl:if test="@typ = '1'">”</xsl:if>
    </em>
</xsl:template>

<xsl:template match="wyroznienie" mode="inline">
    <em class="author-emphasis"><xsl:apply-templates mode="inline" /></em>
</xsl:template>

<xsl:template match="osoba" mode="inline">
    <em class="person"><xsl:apply-templates mode="inline" /></em>
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

