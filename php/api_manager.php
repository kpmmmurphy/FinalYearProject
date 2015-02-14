<?php
    //API Manager
    //Author :: Kevin Murphy
    //Date   :: 16 - Dec - 14

    require_once('database_manager.php');

    //---Constants
    $debug = false;
    //Request Params
    define('PARAM_SERVICE', 'service');
    define('PARAM_GET_CONFIG', 'get_config');
    define('PARAM_UPDATE_CONFIG', 'update_config');
    define('PARAM_UPLOAD_SENSOR_VALUES', 'upload_sensor_values');
    define('PARAM_GET_ALL_CURRENT_DAY_SENSOR_VALUES', 'get_all_current_day_sensor_values');
    define('PARAM_GET_CURRENT_HOUR_SENSOR_VALUES', 'get_current_hour_sensor_values');
    define('PARAM_GET_AGG_SENSOR_VALUES_PER_HOUR', 'get_agg_sensor_values_per_hour');
    define('PARAM_GET_AGG_SENSOR_VALUES_PER_DAY', 'get_agg_sensor_values_per_day');
    define('PARAM_GET_SENSOR_VALUES', 'get_sensor_values');
    define('PARAM_GET_PN_REG_IDS', 'get_reg_ids');
    define('PARAM_INSERT_PN_REG_ID', 'insert_reg_ids');
    define('PARAM_REQUEST_VIDEO_STREAM', 'request_video_stream');
    
    //Response Params
    define('PARAM_LIST_IMAGES', 'list_images');
    define('PARAM_IMAGES', 'images');
    define('PARAM_SENSOR_VALUES', 'sensor_values');
    define('PARAM_SENSOR_VALUES_LIST', 'sensor_values_list');
    define('PARAM_UPLOAD_CAMERA_STILL', 'camera_still');
    define('PARAM_UPLOAD_CAMERA_VIDEO', 'camera_video');
    define('PARAM_STATUS_CODE', 'status_code');
    define('PARAM_PN_REG_IDS', 'pn_reg_ids');
    define('PARAM_PI_PUBLIC_IP', 'pi_public_ip');
    define('PARAM_REQUESTING_VIDEO_STREAM', 'requesting_video_stream');
    
    //Files
    define('DIR_CONFIG', './config/');
    define('DIR_CAMERA', './camera/');
    define('FILE_CONFIG_DEFAULT', 'default_config.json');
    define('FILE_CONFIG', 'config.json');
    
    //Response Status Codes
    define('RESPONSE_SUCCESS', 200);
    define('RESPONSE_FAILED' , 400);
    define('RESPONSE_NOT_FOUND' , 404);
    
    $database_manager = new DatabaseManager();

    $headers    = getallheaders();
    $rawRequest = file_get_contents('php://input', 0, null, null);
    $requestObj = json_decode($rawRequest);

    if($debug){
        echo "\n\nHEADERS::\n\n";
        foreach (getallheaders() as $name => $value) {
            echo "$name: $value\n";
        }

        echo "\n\nREQUEST::\n\n";
        var_dump($requestObj);
    }
    
    //Default failure response
    //$response = array(constant("PARAM_STATUS_CODE") => constant('RESPONSE_FAILED'));
    $response = array();

    //Include meta paramaters
    $include_meta = true;
    
    #$database_manager = new DatabaseManager();
    #$outputs =  $database_manager->getRequestingStreamFlag();
    #echo json_encode($outputs);
    
    if(isset($headers[constant('PARAM_SERVICE')])){

        $requestedService = htmlspecialchars($headers[constant('PARAM_SERVICE')]);
        #$requestedService = "get_sensor_values";
        
        switch($requestedService){

            case constant('PARAM_GET_CONFIG'):
                if($debug){
                    echo "\nGet System Configuration\n";
                }
                
                $file = constant("DIR_CONFIG") . constant("FILE_CONFIG");
                if(!file_exists($file) || filesize($file) == 0){
                    $file = constant("DIR_CONFIG") . constant('FILE_CONFIG_DEFAULT');
                }
                $config_file = fopen($file, "r") or die("Unable to open file!");
                echo fread($config_file, filesize($file));
                fclose($config_file);
                
                #$response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                $include_meta = false;
                break;

            case constant('PARAM_UPDATE_CONFIG'):
                if($debug){
                    echo "\nUpdate System Config\n";
                }
                
                try{
                    $file = constant("DIR_CONFIG") . constant("FILE_CONFIG");
                    if(!file_exists($file)){
                        file_put_contents($file, '');
                    }
                    $config_file = fopen($file, "wb") or die("Unable to open file!");
                    fwrite($config_file, json_encode($requestObj));
                    fclose($config_file);
                    $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                }catch(Exception $e){
                    $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_FAILED');
                }
                break;

            case constant('PARAM_UPLOAD_SENSOR_VALUES'):
                if($debug){
                    echo "\nInsert Sensor Values into DB\n";
                }
                
                #Store Raspberry Pi's Public IP 
                $ip = getenv('HTTP_CLIENT_IP')?:
                      getenv('HTTP_X_FORWARDED_FOR')?:
                      getenv('HTTP_X_FORWARDED')?:
                      getenv('HTTP_FORWARDED_FOR')?:
                      getenv('HTTP_FORWARDED')?:
                      getenv('REMOTE_ADDR');
                
                $database_manager->updatePiPublicIP($ip);
                $database_manager->insertSensorValues($requestObj);

                //Response with streaming status flag
                $streamArray = $database_manager->getRequestingStreamFlag();
                $requestingStream = $streamArray['requesting_stream'];
                $response[constant('PARAM_REQUESTING_VIDEO_STREAM')] = $requestingStream;
                if($requestingStream == 1 || $requestingStream == 2)
                {
                    $database_manager->updateRequestingStreamFlag(0);
                }
                
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                break;

            case constant('PARAM_GET_SENSOR_VALUES'):
                //Get latest sensor values
                if($debug){
                    echo "\nGetting Sensor Values\n";
                }
                $response[constant('PARAM_SENSOR_VALUES')] = $database_manager->selectLatestSensorValues();
                $response[constant("PARAM_STATUS_CODE")]   = constant('RESPONSE_SUCCESS');
                break; 

            case constant('PARAM_LIST_IMAGES'):
                //Get the list of images
                if($debug){
                    echo "\nGetting Images List\n";
                }
                $imgDirList = scandir(constant("DIR_CAMERA"));
                $imgList = array();
                foreach( $imgDirList as $k => $v){
                    $imgList[] = $v;
                }
                
                $response[constant('PARAM_IMAGES')] = $imgList;
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                break;
                
            case constant('PARAM_GET_ALL_CURRENT_DAY_SENSOR_VALUES'):
                if($debug){
                    echo "\nGetting All Current Day Sensor Outputs\n";
                }
                #$response = $database_manager->selectAllCurrentDaySensorValues();
                break;
                
           case constant('PARAM_GET_CURRENT_HOUR_SENSOR_VALUES'):
                if($debug){
                    echo "\nGetting Current Hour Sensor Outputs\n";
                }
                $response[constant("PARAM_SENSOR_VALUES_LIST")] = $database_manager->selectCurrentHourSensorValues();
                $response[constant("PARAM_STATUS_CODE")]        = constant('RESPONSE_SUCCESS');
                break;
                
           case constant('PARAM_GET_AGG_SENSOR_VALUES_PER_HOUR'):
                if($debug){
                    echo "\nGetting Current Hour Sensor Outputs\n";
                }
                $response[constant("PARAM_SENSOR_VALUES_LIST")] = $database_manager->selectAggSensorValuesPerHour();
                $response[constant("PARAM_STATUS_CODE")]        = constant('RESPONSE_SUCCESS');
                break;
                
          case constant('PARAM_GET_AGG_SENSOR_VALUES_PER_DAY'):
                if($debug){
                    echo "\nGetting Current Hour Sensor Outputs\n";
                }
                $response[constant("PARAM_SENSOR_VALUES_LIST")] = $database_manager->selectAggSensorValuesPerDay();
                $response[constant("PARAM_STATUS_CODE")]        = constant('RESPONSE_SUCCESS');
                break;
                
          case constant('PARAM_GET_PN_REG_IDS'):
                if($debug){
                    echo "\nGetting Push Reg IDs\n";
                }
                $response[constant("PARAM_PN_REG_IDS")]  = $database_manager->selectPNRegIDs();
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                break;
                
          case constant('PARAM_INSERT_PN_REG_ID'):
                if($debug){
                    echo "\nInserting Push Reg ID\n";
                }
                $database_manager->insertPNRegID($requestObj);
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                break;

            case constant('PARAM_REQUEST_VIDEO_STREAM'):
                if($debug){
                    echo "\nRequesting Video Stream\n";
                }
                $database_manager->updateRequestingStreamFlag(1);
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                break;

            case constant('PARAM_REQUEST_NEW_IMAGE'):
                if($debug){
                    echo "\nRequesting New Image Capture\n";
                }
                $database_manager->updateRequestingStreamFlag(2);
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
                break;

            default:
                $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_NOT_FOUND');
        }
        
    }else{

        if(isset($_FILES[constant('PARAM_UPLOAD_CAMERA_STILL')])){
            if($debug){
                echo "\nUpload Camera Still\n";
                var_dump($_FILES);
            }
            verifiy_and_upload_file(constant('PARAM_UPLOAD_CAMERA_STILL'));
            $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
        }elseif(isset($_FILES[constant('PARAM_UPLOAD_CAMERA_VIDEO')])){
            if($debug){
                echo "\nUpload Camera Video\n";
                var_dump($_FILES);
            }
            verifiy_and_upload_file(constant('PARAM_UPLOAD_CAMERA_STILL'));
            $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_SUCCESS');
        }else{
            $response[constant("PARAM_STATUS_CODE")] = constant('RESPONSE_NOT_FOUND');
        }

    }

