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
    define('DIR_CONFIG', './config/');
    
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
                $file = constant("DIR_CONFIG") . "default_config.json";
                $config = fopen($file, "r") or die("Unable to open file!");
                echo fread($config, filesize($file));
                break;

            case constant('PARAM_UPDATE_CONFIG'):
                //Update System config
                if($debug){
                    echo "\nUpdate system config\n";
                }
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

            default:
                echo "ERROR :: Requested service not present";
        }

    }else{
        echo "Service Not Set";
    }
?>
