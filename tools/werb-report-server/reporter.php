<?php

//  $date = date('U');

$_POST = json_decode( file_get_contents('php://input'), true );

if( array_key_exists ( 'cmd' , $_GET )  ){
  
  switch( $_POST['cmd'] ){
    case 'report':
      return_data_file();
      break;
    case 'list':
      return_files_list();
      break;
    default:
      return_nothing();
  }    
}
else{
  return_nothing();
}
exit( 0 );

// ---------------------------------------------------------------  
  

  
function return_nothing(){
  
  $json = array(
    'file'=> '',
    'msg' => 'nothing to do',
    'error' => false
  );
  $jsonString = json_encode($json);
  echo $jsonString;
}



function return_files_list(){
  
  $path    = '/data';
  $files = scandir($path);  
  $json = array(
    'files'=>  $files,
    'msg' => 'list of files in data',
    'error' => false

  );
  $jsonString = json_encode($json);
  echo $jsonString;
}



function return_data_file(){
  
  $response = array(
    'file'=> $_POST["file"],
    'msg' => 'data file',
    'error' => false
  );

  $fileFullRef = '/data/'.$response["file"] ;

  if( file_exists( fileFullRef ) ){

    echo file_get_contents( $fileFullRef );
  }
  else{

    $json = array(
      'file'=> $response["file"],
      'msg' => 'file doesn`t exist',
      'error' => true
    );
    $jsonString = json_encode($json);
    echo $jsonString;
  }
} 



 ?>
