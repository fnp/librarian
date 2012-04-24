<?xml version="1.0" encoding="utf-8"?>
<!--

	This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
	Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.

-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:wl="http://wolnelektury.pl/functions"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"
	xmlns:l="http://www.w3.org/1999/xlink">

	<!-- footnote body mode -->
	<xsl:template match="pe" mode="footnotes">
		<!-- we number them absolutely -->
		<xsl:variable name="n" select="count(preceding::pe) + 1"/>

		<xsl:element name="section">
			<xsl:attribute name="id">fn<xsl:value-of select="$n"/></xsl:attribute>

			<p><xsl:apply-templates mode="inline"/></p>
		</xsl:element>
	</xsl:template>
	<xsl:template match="text()" mode="footnotes"/>

	<!-- footnote links -->
	<xsl:template match="pe" mode="inline">
		<xsl:variable name="n" select="count(preceding::pe) + 1"/>
		<xsl:element name="a">
			<xsl:attribute name="type">note</xsl:attribute>
			<xsl:attribute name="l:href">#fn<xsl:value-of select="$n"/></xsl:attribute>

			[<xsl:value-of select="$n"/>]
		</xsl:element>
	</xsl:template>
</xsl:stylesheet>
