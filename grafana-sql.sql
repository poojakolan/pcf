-- MySQL dump 10.13  Distrib 5.5.61, for linux-glibc2.12 (x86_64)
--
-- Host: localhost    Database: grafana
-- ------------------------------------------------------
-- Server version	5.5.61

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
-- Table structure for table `foundries`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/`grafana` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `grafana`;

DROP TABLE IF EXISTS `foundries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `foundries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `foundry_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `pcf_apps`
--

DROP TABLE IF EXISTS `pcf_apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pcf_apps` (
  `id` bigint(225) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `memory` decimal(10,0) DEFAULT NULL,
  `instances` tinyint(10) DEFAULT NULL,
  `disk_space` int(11) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `cpu_used` decimal(20,15) DEFAULT NULL,
  `memory_used` decimal(10,0) DEFAULT NULL,
  `disk_used` decimal(10,0) DEFAULT NULL,
  `space_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `space_fkey_idx` (`space_id`),
  CONSTRAINT `space_fkey` FOREIGN KEY (`space_id`) REFERENCES `pcf_space` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `pcf_org`
--

DROP TABLE IF EXISTS `pcf_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pcf_org` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `org_name` varchar(100) NOT NULL,
  `foundry_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`org_name`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `foundry_id_idx` (`foundry_id`),
  CONSTRAINT `foundry_id` FOREIGN KEY (`foundry_id`) REFERENCES `foundries` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pcf_space`
--

DROP TABLE IF EXISTS `pcf_space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pcf_space` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `space_name` varchar(100) DEFAULT NULL,
  `org_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `org_fkey_idx` (`org_id`),
  CONSTRAINT `org_fkey` FOREIGN KEY (`org_id`) REFERENCES `pcf_org` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-02 15:27:40
