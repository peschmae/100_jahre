CREATE TABLE `registrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_bin NOT NULL,
  `compansions` SMALLINT COLLATE utf8_bin NOT NULL,
  `buffet` varchar(255) COLLATE utf8_bin NOT NULL,
  `vegetarian` SMALLINT COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
