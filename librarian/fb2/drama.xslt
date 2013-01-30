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

	<xsl:template mode="para" match="lista_osob">
        <empty-line/>
		<xsl:apply-templates mode="para"/>
        <empty-line/>
	</xsl:template>

	<xsl:template mode="para" match="kwestia">
        <empty-line/>
		<xsl:apply-templates mode="para"/>
        <empty-line/>
	</xsl:template>

	<xsl:template mode="para" match="lista_osoba">
		<p><xsl:apply-templates mode="inline"/></p>
	</xsl:template>

	<xsl:template mode="para" match="naglowek_listy|naglowek_osoba">
		<p><strong><xsl:apply-templates mode="inline"/></strong></p>
	</xsl:template>

	<xsl:template mode="para" match="miejsce_czas|didaskalia|didask_tekst">
		<p><emphasis><xsl:apply-templates mode="inline"/></emphasis></p>
	</xsl:template>

	<xsl:template mode="inline" match="didaskalia|didask_tekst">
		<emphasis><xsl:apply-templates mode="inline"/></emphasis>
	</xsl:template>

</xsl:stylesheet>
