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
			<xsl:apply-templates mode="poem"/>
		</stanza>
	</xsl:template>

	<!-- XXX: it should be done elsewhere but our cheap verse splitting
		puts it here -->
	<xsl:template match="motyw" mode="poem"/>

	<xsl:template mode="poem" match="wers_normalny|wers_cd|wers_wciety|wers_akap">
		<v><xsl:apply-templates mode="inline"/></v>
	</xsl:template>
</xsl:stylesheet>
