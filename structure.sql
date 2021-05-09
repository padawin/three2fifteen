SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `game` (
  `id` varchar(36) NOT NULL,
  `number_players` int(11) NOT NULL,
  `players` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `current_player` varchar(36) DEFAULT NULL,
  `played_tokens` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `turn` int(11) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_started` timestamp NULL DEFAULT NULL,
  `date_finished` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `game`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

COMMIT;
