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

	<!-- in paragraph mode -->

	<xsl:template mode="para" match="akap|akap_dialog|akap_cd|motto_podpis">
		<!-- paragraphs & similar -->

		<p><xsl:apply-templates mode="inline"/></p>
	</xsl:template>

	<xsl:template mode="para" match="dlugi_cytat|motto|dedykacja|nota">
		<cite><xsl:apply-templates mode="para"/></cite>
	</xsl:template>

	<xsl:template mode="para" match="srodtytul">
		<p><strong><xsl:apply-templates mode="inline"/></strong></p>
	</xsl:template>

	<xsl:template mode="para" match="sekcja_swiatlo">
		<empty-line/><empty-line/><empty-line/>
	</xsl:template>

	<xsl:template mode="para" match="sekcja_asterysk">
		<empty-line/><p>*</p><empty-line/>
	</xsl:template>

	<xsl:template mode="para" match="separator_linia">
		<empty-line/><p>————————</p><empty-line/>
	</xsl:template>

	<xsl:template mode="para" match="tabela">
		<table><xsl:apply-templates mode="para" /></table>
	</xsl:template>
	<xsl:template mode="para" match="wiersz">
		<tr><xsl:apply-templates mode="para" /></tr>
	</xsl:template>
	<xsl:template mode="para" match="kol">
		<td><xsl:apply-templates mode="inline" /></td>
	</xsl:template>



	<xsl:template mode="para" match="*"/>
	<xsl:template mode="sections" match="*"/>
</xsl:stylesheet>
