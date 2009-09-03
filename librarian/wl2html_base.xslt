
<xsl:stylesheet
    version="1.0"
    
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"   
    xmlns:wl2o="http://nowoczesnapolska.org.pl/WL/2.0/Overlay"   
    xmlns:wl="http://wolnelektury.pl/functions"

    exclude-result-prefixes="wl" >

    <xsl:variable name="config" select="document('config.xml')" />

    <xsl:output method="xml"
        encoding="utf-8"
        indent="yes"
        omit-xml-declaration = "yes" />

    <xsl:strip-space elements = "strofa utwor kwestia liryka_l liryka_lp powiesc opowiadanie dramat_wierszowany_lp" />
    <!--     
        Dokument ten opisuje podstawowe przekształcenia potrzebne
     do zamiany dokumentu WLML 1.0 na poprawnie sformatowany
     dokument XHMTL.

    -->

    <xsl:template name="generic-attributes">
        <xsl:param name="element" />
        <xsl:param name="mypath" />
        <xsl:variable name="tag" select="name($element)" />

        <xsl:if test="$with-paths">
        <xsl:attribute name="wl2o:path">
            <xsl:value-of select="$mypath" />
        </xsl:attribute>
        </xsl:if>

        <xsl:if test="$config//editable/*[name() = $tag]">
            <xsl:attribute name="wl2o:editable">editable</xsl:attribute>
        </xsl:if>

        <xsl:attribute name="class">
            <xsl:value-of select="$tag"/>
        </xsl:attribute>
    </xsl:template>

    <xsl:template name="generic-descent">
        <xsl:param name="element" />
        <xsl:param name="mypath" />
        
        <xsl:for-each select="child::node()">            
            <xsl:apply-templates select="." mode="element-tag">
                <xsl:with-param name="offset" select="position()" />
                <xsl:with-param name="parent-path" select="$mypath" />
            </xsl:apply-templates>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="generic-content">
        <xsl:param name="element" />
        <xsl:param name="mypath" />

        <xsl:call-template name="generic-attributes">
            <xsl:with-param name="element" select="$element" />
            <xsl:with-param name="mypath" select="$mypath" />
        </xsl:call-template>

        <xsl:call-template name="generic-descent">
            <xsl:with-param name="element" select="$element" />
            <xsl:with-param name="mypath" select="$mypath" />
        </xsl:call-template>
    </xsl:template>
    
    <!-- Generyczne szablony -->
    <xsl:template name="generic" >
        <xsl:param name="element" />
        <xsl:param name="mypath" />
        <xsl:param name="offset" />

        <!-- <xsl:param name="parent-type" select="'block'" /> -->

        <xsl:variable name="tag" select="name($element)" />        
            
        <xsl:choose>            
            <!-- ignore namespaced elements -->
            <xsl:when test="namespace-uri()" />

            <xsl:when test="$config//block-elements/*[local-name() = $tag]">
                <xsl:element name="div" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>

            <xsl:when test="$config//paragraph-elements/*[local-name() = $tag]">
                <xsl:element name="p" namespace="http://www.w3.org/1999/xhtml">                    
                        <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>
            
            <xsl:when test="$config//inline-elements/*[local-name() = $tag]">
                <xsl:element name="span" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>

            <xsl:when test="$config//header-1-elements/*[local-name() = $tag]">
                <xsl:element name="h1" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>

            <xsl:when test="$config//header-2-elements/*[local-name() = $tag]">
                <xsl:element name="h2" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>

            <xsl:when test="$config//header-3-elements/*[local-name() = $tag]">
                <xsl:element name="h3" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>

            <xsl:when test="$config//header-4-elements/*[local-name() = $tag]">
                <xsl:element name="h4" namespace="http://www.w3.org/1999/xhtml">
                    <xsl:apply-templates select="$element" mode="element-content" >
                        <xsl:with-param name="mypath" select="$mypath"/>
                    </xsl:apply-templates>
                </xsl:element>
            </xsl:when>

            <xsl:when test="$config//no-show-elements/*[local-name() = $tag]" />

            <xsl:otherwise>
                <xsl:message terminate="yes">
                    Nieznany tag '<xsl:value-of select="$tag" />' :(.
                </xsl:message>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    

    <!--
    <special-tags>
        <strofa />
        <lista_osob />
        <sekcja_swiatlo />
        <sekcja_asterysk />
        <separator_linia />
    </special-tags>
    -->    

    <xsl:template match="dlugi_cytat|poezja_cyt" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />
        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="blockquote" >
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>
            <xsl:call-template name="generic-descent">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>
        </xsl:element>
    </xsl:template>


    <xsl:template match="lista_osob" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />
        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="div" >
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>

            <xsl:apply-templates select="./naglowek-listy" mode="element-tag" />
            <ul>
                <xsl:for-each select="./lista_osoba">
                <xsl:apply-templates select="." mode="element-tag">
                    <xsl:with-param name="offset" select="position()" />
                    <xsl:with-param name="parent-path" select="$mypath" />
                </xsl:apply-templates>
                </xsl:for-each>
            </ul>
        </xsl:element>
    </xsl:template>

    <xsl:template match="lista_osoba" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />
        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="li" >
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>
            <xsl:call-template name="generic-descent">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>
        </xsl:element>
    </xsl:template>

    <xsl:template match="separator_linia" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />
        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="hr" >
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>            
        </xsl:element>
    </xsl:template>

    <xsl:template match="sekcja_swiatlo" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />
        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="br" >
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>
        </xsl:element>
    </xsl:template>

    <xsl:template match="sekcja_asterysk" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />
        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="p" >
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>
            *
        </xsl:element>
    </xsl:template>

    <xsl:template match="zastepnik_wersu|wers_akap|wers_cd|wers_wciety" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />

        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[',string($offset),']')" />
       
        <xsl:call-template name="generic-descent">
            <xsl:with-param name="element" select="current()" />
            <xsl:with-param name="mypath" select="$mypath" />
        </xsl:call-template>        
    </xsl:template>

    <!-- strofy -->
    <xsl:template match="strofa" mode="element-tag">
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />

        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:element name="div" >            
            <xsl:call-template name="generic-attributes">
                <xsl:with-param name="element" select="current()" />
                <xsl:with-param name="mypath" select="$mypath" />
            </xsl:call-template>

            <xsl:choose>
                <xsl:when test="count(br) > 0">
                    <xsl:call-template name="verse">
                        <xsl:with-param name="verse-content" select="br[1]/preceding-sibling::text() | br[1]/preceding-sibling::node()" />
                        <xsl:with-param name="verse-type" select="br[1]/preceding-sibling::*[name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd'][1]" />
                        <xsl:with-param name="mypath" select="$mypath" />
                    </xsl:call-template>
                    <xsl:for-each select="br">
        			<!-- Each BR tag "consumes" text after it -->
                        <xsl:variable name="lnum" select="count(preceding-sibling::br)" />
                        <xsl:call-template name="verse">
                            <xsl:with-param name="verse-content"
                                select="following-sibling::text()[count(preceding-sibling::br) = $lnum+1] | following-sibling::node()[count(preceding-sibling::br) = $lnum+1]" />
                            <xsl:with-param name="verse-type" select="following-sibling::*[count(preceding-sibling::br) = $lnum+1 and (name() = 'wers_wciety' or name() = 'wers_akap' or name() = 'wers_cd')][1]" />
                            <xsl:with-param name="mypath" select="$mypath" />
                        </xsl:call-template>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="verse">
                        <xsl:with-param name="verse-content" select="child::node()" />
                        <xsl:with-param name="verse-type" select="wers_wciety|wers_akap|wers_cd[1]" />
                        <xsl:with-param name="mypath" select="$mypath" />
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>

    <xsl:template name="verse">
        <xsl:param name="verse-content" />
        <xsl:param name="verse-type" />
        <xsl:param name="mypath" />

        <xsl:element name="p">
            <xsl:attribute name="class">
                <xsl:value-of select="name($verse-type)" />
            </xsl:attribute>
            <xsl:for-each select="$verse-content">
                <xsl:apply-templates select="." mode="element-tag">
                    <xsl:with-param name="offset" select="position()" />
                    <xsl:with-param name="parent-path" select="$mypath" />
                </xsl:apply-templates>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>


<!-- default content processing -->
    <xsl:template match="*" mode="element-content">
        <xsl:param name="mypath" />
        <xsl:call-template name="generic-content">
            <xsl:with-param name="element" select="current()"/>
            <xsl:with-param name="mypath" select="$mypath"/>
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="*" mode="element-tag" >
        <xsl:param name="offset" />
        <xsl:param name="parent-path" />

        <xsl:variable name="mypath"
            select="concat($parent-path, '/', name(), '[', string($offset),']')" />

        <xsl:call-template name="generic">
            <xsl:with-param name="element" select="current()" />
            <xsl:with-param name="offset" select="$offset" />
            <xsl:with-param name="mypath" select="$mypath" />
        </xsl:call-template>
    </xsl:template>

    <xsl:template match="text()" mode="element-tag">
        
        <xsl:value-of select="wl:substitute_entities(.)" />
        
        <!--<xsl:value-of select="." /> -->
    </xsl:template>

    <xsl:template match="node()" />
    
</xsl:stylesheet>
