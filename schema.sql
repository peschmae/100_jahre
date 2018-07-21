CREATE TABLE `registrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `companions` SMALLINT COLLATE utf8_bin default 0,
  `buffet` varchar(255) COLLATE utf8_bin default '',
  `vegetarian` SMALLINT COLLATE utf8_bin default 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
