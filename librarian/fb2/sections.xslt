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

	<!-- a nice epigraph section -->
	<xsl:template match="dedykacja|nota|nota_red" mode="sections">
		<epigraph>
			<xsl:apply-templates mode="para"/>
			<!-- XXX: <strofa/> can be here as well -->
		</epigraph>
	</xsl:template>

	<!-- main text is split by headings -->
	<xsl:template match="naglowek_rozdzial" mode="sections">
		<!--

		This one's tricky - we need to sections text into sections.
		In order to do that, all elements belonging to a single section
		must have something in common. We assume that this common factor
		is having the same number of following section headings.

		-->

		<section>
			<xsl:apply-templates mode="para"
				select="../*[count(following-sibling::naglowek_rozdzial)
					= count(current()/following-sibling::naglowek_rozdzial)]"/>
		</section>
	</xsl:template>

	<!-- actual headings -->
	<xsl:template match="naglowek_rozdzial" mode="para">
		<title><p><xsl:apply-templates mode="inline"/></p></title>
	</xsl:template>
</xsl:stylesheet>
