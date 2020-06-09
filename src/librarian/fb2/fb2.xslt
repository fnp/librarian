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

	<xsl:include href="description.xslt"/>
	<xsl:include href="footnotes.xslt"/>
	<xsl:include href="inline.xslt"/>
	<xsl:include href="paragraphs.xslt"/>
	<xsl:include href="poems.xslt"/>
	<xsl:include href="sections.xslt"/>
	<xsl:include href="drama.xslt"/>

	<xsl:strip-space elements="*"/>
	<xsl:output encoding="utf-8" method="xml" indent="yes"/>

	<xsl:template match="utwor">
		<FictionBook>
			<xsl:apply-templates mode="outer"/>

			<body name="notes">
				<xsl:apply-templates mode="footnotes"/>
			</body>
		</FictionBook>
	</xsl:template>

	<!-- we can't handle lyrics nicely yet -->
	<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp|dramat_wierszowany_l|dramat_wierszowany_lp" mode="outer">
		<body> <!-- main body for main book flow -->
			<xsl:if test="autor_utworu or nazwa_utworu">
				<title>
					<xsl:apply-templates mode="title"
						select="autor_utworu|dzielo_nadrzedne|nazwa_utworu|podtytul"/>
                    <xsl:call-template name="translators" />
				</title>
			</xsl:if>

			<epigraph>
				<p>
					Utwór opracowany został w&#160;ramach projektu
						<a l:href="http://www.wolnelektury.pl/">Wolne Lektury</a>
					przez <a l:href="http://www.nowoczesnapolska.org.pl/">fundację
						Nowoczesna Polska</a>.
				</p>
			</epigraph>

			<xsl:call-template name="section" />
		</body>
	</xsl:template>

	<xsl:template match="uwaga" mode="outer"/>
	<xsl:template match="extra" mode="outer"/>

	<xsl:template mode="title" match="*">
		<!-- title -->

		<p><xsl:apply-templates mode="inline"/></p>
	</xsl:template>

    <xsl:template name="translators">
        <xsl:if test="//dc:contributor.translator">
            <p>
                <xsl:text>tłum. </xsl:text>
                <xsl:for-each select="//dc:contributor.translator">
                    <xsl:if test="position() != 1">, </xsl:if>
                    <xsl:apply-templates mode="person" />
                </xsl:for-each>
            </p>
        </xsl:if>
    </xsl:template>

    <xsl:template match="text()" mode="person">
        <xsl:value-of select="wl:person_name(.)" />
    </xsl:template>


	<xsl:template match="uwaga" mode="title"/>
	<xsl:template match="extra" mode="title"/>
</xsl:stylesheet>
