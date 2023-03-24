-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Nov 03, 2022 at 04:54 PM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `proj3`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--


--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `id_airplane` varchar(50) NOT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `num_of_seats` int(255) DEFAULT NULL,
  `manufacturing_company` varchar(50) DEFAULT NULL,
  `age` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `name_airport` varchar(50) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `airport_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `air_staff`
--

CREATE TABLE `air_staff` (
  `username` varchar(50) NOT NULL,
  `pass_word` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



--
-- Table structure for table `buys`
--

CREATE TABLE `buys` (
  `email` varchar(50) NOT NULL,
  `ticket_id` char(10) NOT NULL,
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` char(10) NOT NULL,
  `purchase_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `sold_price` decimal(8,2) DEFAULT NULL,
  `card_type` varchar(50) DEFAULT NULL,
  `card_num` varchar(50) DEFAULT NULL,
  `name_on_card` varchar(50) DEFAULT NULL,
  `exp_month` varchar(2) DEFAULT NULL,
  `exp_year` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `pass_w` varchar(50) DEFAULT NULL,
  `building_num` varchar(10) DEFAULT NULL,
  `street` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(3) DEFAULT NULL,
  `phone_num` varchar(50) DEFAULT NULL,
  `passport_num` varchar(40) DEFAULT NULL,
  `passport_exp` date DEFAULT NULL,
  `passport_country` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` char(10) NOT NULL,
  `arr_time` time DEFAULT NULL,
  `arr_airport` varchar(50) DEFAULT NULL,
  `arr_date` date DEFAULT NULL,
  `base_price` decimal(8,2) DEFAULT NULL,
  `id_airplane` varchar(50) DEFAULT NULL,
  `dept_airport` varchar(50) NOT NULL,
  `stats` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `land`
--

CREATE TABLE `land` (
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` char(10) NOT NULL,
  `name_airport` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `manage`
--

CREATE TABLE `manage` (
  `airline_name` varchar(50) NOT NULL,
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ID` char(10) NOT NULL,
  `dept_date` date NOT NULL,
  `dept_time` time NOT NULL,
  `flight_num` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`id_airplane`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`name_airport`);

--
-- Indexes for table `air_staff`
--
ALTER TABLE `air_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `buys`
--
ALTER TABLE `buys`
  ADD PRIMARY KEY (`email`,`ticket_id`,`dept_date`,`dept_time`,`flight_num`),
  ADD KEY `dept_date` (`dept_date`,`dept_time`,`flight_num`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`dept_date`,`dept_time`,`flight_num`),
  ADD KEY `id_airplane` (`id_airplane`),
  ADD KEY `flight_ibfk_2` (`dept_airport`),
  ADD KEY `flight_ibfk_3` (`arr_airport`);

--
-- Indexes for table `land`
--
ALTER TABLE `land`
  ADD PRIMARY KEY (`dept_date`,`dept_time`,`flight_num`),
  ADD KEY `name_airport` (`name_airport`);

--
-- Indexes for table `manage`
--
ALTER TABLE `manage`
  ADD PRIMARY KEY (`airline_name`,`dept_date`,`dept_time`,`flight_num`),
  ADD KEY `dept_date` (`dept_date`,`dept_time`,`flight_num`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ID`,`dept_date`,`dept_time`,`flight_num`),
  ADD KEY `dept_date` (`dept_date`,`dept_time`,`flight_num`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `air_staff`
--
ALTER TABLE `air_staff`
  ADD CONSTRAINT `air_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `buys`
--
ALTER TABLE `buys`
  ADD CONSTRAINT `buys_ibfk_1` FOREIGN KEY (`dept_date`,`dept_time`,`flight_num`) REFERENCES `ticket` (`dept_date`, `dept_time`, `flight_num`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`id_airplane`) REFERENCES `airplane` (`id_airplane`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`dept_airport`) REFERENCES `airport` (`name_airport`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arr_airport`) REFERENCES `airport` (`name_airport`);

--
-- Constraints for table `land`
--
ALTER TABLE `land`
  ADD CONSTRAINT `land_ibfk_1` FOREIGN KEY (`name_airport`) REFERENCES `airport` (`name_airport`);

--
-- Constraints for table `manage`
--
ALTER TABLE `manage`
  ADD CONSTRAINT `manage_ibfk_1` FOREIGN KEY (`dept_date`,`dept_time`,`flight_num`) REFERENCES `flight` (`dept_date`, `dept_time`, `flight_num`),
  ADD CONSTRAINT `manage_ibfk_2` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`dept_date`,`dept_time`,`flight_num`) REFERENCES `flight` (`dept_date`, `dept_time`, `flight_num`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
