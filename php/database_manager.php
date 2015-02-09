<?php

class DatabaseManager
{
    //SQL Tables
    const SQL_TABLE_CURRENT    = 'current_day_sensor_output';
    const SQL_TABLE_PN_DETAILS = 'push_notification_details';

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
            $currentDateAndHour = date("Y-m-d");
            $currentHour = date("H");

            $sqlLatestValues = $this->conn->prepare("SELECT carbon_monoxide, temperature, flammable_gas, motion, date_and_time"
                    . " FROM " . self::SQL_TABLE_CURRENT
                    . " ORDER BY id DESC LIMIT 1");
            
            $sqlMaxValues = $this->conn->prepare("SELECT MAX(carbon_monoxide) AS max_carbon_monoxide,"
                    . " MAX(temperature)     AS max_temperatur, "
                    . " MAX(flammable_gas)   AS max_flammable_gas , "
                    . " MIN(carbon_monoxide) AS min_carbon_monoxide,"
                    . " MIN(temperature)     AS min_temperature, "
                    . " MIN(flammable_gas)   AS min_flammable_gas, "
                    . " SUM(motion)/COUNT(motion)*100 AS percentage_motion" 
                    . " FROM " . self::SQL_TABLE_CURRENT
                    . " WHERE '$currentDateAndHour' = DATE(date_and_time)"
                    . " AND   '$currentHour'        = HOUR(date_and_time)");
            
            $sqlLatestValues->execute();
            $sqlMaxValues->execute();
            
            $sqlLatestValuesArray = $sqlLatestValues->fetch(PDO::FETCH_ASSOC);
            $sqlMaxValuesArray    = $sqlMaxValues->fetch(PDO::FETCH_ASSOC);
            
            $merge_array = array_merge($sqlLatestValuesArray, $sqlMaxValuesArray);
            return $merge_array;
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
            $currentDateAndHour = date("Y-m-d");
            $currentHour = date("H");
            //$currentHour = date("09");
            $sql = $this->conn->prepare("SELECT * FROM " . self::SQL_TABLE_CURRENT .
                    " WHERE '$currentDateAndHour' = DATE(date_and_time)
                      AND '$currentHour' = HOUR(date_and_time)");
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
            $currentDay = date("Y-m-d");
            //$currentDay = "2015-01-20";
            $sql = $this->conn->prepare("SELECT date_and_time, "
                    . " AVG(carbon_monoxide) AS avg_carbon_monoxide,"
                    . " AVG(temperature)     AS avg_temperature, "
                    . " AVG(flammable_gas)   AS avg_flammable_gas , "
                    . " MAX(carbon_monoxide) AS max_carbon_monoxide,"
                    . " MAX(temperature)     AS max_temperature, "
                    . " MAX(flammable_gas)   AS max_flammable_gas , "
                    . " MIN(carbon_monoxide) AS min_carbon_monoxide,"
                    . " MIN(temperature)     AS min_temperature, "
                    . " MIN(flammable_gas)   AS min_flammable_gas , "
                    . " SUM(motion)/COUNT(motion)*100 AS motion"
                    . " FROM " . self::SQL_TABLE_CURRENT 
                    . " WHERE '$currentDay' = DATE(date_and_time)"    
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
        
    public function selectPNRegIDs()
    {
        try
        {
            $sql = $this->conn->prepare("SELECT reg_id "
                    . " FROM " . self::SQL_TABLE_PN_DETAILS);
            $sql->execute();
            return $sql->fetchAll(PDO::FETCH_COLUMN); 
        }
        catch(PDOException $e)
        {
            echo "Error: " . $e->getMessage();
        }
	}
        
    public function insertPNRegID($obj)
    {
        try
        {
            $sql = $this->conn->prepare("INSERT INTO ". self::SQL_TABLE_PN_DETAILS . 
           " (reg_id) VALUES (:reg_id)");
    
            $sql->bindParam(":reg_id", $obj->reg_id);
            $sql->execute();
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