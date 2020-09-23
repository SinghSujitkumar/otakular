-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 28 Agu 2019 pada 15.15
-- Versi server: 10.1.31-MariaDB
-- Versi PHP: 5.6.35

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `braintumor`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `mri_classifications_data`
--

CREATE TABLE `mri_classifications_data` (
  `MRI_id` int(11) NOT NULL,
  `image` varchar(50) NOT NULL,
  `contrast` double DEFAULT '0',
  `energy` double DEFAULT '0',
  `entropy` double DEFAULT '0',
  `homogeneity` double DEFAULT '0',
  `correlation` double DEFAULT '0',
  `result` varchar(30) DEFAULT 'Normal',
  `data_type` varchar(50) DEFAULT 'Training',
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `mri_classifications_data`
--

INSERT INTO `mri_classifications_data` (`MRI_id`, `image`, `contrast`, `energy`, `entropy`, `homogeneity`, `correlation`, `result`, `data_type`, `user_id`) VALUES
(2, '', 19.9697, 0.3535, 0.4559, 0.748, 3.1137, 'BENIGN', 'Training', 0),
(4, '', 85.9331, 0.2976, 0.0089, 0.6881, 3.4358, 'BENIGN', 'Training', 0),
(6, '', 320.2413, 0.3008, 0.5408, 0.678, 4.0389, 'BENIGN', 'Training', 0),
(8, '', 1.2921, 0.0003, 0, 0.0007, 0.0043, 'BENIGN', 'Training', 0),
(10, '', 1.7241, 0.0003, 0.0003, 0.0007, 0.004, 'BENIGN', 'Training', 0),
(12, '', 4.5909, 0.0002, 0, 0.0006, 0.0045, 'BENIGN', 'Training', 0),
(14, '', 3.8531, 0.0002, 0.0004, 0.0006, 0.0044, 'BENIGN', 'Training', 0),
(16, '', 5.9702, 0.0002, 0.0002, 0.0006, 0.0043, 'BENIGN', 'Training', 0),
(18, '', 7.3489, 0.0002, 0.0003, 0.0005, 0.0045, 'BENIGN', 'Training', 0),
(20, '', 9.9897, 0.0002, 0, 0.0005, 0.0046, 'BENIGN', 'Training', 0),
(22, '', 0.3078, 9.6659, 0.516, 0.7174, 3.7161, 'MALIGN', 'Training', 0),
(24, '', 0.252, 15.7194, -0.0816, 0.6646, 3.4083, 'MALIGN', 'Training', 0),
(26, '', 0.2235, 373.4352, 0.4172, 0.5662, 5.3947, 'MALIGN', 'Training', 0),
(28, '', 0.1436, 590.2047, -0.0809, 0.7174, 5.4892, 'MALIGN', 'Training', 0),
(30, '', 0.0002, 3.4852, 0.0003, 0.0005, 0.0057, 'MALIGN', 'Training', 0),
(32, '', 0.0001, 4.5499, -0.0001, 0.0004, 0.0062, 'MALIGN', 'Training', 0),
(34, '', 0.0001, 8.7649, 0.0003, 0.0005, 0.0056, 'MALIGN', 'Training', 0),
(36, '', 0, 1.0561, 0, 0, 0.0006, 'MALIGN', 'Training', 0),
(38, '', 0.0001, 8.7637, 0.0003, 0.0004, 0.0052, 'MALIGN', 'Training', 0),
(40, '', 0, 1.5162, 0, 0, 0.0005, 'MALIGN', 'Training', 0),
(41, '2019828201124.jpg', 373.7551250571037, 0.9095224654410158, 6.891861737461042, 0.9942522202648616, 0.9656188675768456, 'BENIGN', 'Testing', 4),
(42, '2019828201144.jpg', 2011.3777838053907, 0.8710701470754184, 7.134891471427264, 0.9690680991633287, 0.8537045181038367, 'MALIGN', 'Testing', 4),
(43, '201982820122.jpg', 1789.2209984582, 0.8595290252833878, 7.281276622661128, 0.9724845292889275, 0.8826845597032091, 'MALIGN', 'Testing', 4),
(44, '2019828201220.jpg', 674.529993718593, 0.9726549684821123, 5.263759966708437, 0.9896267647753423, 0.7627330055072128, 'MALIGN', 'Testing', 4),
(45, '2019828201234.jpg', 2348.997594506624, 0.8714291422069741, 7.071501392295478, 0.9638760250591052, 0.8245679868834057, 'MALIGN', 'Testing', 4),
(46, '2019828201249.jpg', 2373.991341651439, 0.8223613458546924, 6.672049828530094, 0.9634916596184382, 0.8735866754015453, 'MALIGN', 'Testing', 4),
(47, '2019828201335.jpg', 134.40430847418912, 0.9959973029632959, 5.14876307095369, 0.9979330681808172, 0.6515058078899938, 'BENIGN', 'Testing', 4);

-- --------------------------------------------------------

--
-- Struktur dari tabel `type_user`
--

CREATE TABLE `type_user` (
  `type_user_id` int(11) NOT NULL,
  `type_user_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `user_id` tinyint(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `last_login` datetime NOT NULL,
  `type_user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`user_id`, `name`, `email`, `username`, `password`, `last_login`, `type_user_id`) VALUES
(1, 'Herman Dzumafo', 'herman@yahoo', 'sss', '9f6e6800cfae7749eb6c486619254b9c', '0000-00-00 00:00:00', 2),
(2, 'Admin', 'example@gmail.com', 'admin123', 'b19114175dddde482a8a8064a4e59d0e', '0000-00-00 00:00:00', 1),
(3, 'admin ke dua', 'adminkedua@gmail.com', 'adminkedua', '8f1b8c1bb2622e1f02f15bc864d3a93a', '2019-06-08 09:23:53', 2),
(4, 'Jajang Sofian', 'jajangsummakers@yahoo.co.id', 'jajsofy0078', '6dbf55df743d02a2edd4c3928c9f7205', '2019-08-28 20:14:15', 2),
(5, 'hermansu', 'hermansu@gmail.com', 'hermansu', '81dc9bdb52d04dc20036dbd8313ed055', '0000-00-00 00:00:00', 2);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `mri_classifications_data`
--
ALTER TABLE `mri_classifications_data`
  ADD PRIMARY KEY (`MRI_id`);

--
-- Indeks untuk tabel `type_user`
--
ALTER TABLE `type_user`
  ADD PRIMARY KEY (`type_user_id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `mri_classifications_data`
--
ALTER TABLE `mri_classifications_data`
  MODIFY `MRI_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT untuk tabel `type_user`
--
ALTER TABLE `type_user`
  MODIFY `type_user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `user_id` tinyint(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
