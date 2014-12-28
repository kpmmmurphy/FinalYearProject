<?php
    //API Manager
    //Author :: Kevin Murphy
    //Date   :: 16 - Dec - 14

    require_once('database_manager.php');

    //---Constants
    $debug = true;
    //Request Params
    define('PARAM_SERVICE', 'service');
    define('PARAM_GET_CONFIG', 'get_config');
    define('PARAM_UPDATE_CONFIG', 'update_config');
    define('PARAM_UPLOAD_SENSOR_VALUES', 'upload_sensor_values');
    define('PARAM_GET_SENSOR_VALUES', 'get_sensor_values');
    define('PARAM_SENSOR_VALUES', 'sensor_values');
    define('PARAM_UPLOAD_CAMERA_STILL', 'upload_camera_still');
    //Files
    define('DIR_CONFIG', './config/');
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

        echo "\n";
    }

    
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
                if(!file_exists($file)){
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

                $file = constant("DIR_CONFIG") . constant("FILE_CONFIG");
                if(!file_exists($file)){
                    file_put_contents($file, '');
                    echo "yeeees";
                }
                $config_file = fopen($file, "w") or die("Unable to open file!");
                fwrite($config_file, $requestObj);
                fclose($config_file);
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
                echo json_encode($database_manager->selectLatestSensorValues());
                break;

            case constant('PARAM_UPLOAD_CAMERA_STILL'):
                //Upload camera still
                if($debug){
                    echo "\Upload Camera Still\n";
                }
                print_r($_FILES);
                break;

            default:
                echo "ERROR :: Requested service not present";
        }

    }else{
        echo "Service Not Set";
    }
?>
