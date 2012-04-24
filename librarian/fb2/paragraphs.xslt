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

	<xsl:template mode="para" match="autor_utworu|nazwa_utworu|akap|akap_dialog">
		<!-- paragraphs & similar -->

		<p><xsl:apply-templates mode="inline"/></p>
	</xsl:template>

	<!-- in global scope -->

	<xsl:template mode="sections" match="akap|akap_dialog">
		<!-- paragraphs & similar -->

		<p><xsl:apply-templates mode="inline"/></p>
	</xsl:template>
	<xsl:template mode="sections" match="autor_utworu|nazwa_utworu"/>
</xsl:stylesheet>
