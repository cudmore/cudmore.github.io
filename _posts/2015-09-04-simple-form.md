---
layout: post
title: "simple form in jekyll"
category: post
date: 2015-09-04 22:01:06
tags:
- jekyll
---

<head>
  <style>
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</style>
</head>

<BR>
<BR>
###Software request form

<form action="//formspree.io/robert.cudmore@gmail.com"
      method="POST">
    
    <table style="width:500px">
    <tr>
    <td>
    Name:
    </td>
    <td>
    <input type="text" name="name" size="50"><BR>
	</td>
	</tr>

    <TR>
    <TD>
    Institution:
    </TD>
    <TD>
    <input type="text" name="Institution" size="50"><BR>
	</TD>
	</TR>
	
    <TR>
    <TD>
    Lab:
    </TD>
    <TD>
    <input type="text" name="Lab" placeholder="" size="50"><BR>
    </TD>
    </TR>
    
    <TR>
    <TD>
    email:
    </TD>
    <TD>
    <input type="email" name="_replyto" placeholder="" size="50"><BR>
    </TD>
    </TR>
    
    <TR>
    <TD>
    retype email:
    </TD>
    <TD>
    <input type="email" name="_replyto2" placeholder="" size="50"><BR>
    </TD>
    </TR>

<TR>
<TD>
Message
</TD>
<TD>
    <textarea name="message" rows="5" cols="48" placeholder=""></textarea>
</TD>
</TR>

	</table>

	<input type="hidden" name="whereicamefrom" value="MapManager" />

    <input type="hidden" name="_next" value="/thanks/" />

	<input type="text" name="_gotcha" style="display:none" />

 <TR>
 <TD>
	<input type="submit" class="btn btn-primary btn-md" value="Submit">

 </TD>
 </TR>
</form>

<BR>
