-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: zanner.org.ua    Database: bMRI_db
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1

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
-- Table structure for table `image_analysis`
--

DROP TABLE IF EXISTS `image_analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image_analysis` (
  `image_id` int(11) NOT NULL,
  `segment` text COLLATE utf8_unicode_ci,
  `tumor` text COLLATE utf8_unicode_ci,
  `diagnosis` int(11) DEFAULT NULL,
  `recommendations` text COLLATE utf8_unicode_ci,
  `confidence` float DEFAULT NULL,
  `verified` tinyint(1) DEFAULT NULL,
  `dt` datetime DEFAULT NULL,
  PRIMARY KEY (`image_id`),
  KEY `diagnosis` (`diagnosis`),
  CONSTRAINT `image_analysis_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `images` (`image_id`) ON DELETE CASCADE,
  CONSTRAINT `image_analysis_ibfk_2` FOREIGN KEY (`diagnosis`) REFERENCES `tumor_types` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_analysis`
--

LOCK TABLES `image_analysis` WRITE;
/*!40000 ALTER TABLE `image_analysis` DISABLE KEYS */;
INSERT INTO `image_analysis` VALUES (5,'analyzed_12_2019-12-20 23:40:30_9.jpeg','Tumor detected with a probability: 1.0',2,NULL,1,0,'2019-12-20 23:42:21'),(6,'analyzed_13_2019-12-20 23:54:08_2.jpg','Tumor detected with a probability: 1.0',2,NULL,1,0,'2019-12-20 23:54:27'),(8,'analyzed_12_2019-12-20 22:24:28_9.png','Tumor detected with a probability: 1.0',2,NULL,1,0,'2019-12-20 22:24:47'),(12,'analyzed_1_2019-12-21 08:53:07_1.png','Tumor detected with a probability: 1.0',2,NULL,1,0,'2019-12-21 08:53:26'),(13,'analyzed_1_2019-12-21 08:54:06_1.png','Tumor detected with a probability: 0.8853302597999573',2,NULL,0.88533,0,'2020-02-03 16:43:41'),(19,'1_2020-02-03 16:43:46_1.jpeg','NO tumors detected with a probability: 1.0',1,NULL,1,0,'2020-02-03 16:43:55');
/*!40000 ALTER TABLE `image_analysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_types`
--

DROP TABLE IF EXISTS `image_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_types`
--

LOCK TABLES `image_types` WRITE;
/*!40000 ALTER TABLE `image_types` DISABLE KEYS */;
INSERT INTO `image_types` VALUES (1,'MRI'),(2,'fMRI'),(3,'CT');
/*!40000 ALTER TABLE `image_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `images` (
  `image_id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `im_type` int(11) DEFAULT NULL,
  `image` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`image_id`),
  UNIQUE KEY `image_id` (`image_id`) USING BTREE,
  KEY `patient_id` (`patient_id`),
  KEY `im_type` (`im_type`),
  CONSTRAINT `images_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_info` (`pid`) ON DELETE CASCADE,
  CONSTRAINT `images_ibfk_2` FOREIGN KEY (`im_type`) REFERENCES `image_types` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (5,12,'2019-12-20 23:40:30',1,'12_2019-12-20 23:40:30_9.jpeg'),(6,13,'2019-12-20 23:54:08',1,'13_2019-12-20 23:54:08_2.jpg'),(7,12,'2019-12-20 22:06:52',1,'12_2019-12-20 22:06:52_9.jpg'),(8,12,'2019-12-20 22:24:28',1,'12_2019-12-20 22:24:28_9.png'),(11,12,'2019-12-21 05:27:51',1,'12_2019-12-21 05:27:51_9.png'),(12,1,'2019-12-21 08:53:07',1,'1_2019-12-21 08:53:07_1.png'),(13,1,'2019-12-21 08:54:06',1,'1_2019-12-21 08:54:06_1.png'),(19,1,'2020-02-03 16:43:46',1,'1_2020-02-03 16:43:46_1.jpeg');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_info`
--

DROP TABLE IF EXISTS `patient_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient_info` (
  `pid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'patient id',
  `last_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `first_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ssn` int(11) DEFAULT NULL COMMENT 'patient social security number',
  `gender` char(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `therapist_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  UNIQUE KEY `pid` (`pid`) USING BTREE,
  KEY `therapist_id` (`therapist_id`),
  CONSTRAINT `patient_info_ibfk_1` FOREIGN KEY (`therapist_id`) REFERENCES `therapists` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_info`
--

LOCK TABLES `patient_info` WRITE;
/*!40000 ALTER TABLE `patient_info` DISABLE KEYS */;
INSERT INTO `patient_info` VALUES (1,'Roberto','Elliot',456978219,'m',12,1),(2,'Lever','Carly',586325789,'f',25,1),(3,'McLean','Elle',987235476,'f',19,1),(4,'Barnes','Isabel',889456258,'f',58,1),(6,'Jose','Casper',456325897,'m',56,1),(7,'Marx','Thomas',123456789,'m',32,1),(8,'Eric','Foreman',416325897,'m',56,1),(9,'Robert','Chase',123446789,'m',32,1),(10,'Allison','Cameron',156325897,'f',56,1),(11,'Chris','Taub',123453789,'m',32,1),(12,'Esmall','Sem',173857483,'m',34,9),(13,'Smith','Alex',565758594,'m',45,2);
/*!40000 ALTER TABLE `patient_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `therapists`
--

DROP TABLE IF EXISTS `therapists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `therapists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `therapists`
--

LOCK TABLES `therapists` WRITE;
/*!40000 ALTER TABLE `therapists` DISABLE KEYS */;
INSERT INTO `therapists` VALUES (1,'Shaun','Murphy','Dr.','good_doctor','pbkdf2:sha256:150000$15D4pjEH$3572539ed1efdd7b6025504acfd457fa1f0ccd5d9e7dbce28a1cc6ebd42144a1'),(2,'Carly','Lever','nurse','alexsmith','pbkdf2:sha256:150000$r62hdKmb$3658428f759d0fdc733e2b8cea00c6dcd70c41138d96eee7e15e4fd74b8076f1'),(3,'Lea','Dilallo','Dr.','lea_diablo',NULL),(4,'Claire','Brown','Dr.','clairbrown',NULL),(5,'Aaron','Glassman','Dr.','glassy',NULL),(6,'Gregory','House','Dr.','greg_h',NULL),(7,'Lisa','Cuddy','Dr.','lisa228',NULL),(8,'James','Wilson','Dr.','james_w',NULL),(9,'Vladyslav','Zalevskyi','dr','vzalevskyi','pbkdf2:sha256:150000$qkbG0oVb$f30a0bc495dbee5cd831e33c04f97a5229bb99e98dd17ca2c81fd8a40fccdefa'),(10,'Alex','Turner','dr','alex111','pbkdf2:sha256:150000$apkUe7Tc$6c9e3cbda9813186fa56193f57c5121f1867a141de2688ce1969826b71cbf199');
/*!40000 ALTER TABLE `therapists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tumor_types`
--

DROP TABLE IF EXISTS `tumor_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tumor_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `descr` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tumor_types`
--

LOCK TABLES `tumor_types` WRITE;
/*!40000 ALTER TABLE `tumor_types` DISABLE KEYS */;
INSERT INTO `tumor_types` VALUES (1,'absent','no tumor or abnormalities detected'),(2,'benign','does not invade its surrounding tissue or spread around the body'),(3,'malignant','may invade its surrounding tissue or spread around the body');
/*!40000 ALTER TABLE `tumor_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-04 15:09:53
