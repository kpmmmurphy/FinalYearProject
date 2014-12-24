<?php

class DatabaseManager
{
	//SQL Tables
    const SQL_TABLE_CURRENT = 'current_day_sensor_output';

    private $conn = NULL;

    private $serverName = "localhost";
    private $username   = "kpm2";
    private $password   = "shiegeib";
    private $database   = "2015_kpm2";

	function __construct()
	{
        $this->conn = new mysqli($this->serverName, $this->username, $this->password, $this->database);
        // Check connection
	    if ($this->conn->connect_error) {
	        die("Connection failed: " . $conn->connect_error);
	    }
	}

	function __destruct() {
        self::closeConn();
    }

    public function insertSensorValues($values)
    {
	    $date_and_time   = date("l jS \of F Y h:i:s A");
	    $motion          = $values->motion;
	    $temperature     = $values->temperature;
	    $carbon_monoxide = $values->carbon_monoxide;
	    $flammable_gas   = $values->flammable_gas;

	    $sql = "INSERT INTO ". self::SQL_TABLE_CURRENT . 
	           " (carbon_monoxide, temperature, flammable_gas, motion)
	             VALUES ('$carbon_monoxide', '$temperature', '$flammable_gas', '$motion')";

	    if ($this->conn->query($sql) === TRUE) {
	        echo "New record created successfully";
	    } else {
	        echo "Error: " . $sql . "<br>" . $this->conn->error;
	    }	    
	}

	private function closeConn()
	{
		$this->conn->close();
	}

}

?>