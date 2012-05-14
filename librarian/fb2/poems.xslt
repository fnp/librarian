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

	<!-- poems -->

	<!-- match poem citations -->
	<xsl:template mode="para" match="poezja_cyt">
		<cite>
			<poem>
				<xsl:apply-templates mode="para"/>
			</poem>
		</cite>
	</xsl:template>

	<!-- regular poem elements -->
	<xsl:template mode="para" match="strofa">
		<stanza>
			<xsl:call-template name="split-poem">
				<xsl:with-param name="list" select="."/>
			</xsl:call-template>
		</stanza>
	</xsl:template>

	<!-- split into verses -->
	<xsl:template name="split-poem">
		<xsl:param name="list"></xsl:param>

		<xsl:if test="$list != ''">
			<xsl:variable name="before"
				select="substring-before(concat($list, '/'), '/')"/>
			<xsl:variable name="after"
				select="substring-after($list, '/')"/>

			<v>
				<xsl:value-of select="$before"/>
			</v>

			<xsl:call-template name="split-poem">
				<xsl:with-param name="list" select="$after"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
