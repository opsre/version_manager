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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `code` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_products_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;


-- version_test.users definition

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
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
  KEY `users_index_0` (`username`,`email`),
  CONSTRAINT `fk_users_role_id` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;



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
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `versions_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `versions_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `roles_index_0` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_product_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    permission_type VARCHAR(20) NOT NULL, -- 只读: read，编辑: edit，管理: admin
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);