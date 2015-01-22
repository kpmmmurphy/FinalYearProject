<?php

class DatabaseManager
{
    //SQL Tables
    const SQL_TABLE_CURRENT       = 'current_day_sensor_output';
    const SQL_TABLE_HOUR_VALUES   = 'sensor_output_hour_values';
    const SQL_TABLE_DAY_VALUES    = 'sensor_output_day_values';

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
                return $sql->fetchAll(PDO::FETCH_ASSOC); 
            }
            catch(PDOException $e)
            {
                echo "Error: " . $e->getMessage();
            }
	}
        
        public function selectAllCurrentDaySensorValues()
        {
            try
            {
                $sql = $this->conn->prepare("SELECT * FROM " . self::SQL_TABLE_CURRENT);
                $sql->execute();
                return $sql->fetchAll(PDO::FETCH_ASSOC); 
            }
            catch(PDOException $e)
            {
                echo "Error: " . $e->getMessage();
            }
	}
        
        public function selectCurrentHourSensorValues()
        {
            try
            {
                $currentHour = date("Y-m-d H");
                #$currentHour = "2015-01-20 12";
                $sql = $this->conn->prepare("SELECT * FROM " . self::SQL_TABLE_CURRENT .
                        " WHERE date_and_time >= '" . $currentHour . "'");
                $sql->execute();
                return $sql->fetchAll(PDO::FETCH_ASSOC); 
            }
            catch(PDOException $e)
            {
                echo "Error: " . $e->getMessage();
            }
	}
        
        public function selectAverageSensorValuesPerHour()
        {
            try
            {
                $sql = $this->conn->prepare("SELECT date_and_time, "
                        . " AVG(carbon_monoxide) AS avg_carbon_monoxide,"
                        . " AVG(temperature) AS avg_temperature, "
                        . " AVG(flammable_gas) AS avg_flammable_gas , "
                        . " SUM(motion)/COUNT(motion)*100 AS motion"
                        . " FROM " . self::SQL_TABLE_CURRENT 
                        . " GROUP BY hour(date_and_time)");
                $sql->execute();
                return $sql->fetchAll(PDO::FETCH_ASSOC); 
            }
            catch(PDOException $e)
            {
                echo "Error: " . $e->getMessage();
            }
	}
        
        public function selectAggSensorValuesPerHour()
        {
            try
            {
                $sql = $this->conn->prepare("SELECT date_and_time, "
                        . " AVG(carbon_monoxide) AS avg_carbon_monoxide,"
                        . " AVG(temperature) AS avg_temperature, "
                        . " AVG(flammable_gas) AS avg_flammable_gas , "
                        . " MAX(carbon_monoxide) AS max_carbon_monoxide,"
                        . " MAX(temperature)     AS max_temperature, "
                        . " MAX(flammable_gas)   AS max_flammable_gas , "
                        . " MIN(carbon_monoxide) AS min_carbon_monoxide,"
                        . " MIN(temperature)     AS min_temperature, "
                        . " MIN(flammable_gas)   AS min_flammable_gas , "
                        . " SUM(motion)/COUNT(motion)*100 AS motion"
                        . " FROM " . self::SQL_TABLE_CURRENT 
                        . " GROUP BY hour(date_and_time)");
                $sql->execute();
                return $sql->fetchAll(PDO::FETCH_ASSOC); 
            }
            catch(PDOException $e)
            {
                echo "Error: " . $e->getMessage();
            }
	}
        
        public function selectAggSensorValuesPerDay()
        {
            try
            {
                $sql = $this->conn->prepare("SELECT date_and_time, "
                        . " AVG(carbon_monoxide) AS avg_carbon_monoxide,"
                        . " AVG(temperature) AS avg_temperature, "
                        . " AVG(flammable_gas) AS avg_flammable_gas , "
                        . " MAX(carbon_monoxide) AS max_carbon_monoxide,"
                        . " MAX(temperature)     AS max_temperature, "
                        . " MAX(flammable_gas)   AS max_flammable_gas , "
                        . " MIN(carbon_monoxide) AS min_carbon_monoxide,"
                        . " MIN(temperature)     AS min_temperature, "
                        . " MIN(flammable_gas)   AS min_flammable_gas , "
                        . " SUM(motion)/COUNT(motion)*100 AS motion"
                        . " FROM " . self::SQL_TABLE_CURRENT 
                        . " GROUP BY day(date_and_time)");
                $sql->execute();
                return $sql->fetchAll(PDO::FETCH_ASSOC); 
            }
            catch(PDOException $e)
            {
                echo "Error: " . $e->getMessage();
            }
	}
        
	private function closeConn()
	{
		$this->conn = null;
	}

}

?>