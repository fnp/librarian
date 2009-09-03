<xsl:stylesheet version="1.0"    
    xmlns="http://www.w3.org/1999/xhtml"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:param name="with-paths" select="boolean(0)" />
    <xsl:param name="base-path" select="'.'"/>
    <xsl:param name="base-offset" select="1" />    
    
    <xsl:include href="wl2html_base.xslt" />    
    <xsl:output encoding="utf-8" indent="yes" omit-xml-declaration = "yes" /> 

    <xsl:template match="/">
        <xsl:message>Processing...</xsl:message>
        <xsl:apply-templates select="/*" mode="element-tag">
            <xsl:with-param name="offset" select="$base-offset" />
            <xsl:with-param name="parent-path" select="$base-path" />
        </xsl:apply-templates>
    </xsl:template>   

</xsl:stylesheet>