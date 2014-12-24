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
        $this->conn = new PDO("mysql:host=$this->servername;dbname=$this->database", $this->username, $this->password);
        $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);	}

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
	    try
    	{
            $sql = $this->conn->prepare("SELECT * FROM " . self::SQL_TABLE_CURRENT . " ORDER BY id DESC LIMIT 1");
            $sql->execute();
    	}
    	catch(PDOException $e)
        {
            echo "Error: " . $e->getMessage();
    	}
        return $sql->fetchAll(PDO::FETCH_ASSOC);      
	}

	private function closeConn()
	{
		$this->conn = null;
	}

}

?>