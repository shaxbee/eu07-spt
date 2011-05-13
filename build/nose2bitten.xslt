<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  
  

  


  

  <head>
    <title>
      Attachment – Bitten
    </title>
        <link rel="search" href="/search" />
        <link rel="help" href="/wiki/TracGuide" />
        <link rel="alternate" href="/raw-attachment/ticket/147/nose2bitten.xslt" type="application/xslt+xml; charset=utf-8" title="Original Format" />
        <link rel="up" href="/ticket/147" title="Ticket #147" />
        <link rel="start" href="/wiki" />
        <link rel="stylesheet" href="http://www.edgewall.org/chrome/common11/css/trac.css" type="text/css" /><link rel="stylesheet" href="/pygments/trac.css" type="text/css" /><link rel="stylesheet" href="http://www.edgewall.org/chrome/common11/css/code.css" type="text/css" /><link rel="stylesheet" href="/chrome/bitten/bitten.css" type="text/css" />
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <link rel="icon" href="/favicon.ico" type="image/x-icon" />
      <link type="application/opensearchdescription+xml" rel="search" href="/search/opensearch" title="Search Bitten" />
    <script type="text/javascript" src="http://www.edgewall.org/chrome/common11/js/jquery.js"></script><script type="text/javascript" src="http://www.edgewall.org/chrome/common11/js/trac.js"></script><script type="text/javascript" src="http://www.edgewall.org/chrome/common11/js/search.js"></script>
    <!--[if lt IE 7]>
    <script type="text/javascript" src="http://www.edgewall.org/chrome/common11/js/ie_pre7_hacks.js"></script>
    <![endif]-->
    <link rel="stylesheet" type="text/css" href="http://www.edgewall.org/css/projects.css" />
  </head>
  <body>
    <div id="wrapper">
      <div id="topbar">
        <a id="home-link" href="http://www.edgewall.org/">Edgewall Software</a>
      </div>
      <div id="ew-header">
        <div id="topnav"><ul>
         <li><a href="http://www.edgewall.org/">Home</a></li>
         <li>
           <a class="trac" href="http://trac.edgewall.org/">Trac</a>
         </li>
         <li>
           <a class="genshi" href="http://genshi.edgewall.org/">Genshi</a>
         </li>
         <li>
           <a class="babel" href="http://babel.edgewall.org/">Babel</a>
         </li>
         <li class="active">
           <a class="bitten" href="http://bitten.edgewall.org/">Bitten</a>
         </li>
         <li>
           <a class="posterity" href="http://posterity.edgewall.org/">Posterity</a>
         </li></ul>
       </div>
     </div>
     <div id="ew-main">
       <div id="ew-content">
         <div>
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript"></script>
<script type="text/javascript">_uacct = "UA-598265-6";urchinTracker();</script>
<div id="left">
  <div class="block"><ul>
    <li><a href="/">Home</a></li><li><a href="/wiki/Download">Download</a></li><li><a href="/wiki/Documentation">Documentation</a></li><li><a href="/wiki/MailingList">Mailing Lists</a></li><li><a href="/wiki/License">License</a></li><li><a href="/wiki/BittenFaq">FAQ</a></li>
  </ul></div>
</div>
</div>
    <div id="banner">
      <div id="header">
        <a id="logo" href="http://bitten.edgewall.org/"><img src="http://www.edgewall.org/gfx/bitten_logo_small.png" alt="Bitten - Continuous Integration Rethought" height="85" width="204" /></a>
      </div>
      <form id="search" action="/search" method="get">
        <div>
          <label for="proj-search">Search:</label>
          <input type="text" id="proj-search" name="q" size="18" value="" />
          <input type="submit" value="Search" />
        </div>
      </form>
      <div id="metanav" class="nav">
    <ul>
      <li class="first"><a href="/login">Login</a></li><li><a href="/prefs">Preferences</a></li><li><a href="/wiki/TracGuide">Help/Guide</a></li><li class="last"><a href="/about">About Trac</a></li>
    </ul>
  </div>
    </div>
    <div id="mainnav" class="nav">
    <ul>
      <li class="first"><a href="/wiki">Wiki</a></li><li><a href="/timeline">Timeline</a></li><li><a href="/roadmap">Roadmap</a></li><li><a class="" href="/build">Build Status</a></li><li><a href="/browser">Browse Source</a></li><li><a href="/query">View Tickets</a></li><li><a href="/newticket">New Ticket</a></li><li class="last"><a href="/search">Search</a></li>
    </ul>
  </div>
    <div id="main">
      <div id="ctxtnav" class="nav">
        <h2>Context Navigation</h2>
          <ul>
              <li class="last first"><a href="/ticket/147">Back to Ticket #147</a></li>
          </ul>
        <hr />
      </div>
    <div id="content" class="attachment">
        <h1><a href="/ticket/147">Ticket #147</a>: nose2bitten.xslt</h1>
        <table id="info" summary="Description">
          <tbody>
            <tr>
              <th scope="col">
                File nose2bitten.xslt, <span title="1511 bytes">1.5 KB</span>
                (added by Pedro Ferreira &lt;pedro.ferreira@…&gt;,  <a class="timeline" href="/timeline?from=2010-11-22T10%3A38%3A52%2B0100&amp;precision=second" title="2010-11-22T10:38:52+0100 in Timeline">6 months</a> ago)
              </th>
            </tr>
            <tr>
              <td class="message searchable">
                <p>
