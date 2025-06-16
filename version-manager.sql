
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

-- version_test.users definition

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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO version_test.roles (name,description,status,created_at,updated_at) VALUES
	 ('管理员','系统管理员，拥有所有权限',1,'2025-06-08 13:59:09','2025-06-08 13:59:09'),
	 ('开发者','开发人员，负责代码开发和版本管理',1,'2025-06-08 14:04:35','2025-06-08 14:04:35'),
	 ('产品经理','产品人员，负责产品功能设计',1,'2025-06-08 14:06:41','2025-06-08 14:06:41'),
	 ('测试人员','测试人员，负责产品功能测试',1,'2025-06-08 14:07:07','2025-06-08 14:07:07'),
	 ('只读用户','其它部门临时使用',1,'2025-06-08 14:07:52','2025-06-08 14:07:52');

INSERT INTO version_test.users (username,name,email,password_hash,is_admin,created_at,updated_at,status,role_id,department,last_login_at) VALUES
	 ('test',NULL,'test0607@qq.com','pbkdf2:sha256:600000$eydqw75JnHVaSfYt$be3e096d06c98ed549cda9d5137dfcddfe02fbd23f7f315ed26e2e83b6371a96',1,'2025-06-16 12:34:20','2025-06-16 12:34:20',1,1,'运维部',NULL);
