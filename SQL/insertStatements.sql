a. 
-- Dumping data for table `airline`
--
INSERT INTO `airline` (`airline_name`) VALUES
('Delta'),
('JetBlue'),
('Qatar Airways'),
('Spirit');

b. 
-- --------------------------------------------------------
-- Dumping data for table `airport`
--
INSERT INTO `airport` (`name_airport`, `city`, `country`, `airport_type`) VALUES
('JFK', 'NYC', NULL, NULL),
('PVG', 'Shanghai', NULL, NULL);

c.
-- --------------------------------------------------------
--
-- Dumping data for table `customer`
--
INSERT INTO `customer` (`email`, `name`, `pass_w`, `building_num`, `street`, `city`, `state`, `phone_num`, `passport_num`, `passport_exp`, `passport_country`, `date_of_birth`) VALUES
('leisha@gmail.com', 'leisha', 'tandon101', '123', 'churchill', 'new york', 'NY', '6503882938', '559237WH32', '2001-09-22', 'united states', '2001-08-24'),
('reanna@gmail.com', 'reanna', 'college123', '001', 'lilac', 'mountain view', 'CA', '6503392837', 'HFS127439', '2001-09-22', 'united states', '1999-06-09'),
('sue@gmail.com', 'sue', 'nyc1234', '899', 'lilac', 'mountain view', 'CA', '6507778888', 'JFKDL31', '2001-09-22', 'united states', '1800-03-09');

d.
-- --------------------------------------------------------
-- Dumping data for table `airplane`
--
INSERT INTO `airplane` (`id_airplane`, `airline_name`, `num_of_seats`, `manufacturing_company`, `age`) VALUES
('1234567', 'Delta', 200, 'Boeing', '2017-04-06'),
('654321', 'Qatar Airways', 300, 'Boeing', '2019-06-28'),
('987654', 'Spirit', 100, 'Airbus', '2012-11-11')
('6734913', 'JetBlue', 90, 'Airbus', '2012-03-19');


e.
-- --------------------------------------------------------
--
-- Dumping data for table `air_staff`
--
INSERT INTO `air_staff` (`username`, `pass_word`, `first_name`, `last_name`, `date_of_birth`, `email`, `airline_name`, `phone_number`) VALUES
('kbrinkman', 'league101', 'kayla', 'brinkman', '2001-10-04', 'kbrinkman@gmail.com', 'JetBlue', '6507423381');

f.
-- --------------------------------------------------------
--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`dept_date`, `dept_time`, `flight_num`, `arr_time`, `arr_airport`, `arr_date`, `base_price`, `id_airplane`, `dept_airport`, `stats`) VALUES
('2022-01-01', '08:20:00', '32', '17:00:00', 'PVG', '2022-01-02', '700.00', '987654', 'PVG', 'Canceled'),
('2022-02-12', '04:00:00', '66', '21:00:00', 'JFK', '2022-02-13', '800.00', '1234567', 'PVG', 'Canceled'),
('2022-03-04', '21:00:00', '40', '04:00:00', 'PVG', '2022-03-05', '590.00', '1234567', 'JFK', 'On Time'),
('2022-10-30', '15:23:00', '41', '10:00:00', 'JFK', '2022-10-31', '1000.00', '1234567', 'PVG', 'On Time'),
('2022-11-01', '13:00:00', '12', '02:00:00', 'PVG', '2022-11-02', '900.00', '987654', 'JFK', 'On Time');
('2023-01-01','09:20:00','100','12:00:00','PVG','2023-01-02','800.00','987654','JFK','Delayed')

.g
-- --------------------------------------------------------
--
-- Dumping data for table `buys`
--
INSERT INTO `buys` (`email`, `ticket_id`, `dept_date`, `dept_time`, `flight_num`, `purchase_timestamp`, `sold_price`, `card_type`, `card_num`, `name_on_card`, `exp_month`, `exp_year`) VALUES
('leisha@gmail.com', '444444', '2022-03-04', '21:00:00', '40', '2022-11-03 16:37:02', '800.00', 'credit', '87643592', 'Leisha', '10', '2035'),
('sue@gmail.com', '111111', '2022-11-01', '13:00:00', '12', '2022-10-31 12:21:12', '950.00', 'debit', '4531901', 'Sue', '08', '2024');

-- --------------------------------------------------------
--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ID`, `dept_date`, `dept_time`, `flight_num`) VALUES
('999999', '2022-03-04', '21:00:00', '40'),
('444444', '2022-11-01', '13:00:00', '12');

-- --------------------------------------------------------
--
-- Dumping data for table `manage`
--

INSERT INTO `manage` (`airline_name`, `dept_date`, `dept_time`, `flight_num`)VALUES
('Delta', '2022-03-04', '21:00:00', '40'),
('Spirit', '2022-11-01', '13:00:00', '12');

