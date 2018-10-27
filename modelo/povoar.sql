-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema equipe385145
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `equipe385145` ;

-- -----------------------------------------------------
-- Schema equipe385145
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `equipe385145` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `equipe385145` ;

-- -----------------------------------------------------
-- Table `autor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `autor` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `autor` (
  `cpf` CHAR(11) NOT NULL,
  `nome` VARCHAR(60) NOT NULL,
  `nacionalidade` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`cpf`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuario` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `usuario` (
  `matricula` INT NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(100) NOT NULL,
  `tipo` ENUM('aluno', 'professor', 'funcionario') NOT NULL,
  `senha` CHAR(64) NOT NULL,
  `permissao` ENUM('administrador', 'bibliotecario', 'usuario') NOT NULL,
  PRIMARY KEY (`matricula`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `curso`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `curso` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `curso` (
  `cod_curso` INT NOT NULL,
  `nome_curso` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`cod_curso`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `aluno`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `aluno` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `aluno` (
  `matricula` INT NOT NULL,
  `data_de_conlusao_prevista` DATE NOT NULL,
  `data_de_ingresso` DATE NOT NULL,
  `cod_curso` INT NOT NULL,
  PRIMARY KEY (`matricula`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `professor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `professor` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `professor` (
  `mat_siape` INT NOT NULL,
  `data_de_contratacao` DATE NOT NULL,
  `regime_trabalho` ENUM('20H', '40H', 'DE') NOT NULL,
  `cod_curso` INT NOT NULL,
  PRIMARY KEY (`mat_siape`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `funcionario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `funcionario` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `funcionario` (
  `matricula` INT NOT NULL,
  PRIMARY KEY (`matricula`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `telefones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `telefones` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `telefones` (
  `matricula` INT NOT NULL,
  `numero` CHAR(11) NOT NULL,
  PRIMARY KEY (`matricula`, `numero`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `categoria` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `categoria` (
  `cod_categoria` INT NOT NULL,
  `descricao` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`cod_categoria`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `livro`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `livro` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `livro` (
  `isbn` CHAR(13) NOT NULL,
  `titulo` VARCHAR(100) NOT NULL,
  `ano` YEAR(4) NOT NULL,
  `editora` VARCHAR(45) NOT NULL,
  `qt_copias` INT NOT NULL,
  `cod_categoria` INT NOT NULL,
  PRIMARY KEY (`isbn`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `autor_livro`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `autor_livro` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `autor_livro` (
  `autor_cpf` CHAR(11) NOT NULL,
  `livro_isbn` CHAR(13) NOT NULL,
  PRIMARY KEY (`autor_cpf`, `livro_isbn`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `emprestimo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `emprestimo` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `emprestimo` (
  `matricula` INT NOT NULL,
  `isbn` CHAR(13) NOT NULL,
  `data_de_emprestimo` DATETIME NOT NULL,
  PRIMARY KEY (`matricula`, `isbn`))
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reserva`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reserva` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reserva` (
  `matricula` INT NOT NULL,
  `isbn` CHAR(13) NOT NULL,
  `data_de_reserva` DATETIME NULL,
  PRIMARY KEY (`matricula`, `isbn`))
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
