<?php
    //API Manager
    //Author :: Kevin Murphy
    //Date   :: 16 - Dec - 14

    //---Constants
    $debug = true;
    //Request Params
    define('PARAM_SERVICE', 'service');
    define('PARAM_GET_CONFIG', 'get_config');
    define('PARAM_UPDATE_CONFIG', 'update_config');
    define('PARAM_UPLOAD_SENSOR_VALUES', 'upload_sensor_values');
    define('PARAM_SENSOR_VALUES', 'sensor_values');
    //SQL Tables
    define('SQL_TABLE_CURRENT', 'current_day_sensor_output');

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
                insertSensorValues($requestObj);
                break;

        }
    }else{
        echo "Service Not Set";
    }

function insertSensorValues($values)
{   
    $serverName = "localhost";
    $username   = "kpm2";
    $password   = "shiegeib";
    $database   = "2015_kpm2";
    $conn = new mysqli($serverName, $username, $password, $database);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $date_and_time   = date("l jS \of F Y h:i:s A");
    $motion          = $values->motion;
    $temperature     = $values->temperature;
    $carbon_monoxide = $values->carbon_monoxide;
    $flammable_gas   = $values->flammable_gas;

    $sql = "INSERT INTO ". constant('SQL_TABLE_CURRENT') . 
           " (carbon_monoxide, temperature, flammable_gas, motion)
             VALUES ('$carbon_monoxide', '$temperature', '$flammable_gas', '$motion')";

    if ($conn->query($sql) === TRUE) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    $conn->close();
}
?>
