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
    
    //Response Params
    define('PARAM_LIST_IMAGES', 'list_images');
    define('PARAM_SENSOR_VALUES', 'sensor_values');
    define('PARAM_SENSOR_VALUES_LIST', 'sensor_values_list');
    define('PARAM_UPLOAD_CAMERA_STILL', 'camera_still');
    define('PARAM_UPLOAD_CAMERA_VIDEO', 'camera_video');
    define('PARAM_STATUS_CODE', 'status_code');
    define('PARAM_PN_REG_IDS', 'pn_reg_ids');
    
    
    //Files
    define('DIR_CONFIG', './config/');
    define('DIR_CAMERA', './camera/');
    define('FILE_CONFIG_DEFAULT', 'default_config.json');
    define('FILE_CONFIG', 'config.json');

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
    
    //$database_manager = new DatabaseManager();
    //$outputs = array(constant("PARAM_PN_REG_IDS") => $database_manager->selectPNRegIDs());
    //echo json_encode($outputs);
    
    if(isset($headers[constant('PARAM_SERVICE')])){

        $requestedService = htmlspecialchars($headers[constant('PARAM_SERVICE')]);

        $database_manager = new DatabaseManager();

        switch($requestedService){

            case constant('PARAM_GET_CONFIG'):
                //Return System Configuration
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
                break;

            case constant('PARAM_UPDATE_CONFIG'):
                //Update System config
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
                    $response = array(constant("PARAM_STATUS_CODE") => 200);
                }catch(Exception $e){
                    $response = array(constant("PARAM_STATUS_CODE") => 400);
                }
                echo json_encode($response);
                break;

            case constant('PARAM_UPLOAD_SENSOR_VALUES'):
                //Insert Sensor value 
                if($debug){
                    echo "\nInsert Sensor Values into DB\n";
                }
                $database_manager->insertSensorValues($requestObj);
                break;

            case constant('PARAM_GET_SENSOR_VALUES'):
                //Get latest sensor values
                if($debug){
                    echo "\nGetting Sensor Values\n";
                }
                echo json_encode(array($database_manager->selectLatestSensorValues()));
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
                $imgListResponse = array('images' => $imgList);
                echo json_encode($imgListResponse);
                break;
                
            case constant('PARAM_GET_ALL_CURRENT_DAY_SENSOR_VALUES'):
                if($debug){
                    echo "\nGetting All Current Day Sensor Outputs\n";
                }
                echo json_encode($database_manager->selectAllCurrentDaySensorValues());
                break;
                
           case constant('PARAM_GET_CURRENT_HOUR_SENSOR_VALUES'):
                if($debug){
                    echo "\nGetting Current Hour Sensor Outputs\n";
                }
                $outputs = array(constant("PARAM_SENSOR_VALUES_LIST") => $database_manager->selectCurrentHourSensorValues());
                echo json_encode($outputs);
                break;
                
           case constant('PARAM_GET_AGG_SENSOR_VALUES_PER_HOUR'):
                if($debug){
                    echo "\nGetting Current Hour Sensor Outputs\n";
                }
                $outputs = array(constant("PARAM_SENSOR_VALUES_LIST") => $database_manager->selectAggSensorValuesPerHour());
                echo json_encode($outputs);
                break;
                
          case constant('PARAM_GET_AGG_SENSOR_VALUES_PER_DAY'):
                if($debug){
                    echo "\nGetting Current Hour Sensor Outputs\n";
                }
                $outputs = array(constant("PARAM_SENSOR_VALUES_LIST") => $database_manager->selectAggSensorValuesPerDay());
                echo json_encode($outputs);
                break;
                
          case constant('PARAM_GET_PN_REG_IDS'):
                if($debug){
                    echo "\nGetting Push Reg IDs\n";
                }
                $outputs = array(constant("PARAM_PN_REG_IDS") => $database_manager->selectPNRegIDs());
                echo json_encode($outputs);
                break;
                
          case constant('PARAM_INSERT_PN_REG_ID'):
                if($debug){
                    echo "\nInserting Push Reg ID\n";
                }
                $database_manager->insertPNRegID($requestObj);
                break;
                
            default:
                echo "ERROR :: Requested service not present";
        }

    }else{

        if(isset($_FILES[constant('PARAM_UPLOAD_CAMERA_STILL')])){
            if($debug){
                echo "\nUpload Camera Still\n";
                var_dump($_FILES);
            }
            verifiy_and_upload_file(constant('PARAM_UPLOAD_CAMERA_STILL'));
        }elseif(isset($_FILES[constant('PARAM_UPLOAD_CAMERA_VIDEO')])){
            if($debug){
                echo "\nUpload Camera Video\n";
                var_dump($_FILES);
            }
        }else{
            echo "Service Not Set";
        }

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
