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
  `nickname` VARCHAR(45) NULL,
  `senha` CHAR(64) NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `endereco` VARCHAR(100) NOT NULL,
  `tipo` ENUM('aluno', 'professor', 'funcionario') NOT NULL,
  `permissao` ENUM('administrador', 'bibliotecario', 'usuario') NOT NULL,
  PRIMARY KEY (`matricula`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `nickname_UNIQUE` ON `usuario` (`nickname` ASC) VISIBLE;

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
  PRIMARY KEY (`matricula`),
  CONSTRAINT `fk_aluno_usuario`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_aluno_curso1`
    FOREIGN KEY (`cod_curso`)
    REFERENCES `curso` (`cod_curso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_aluno_usuario_idx` ON `aluno` (`matricula` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_aluno_curso1_idx` ON `aluno` (`cod_curso` ASC) VISIBLE;

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
  PRIMARY KEY (`mat_siape`),
  CONSTRAINT `fk_professor_usuario1`
    FOREIGN KEY (`mat_siape`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_professor_curso1`
    FOREIGN KEY (`cod_curso`)
    REFERENCES `curso` (`cod_curso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_professor_usuario1_idx` ON `professor` (`mat_siape` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_professor_curso1_idx` ON `professor` (`cod_curso` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `funcionario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `funcionario` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `funcionario` (
  `matricula` INT NOT NULL,
  PRIMARY KEY (`matricula`),
  CONSTRAINT `fk_funcionario_usuario1`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_funcionario_usuario1_idx` ON `funcionario` (`matricula` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `telefones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `telefones` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `telefones` (
  `matricula` INT NOT NULL,
  `numero` CHAR(11) NOT NULL,
  PRIMARY KEY (`matricula`, `numero`),
  CONSTRAINT `fk_telefones_usuario1`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
  `ano` INT NOT NULL,
  `editora` VARCHAR(45) NOT NULL,
  `qt_copias` INT NOT NULL,
  `cod_categoria` INT NOT NULL,
  PRIMARY KEY (`isbn`),
  CONSTRAINT `fk_livro_categoria1`
    FOREIGN KEY (`cod_categoria`)
    REFERENCES `categoria` (`cod_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
PACK_KEYS = DEFAULT;

SHOW WARNINGS;
CREATE INDEX `fk_livro_categoria1_idx` ON `livro` (`cod_categoria` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `autor_livro`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `autor_livro` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `autor_livro` (
  `autor_cpf` CHAR(11) NOT NULL,
  `livro_isbn` CHAR(13) NOT NULL,
  PRIMARY KEY (`autor_cpf`, `livro_isbn`),
  CONSTRAINT `fk_autor_has_livro_autor1`
    FOREIGN KEY (`autor_cpf`)
    REFERENCES `autor` (`cpf`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_autor_has_livro_livro1`
    FOREIGN KEY (`livro_isbn`)
    REFERENCES `livro` (`isbn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_autor_has_livro_livro1_idx` ON `autor_livro` (`livro_isbn` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_autor_has_livro_autor1_idx` ON `autor_livro` (`autor_cpf` ASC) VISIBLE;

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
  PRIMARY KEY (`matricula`, `isbn`),
  CONSTRAINT `fk_usuario_has_livro_usuario1`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_has_livro_livro1`
    FOREIGN KEY (`isbn`)
    REFERENCES `livro` (`isbn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_usuario_has_livro_livro1_idx` ON `emprestimo` (`isbn` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_usuario_has_livro_usuario1_idx` ON `emprestimo` (`matricula` ASC) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `reserva`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reserva` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `reserva` (
  `matricula` INT NOT NULL,
  `isbn` CHAR(13) NOT NULL,
  `data_de_reserva` DATETIME NOT NULL,
  PRIMARY KEY (`matricula`, `isbn`),
  CONSTRAINT `fk_usuario_has_livro_usuario2`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_has_livro_livro2`
    FOREIGN KEY (`isbn`)
    REFERENCES `livro` (`isbn`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_usuario_has_livro_livro2_idx` ON `reserva` (`isbn` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_usuario_has_livro_usuario2_idx` ON `reserva` (`matricula` ASC) VISIBLE;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `autor`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('12345678980', 'João Antônio', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('98765432199', 'Maria do rosário', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('85296374180', 'Raimundo Antônio', 'Brasileira');

COMMIT;


-- -----------------------------------------------------
-- Data for table `usuario`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (389118, NULL, '1234', 'Samuel Hericles', 'Rua 22 de novembro - 678 - Marco', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (394192, NULL, '0101', 'Manoel Vilela', 'Rua São José - 563 - Sobral', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (385145, NULL, '8921', 'Gerônimo Aguiar', 'Rua Não sei - s/N - Itarema', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400100, 'Admin', 'root', 'Fernando', 'Rua dos Professores - s/N - Sobral', 'professor', 'administrador');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (300300, NULL, '0000', 'Germano', 'Rua dos Funcionarios', 'funcionario', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400500, NULL, '0000', 'Marcelo', 'Rua dos Professores - S/N - Sobral', 'professor', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400101, NULL, '0000', 'Francisco', 'Rua dos Professores', 'professor', 'usuario');

COMMIT;


-- -----------------------------------------------------
-- Data for table `curso`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (001, 'engenharia da computação');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (002, 'engenharia elétrica');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (003, 'psicologia');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (004, 'finanças');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (005, 'economia');

COMMIT;


-- -----------------------------------------------------
-- Data for table `aluno`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `aluno` (`matricula`, `data_de_conlusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (389118, '2021-01-01', '2016-07-01', 001);
INSERT INTO `aluno` (`matricula`, `data_de_conlusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (385145, '2021-01-01', '2016-08-02', 001);
INSERT INTO `aluno` (`matricula`, `data_de_conlusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (394192, '2021-01-01', '2016-08-16', 002);

COMMIT;


-- -----------------------------------------------------
-- Data for table `professor`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400100, '2005-10-10', 'DE', 001);
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400500, '2007-10-15', '40H', 002);
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400101, '2006-08-15', '20H', 003);

COMMIT;


-- -----------------------------------------------------
-- Data for table `funcionario`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `funcionario` (`matricula`) VALUES (300300);

COMMIT;


-- -----------------------------------------------------
-- Data for table `telefones`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (394192, '88997502676');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (385145, '88997502666');

COMMIT;


-- -----------------------------------------------------
-- Data for table `categoria`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (01, 'engenharia');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (02, 'psicologia');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (03, 'física');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (04, 'matemática');

COMMIT;


-- -----------------------------------------------------
-- Data for table `livro`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567890', 'manual SIGGA UFC', 2018, 'UFC-Sobral', 100, 02);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9788529637410', 'Guia prático de sobrevivência na universidade', 1980, 'UFC-Central', 100, 01);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567800', 'Banco de dados', 2008, 'UFC-Quixadá', 100, 03);

COMMIT;


-- -----------------------------------------------------
-- Data for table `autor_livro`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('12345678980', '9788529637410');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('98765432199', '9781234567800');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('85296374180', '9781234567800');

COMMIT;


-- -----------------------------------------------------
-- Data for table `emprestimo`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`) VALUES (400500, '9788529637410', '2018-04-20');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`) VALUES (389118, '9788529637410', '2018-03-27');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`) VALUES (394192 , '9788529637410', '2000-01-01');

COMMIT;


-- -----------------------------------------------------
-- Data for table `reserva`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`) VALUES (389118, '9788529637410', '2018-01-10');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`) VALUES (394192 , '9788529637410', '2018-12-08');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`) VALUES (385145, '9788529637410', '2018-10-12');

COMMIT;

