<!doctype html>
<html lang="de">

<head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Cyber RoadRunner - Nachricht versandt!</title>
        
        <link rel="stylesheet" href="./assets/css/style.css"> 
</head>
<body style="background-color: rgb(13, 38, 78);">

<div style="padding-top: 100px; color: white !important;" align="center">
	<img src="assets/images/logo-dark.png" width="400px"/>
        <p style="font-size: 24px;"> Ihre Nachricht wurde versandt! </p>
        <br>
        <p> Sie werden gleich zurück zur Hauptseite geleitet. </p>        
        <p> Die Weiterleitung funktioniert nicht? <a href="https://cyber-roadrunner.de" style="color: white; text-decoration: underline;">Hier gehts zurück!</a> </p>
</div>

<?php
        $empfaenger = 'info@cyber-roadrunner.de';

        $betreff = $_POST['whatabout'];

        $nachricht = $_POST['message_content'];

        $header = 'From: '.$_POST['your_name'].' <'.$_POST['email']."> \r\n".
                'Reply-To: '.$_POST['email']."\r\n".
                'X-Mailer: PHP/'.phpversion();

        mail($empfaenger, $betreff, $nachricht, $header);

?>
<meta http-equiv="refresh" content="2;url=index.html">

<!--    
        PHP-Einstellungen:
        https://www.quackit.com/php/tutorial/php_mail_configuration.cfm
-->

</body>