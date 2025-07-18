-- MySQL dump 10.13  Distrib 5.7.44, for Win64 (x86_64)
--
-- Host: localhost    Database: version_test
-- ------------------------------------------------------
-- Server version	5.7.44

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) DEFAULT NULL,
  `original_filename` varchar(255) DEFAULT NULL,
  `file_path` varchar(500) DEFAULT NULL,
  `file_size` int(11) DEFAULT NULL,
  `file_type` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `version_id` int(11) DEFAULT NULL,
  `uploader_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `uploader_id` (`uploader_id`),
  KEY `version_id` (`version_id`),
  CONSTRAINT `files_ibfk_1` FOREIGN KEY (`uploader_id`) REFERENCES `users` (`id`),
  CONSTRAINT `files_ibfk_2` FOREIGN KEY (`version_id`) REFERENCES `versions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_logs`
--

DROP TABLE IF EXISTS `operation_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operation_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operation_time` datetime DEFAULT NULL,
  `operation_type` varchar(50) NOT NULL,
  `object_type` varchar(50) NOT NULL,
  `object_name` varchar(100) DEFAULT NULL,
  `object_id` varchar(50) DEFAULT NULL,
  `operator_id` int(11) DEFAULT NULL,
  `details` text,
  PRIMARY KEY (`id`),
  KEY `ix_operation_logs_object_id` (`object_id`),
  KEY `ix_operation_logs_object_type` (`object_type`),
  KEY `ix_operation_logs_operation_time` (`operation_time`),
  KEY `ix_operation_logs_operation_type` (`operation_type`),
  KEY `ix_operation_logs_operator_id` (`operator_id`),
  CONSTRAINT `operation_logs_ibfk_1` FOREIGN KEY (`operator_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_logs`
--

LOCK TABLES `operation_logs` WRITE;
/*!40000 ALTER TABLE `operation_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `operation_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `code` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_products_code` (`code`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_roles_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'管理员','系统管理员，拥有所有权限',1,'2025-06-08 13:59:09','2025-06-08 13:59:09'),(2,'开发者','开发人员，负责代码开发和版本管理',1,'2025-06-08 14:04:35','2025-06-08 14:04:35'),(3,'产品经理','产品人员，负责产品功能设计',1,'2025-06-08 14:06:41','2025-06-08 14:06:41'),(4,'测试人员','测试人员，负责产品功能测试',1,'2025-06-08 14:07:07','2025-06-08 14:07:07'),(5,'只读用户','其它部门临时使用',1,'2025-06-08 14:07:52','2025-06-08 14:07:52');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_product_permissions`
--

DROP TABLE IF EXISTS `user_product_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_product_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `permission_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `user_product_permissions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_product_permissions_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_product_permissions`
--

LOCK TABLES `user_product_permissions` WRITE;
/*!40000 ALTER TABLE `user_product_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_product_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  `role_id` int(11) DEFAULT NULL,
  `department` varchar(64) DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `fk_users_role_id` (`role_id`),
  CONSTRAINT `fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'test',NULL,'test0607@qq.com','pbkdf2:sha256:600000$eydqw75JnHVaSfYt$be3e096d06c98ed549cda9d5137dfcddfe02fbd23f7f315ed26e2e83b6371a96',1,'2025-06-16 12:34:20','2025-06-16 12:34:20',1,1,'运维部',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `versions`
--

DROP TABLE IF EXISTS `versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `versions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `version_number` varchar(50) NOT NULL,
  `description` text,
  `release_notes` text,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `released_at` datetime DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `lock_status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `versions_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `versions_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `versions`
--

LOCK TABLES `versions` WRITE;
/*!40000 ALTER TABLE `versions` DISABLE KEYS */;
/*!40000 ALTER TABLE `versions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'version_test'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-10 11:39:35
