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
    email varchar(256) NOT NULL,
    password varchar(255) NOT NULL,
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
(0, 'English'),
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
(0, 'student'),
(0, 'office worker'),
(0, 'engineer'),
(0, 'hospitality industr'),
(0, 'medical industry'),
(0, 'financial industry'),
(0, 'primary industry'),
(0, 'child'),
(0, 'teenager'),
(0, 'adult'),
(0, 'noughty'),
(0, 'middle age'),
(0, 'elderly'),
(0, 'enthusiast'),
(0, 'athelete'),
(0, 'male'),
(0, 'female');

CREATE TABLE users_communitytags(
    user_id INT,
    community_tag_id INT,
    PRIMARY KEY(user_id, community_tag_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (community_tag_id)
        REFERENCES communitytags(id) ON DELETE CASCADE
);

INSERT INTO users_communitytags VALUES
(1, 1),
(1, 3),
(1, 17),
(2, 2),
(2, 10),
(2, 16);


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
(0, '草', 2, 2),
(0, 'hoge', 2, 1),
(0, 'Sup?', 1, 1),
(0, '三密', 2, 2),
(0, '台パン', 1, 2);

CREATE TABLE categorytags(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(30) UNIQUE NOT NULL
);

INSERT INTO categorytags VALUES
(0, 'slang'),
(0, 'formal'),
(0, 'polite'),
(0, 'casual'),
(0, 'offensive'),
(0, 'intelligent'),
(0, 'pedantic'),
(0, 'writtern language'),
(0, 'spoken language'),
(0, 'poetic'),
(0, 'proverb'),
(0, 'obsolete'),
(0, 'archaic'),
(0, 'science'),
(0, 'technical term');

CREATE TABLE indices_users_communitytags(
    index_id INT,
    user_id INT,
    PRIMARY KEY(index_id, user_id),
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
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

INSERT INTO indices_categorytags VALUES
(1, 8),
(2, 1),
(3, 1),
(4, 4),
(5, 6),
(6, 5);

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
(0, 1, 1, 'to get pleasure from something', '', ''),
(0, 1, 5, '集団感染防止のために避けるべきとされる密閉・密集・密接を指す。3つの「密」・三つの密とも表記され、一般に3密と略される。', '2020年（令和2年）の新型コロナウイルス感染症（COVID-19）拡大期に総理大臣官邸・厚生労働省が掲げた標語', '英語圏ではThree Cs・3Csとして普及'),
(0, 2, 6, 'アーケードゲームなどで、主に負けた腹いせなどとして、筐体を叩くなどの行為を意味する', '', '一般的に、迷惑行為とされるほか、筐体が破損した場合には器物損壊罪の適用もありうる'),
(0, 1, 6, 'クレーンゲームなどで景品を落とすこと', '', ''),
(0, 2, 3, 'プログラムのサンプルコードなどで、特に意味がない、何を入れてもかまわないときに使う言葉', '', ''),
(0, 1, 4, 'やぁ。最近どう？何かあった？', '', 'メールやSNS上でよく見かける表現');

CREATE TABLE answers_infomative(
    answer_id INT,
    user_id INT,
    PRIMARY KEY(answer_id , user_id),
    FOREIGN KEY (answer_id )
        REFERENCES answers(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE example_answer(
    id INT PRIMARY KEY AUTO_INCREMENT,
    example_sentence varchar(255) NOT NULL,
    answer_id INT NOT NULL,
    FOREIGN KEY (answer_id)
        REFERENCES answers(id) ON DELETE CASCADE
);

INSERT INTO example_answer VALUES
(0, 'おもしろすぎわろたwww', 1),
(0, 'We enjoyed our dinner.', 2),
(0, '３密を意識して過ごす。', 5);

CREATE TABLE favorite_indices(
    user_id INT NOT NULL,
    index_id INT NOT NULL,
    PRIMARY KEY(user_id, index_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE
);
