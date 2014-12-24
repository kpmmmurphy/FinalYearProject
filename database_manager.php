<?php

class DatabaseManager
{
	//SQL Tables
    const SQL_TABLE_CURRENT = 'current_day_sensor_output';

    private $conn = NULL;

    private $servername = "localhost";
    private $username   = "kpm2";
    private $password   = "shiegeib";
    private $database   = "2015_kpm2";

	function __construct()
	{
        #$this->conn = new mysqli($this->serverName, $this->username, $this->password, $this->database);
        $this->conn = new PDO("mysql:host=$this->servername;dbname=$this->database", $this->username, $this->password);
        $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        // Check connection
	    //if ($this->conn->connect_error) {
	    //    die("Connection failed: " . $conn->connect_error);
	    //}
	}

	function __destruct() {
        $this->closeConn();
    }

    public function insertSensorValues($values)
    {
    	try
    	{
            $sql = $this->conn->prepare("INSERT INTO ". self::SQL_TABLE_CURRENT . 
	           " (carbon_monoxide, temperature, flammable_gas, motion)
	             VALUES (:carbon_monoxide, :temperature, :flammable_gas, :motion)");
        
            $sql->bindParam(":carbon_monoxide", $values->carbon_monoxide);
            $sql->bindParam(":temperature"    , $values->temperature);
            $sql->bindParam(":flammable_gas"  , $values->flammable_gas);
            $sql->bindParam(":motion"         , $values->motion);
            $sql->execute();
    	}
    	catch(PDOException $e)
        {
            echo "Error: " . $e->getMessage();
    	}  
	}

	public function selectLatestSensorValues()
    {
	    $date_and_time   = date("l jS \of F Y h:i:s A");
	    $motion          = $values->motion;
	    $temperature     = $values->temperature;
	    $carbon_monoxide = $values->carbon_monoxide;
	    $flammable_gas   = $values->flammable_gas;

	    $sql = "SELECT * ". 
	           "FROM " . self::SQL_TABLE_CURRENT . 
	           "WHERE id = MAX(id)";

	    if ($this->conn->query($sql) === TRUE) {
	        echo "New record created successfully";
	    } else {
	        echo "Error: " . $sql . "<br>" . $this->conn->error;
	    }	    
	}

	private function closeConn()
	{
		#$this->conn->close();
		$this->conn = null;
	}

}

?>