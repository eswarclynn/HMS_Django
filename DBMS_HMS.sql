CREATE SCHEMA IF NOT EXISTS `hosteldb`;
USE `hosteldb` ;


CREATE TABLE IF NOT EXISTS `hosteldb`.`institute_institutestd` (
  `regd_no` INT(11) NOT NULL,
  `roll_no` INT(11) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `branch` VARCHAR(3) NOT NULL,
  `pwd` VARCHAR(1) NOT NULL,
  `phone` INT(11) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `year` INT(11) NOT NULL,
  `email_id` VARCHAR(50) NOT NULL,
  `dob` DATE NOT NULL,
  `hosteller` VARCHAR(1) NOT NULL,
  `paid` VARCHAR(1) NOT NULL,
  `gender` VARCHAR(7) NOT NULL,
  PRIMARY KEY (`regd_no`));


CREATE TABLE IF NOT EXISTS `hosteldb`.`complaints_complaints` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(40) NOT NULL,
  `summary` VARCHAR(200) NOT NULL,
  `detailed` LONGTEXT NOT NULL,
  `complainee_id` INT(11) NULL DEFAULT NULL,
  `regd_no_id` INT(11) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `date` DATE NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`complainee_id`)
    REFERENCES `hosteldb`.`institute_institutestd` (`regd_no`),
    FOREIGN KEY (`regd_no_id`)
    REFERENCES `hosteldb`.`institute_institutestd` (`regd_no`));



CREATE TABLE IF NOT EXISTS `hosteldb`.`institute_officials` (
  `emp_id` INT(11) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `designation` VARCHAR(20) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `phone` INT(11) NOT NULL,
  `email_id` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`emp_id`));



CREATE TABLE IF NOT EXISTS `hosteldb`.`complaints_officialcomplaints` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(40) NOT NULL,
  `summary` VARCHAR(200) NOT NULL,
  `detailed` LONGTEXT NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `date` DATE NOT NULL,
  `complainee_id` INT(11) NULL DEFAULT NULL,
  `regd_no_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`complainee_id`)
    REFERENCES `hosteldb`.`institute_institutestd` (`regd_no`),
    FOREIGN KEY (`regd_no_id`)
    REFERENCES `hosteldb`.`institute_officials` (`emp_id`));



CREATE TABLE IF NOT EXISTS `hosteldb`.`institute_blocks` (
  `block_name` VARCHAR(50) NOT NULL,
  `room_type` VARCHAR(2) NOT NULL,
  `emp_id_id` INT(11) NOT NULL,
  `block_id` INT(11) NOT NULL,
  `capacity` INT(11) NOT NULL,
  `gender` VARCHAR(7) NOT NULL,
  PRIMARY KEY (`block_id`),
    FOREIGN KEY (`emp_id_id`)
    REFERENCES `hosteldb`.`institute_officials` (`emp_id`));



CREATE TABLE IF NOT EXISTS `hosteldb`.`students_attendance` (
  `dates` LONGTEXT NOT NULL,
  `regd_no_id` INT(11) NOT NULL,
  `status` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`regd_no_id`),
    FOREIGN KEY (`regd_no_id`)
    REFERENCES `hosteldb`.`institute_institutestd` (`regd_no`));



CREATE TABLE IF NOT EXISTS `hosteldb`.`students_details` (
  `room_no` INT(11) NOT NULL,
  `block_id_id` INT(11) NOT NULL,
  `regd_no_id` INT(11) NOT NULL,
  `floor` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`regd_no_id`),

    FOREIGN KEY (`block_id_id`)
    REFERENCES `hosteldb`.`institute_blocks` (`block_id`),

    FOREIGN KEY (`regd_no_id`)
    REFERENCES `hosteldb`.`institute_institutestd` (`regd_no`));



CREATE TABLE IF NOT EXISTS `hosteldb`.`students_outing` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `fromDate` DATE NOT NULL,
  `fromTime` TIME NOT NULL,
  `toDate` DATE NOT NULL,
  `purpose` VARCHAR(150) NOT NULL,
  `parent_mobile` BIGINT(20) NOT NULL,
  `regd_no_id` INT(11) NOT NULL,
  `permission` VARCHAR(20) NOT NULL,
  `toTime` TIME NOT NULL,
  PRIMARY KEY (`id`),

    FOREIGN KEY (`regd_no_id`)
    REFERENCES `hosteldb`.`institute_institutestd` (`regd_no`));


