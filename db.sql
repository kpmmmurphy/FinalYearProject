-- MySQL dump 10.13  Distrib 5.5.40, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: TEST
-- ------------------------------------------------------
-- Server version	5.5.40-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `TESTING`
--

DROP TABLE IF EXISTS `TESTING`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TESTING` (
  `value` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TESTING`
--

LOCK TABLES `TESTING` WRITE;
/*!40000 ALTER TABLE `TESTING` DISABLE KEYS */;
INSERT INTO `TESTING` VALUES (12,'MQ7');
/*!40000 ALTER TABLE `TESTING` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `current_day_sensor_output`
--

DROP TABLE IF EXISTS `current_day_sensor_output`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current_day_sensor_output` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_and_time` datetime NOT NULL,
  `carbon_monoxide` int(11) NOT NULL,
  `temperature` int(11) NOT NULL,
  `flammable_gas` int(11) NOT NULL,
  `motion` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_day_sensor_output`
--

LOCK TABLES `current_day_sensor_output` WRITE;
/*!40000 ALTER TABLE `current_day_sensor_output` DISABLE KEYS */;
/*!40000 ALTER TABLE `current_day_sensor_output` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_output_averages`
--

DROP TABLE IF EXISTS `sensor_output_averages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_output_averages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_and_time` date NOT NULL,
  `mq7_carbon_monoxide` int(11) NOT NULL,
  `temperature` int(11) NOT NULL,
  `flammable_gas` int(11) NOT NULL,
  `smoke` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_output_averages`
--

LOCK TABLES `sensor_output_averages` WRITE;
/*!40000 ALTER TABLE `sensor_output_averages` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor_output_averages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_admin_details`
--

DROP TABLE IF EXISTS `system_admin_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_admin_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `device_id` varchar(255) NOT NULL,
  `date_and_time` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_admin_details`
--

LOCK TABLES `system_admin_details` WRITE;
/*!40000 ALTER TABLE `system_admin_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_admin_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_details`
--

DROP TABLE IF EXISTS `system_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_address` varchar(255) NOT NULL,
  `gps_coords_aprrox` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_details`
--

LOCK TABLES `system_details` WRITE;
/*!40000 ALTER TABLE `system_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-16 17:47:30
