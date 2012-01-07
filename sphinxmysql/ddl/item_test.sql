CREATE TABLE `item` (
      `item_id` int(32) NOT NULL AUTO_INCREMENT,
      `tags` varchar(2048) NOT NULL,
      `publish_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
