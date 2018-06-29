DROP DATABASE IF EXISTS `akila`;
CREATE DATABASE `akila`;
SET FOREIGN_KEY_CHECKS=0;
USE `akila`;


/*
businessAccountUID	Varchar(50)
businessEntityName	Varchar(100)
EIN	Varchar(50)
firstName	Varchar(50)
middleName	Varchar(50)
lastName	Varchar (50)
emailID	Varchar(100)
password	Varchar(50)
contactNumber	Varchar(50)
businessAddress	Varchar(200)
City	Varchar(50)
Country	Varchar(50)
zipCode	Varchar(50)
*/

DROP TABLE IF EXISTS `business_accounts`;
CREATE TABLE `business_accounts` (
		`businessAccountUID`                                varchar(50) NOT NULL PRIMARY KEY,
		`businessEntityName`                                varchar(50) NOT NULL ,
		`EIN`                                               varchar(50) NOT NULL UNIQUE,
		`firstName`                                         varchar(50) NOT NULL ,
		`middleName`                                        varchar(50) ,
		`lastName`                                          varchar(50) ,
		`emailID`                                           varchar(100) NOT NULL UNIQUE,
		`password`                                          varchar(50) NOT NULL ,
		`contactNumber`                                     varchar(50) NOT NULL ,
		`address`                                           varchar(200) NOT NULL ,
		`city`                                              varchar(50) NOT NULL ,
		`country`                                           varchar(50) NOT NULL ,
		`zipCode`                                           varchar(20) NOT NULL ,
		INDEX (`emailID`),
		INDEX (`contactNumber`)
);

/*
d)	Delivery channels
Oid_index	int
channelType	Varchar(50)
webHookUrl	Varchar(100)
supported	Enum(Yes/No)
*/
DROP TABLE IF EXISTS `delivery_channel`;
CREATE TABLE `delivery_channel` (
		`oid_index`                                     	int unsigned NOT NULL  PRIMARY KEY,
		`channelType`                                       varchar(50) NOT NULL UNIQUE,
		`webHookUrl`                                        varchar(50) ,
		`supported`                                         enum('YES','NO') NOT NULL default 'NO' 
);
INSERT `delivery_channel` SET `oid_index` ='0', `channelType` = 'SMS', supported='YES';
INSERT `delivery_channel` SET `oid_index` ='1', `channelType` = 'WHATSAPP', supported='NO';
INSERT `delivery_channel` SET `oid_index` ='2', `channelType` = 'FB', supported='NO';

/*
d)	Hotel_Room_info
Oid_index	int
RoomType	Enum
imageUrl1	Varchar(200)
imageUrl2	Varchar(200)
imageUrl3	Varchar(200)
imageUrl4	Varchar(200)
imageUrl5	Varchar(200)
imageUrl6	Varchar(200)
facilities  Varchar(500)
*/
DROP TABLE IF EXISTS `hotel_room_info`;
CREATE TABLE `hotel_room_info` (
		`oid_index`                                     	int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
		`roomType`                                       enum('STANDARD_SINGLE','STANDARD_DOUBLE','DELUXE_SINGLE','DELUXE_DOUBLE','EXECUTIVE_SUITE','PRESEDENTIAL_SUITE','OTHERS') NOT NULL default 'STANDARD_DOUBLE',
		`imageUrl1`                                        varchar(200) ,
		`imageUrl2`                                        varchar(200) ,
		`imageUrl3`                                        varchar(200) ,
		`imageUrl4`                                        varchar(200) ,
		`imageUrl5`                                        varchar(200) ,
		`imageUrl6`                                        varchar(200) ,
		`facilities`									   varchar(500),
		`isKitchen`										   enum('YES','NO') NOT NULL default 'NO',
		`isMicrowave`									   enum('YES','NO') NOT NULL default 'NO',
		`isBreakfast`									   enum('YES','NO') NOT NULL default 'NO'
);

/*
d)	Hotel_Booking_info
bookingID     varchar(100)
firstName     varchat(100)
middleName     varchat(100)
lastName     varchat(100)
emailID       varchar(100)
contactNo.    varchar(100)
Address   Varchar(200)
city          varchar(100)
state	      varchar(100)
country	      varchar(100)
zipcode       varchar(50)
RoomType	Enum
DateOfBooking Varchar(100)
checkInDate   varchar(100)
checkOutDate  varchar(100)
`status`      enum('BOOKED','CHECKED-IN','CHECKED-OUT','CANCELLED') NOT NULL ,
*/

DROP TABLE IF EXISTS `booking_info`;
CREATE TABLE `booking_info` (
		`bookingID`                                         varchar(50) NOT NULL PRIMARY KEY,
		`firstName`                                         varchar(50) NOT NULL ,
		`middleName`                                        varchar(50) ,
		`lastName`                                          varchar(50) ,
		`emailID`                                           varchar(100) NOT NULL UNIQUE,
		`contactNumber`                                     varchar(50) NOT NULL ,
		`address`                                           varchar(200) NOT NULL ,
		`city`                                              varchar(50) NOT NULL ,
		`state`                                              varchar(50) NOT NULL ,
		`country`                                           varchar(50) NOT NULL ,
		`zipCode`                                           varchar(20) NOT NULL ,
		`roomType`                                       enum('STANDARD_SINGLE','STANDARD_DOUBLE','DELUXE_SINGLE','DELUXE_DOUBLE','EXECUTIVE_SUITE','PRESEDENTIAL_SUITE','OTHERS') NOT NULL default 'STANDARD_DOUBLE',
		`DateOfBooking`                                     DATETIME NOT NULL ,
		`CheckInDate`                                      DATETIME  NOT NULL ,
		`CheckOutDate`                                     DATETIME  NOT NULL ,
		`status`                                     enum('BOOKED','CHECKED-IN','CHECKED-OUT','CANCELLED') NOT NULL ,
		INDEX (`emailID`),
		INDEX (`contactNumber`)
);


/*
d) messages
message_uuid     varchar(200)	
source             varchar(50)
destination               varchar(50)
message_content  varchar(500)
message_time     DATETIME,
session_id        varchar(100)
*/
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
		`message_uuid`                                 	varchar(100) NOT NULL PRIMARY KEY,
		`source`                                        varchar(50) ,
		`destination`                                    varchar(50) ,
		`message_content`                                 varchar(500) ,
		`message_time`                                        DATETIME ,
		`session_id`                                        DATETIME 
);



