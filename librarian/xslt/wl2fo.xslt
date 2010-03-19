<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    version="1.0"

    xmlns:wlml="http://nowoczesnapolska.org.pl/ML/Lektury/1.1"

    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"   
    xmlns:fo="http://www.w3.org/1999/XSL/Format"
    xmlns:wl="http://wolnelektury.pl/functions" >

    <xsl:output method="xml"
        encoding="utf-8"
        indent="yes"
        omit-xml-declaration = "yes" />

<!-- generic template parameters -->

    <xsl:param name="verse-numbers-interval" select="5" />

<!-- main templates -->

    <xsl:template match="/">
        <fo:root >

            <fo:layout-master-set>
    <!-- layout information -->
                <fo:simple-page-master
                    master-name="title-page"
                  page-height="29.7cm"
                  page-width="21cm"
                  margin-top="2.5cm"
                  margin-bottom="2.5cm"
                  margin-left="2.5cm"
                  margin-right="2.5cm">      
                    <fo:region-body />     
                </fo:simple-page-master>

                <fo:simple-page-master
                    master-name="blank-page"
                    page-height="29.7cm"
                    page-width="21cm"

                    margin-top="2.5cm"
                    margin-bottom="2.5cm"
                    margin-left="2.5cm"
                    margin-right="2.5cm">
                    <fo:region-body />
                </fo:simple-page-master>

                <fo:simple-page-master
        master-name="first-main"
                  page-height="29.7cm"
                  page-width="21cm"
                  margin-top="2cm"
                  margin-bottom="2cm"
                  margin-left="3cm"
                  margin-right="2cm">
                    <fo:region-body
                margin-top="2cm"
                margin-bottom="2cm" />
                    <fo:region-after
                region-name="odd-after"
                display-align="after"
                extent="2cm" />
                </fo:simple-page-master>

                <fo:simple-page-master
        master-name="odd"
                  page-height="29.7cm"
                  page-width="21cm"
                  margin-top="2cm"
                  margin-bottom="2cm"
                  margin-left="3cm"
                  margin-right="2cm">
                    <fo:region-body
                margin-top="2cm"
                margin-bottom="2cm" />

                    <fo:region-before
                region-name="odd-before"
                extent="2cm" />

                    <fo:region-after
                region-name="odd-after"
                display-align="after"
                extent="2cm" />
                </fo:simple-page-master>

                <fo:simple-page-master
        master-name="even"
                  page-height="29.7cm"
                  page-width="21cm"
                  margin-top="2cm"
                  margin-bottom="2cm"
                  margin-left="2cm"
                  margin-right="3cm">
                    <fo:region-body
                margin-top="2cm"
                margin-bottom="2cm" />

                    <fo:region-before
                region-name="even-before"
                extent="2cm" />

                    <fo:region-after
                region-name="even-after"
                display-align="after"
                extent="2cm" />
                </fo:simple-page-master>


                <fo:page-sequence-master master-name="book-titles">
                    <fo:single-page-master-reference master-reference="title-page" />
                    <fo:repeatable-page-master-reference master-reference="blank-page" />
                </fo:page-sequence-master>

                <fo:page-sequence-master master-name="main">
                    <fo:repeatable-page-master-alternatives>
                        <fo:conditional-page-master-reference
                master-reference="first-main"
                page-position="first"
                odd-or-even="odd" />

                        <fo:conditional-page-master-reference
                master-reference="odd"
                page-position="rest"
                odd-or-even="odd" />

                        <fo:conditional-page-master-reference
                master-reference="even"
                page-position="any"
                odd-or-even="even" />                
                    </fo:repeatable-page-master-alternatives>

                </fo:page-sequence-master>

            </fo:layout-master-set>
  <!-- end: defines page layout -->

<!--
    TITLE PAGE, COPYRIGHT, ETC. \
-->
            <fo:page-sequence
                master-reference="book-titles">

                <fo:flow flow-name="xsl-region-body"
                    font-family="Antique"
                    text-align="center"
                >

                    <fo:block font-size="32pt" display-align="center" >
                        <fo:marker marker-class-name="author">
                            <xsl:value-of select="//wlml:author" />
                        </fo:marker>
                        <xsl:apply-templates select="//wlml:author/node()" mode="title"/>
                    </fo:block>
  
                    <fo:block font-size="48pt" display-align="center" >
                        <fo:marker marker-class-name="main-title">
                            <xsl:value-of select="//wlml:title" />
                        </fo:marker>
                        <xsl:apply-templates select="//wlml:title/node()" mode="title"/>
                    </fo:block>
                </fo:flow>
            </fo:page-sequence>

<!--
    MAIN BOOK CONTENT
