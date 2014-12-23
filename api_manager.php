<?php
    //API Manager
    //Author :: Kevin Murphy
    //Date   :: 16 - Dec - 14

    //Costants
    define('PARAM_SERVICE', 'service');
    define('PARAM_GET_CONFIG', 'get_config');
    define('PARAM_UPDATE_CONFIG', 'update_config');
    define('PARAM_UPLOAD_SENSOR_VALUES', 'upload_sensor_values');
    define('PARAM_SENSOR_VALUES', 'sensor_values');

    $serverName = "localhost";
    $username   = "kpm2";
    $password   = "shiegeib";
    $database   = "2015_kpm2";

    $request = json_decode(file_get_contents('php://input'));
    #$request = json_decode(stripslashes(file_get_contents('php://input')));
    $request = json_encode($request, 2);
    echo $request->sensor_values;
    if(isset($_POST[constant('PARAM_SERVICE')])){

        $requestedService = htmlspecialchars($_POST[constant('PARAM_SERVICE')]);
        switch($requestedService){

            case constant('PARAM_GET_CONFIG'):
                //Return System Configuration
                echo "Get System Configuration";
                break;

            case constant('PARAM_UPDATE_CONFIG'):
                //Update System config
                echo "Update system config";
                break;

            case constant('PARAM_UPLOAD_SENSOR_VALUES'):
                //Insert Sensor value 
                echo "Inset Sensor Values into DB";
                print_r($_POST);
                print "JSON" . $json;
                $sensorValues = htmlspecialchars($_POST[constant('PARAM_SENSOR_VALUES')]);
                insertSensorValues($sensorValues);
                break;

        }
    }else{
        echo "Service Not Set";
    }

function insertSensorValues($values)
{
    $json_values = json_encode($values);
    
    echo "Motion" . $json_values->motion;
}

?>
