CREATE DATABASE IF NOT EXISTS ob_imobiliaria_db;

USE ob_imobiliaria_db;

CREATE TABLE IF NOT EXISTS casa_feliz_imobiliaria (
    id INT AUTO_INCREMENT PRIMARY KEY,
	codigo VARCHAR(255) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    preco DECIMAL(10, 2),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    qtde_quartos INT,
    qtde_banheiros INT,
    qtde_vagas INT,
    qtde_suite INT,
    area_total_m2 DECIMAL(10, 2),
    area_privativa DECIMAL(10, 2),
    data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=INNODB;

