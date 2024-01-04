-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Gen 04, 2024 alle 17:08
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_botbenzina`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `impianti`
--

CREATE TABLE `impianti` (
  `idImpianto` int(11) NOT NULL,
  `Gestore` text NOT NULL,
  `Bandiera` varchar(64) NOT NULL,
  `TipoImpianto` varchar(32) NOT NULL,
  `NomeImpianto` text NOT NULL,
  `Indirizzo` text NOT NULL,
  `Comune` varchar(64) NOT NULL,
  `Provincia` varchar(3) NOT NULL,
  `Latitudine` double NOT NULL,
  `Longitudine` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `prezzi`
--

CREATE TABLE `prezzi` (
  `idImpianto` int(11) NOT NULL,
  `tipoCarburante` varchar(32) NOT NULL,
  `prezzo` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `tipoCarburante` varchar(32) NOT NULL,
  `Consumo` int(11) NOT NULL,
  `Capienza` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `impianti`
--
ALTER TABLE `impianti`
  ADD PRIMARY KEY (`idImpianto`);

--
-- Indici per le tabelle `prezzi`
--
ALTER TABLE `prezzi`
  ADD KEY `FK1` (`idImpianto`);

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `prezzi`
--
ALTER TABLE `prezzi`
  ADD CONSTRAINT `FK1` FOREIGN KEY (`idImpianto`) REFERENCES `impianti` (`idImpianto`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
