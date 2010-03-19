<?xml version="1.0" encoding="utf-8"?>
<!--
#
#    This file is part of Librarian.
#
#    Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>
#    
#    For full list of contributors see AUTHORS file. 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
-->
<xsl:stylesheet version="1.0"    
    xmlns="http://www.w3.org/1999/xhtml"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:param name="with-paths" select="boolean(0)" />       
    <xsl:param name="with-annotations" select="boolean(1)" />
    
    <xsl:include href="wl2html_base.xslt" />
    <xsl:output encoding="utf-8" indent="yes" omit-xml-declaration = "yes" />

    <xsl:template match="/">
        <div class="document">

            <xsl:if test="with-toc" />

            <xsl:apply-templates select="/utwor" mode="element-tag">                
                <xsl:with-param name="parentpath" select="''" />
                <xsl:with-param name="offset" select="0" />
                <xsl:with-param name="mixed" select="false()" />
            </xsl:apply-templates>

            <xsl:if test="with-annotations" />
        </div>
    </xsl:template>

</xsl:stylesheet>