I have created a small XSLT that translates nosetests XUtil output into a Bitten unit test report. I haven't tested it extensively, but should work reasonably well.
</p>

              </td>
            </tr>
          </tbody>
        </table>
        <div id="preview" class="searchable">
    <table class="code"><thead><tr><th class="lineno" title="Line numbers">Line</th><th class="content"> </th></tr></thead><tbody><tr><th id="L1"><a href="#L1">1</a></th><td><span class="nt">&lt;xsl:transform</span> <span class="na">version=</span><span class="s">"1.0"</span> <span class="na">xmlns:xsl=</span><span class="s">"http://www.w3.org/1999/XSL/Transform"</span><span class="nt">&gt;</span></td></tr><tr><th id="L2"><a href="#L2">2</a></th><td>    <span class="nt">&lt;xsl:template</span> <span class="na">match=</span><span class="s">"/testsuite"</span><span class="nt">&gt;</span></td></tr><tr><th id="L3"><a href="#L3">3</a></th><td>        <span class="nt">&lt;report</span> <span class="na">category=</span><span class="s">"test"</span><span class="nt">&gt;</span></td></tr><tr><th id="L4"><a href="#L4">4</a></th><td>            <span class="nt">&lt;xsl:for-each</span> <span class="na">select=</span><span class="s">"testcase"</span><span class="nt">&gt;</span></td></tr><tr><th id="L5"><a href="#L5">5</a></th><td>                <span class="nt">&lt;test&gt;</span></td></tr><tr><th id="L6"><a href="#L6">6</a></th><td>                    <span class="nt">&lt;duration&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"@time"</span> <span class="nt">/&gt;&lt;/duration&gt;</span></td></tr><tr><th id="L7"><a href="#L7">7</a></th><td>                    <span class="nt">&lt;fixture&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"@classname"</span> <span class="nt">/&gt;&lt;/fixture&gt;</span></td></tr><tr><th id="L8"><a href="#L8">8</a></th><td>                    <span class="nt">&lt;name&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"@name"</span> <span class="nt">/&gt;&lt;/name&gt;</span></td></tr><tr><th id="L9"><a href="#L9">9</a></th><td>                    <span class="nt">&lt;xsl:choose&gt;</span></td></tr><tr><th id="L10"><a href="#L10">10</a></th><td>                        <span class="nt">&lt;xsl:when</span> <span class="na">test=</span><span class="s">"count(error) &amp;gt; 0"</span><span class="nt">&gt;</span></td></tr><tr><th id="L11"><a href="#L11">11</a></th><td>                            <span class="nt">&lt;status&gt;</span>error<span class="nt">&lt;/status&gt;</span></td></tr><tr><th id="L12"><a href="#L12">12</a></th><td>                            <span class="nt">&lt;traceback&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"error"</span> <span class="nt">/&gt;&lt;/traceback&gt;</span></td></tr><tr><th id="L13"><a href="#L13">13</a></th><td>                        <span class="nt">&lt;/xsl:when&gt;</span></td></tr><tr><th id="L14"><a href="#L14">14</a></th><td>                        <span class="nt">&lt;xsl:when</span> <span class="na">test=</span><span class="s">"count(failure) &amp;gt; 0"</span><span class="nt">&gt;</span></td></tr><tr><th id="L15"><a href="#L15">15</a></th><td>                            <span class="nt">&lt;status&gt;</span>failure<span class="nt">&lt;/status&gt;</span></td></tr><tr><th id="L16"><a href="#L16">16</a></th><td>                            <span class="nt">&lt;traceback&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"failure"</span> <span class="nt">/&gt;&lt;/traceback&gt;</span></td></tr><tr><th id="L17"><a href="#L17">17</a></th><td>                        <span class="nt">&lt;/xsl:when&gt;</span></td></tr><tr><th id="L18"><a href="#L18">18</a></th><td>                        <span class="nt">&lt;xsl:when</span> <span class="na">test=</span><span class="s">"count(skipped) &amp;gt; 0"</span><span class="nt">&gt;</span></td></tr><tr><th id="L19"><a href="#L19">19</a></th><td>                            <span class="nt">&lt;status&gt;</span>ignore<span class="nt">&lt;/status&gt;</span></td></tr><tr><th id="L20"><a href="#L20">20</a></th><td>                            <span class="nt">&lt;traceback&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"skipped"</span> <span class="nt">/&gt;&lt;/traceback&gt;</span></td></tr><tr><th id="L21"><a href="#L21">21</a></th><td>                        <span class="nt">&lt;/xsl:when&gt;</span></td></tr><tr><th id="L22"><a href="#L22">22</a></th><td>                        <span class="nt">&lt;xsl:otherwise&gt;</span></td></tr><tr><th id="L23"><a href="#L23">23</a></th><td>                            <span class="nt">&lt;status&gt;</span>success<span class="nt">&lt;/status&gt;</span></td></tr><tr><th id="L24"><a href="#L24">24</a></th><td>                            <span class="nt">&lt;stdout&gt;&lt;xsl:value-of</span> <span class="na">select=</span><span class="s">"."</span> <span class="nt">/&gt;&lt;/stdout&gt;</span></td></tr><tr><th id="L25"><a href="#L25">25</a></th><td>                        <span class="nt">&lt;/xsl:otherwise&gt;</span></td></tr><tr><th id="L26"><a href="#L26">26</a></th><td>                    <span class="nt">&lt;/xsl:choose&gt;</span></td></tr><tr><th id="L27"><a href="#L27">27</a></th><td>                <span class="nt">&lt;/test&gt;</span></td></tr><tr><th id="L28"><a href="#L28">28</a></th><td>            <span class="nt">&lt;/xsl:for-each&gt;</span></td></tr><tr><th id="L29"><a href="#L29">29</a></th><td>        <span class="nt">&lt;/report&gt;</span></td></tr><tr><th id="L30"><a href="#L30">30</a></th><td>    <span class="nt">&lt;/xsl:template&gt;</span></td></tr><tr><th id="L31"><a href="#L31">31</a></th><td><span class="nt">&lt;/xsl:transform&gt;</span></td></tr></tbody></table>
        </div>
    </div>
    <div id="altlinks">
      <h3>Download in other formats:</h3>
      <ul>
        <li class="last first">
          <a rel="nofollow" href="/raw-attachment/ticket/147/nose2bitten.xslt">Original Format</a>
        </li>
      </ul>
    </div>
    </div>
    <div id="footer" lang="en" xml:lang="en"><hr />
      <a id="tracpowered" href="http://trac.edgewall.org/"><img src="http://www.edgewall.org/chrome/common11/trac_logo_mini.png" height="30" width="107" alt="Trac Powered" /></a>
      <p class="left">
        Powered by <a href="/about"><strong>Trac 0.11.8dev-r10236</strong></a><br />
        By <a href="http://www.edgewall.org/">Edgewall Software</a>.
      </p>
      <p class="right">Visit the Trac open source project at<br /><a href="http://trac.edgewall.org/">http://trac.edgewall.org/</a></p>
    </div>
        </div><!-- #ew-content -->
      </div>
    </div>
    <div id="ew-footer">
      <p><a href="mailto:info@edgewall.com">info@edgewall.com</a></p>
      <p>Copyright © 2003-2010 Edgewall Software. All rights reserved.</p>
    </div>
    <div id="right">
 <script type="text/javascript"><!--
  google_ad_client = "pub-3746245347013177";
  google_ad_width = 120;
  google_ad_height = 600;
  google_ad_format = "120x600_as";
  google_ad_channel ="9044578517";
  google_ad_type = "text_image";
  google_color_border = "8b8d8d";
  /*google_color_border = "6b6d6d";*/
  google_color_bg = "6b6d6d";
  /*google_color_bg = "4b4d4d";*/
  google_color_link = "336699";
  google_color_url = "E2B200";
  google_color_text = "8c8c8c";
  /*google_color_text = "cccccc";*/
  //--></script>
 <script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
 </script>
   </div>
  </body>
</html>