-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : mer. 06 avr. 2022 à 21:58
-- Version du serveur :  10.3.34-MariaDB-0ubuntu0.20.04.1
-- Version de PHP : 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `laJolieBoiteACode`
--

-- --------------------------------------------------------

--
-- Structure de la table `commentaire`
--

CREATE TABLE `commentaire` (
  `id.commentaire` int(11) NOT NULL,
  `description` varchar(255) NOT NULL,
  `auteur` varchar(100) NOT NULL,
  `dateDeCreation` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `commentaire`
--

INSERT INTO `commentaire` (`id.commentaire`, `description`, `auteur`, `dateDeCreation`) VALUES
(1, 'Problème technique', 'Bernard', '2022-04-20'),
(2, 'Très bon contact', 'Le flanc', '2022-04-19');

-- --------------------------------------------------------

--
-- Structure de la table `contact`
--

CREATE TABLE `contact` (
  `idcontacct` int(11) NOT NULL,
  `nom` varchar(45) NOT NULL,
  `prenom` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `poste` varchar(45) DEFAULT NULL,
  `telephone` varchar(45) DEFAULT NULL,
  `statut` tinyint(4) DEFAULT NULL,
  `prospect_idprospect` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `contact`
--

INSERT INTO `contact` (`idcontacct`, `nom`, `prenom`, `email`, `poste`, `telephone`, `statut`, `prospect_idprospect`) VALUES
(1, 'FLANTIER', 'Bernard', 'bernard-flantier@gmail.com', 'Directeur', '0684764523', 1, 1),
(2, 'Le flanc', 'Didier', 'didier@gmail.com', 'Directeur', '0674546169', 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `facture`
--

CREATE TABLE `facture` (
  `idfacture` int(11) NOT NULL,
  `dateFacture` varchar(45) NOT NULL,
  `prospect_idprospect` int(11) NOT NULL,
  `personne_idcontact` int(11) NOT NULL,
  `NumeroFacture` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `facture`
--

INSERT INTO `facture` (`idfacture`, `dateFacture`, `prospect_idprospect`, `personne_idcontact`, `NumeroFacture`) VALUES
(1, '2022-03-30', 2, 1, '585'),
(2, '2022-04-14', 1, 1, '4');

-- --------------------------------------------------------

--
-- Structure de la table `prospect`
--

CREATE TABLE `prospect` (
  `idprospect` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `NSiret` varchar(30) NOT NULL,
  `adressePostale` varchar(255) NOT NULL,
  `codePostal` varchar(45) NOT NULL,
  `ville` varchar(45) NOT NULL,
  `description` longtext DEFAULT NULL,
  `url` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `prospect`
--

INSERT INTO `prospect` (`idprospect`, `nom`, `NSiret`, `adressePostale`, `codePostal`, `ville`, `description`, `url`) VALUES
(1, 'CAP', '25455654784576', '5 rue de la poterie', '35000', 'Rennes', 'Entreprise de construction', 'https://www.lesmaisonsguillaume.com/'),
(2, 'Decathlon', '45789562354578', 'Rue René Collin', '35000', 'Rennes', 'Vente de matériel sportifs', 'https://www.decathlon.fr/'),
(4, 'DBL', '15153532132132', '1 rue Marchand', '35000', 'Rennes', 'Entreprise de construction', 'https://www.dblconstructions.fr/');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `idutilisateur` int(11) NOT NULL,
  `login` varchar(45) NOT NULL,
  `motDePasse` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`idutilisateur`, `login`, `motDePasse`) VALUES
(1, 'axel', 'axel'),
(2, 'yohann', 'yohann');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `commentaire`
--
ALTER TABLE `commentaire`
  ADD PRIMARY KEY (`id.commentaire`);

--
-- Index pour la table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`idcontacct`),
  ADD UNIQUE KEY `idcontact_UNIQUE` (`idcontacct`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`),
  ADD KEY `fk_contact_prospect_idx` (`prospect_idprospect`);

--
-- Index pour la table `facture`
--
ALTER TABLE `facture`
  ADD PRIMARY KEY (`idfacture`),
  ADD UNIQUE KEY `idfacture_UNIQUE` (`idfacture`),
  ADD UNIQUE KEY `NumeroFacture_UNIQUE` (`NumeroFacture`),
  ADD KEY `fk_facture_prospect_idx` (`prospect_idprospect`),
  ADD KEY `fk_facture_personne_idx` (`personne_idcontact`);

--
-- Index pour la table `prospect`
--
ALTER TABLE `prospect`
  ADD PRIMARY KEY (`idprospect`),
  ADD UNIQUE KEY `idprospect_UNIQUE` (`idprospect`),
  ADD UNIQUE KEY `NSiret_UNIQUE` (`NSiret`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`idutilisateur`),
  ADD UNIQUE KEY `idutilisateur_UNIQUE` (`idutilisateur`),
  ADD UNIQUE KEY `login_UNIQUE` (`login`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `commentaire`
--
ALTER TABLE `commentaire`
  MODIFY `id.commentaire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `contact`
--
ALTER TABLE `contact`
  MODIFY `idcontacct` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `facture`
--
ALTER TABLE `facture`
  MODIFY `idfacture` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `prospect`
--
ALTER TABLE `prospect`
  MODIFY `idprospect` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `idutilisateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `contact`
--
ALTER TABLE `contact`
  ADD CONSTRAINT `fk_contact_prospect` FOREIGN KEY (`prospect_idprospect`) REFERENCES `prospect` (`idprospect`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Contraintes pour la table `facture`
--
ALTER TABLE `facture`
  ADD CONSTRAINT `fk_facture_personne` FOREIGN KEY (`personne_idcontact`) REFERENCES `contact` (`idcontacct`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_facture_prospect` FOREIGN KEY (`prospect_idprospect`) REFERENCES `prospect` (`idprospect`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