//Add Meta data to response
if($include_meta)
{
    $ip_address_array = $database_manager->getPiPublicIP();
    $response[constant('PARAM_PI_PUBLIC_IP')]  = $ip_address_array['ip_address'];
}

//Echo the response
if( count($response) > 0)
{
    echo json_encode($response);
}

/*
 * Code largely taken from ->
 * http://www.w3schools.com/php/php_file_upload.asp
 */

function verifiy_and_upload_file($fileName)
{
    $debug = false;
    $target_file = constant("DIR_CAMERA") . basename($_FILES[$fileName]["name"]);
    //$check = getimagesize($_FILES[$fileName]["tmp_name"]);
    $uploadOk = 1;
    $imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

    /*if($check !== false) {
        if($debug){
            echo "File is an image - " . $check["mime"] . ".";
        }
        $uploadOk = 1;
    } else {
        if($debug){
            echo "File is not an image.";
        }
        $uploadOk = 0;
    }*/

    // Check file size
    if ($_FILES[$fileName]["size"] > 1000000) {
        if($debug){
            echo "Sorry, your file is too large.";
        }
        $uploadOk = 0;
    }

    /*if($imageFileType === "image/jpg" or $imageFileType === "image/png" or $imageFileType === "image/jpeg"
       or $imageFileType === "image/h264") {
        if($debug){
            echo "Sorry, only JPG, JPEG, PNG & h264 files are allowed.";
        }
        $uploadOk = 0;
    }*/

    if ($uploadOk == 0) {
        if($debug){
            echo "Sorry, your file was not uploaded.";
        }
    } else {
        if (move_uploaded_file($_FILES[$fileName]["tmp_name"], $target_file)) {
            if($debug){
                echo "The file ". basename( $_FILES[$fileName]["name"]). " has been uploaded.";
            }
        } else {
            if($debug){
                echo "Sorry, there was an error uploading your file.";
            }
        }
    }
}

?>
