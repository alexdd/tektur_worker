<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:sch="http://purl.oclc.org/dsdl/schematron"
    version="3.0"> 
    
    <xsl:strip-space elements="*"/>
    
    <xsl:output indent="yes" method="xml"/>
    
    <xsl:variable name="messages" select="doc('src/messages.xml')"/>
    
    <xsl:template name="write-skeleton">
    	<xsl:comment>*** DO NOT EDIT! This file has autmatically been generated. ***</xsl:comment>
		<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    				xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
    				xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    				xmlns:xs="http://www.w3.org/2001/XMLSchema">
    		<sch:pattern>
        		<sch:title>Schematron-Rules for CKEditor support in COIN</sch:title>
        		<xsl:apply-templates select="descendant::sch:rule"/>
    		</sch:pattern>
		    <sch:include href="diagnostics-ckeditor-de.sch"/>
    		<sch:include href="diagnostics-ckeditor-en.sch"/>
		</sch:schema>    
    </xsl:template>
    
    <xsl:template match="sch:rule">
        <xsl:copy copy-namespaces="no">
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="sch:assert">
        <xsl:copy copy-namespaces="no">
        	<xsl:attribute name="id" select="concat('dyck_i',format-number(count(preceding::sch:assert),'##'))"/>
        	<xsl:attribute name="diagnostics" select="concat('dyck_i_',.,'_en dyck_i_',.,'_de')"/>
        	<xsl:copy-of select="@test"/>
            <xsl:value-of select="$messages//message[@id=normalize-space(current())]/en"/>
        </xsl:copy>
    </xsl:template>
        
    <xsl:template match="/">
    	<xsl:call-template name="write-skeleton"/>
        <xsl:result-document href="diagnostics-ckeditor-de.sch">
	    	<xsl:comment>*** DO NOT EDIT! This file has autmatically been generated. ***</xsl:comment>
            <sch:diagnostics xmlns:sch="http://purl.oclc.org/dsdl/schematron">
            	<xsl:for-each select="$messages//message/de">
    				<sch:diagnostic id="dyck_i_{../@id}_de" xml:lang="de">
						<xsl:value-of select="."/>
					</sch:diagnostic>
            	</xsl:for-each>
            </sch:diagnostics>
        </xsl:result-document>
        <xsl:result-document href="diagnostics-ckeditor-en.sch">
	    	<xsl:comment>*** DO NOT EDIT! This file has autmatically been generated. ***</xsl:comment>
            <sch:diagnostics xmlns:sch="http://purl.oclc.org/dsdl/schematron">
            	<xsl:for-each select="$messages//message/en">
    				<sch:diagnostic id="dyck_i_{../@id}_en" xml:lang="en">
						<xsl:value-of select="."/>
					</sch:diagnostic>
            	</xsl:for-each>
            </sch:diagnostics>
        </xsl:result-document>
    </xsl:template>
    
    <!-- default copy rule -->
    
    <xsl:template match="node()|@*" mode="#all">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*" mode="#current"/>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>