/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50529
 Source Host           : localhost
 Source Database       : braintumor

 Target Server Type    : MySQL
 Target Server Version : 50529
 File Encoding         : utf-8

 Date: 08/07/2019 13:40:55 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `mri_classifications_data`
-- ----------------------------
DROP TABLE IF EXISTS `mri_classifications_data`;
CREATE TABLE `mri_classifications_data` (
  `MRI_id` int(11) NOT NULL AUTO_INCREMENT,
  `image` varchar(50) NOT NULL,
  `contrast` double DEFAULT '0',
  `energy` double DEFAULT '0',
  `entropy` double DEFAULT '0',
  `homogeneity` double DEFAULT '0',
  `correlation` double DEFAULT '0',
  `result` varchar(30) DEFAULT 'Normal',
  `data_type` varchar(50) DEFAULT 'Training',
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`MRI_id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `mri_classifications_data`
-- ----------------------------
BEGIN;
INSERT INTO `mri_classifications_data` VALUES ('2', '', '19.9697', '0.3535', '0.4559', '0.748', '3.1137', '1', 'Training', '0'), ('3', '', '85.9331', '0.2976', '0.0089', '0.6881', '3.4358', '1', 'Training', '0'), ('4', '', '320.2413', '0.3008', '0.5408', '0.678', '4.0389', '1', 'Training', '0'), ('5', '', '1.2921', '0.0003', '0', '0.0007', '0.0043', '1', 'Training', '0'), ('6', '', '1.7241', '0.0003', '0.0003', '0.0007', '0.004', '1', 'Training', '0'), ('7', '', '4.5909', '0.0002', '0', '0.0006', '0.0045', '1', 'Training', '0'), ('8', '', '3.8531', '0.0002', '0.0004', '0.0006', '0.0044', '1', 'Training', '0'), ('9', '', '5.9702', '0.0002', '0.0002', '0.0006', '0.0043', '1', 'Training', '0'), ('10', '', '7.3489', '0.0002', '0.0003', '0.0005', '0.0045', '1', 'Training', '0'), ('11', '', '9.9897', '0.0002', '0', '0.0005', '0.0046', '1', 'Training', '0'), ('12', '', '9.6659', '0.3078', '0.516', '0.7174', '3.7161', '2', 'Training', '0'), ('13', '', '15.7194', '0.252', '-0.0816', '0.6646', '3.4083', '2', 'Training', '0'), ('14', '', '373.4352', '0.2235', '0.4172', '0.5662', '5.3947', '2', 'Training', '0'), ('15', '', '590.2047', '0.1436', '-0.0809', '0.7174', '5.4892', '2', 'Training', '0'), ('16', '', '3.4852', '0.0002', '0.0003', '0.0005', '0.0057', '2', 'Training', '0'), ('17', '', '4.5499', '0.0001', '-0.0001', '0.0004', '0.0062', '2', 'Training', '0'), ('18', '', '8.7649', '0.0001', '0.0003', '0.0005', '0.0056', '2', 'Training', '0'), ('19', '', '1.0561', '0', '0', '0', '0.0006', '2', 'Training', '0'), ('20', '', '8.7637', '0.0001', '0.0003', '0.0004', '0.0052', '2', 'Training', '0'), ('21', '', '1.5162', '0', '0', '0', '0.0005', '2', 'Training', '0'), ('33', '201987131428.jpg', '373.7551250571037', '0.9095224654410158', '6.891861737461042', '0.9942522202648616', '0.9656188675768456', 'BENIGN', 'Testing', '4'), ('34', '201987131433.jpg', '850.7610781178621', '0.9420180322864422', '5.119502108445206', '0.9869166013884006', '0.8688724259981029', 'BENIGN', 'Testing', '4'), ('35', '201987131439.jpg', '366.36592051164916', '0.9862694871150035', '6.294902069330991', '0.9943658548809453', '0.7402550973265252', 'MALIGN', 'Testing', '4'), ('36', '201987131443.jpg', '1789.2209984582', '0.8595290252833878', '7.281276622661128', '0.9724845292889275', '0.8826845597032091', 'MALIGN', 'Testing', '4'), ('37', '201987131449.jpg', '911.0010421425309', '0.9536403204216788', '6.776184785121711', '0.9859902032703451', '0.817562822000444', 'MALIGN', 'Testing', '4'), ('38', '201987131457.jpg', '784.3778837368661', '0.9116933827635092', '6.517116937442124', '0.9879374729533285', '0.9231788726138148', 'MALIGN', 'Testing', '4'), ('39', '20198713157.jpg', '2486.716936957515', '0.8320656504566665', '5.991216314337407', '0.9617581131092561', '0.8589691924862728', 'MALIGN', 'Testing', '4'), ('43', '201987133711.jpg', '1738.4062928277754', '0.8633934014801259', '7.238921276631486', '0.9732659814100856', '0.8831217079575294', 'MALIGN', 'Testing', '4'), ('44', '201987133723.jpg', '1853.1266845591595', '0.887917906302468', '6.275409371788025', '0.9715017579958914', '0.8452057624153415', 'MALIGN', 'Testing', '4'), ('45', '201987133729.jpg', '1201.9463296596618', '0.8970631740026259', '7.33529422470879', '0.9815159116405798', '0.8957325340555994', 'BENIGN', 'Testing', '4'), ('46', '201987133755.jpg', '1201.9463296596618', '0.8970631740026259', '7.33529422470879', '0.9815159116405798', '0.8957325340555994', 'MALIGN', 'Testing', '4');
COMMIT;

-- ----------------------------
--  Table structure for `type_user`
-- ----------------------------
DROP TABLE IF EXISTS `type_user`;
CREATE TABLE `type_user` (
  `type_user_id` int(11) NOT NULL AUTO_INCREMENT,
  `type_user_name` varchar(20) NOT NULL,
  PRIMARY KEY (`type_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` tinyint(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `last_login` datetime NOT NULL,
  `type_user_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Records of `user`
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES ('1', 'Herman Dzumafo', 'herman@yahoo', 'sss', '9f6e6800cfae7749eb6c486619254b9c', '0000-00-00 00:00:00', '2'), ('2', 'Admin', 'example@gmail.com', 'admin123', 'b19114175dddde482a8a8064a4e59d0e', '0000-00-00 00:00:00', '1'), ('3', 'admin ke dua', 'adminkedua@gmail.com', 'adminkedua', '8f1b8c1bb2622e1f02f15bc864d3a93a', '2019-06-08 09:23:53', '2'), ('4', 'Jajang Sofian', 'jajangsummakers@yahoo.co.id', 'jajsofy0078', '6dbf55df743d02a2edd4c3928c9f7205', '2019-08-07 11:18:35', '2'), ('5', 'hermansu', 'hermansu@gmail.com', 'hermansu', '81dc9bdb52d04dc20036dbd8313ed055', '0000-00-00 00:00:00', '2');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
