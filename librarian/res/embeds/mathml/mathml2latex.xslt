<xsl:stylesheet version = '1.0'
xmlns:xsl='http://www.w3.org/1999/XSL/Transform'
xmlns:ldf="http://planet-sl.org/ldf"
xmlns:mml="http://www.w3.org/1998/Math/MathML">

<xsl:output method="txt" encoding="utf-8" omit-xml-declaration="yes"/> 

<xsl:template match="mtext">
	<xsl:text>\textrm{</xsl:text>
	<xsl:apply-templates select="node()"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="mi">
	<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="mn">
	<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="mo">
	<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="msup">
	<xsl:text>{</xsl:text>
	<xsl:apply-templates select="*[1]"/>
	<xsl:text>}^{</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="msub">
	<xsl:text>{</xsl:text>
	<xsl:apply-templates select="*[1]"/>
	<xsl:text>}_{</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="mrow">
	<xsl:text>{</xsl:text>
	<xsl:apply-templates select="node()"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="mfenced">
	<xsl:text>(</xsl:text>
	<xsl:apply-templates select="node()"/>
	<xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="mfrac">
	<xsl:text>\frac{</xsl:text>
	<xsl:apply-templates select="*[1]"/>
	<xsl:text>}{</xsl:text>
	<xsl:apply-templates select="*[2]"/>
	<xsl:text>}</xsl:text>
</xsl:template>

<xsl:template match="varepsilon">
	<xsl:text>\varepsilon </xsl:text>
</xsl:template>

</xsl:stylesheet>
