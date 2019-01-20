<?php

$_POST = json_decode(file_get_contents('php://input'), true);

$response = array(
  'main'=> $_POST["main"],
  'vs'=> $_POST["vs"],
  'dayweek'=> $_POST["dayweek"],
  'showdate'=> $_POST["showdate"],
);

$fileName =  $_POST["showdate"].'__'.date('U');

$fp = fopen('data/show_'.$fileName.'.json', 'w');
$fwrite = fwrite($fp, json_encode($response));
if ($fwrite === false) {
    header('HTTP/1.1 404 Not Found');
}
else{
  header('HTTP/1.1 200 OK');
  print json_encode( $response );
}
fclose($fp);


 ?>
