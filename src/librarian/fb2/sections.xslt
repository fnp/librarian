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

    <xsl:template name="section">
        <!-- All the <_section> are in the end. -->
        <xsl:if test="count(*) &gt; count(_section)">
            <section>
                <xsl:choose>
                    <xsl:when test="(local-name() = 'liryka_l' or local-name() = 'liryka_lp')
                                     and count(_section) = 0">
                        <poem>
                            <xsl:apply-templates mode="para" />
                        </poem>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates mode="para" />
                    </xsl:otherwise>
                </xsl:choose>
            </section>
        </xsl:if>

        <!-- Now, recursively, all the _section tags. -->
        <xsl:apply-templates mode="section" select="_section" />
    </xsl:template>

    <xsl:template match="_section" mode="para" />
    <xsl:template match="_section" mode="section" >
        <section>
            <xsl:call-template name="section" />
        </section>
    </xsl:template>

	<!-- actual headings -->
	<xsl:template match="naglowek_czesc|naglowek_rozdzial|naglowek_podrozdzial|naglowek_akt|naglowek_scena" mode="para">
		<title><p><xsl:apply-templates mode="inline"/></p></title>
	</xsl:template>
</xsl:stylesheet>
