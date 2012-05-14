<?xml version="1.0" encoding="utf-8"?>
<!--

	This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
	Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.

-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">

	<!-- description parsing -->
	<xsl:template match="rdf:Description" mode="outer">
		<description>
			<!-- need to keep ordering here... -->

			<title-info>
				<!-- obligatory: genre, author, book-title, lang -->

				<!-- XXX -->
				<genre>literature</genre> 
				<xsl:apply-templates mode="description"
					select="dc:creator"/>
				<xsl:apply-templates mode="description"
					select="dc:title"/>
				<xsl:apply-templates mode="description"
					select="dc:date.pd"/>
				<xsl:apply-templates mode="description"
					select="dc:language"/>
			</title-info>
			<document-info>
				<!-- obligatory: author, date, id, version -->

				<xsl:apply-templates mode="description"
					select="dc:contributor.editor"/>
				<xsl:apply-templates mode="description"
					select="dc:contributor.technical_editor"/>
				<program-used>book2fb2</program-used>
				<!-- maybe today's date instead? -->
				<xsl:apply-templates mode="description"
					select="dc:date"/>
				<xsl:apply-templates mode="description"
					select="dc:identifier.url"/>
				<!-- XXX -->
				<version>0</version>
			</document-info>
			<publish-info>
				<xsl:apply-templates mode="description"
					select="dc:publisher"/>
			</publish-info>
		</description>
	</xsl:template>

	<xsl:template mode="description"
			match="dc:creator|dc:contributor.editor|dc:contributor.technical_editor">
		<!-- last name, first name -->
		<xsl:variable name="last"
			select="normalize-space(substring-before(., ','))"/>
		<xsl:variable name="first"
			select="normalize-space(substring-after(., ','))"/>

		<author>
			<first-name><xsl:value-of select="$first"/></first-name>
			<last-name><xsl:value-of select="$last"/></last-name>
		</author>
	</xsl:template>
	<xsl:template mode="description" match="dc:title">
		<book-title><xsl:value-of select="."/></book-title>
	</xsl:template>
	<xsl:template mode="description" match="dc:language">
		<lang><xsl:value-of select="."/></lang>
	</xsl:template>
	<xsl:template mode="description" match="dc:date.pd|dc:date">
		<date><xsl:value-of select="."/></date>
	</xsl:template>
	<xsl:template mode="description" match="dc:publisher">
		<publisher><xsl:value-of select="."/></publisher>
	</xsl:template>
	<xsl:template mode="description" match="dc:identifier.url">
		<id><xsl:value-of select="."/></id>
	</xsl:template>
</xsl:stylesheet>