-->
            <fo:page-sequence
        master-reference="main"
        initial-page-number="1"
        force-page-count="even"
    >

    <fo:static-content
     flow-name="xsl-footnote-separator">
      <fo:block text-align-last="justify">
	<fo:leader leader-pattern="rule"/>
      </fo:block>
    </fo:static-content>

                <fo:static-content
                    flow-name="odd-after" font-family="Antique" text-align="center">
                    <fo:block>
                        <fo:page-number />
                    </fo:block>
                </fo:static-content>

                <fo:static-content
                    flow-name="even-after" font-family="Antique" text-align="center">
                    <fo:block>
                        <fo:page-number />
                    </fo:block>
                </fo:static-content>


                <fo:static-content
        flow-name="even-before"
        font-family="Antique"
        text-align="right">

                    <fo:block border-bottom-width="0.2mm"
        border-bottom-style="solid"
        border-bottom-color="black">
                        <fo:retrieve-marker retrieve-class-name="main-title" />
                    </fo:block>
                </fo:static-content>

                <fo:static-content
        flow-name="odd-before"
        font-family="Antique"
        text-align="left">
   
                    <fo:block border-after-width="0.2mm"
        border-after-style="solid"
        border-after-color="black">
                        <fo:retrieve-marker retrieve-class-name="chapter-title" />
                    </fo:block>
                </fo:static-content>


    
                <fo:flow flow-name="xsl-region-body" font-family="Antique">
        
                    <fo:marker marker-class-name="author">
                        <xsl:value-of select="//wlml:author" />
                    </fo:marker>
                    <fo:marker marker-class-name="main-title">
                        <xsl:value-of select="//wlml:title" />
                    </fo:marker>

                    <xsl:apply-templates select="//wlml:main-text" />
                </fo:flow>
    
            </fo:page-sequence>
        </fo:root>
    </xsl:template>

    <xsl:template match="wlml:main-text">        
        <xsl:apply-templates select="child::*" />
    </xsl:template>

<!-- 
    PROZA: elementy proste 
-->

    <xsl:template match="wlml:chapter">
        <fo:block text-align="left" font-size="32pt" font-weight="bold" font-variant="small-caps">
            <fo:marker marker-class-name="chapter-title">
                <xsl:apply-templates select="node()" />
            </fo:marker>
            <xsl:apply-templates select="node()" />            
        </fo:block>
    </xsl:template>

    <xsl:template match="wlml:p">
        <fo:block
        space-before="1em" 
        space-after="1em" 
        start-indent="1.5em">        
            <xsl:apply-templates select="child::node()" />
        </fo:block>
    </xsl:template>

    <xsl:template match="wlml:pd">
        <fo:block
        space-before="1em" 
        space-after="1em" 
        start-indent="0em"
    >&#x2014;&#x00a0;
            <xsl:apply-templates select="child::node()" />
        </fo:block>
    </xsl:template>

    <xsl:template match="wlml:pd/text()[1]">
        <xsl:value-of select="substring-after(., '&#x2014; ')" />
    </xsl:template>

<!-- 
    POEZJA
-->
    <xsl:template match="wlml:stanza">
        <fo:list-block
            space-before="1.5em" space-after="1.5em">
            <xsl:apply-templates select="child::node()" />            
        </fo:list-block>
    </xsl:template>

    <xsl:template match="wlml:v|wlml:vi|wlml:vc">
        <fo:list-item>
            <xsl:attribute name="id"><xsl:value-of select="local-name()"/>-<xsl:value-of select="generate-id()"/></xsl:attribute>

            <xsl:if test="count(preceding-sibling::wlml:v|preceding-sibling::wlml:vi|preceding-sibling::wlml:vc) &lt; 2">
                <xsl:attribute name="keep-with-previous.within-page">always</xsl:attribute>
            </xsl:if>

            <xsl:if test="count(following-sibling::wlml:v|following-sibling::wlml:vi|following-sibling::wlml:vc) &lt; 2">
                <xsl:attribute name="keep-with-next.within-page">always</xsl:attribute>
            </xsl:if>

            <xsl:variable name="vc"><xsl:number count="wlml:v|wlml:vi|wlml:vc" level="any" from="wlml:chapter" /></xsl:variable>

            <fo:list-item-label start-indent="-1cm">
                <fo:block><xsl:if test="($vc mod 5) = 0"><xsl:value-of select="$vc" /></xsl:if></fo:block>
            </fo:list-item-label>
            <fo:list-item-body start-indent="0cm">
                <fo:block><xsl:apply-templates select="node()" /></fo:block>
            </fo:list-item-body>
        </fo:list-item>
    </xsl:template>

<!--
    Wyroznienia
-->
    <xsl:template match="wlml:df">
        <fo:inline font-style="italic">
            <xsl:apply-templates select="node()" />
        </fo:inline>
    </xsl:template>


<!--
    Przypisy
-->
<xsl:template match="wlml:mark[//wlml:annotation/@refs = @id]">
    <xsl:variable name="annot" select="//wlml:annotation[@refs = current()/@id]" />
    <fo:footnote>
        <fo:inline><xsl:number level="any" /></fo:inline>
        <fo:footnote-body>
            <fo:block><xsl:apply-templates select="$annot/node()" /></fo:block>
        </fo:footnote-body>
    </fo:footnote>
</xsl:template>

<xsl:template match="*" />

</xsl:stylesheet>
