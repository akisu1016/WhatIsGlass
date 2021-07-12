-- テーブルの初期化 --
DROP DATABASE IF EXISTS WhatIsGrass;
CREATE DATABASE WhatIsGrass;
USE WhatIsGrass;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS users_languages;
DROP TABLE IF EXISTS communitytags;
DROP TABLE IF EXISTS users_communitytags;
DROP TABLE IF EXISTS indices;
DROP TABLE IF EXISTS categorytags;
DROP TABLE IF EXISTS indices_communitytags_count;
DROP TABLE IF EXISTS indices_categorytags;
DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS example_answer;
DROP TABLE IF EXISTS favorite_indices;


CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    email varchar(254) NOT NULL,
    password varchar(254) NOT NULL,
    icon varchar(300)
);

INSERT INTO users VALUES
(0, '英語太郎', 'English@gmail.com', 'english', 'iconpath/english'),
(0, '日本太郎', 'japanese@gmail.com', 'japanese', null);

CREATE TABLE languages(
    id INT PRIMARY KEY AUTO_INCREMENT,
    language varchar(20) UNIQUE KEY NOT NULL
);

INSERT INTO languages VALUES
(0, '英語'),
(0, '日本語');

CREATE TABLE users_languages(
    user_id INT,
    language_id INT,
    PRIMARY KEY(user_id, language_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id)
        REFERENCES languages(id) ON DELETE CASCADE
);

INSERT INTO users_languages VALUES
(1, 1),
(2, 2);

CREATE TABLE communitytags(
    id INT PRIMARY KEY AUTO_INCREMENT,
    `name` varchar(30) UNIQUE NOT NULL
);

INSERT INTO communitytags VALUES
(0, '社会人'),
(0, '学生');

CREATE TABLE users_communitytags(
    user_id INT,
    community_tag_id INT,
    PRIMARY KEY(user_id, community_tag_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (community_tag_id)
        REFERENCES communitytags(id) ON DELETE CASCADE
);


CREATE TABLE indices(
    id INT PRIMARY KEY AUTO_INCREMENT,
    `index` varchar(50) NOT NULL,
    questioner INT NOT NULL,
    language_id INT NOT NULL,
    frequently_used_count INT NOT NULL default 0,
    `date` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (questioner)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id)
        REFERENCES languages(id) ON DELETE CASCADE
);

INSERT INTO indices(id, `index`, questioner, language_id) VALUES
(0, 'enjoy', 1, 1),
(0, '草', 2, 2);

CREATE TABLE categorytags(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(30) UNIQUE NOT NULL
);

INSERT INTO categorytags VALUES
(0, '一般英語'),
(0, '一般日本語');

CREATE TABLE indices_communitytags_count(
    index_id INT,
    community_tag_id INT,
    count INT NOT NULL default 0,
    PRIMARY KEY(index_id, community_tag_id),
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE,
    FOREIGN KEY (community_tag_id)
        REFERENCES communitytags(id) ON DELETE CASCADE
);

CREATE TABLE indices_categorytags(
    index_id INT,
    category_tag_id INT,
    PRIMARY KEY(index_id, category_tag_id),
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE,
    FOREIGN KEY (category_tag_id)
        REFERENCES categorytags(id) ON DELETE CASCADE
);

CREATE TABLE answers(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    index_id INT NOT NULL,
    `definition` varchar(100) NOT NULL,
    origin varchar(300),
    note varchar(200),
    informative_count INT NOT NULL default 0,
    `date` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE
);

INSERT INTO answers(id, user_id, index_id, `definition`, origin, note) VALUES
(0, 2, 2, '葉っぱ、おもろい', 'わからんてぃうす', 'いっぱい意味あるよ'),
(0, 1, 1, 'to get pleasure from something', '', '');

CREATE TABLE example_answer(
    id INT PRIMARY KEY AUTO_INCREMENT,
    example_sentence varchar(200) NOT NULL,
    answer_id INT NOT NULL,
    FOREIGN KEY (answer_id)
        REFERENCES answers(id) ON DELETE CASCADE
);

INSERT INTO example_answer VALUES
(0, 'おもしろすぎわろたwww', 1),
(0, 'We enjoyed our dinner.', 2);

CREATE TABLE favorite_indices(
    user_id INT NOT NULL,
    index_id INT NOT NULL,
    PRIMARY KEY(user_id, index_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE
);
