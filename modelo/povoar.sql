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
  `nickname` VARCHAR(45) BINARY NULL,
  `senha_hash` CHAR(64) NOT NULL,
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
  `data_de_conclusao_prevista` DATE NOT NULL,
  `data_de_ingresso` DATE NOT NULL,
  `cod_curso` INT NOT NULL,
  PRIMARY KEY (`matricula`),
  CONSTRAINT `fk_aluno_usuario`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_aluno_curso1`
    FOREIGN KEY (`cod_curso`)
    REFERENCES `curso` (`cod_curso`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
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
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_professor_curso1`
    FOREIGN KEY (`cod_curso`)
    REFERENCES `curso` (`cod_curso`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE)
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
    ON DELETE CASCADE
    ON UPDATE CASCADE)
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
    ON DELETE CASCADE
    ON UPDATE CASCADE)
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
    ON UPDATE CASCADE)
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
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_autor_has_livro_livro1`
    FOREIGN KEY (`livro_isbn`)
    REFERENCES `livro` (`isbn`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
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
  `data_de_emprestimo` DATE NOT NULL,
  `data_de_devolucao` DATE NOT NULL,
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
    ON UPDATE CASCADE)
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
  `data_contemplado` DATETIME NULL,
  PRIMARY KEY (`matricula`, `isbn`),
  CONSTRAINT `fk_usuario_has_livro_usuario2`
    FOREIGN KEY (`matricula`)
    REFERENCES `usuario` (`matricula`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_usuario_has_livro_livro2`
    FOREIGN KEY (`isbn`)
    REFERENCES `livro` (`isbn`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_usuario_has_livro_livro2_idx` ON `reserva` (`isbn` ASC) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_usuario_has_livro_usuario2_idx` ON `reserva` (`matricula` ASC) VISIBLE;

SHOW WARNINGS;
USE `equipe385145` ;

-- -----------------------------------------------------
-- View `view_professor_curso`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `view_professor_curso` ;
SHOW WARNINGS;
USE `equipe385145`;
CREATE 
     OR REPLACE ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `view_professor_curso` AS
    SELECT 
        `usuario`.`nome` AS `nome`,
        `curso`.`nome_curso` AS `nome_curso`
    FROM
        ((`professor`
        JOIN `curso` ON ((`professor`.`cod_curso` = `curso`.`cod_curso`)))
        JOIN `usuario` ON ((`professor`.`mat_siape` = `usuario`.`matricula`)))
    ORDER BY `usuario`.`nome`;
SHOW WARNINGS;

-- -----------------------------------------------------
-- View `view_livro_categoria`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `view_livro_categoria` ;
SHOW WARNINGS;
USE `equipe385145`;
CREATE  OR REPLACE VIEW view_livro_categoria AS
SELECT titulo, descricao as nome_categoria
FROM livro
NATURAL JOIN categoria
ORDER BY descricao;
SHOW WARNINGS;

-- -----------------------------------------------------
-- View `view_livro_ano`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `view_livro_ano` ;
SHOW WARNINGS;
USE `equipe385145`;
CREATE  OR REPLACE VIEW view_livro_ano AS
SELECT titulo, ano
FROM livro
ORDER BY ano;
SHOW WARNINGS;

-- -----------------------------------------------------
-- View `view_livro_editora`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `view_livro_editora` ;
SHOW WARNINGS;
USE `equipe385145`;
CREATE  OR REPLACE VIEW view_livro_editora AS
SELECT titulo, editora
FROM livro
ORDER BY editora;
SHOW WARNINGS;

-- -----------------------------------------------------
-- View `view_livro_autores`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `view_livro_autores` ;
SHOW WARNINGS;
USE `equipe385145`;
CREATE  OR REPLACE VIEW view_livro_autores AS
SELECT 
  titulo, 
  GROUP_CONCAT(nome ORDER BY nome SEPARATOR ', ') as autores 
FROM autor_livro 
JOIN livro ON isbn=livro_isbn 
JOIN autor ON autor_cpf=cpf 
GROUP BY isbn;
SHOW WARNINGS;

-- -----------------------------------------------------
-- View `view_reserva_livro`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `view_reserva_livro` ;
SHOW WARNINGS;
USE `equipe385145`;
CREATE  OR REPLACE VIEW view_reserva_livro AS
SELECT isbn, titulo, nome as nome_usuario, data_de_reserva, data_contemplado
FROM reserva
NATURAL JOIN livro
NATURAL JOIN usuario
ORDER BY titulo, data_de_reserva;
SHOW WARNINGS;
USE `equipe385145`;

DELIMITER $$

USE `equipe385145`$$
DROP TRIGGER IF EXISTS `trg_2` $$
SHOW WARNINGS$$
USE `equipe385145`$$
CREATE DEFINER = CURRENT_USER TRIGGER trg_2
  BEFORE DELETE ON equipe385145.usuario
  FOR EACH ROW
BEGIN  
    DECLARE msg VARCHAR(128);    
    IF (SELECT count(*) FROM usuario WHERE permissao='administrador')=1 THEN
        SET msg = concat('Deve existir ao menos um administrador. Não é possível apagar o último.');
        SIGNAL SQLSTATE'45000' SET message_text = msg;        
  END IF; 
END$$

SHOW WARNINGS$$

USE `equipe385145`$$
DROP TRIGGER IF EXISTS `trg_1` $$
SHOW WARNINGS$$
USE `equipe385145`$$
CREATE DEFINER = CURRENT_USER TRIGGER trg_1
	BEFORE INSERT ON equipe385145.aluno 
	FOR EACH ROW
   
BEGIN
	
    DECLARE msg VARCHAR(128);    
    
    IF NEW.data_de_conclusao_prevista < now() THEN
        SET msg = concat('Pela a data de conclusão, você deve está formando.');
        SIGNAL SQLSTATE'45000' SET message_text = msg;
	END IF; 
        IF NEW.data_de_conclusao_prevista < NEW.data_de_ingresso THEN
        SET msg = concat('Data de conclusão menor que a data de ingresso.');
        SIGNAL SQLSTATE'45000' SET message_text = msg;
	END IF; 

END$$

SHOW WARNINGS$$

DELIMITER ;

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
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('85296374810', 'Aldous Huxley', 'Alemã');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('25896374180', 'Paulo Freire', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('85296743180', 'Pedro Bandeira', 'Italina');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('89746516516', 'Miguel de Cervantes', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('12341361697', 'Robert T Kiyosaki', 'Russo');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('12442534313', 'Pierre Clastres', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('13461134151', 'Alcida Rita Ramos', 'Americana');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('12364145234', 'Florestan Fernandes', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('89852568543', 'Sun Tzu', 'Sul Coreano');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('55826365326', 'Holanda', 'Brasileira');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('84825393938', 'Darcy Ribeirp', 'Sul Africano');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('63634635433', 'Hal Elrod', 'Argentino');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('34934348354', 'Eckhart Tolle', 'Sul Coreano');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('43643243236', 'Daniel Kahneman', 'Argentino');
INSERT INTO `autor` (`cpf`, `nome`, `nacionalidade`) VALUES ('33634654534', 'Mark Manson', 'Americana');

COMMIT;


-- -----------------------------------------------------
-- Data for table `usuario`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (389118, 'Samuel', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'Samuel Hericles', 'Rua 22 de novembro - 678 - Marco', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (394192, 'Manoel', '07334386287751ba02a4588c1a0875dbd074a61bd9e6ab7c48d244eacd0c99e0', 'Manoel Vilela', 'Rua São José - 563 - Sobral', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (385145, 'Geronimo', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Gerônimo Aguiar', 'Rua Não sei - s/N - Itarema', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400500, 'Admin', '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2', 'Fernando', 'Rua dos Professores - s/N - Sobral', 'professor', 'administrador');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (300300, 'Germano', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Germano', 'Rua dos Funcionarios', 'funcionario', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400501, 'NULL', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Marcelo', 'Rua dos Professores - S/N - Sobral', 'professor', 'administrador');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400502, 'Francisco', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Francisco', 'Rua dos Professores', 'professor', 'administrador');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (389001, 'Aluno02', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Aluno02', 'Rua Nova dos Alunos', 'aluno', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (389002, 'Aluno03', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Aluno03', 'Av. dos Alunos', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (389003, 'Aluno04', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Aluno04', 'Rua dos Alunos', 'aluno', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (389004, 'Aluno05', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Aluno05', 'Rua Nova dos Alunos', 'aluno', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400503, 'Professor01', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Professor01', 'Rua Nova dos Professores', 'professor', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (400504, 'Professor02', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Professor02', 'Av. dos Professores', 'professor', 'usuario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (300301, 'Funcionario01', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Funcionário01', 'Rua dos Funcionarios', 'funcionario', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (300302, 'Funcionario02', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Funcionário02', 'Rua Nova dos Funcionarios', 'funcionario', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (300303, 'Funcionario03', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Funcionário03', 'Av. dos Funcionairos', 'funcionario', 'bibliotecario');
INSERT INTO `usuario` (`matricula`, `nickname`, `senha_hash`, `nome`, `endereco`, `tipo`, `permissao`) VALUES (300304, 'Funcionario04', '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0', 'Funcionário04', 'Rua dos Funcionarios', 'funcionario', 'usuario');

COMMIT;


-- -----------------------------------------------------
-- Data for table `curso`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (001, 'Engenharia da Computação');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (002, 'Engenharia Elétrica');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (003, 'Psicologia');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (004, 'Finanças');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (005, 'Economia');
INSERT INTO `curso` (`cod_curso`, `nome_curso`) VALUES (006, 'Medicina');

COMMIT;


-- -----------------------------------------------------
-- Data for table `aluno`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `aluno` (`matricula`, `data_de_conclusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (389118, '2021-01-01', '2016-07-01', 001);
INSERT INTO `aluno` (`matricula`, `data_de_conclusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (385145, '2021-01-01', '2016-08-02', 001);
INSERT INTO `aluno` (`matricula`, `data_de_conclusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (394192, '2021-01-01', '2016-08-16', 001);
INSERT INTO `aluno` (`matricula`, `data_de_conclusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (389001, '2020-01-01', '2015-05-04', 002);
INSERT INTO `aluno` (`matricula`, `data_de_conclusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (389002, '2019-01-01', '2016-08-01', 005);
INSERT INTO `aluno` (`matricula`, `data_de_conclusao_prevista`, `data_de_ingresso`, `cod_curso`) VALUES (389003, '2024-01-01', '2019-12-12', 005);

COMMIT;


-- -----------------------------------------------------
-- Data for table `professor`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400500, '2007-10-15', '40H', 002);
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400501, '2006-08-14', 'DE', 004);
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400502, '2006-08-13', '40H', 005);
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400503, '2006-08-12', '20H', 006);
INSERT INTO `professor` (`mat_siape`, `data_de_contratacao`, `regime_trabalho`, `cod_curso`) VALUES (400504, '2006-08-12', 'DE', 006);

COMMIT;


-- -----------------------------------------------------
-- Data for table `funcionario`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `funcionario` (`matricula`) VALUES (300300);
INSERT INTO `funcionario` (`matricula`) VALUES (300301);
INSERT INTO `funcionario` (`matricula`) VALUES (300302);
INSERT INTO `funcionario` (`matricula`) VALUES (300303);
INSERT INTO `funcionario` (`matricula`) VALUES (300304);

COMMIT;


-- -----------------------------------------------------
-- Data for table `telefones`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (394192, '88997502674');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (385145, '88997502675');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (389118, '88997502676');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (389001, '88997502677');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (389002, '88997502678');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (389003, '88997502679');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (389003, '88997502683');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (400500, '88997502692');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (400501, '88997502693');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (400502, '88997502694');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (400503, '88997502695');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (400504, '88997502696');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (300300, '88997502726');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (300301, '88997502727');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (300302, '88997502728');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (300303, '88997502729');
INSERT INTO `telefones` (`matricula`, `numero`) VALUES (300304, '88997502730');

COMMIT;


-- -----------------------------------------------------
-- Data for table `categoria`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (01, 'Engenharia');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (02, 'Psicologia');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (03, 'Física');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (04, 'Matemática');
INSERT INTO `categoria` (`cod_categoria`, `descricao`) VALUES (05, 'Social');

COMMIT;


-- -----------------------------------------------------
-- Data for table `livro`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567890', 'Manual SIGAA UFC', 2018, 'UFC-Sobral', 10, 01);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9788529637410', 'Guia prático de sobrevivência na universidade', 1980, 'UFC-Central', 10, 02);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567800', 'Banco de dados', 2008, 'UFC-Quixadá', 10, 01);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567801', 'A Droga da obediência', 2007, 'Moderna', 8, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567802', 'Pedagogia da Autonomia', 2006, 'Paz Terra', 9, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567803', 'Admirável mundo novo', 2005, 'GlobodeBolso', 7, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567804', 'Dom Quixote ', 2004, 'Scipione', 6, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567805', 'A arte da guerra', 2003, 'Paz Terra', 3, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567806', 'Comunicação não-violenta', 2002, 'Summus', 2, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567807', 'O negro no mundo dos brancos ', 2001, 'Global Editora', 1, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567808', 'Cultura em movimento', 2000, 'Selo Negro', 2, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567809', 'O Poder do agora', 2000, 'Sextante', 8, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567810', 'Inferno somo nós', 2001, '7 Mares', 5, 05);
INSERT INTO `livro` (`isbn`, `titulo`, `ano`, `editora`, `qt_copias`, `cod_categoria`) VALUES ('9781234567811', 'Rápido e devagar: Duas formas de Pensar', 2004, 'Objetiva', 8, 05);

COMMIT;


-- -----------------------------------------------------
-- Data for table `autor_livro`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('12345678980', '9788529637410');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('98765432199', '9781234567800');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('25896374180', '9781234567800');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('12341361697', '9781234567802');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('89746516516', '9781234567803');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('12341361697', '9781234567806');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('89746516516', '9781234567807');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('12442534313', '9781234567808');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('89746516516', '9781234567802');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('34934348354', '9781234567803');
INSERT INTO `autor_livro` (`autor_cpf`, `livro_isbn`) VALUES ('34934348354', '9781234567802');

COMMIT;


-- -----------------------------------------------------
-- Data for table `emprestimo`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (400500, '9788529637410', '2018-04-01', '2018-05-01');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (389118, '9788529637410', '2018-03-01', '2018-03-16');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (394192 , '9788529637410', '2000-01-01', '2000-01-16');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (400501, '9781234567802', '2018-08-01', '2018-08-16');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (400502, '9781234567803', '2018-11-01', '2018-11-16');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (400503, '9781234567804', '2018-11-02', '2018-11-17');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (300301, '9781234567805', '2018-11-03', '2018-11-18');
INSERT INTO `emprestimo` (`matricula`, `isbn`, `data_de_emprestimo`, `data_de_devolucao`) VALUES (300302, '9781234567806', '2018-11-04', '2018-11-19');

COMMIT;


-- -----------------------------------------------------
-- Data for table `reserva`
-- -----------------------------------------------------
START TRANSACTION;
USE `equipe385145`;
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (389118, '9788529637410', '2018-01-10', '2018-01-25');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (394192 , '9788529637410', '2018-12-08', '2018-12-10');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (385145, '9788529637410', '2018-10-12', '2018-10-27');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (400500, '9781234567802', '2018-12-12', '2018-12-27');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (300300, '9781234567802', '2018-12-01', '2018-12-16');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (400501, '9781234567803', '2018-01-01', '2018-01-16');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (300301, '9781234567804', '2018-02-02', '2018-02-18');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (400502, '9781234567805', '2018-03-03', '2018-03-19');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (300302, '9781234567808', '2018-04-04', '2018-04-20');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (400503, '9781234567808', '2018-05-05', '2018-05-21');
INSERT INTO `reserva` (`matricula`, `isbn`, `data_de_reserva`, `data_contemplado`) VALUES (300303, '9781234567809', '2018-06-06', '2018-06-22');

COMMIT;

