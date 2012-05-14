<?xml version="1.0" encoding="utf-8"?>
<!--

	This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
	Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.

-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:wl="http://wolnelektury.pl/functions"
	xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"
	xmlns:l="http://www.w3.org/1999/xlink">

	<xsl:include href="description.xslt"/>
	<xsl:include href="footnotes.xslt"/>
	<xsl:include href="inline.xslt"/>
	<xsl:include href="paragraphs.xslt"/>
	<xsl:include href="poems.xslt"/>
	<xsl:include href="sections.xslt"/>

	<xsl:strip-space elements="*"/>
	<xsl:output encoding="utf-8" method="xml" indent="yes"/>

	<xsl:template match="utwor">
		<FictionBook>
			<xsl:apply-templates mode="outer"/>

			<body name="footnotes">
				<xsl:apply-templates mode="footnotes"/>
			</body>
		</FictionBook>
	</xsl:template>

	<!-- we can't handle lyrics nicely yet -->
	<xsl:template match="powiesc|opowiadanie|liryka_l|liryka_lp" mode="outer">
		<body> <!-- main body for main book flow -->
			<xsl:if test="autor_utworu or nazwa_utworu">
				<title>
					<xsl:apply-templates mode="title"
						select="autor_utworu|dzielo_nadrzedne|nazwa_utworu"/>
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

			<xsl:variable name="sections" select="count(naglowek_rozdzial)"/>
			<section>
				<xsl:choose>
					<xsl:when test="local-name() = 'liryka_l'">
						<poem>
							<xsl:apply-templates mode="para"/>
						</poem>
					</xsl:when>

					<xsl:otherwise>
						<xsl:apply-templates mode="para"
							select="*[count(following-sibling::naglowek_rozdzial)
							= $sections]"/>
					</xsl:otherwise>
				</xsl:choose>
			</section>

			<xsl:apply-templates mode="sections"/>
		</body>
	</xsl:template>

	<xsl:template match="uwaga" mode="outer"/>
	<xsl:template match="extra" mode="outer"/>

	<xsl:template mode="title" match="*">
		<!-- title -->

		<p><xsl:apply-templates mode="inline"/></p>
	</xsl:template>

	<xsl:template match="uwaga" mode="title"/>
	<xsl:template match="extra" mode="title"/>
</xsl:stylesheet>
