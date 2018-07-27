from lxml import etree

xslt_root = etree.XML('''\
	<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
		<xsl:template match="/">
			<foo><xsl:value-of select="/a/b/text()" /></foo>
		</xsl:template>
	</xsl:stylesheet>''')
transform = etree.XSLT(xslt_root)
f = '<a><b>Text</b></a>'
doc = etree.fromstring(f)
result_tree = transform(doc)
print(result_tree)