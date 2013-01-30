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

	<!-- inline elements -->

	<!-- ignored -->
	<xsl:template match="motyw" mode="inline"/>

	<!-- formatting -->
	<xsl:template match="slowo_obce" mode="inline">
		<emphasis>
			<xsl:apply-templates mode="inline"/>
		</emphasis>
	</xsl:template>
	<xsl:template match="tytul_dziela" mode="inline">
		<emphasis>
            <xsl:if test="@typ">„</xsl:if>
			<xsl:apply-templates mode="inline"/>
            <xsl:if test="@typ">”</xsl:if>
		</emphasis>
	</xsl:template>
	<xsl:template match="wyroznienie" mode="inline">
		<strong>
			<xsl:apply-templates mode="inline"/>
		</strong>
	</xsl:template>

	<!-- text -->
	<xsl:template match="text()" mode="inline">
		<xsl:value-of select="wl:substitute_entities(.)"/>
	</xsl:template>

	<xsl:template match="uwaga" mode="inline"/>
	<xsl:template match="extra" mode="inline"/>
</xsl:stylesheet>
