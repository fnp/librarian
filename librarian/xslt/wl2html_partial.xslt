<?xml version="1.0" encoding="utf-8"?>
<!--

   This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
   Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.

-->
<xsl:stylesheet version="1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:param name="with-paths" select="boolean(0)" />
    <xsl:param name="base-path" select="'.'"/>
    <xsl:param name="base-offset" select="0" />

    <xsl:include href="wl2html_base.xslt" />

    <xsl:output
        encoding="utf-8"
        indent="yes"
        omit-xml-declaration = "yes" />

    <xsl:template match="/">
        <chunk>
        <xsl:apply-templates select="//chunk/child::node()" mode="element-tag">
            <xsl:with-param name="offset" select="$base-offset" />
            <xsl:with-param name="parent-path" select="$base-path" />
            <xsl:with-param name="mixed" select="true()" />
        </xsl:apply-templates>
        </chunk>
    </xsl:template>

</xsl:stylesheet>