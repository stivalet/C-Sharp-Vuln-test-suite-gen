<?php
/*
/* 
Unsafe sample
input : backticks interpretation, reading the file /tmp/tainted.txt
Uses a magic_quotes_filter via filter_var function
construction : concatenation with simple quote
*/



/*Copyright 2014 Herve BUHLER, David LUCAS, Fabien NOLLET, Axel RESZETKO

Permission is hereby granted, without written agreement or royalty fee, to

use, copy, modify, and distribute this software and its documentation for

any purpose, provided that the above copyright notice and the following

three paragraphs appear in all copies of this software.


IN NO EVENT SHALL AUTHORS BE LIABLE TO ANY PARTY FOR DIRECT,

INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE 

USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF AUTHORS HAVE

BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


AUTHORS SPECIFICALLY DISCLAIM ANY WARRANTIES INCLUDING, BUT NOT

LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A

PARTICULAR PURPOSE, AND NON-INFRINGEMENT.


THE SOFTWARE IS PROVIDED ON AN "AS-IS" BASIS AND AUTHORS HAVE NO

OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR

MODIFICATIONS.*/


$tainted = `cat /tmp/tainted.txt`;$sanitized = filter_var($tainted, FILTER_SANITIZE_MAGIC_QUOTES);
if (filter_var($sanitized, FILTER_VALIDATE_MAGIC_QUOTES))
$checked_data = $sanitized ;
else
$checked_data = "" ;$query = "//User[username/text()='". $checked_data . "']";$xml = simplexml_load_file("users.xml");//file load
echo "query : ". $query ."<br /><br />" ;

//flaw
$res=$xml->xpath($query);//execution
print_r($res);
echo "<br />" ;
 ?>