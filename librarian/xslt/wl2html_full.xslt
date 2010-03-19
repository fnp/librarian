<xsl:stylesheet version="1.0"    
    xmlns="http://www.w3.org/1999/xhtml"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:param name="with-paths" select="boolean(0)" />       
    <xsl:param name="with-annotations" select="boolean(1)" />
    
    <xsl:include href="wl2html_base.xslt" />
    <xsl:output encoding="utf-8" indent="yes" omit-xml-declaration = "yes" />

    <xsl:template match="/">
        <div class="document">

            <xsl:if test="with-toc" />

            <xsl:apply-templates select="/utwor" mode="element-tag">                
                <xsl:with-param name="parentpath" select="''" />
                <xsl:with-param name="offset" select="0" />
                <xsl:with-param name="mixed" select="false()" />
            </xsl:apply-templates>

            <xsl:if test="with-annotations" />
        </div>
    </xsl:template>

</xsl:stylesheet>