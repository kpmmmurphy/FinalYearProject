<?php
    //API Manager
    //Author :: Kevin Murphy
    //Date   :: 16 - Dec - 14

    //Costants
    $debug = true;
    define('PARAM_SERVICE', 'service');
    define('PARAM_GET_CONFIG', 'get_config');
    define('PARAM_UPDATE_CONFIG', 'update_config');
    define('PARAM_UPLOAD_SENSOR_VALUES', 'upload_sensor_values');
    define('PARAM_SENSOR_VALUES', 'sensor_values');

    $serverName = "localhost";
    $username   = "kpm2";
    $password   = "shiegeib";
    $database   = "2015_kpm2";

    $request = file_get_contents('php://input', 0, null, null);
    var_dump(json_decode($request));
    #echo $request->service;
    if($debug){
        echo "\n";
        foreach (getallheaders() as $name => $value) {
            echo "$name: $value\n";
        }
    }
    
    #$jsonString = file_get_contents('php://input', 0, null, null);
    #$request = json_decode($jsonString , true);
    #echo "\n" . "Motion" . $request['motion'] . "\n";
    #foreach ($request as $name => $value) {
    #        echo "$name: $value\n";
    #    }
    $headers = getallheaders();
    
    if(isset($headers[constant('PARAM_SERVICE')])){
        $requestedService = htmlspecialchars($headers[constant('PARAM_SERVICE')]);

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
                echo "\nInsert Sensor Values into DB\n";
                #insertSensorValues($sensorValues);
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
