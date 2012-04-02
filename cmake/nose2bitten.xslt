<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/testsuite">
	    <report category="test">
            <xsl:for-each select="testcase">
	            <test>
                    <duration><xsl:value-of select="@time" /></duration>
                    <fixture><xsl:value-of select="@classname" /></fixture>
                    <name><xsl:value-of select="@name" /></name>
                    <xsl:choose>
                        <xsl:when test="count(error) &gt; 0">
                            <status>error</status>
                            <traceback><xsl:value-of select="error" /></traceback>
                        </xsl:when>
                        <xsl:when test="count(failure) &gt; 0">
                            <status>failure</status>
                            <traceback><xsl:value-of select="failure" /></traceback>
                        </xsl:when>
                        <xsl:when test="count(skipped) &gt; 0">
                            <status>ignore</status>
                            <traceback><xsl:value-of select="skipped" /></traceback>
                        </xsl:when>
                        <xsl:otherwise>
                            <status>success</status>
                            <stdout><xsl:value-of select="." /></stdout>
                        </xsl:otherwise>
                    </xsl:choose>
	            </test>
            </xsl:for-each>
        </report>
    </xsl:template>
</xsl:transform>
