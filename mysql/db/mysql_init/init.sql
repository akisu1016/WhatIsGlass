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
    icon varchar(300),
    answer_filter INT default 2
);

INSERT INTO users VALUES
(1, 'テスト太郎', 'test@gmail.com', 'pass_japanese', null, 2),
(2, '英語太郎', 'English@gmail.com', 'pass_english', 'iconpath/english', 1),
(3, '日本太郎', 'japanese@gmail.com', 'pass_japanese', null, 2),
(4, '中国太郎', 'chinese@gmail.com', 'pass_chinese', null, 3),
(5, '韓国太郎', 'korean@gmail.com', 'pass_korean', null, 4),
(6, 'イタリア太郎', 'italian@gmail.com', 'pass_italian', null, 5),
(7, 'フランス太郎', 'french@gmail.com', 'pass_french', null, 6),
(8, 'スペイン太郎', 'spanish@gmail.com', 'pass_spanish', null, 7),
(9, 'ECC太郎', 'ecc@gmail.com', 'pass_ecc', null, 1),
(10, '芝山友章', 'shibayama@gmail.com', 'pass_shibayama', null, 2),
(11, '愛宕和也', 'atago@gmail.com', 'pass_atago', null, 2),
(12, '于文博', 'u@gmail.com', 'pass_u', null, 3),
(13, '松下玲司', 'matsushita@gmail.com', 'pass_matsushita', null, 2),
(14, 'ハイブリッド太郎', 'hybrid@gmail.com', 'pass_hybrid', null, 1);


CREATE TABLE languages(
    id INT PRIMARY KEY AUTO_INCREMENT,
    language varchar(20) UNIQUE KEY NOT NULL
);

INSERT INTO languages VALUES
(1, 'English'),
(2, '日本語'),
(3, '简体中文'),
(4, '한국어'),
(5, 'Italiano'),
(6, 'Français'),
(7, 'Español');

CREATE TABLE user_first_languages(
    user_id INT,
    language_id INT,
    PRIMARY KEY(user_id, language_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id)
        REFERENCES languages(id) ON DELETE CASCADE
);

INSERT INTO user_first_languages VALUES
(1, 2),
(2, 1),
(3, 2),
(4, 3),
(5, 4),
(6, 5),
(7, 6),
(8, 1),
(9, 2),
(10, 2),
(11, 2),
(12, 3),
(13, 2),
(14, 1);

CREATE TABLE user_second_languages(
    user_id INT,
    language_id INT,
    PRIMARY KEY(user_id, language_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id)
        REFERENCES languages(id) ON DELETE CASCADE
);

INSERT INTO user_second_languages VALUES
(10, 1),
(11, 1),
(12, 2),
(13, 1),
(14, 2);

CREATE TABLE communitytags(
    id INT PRIMARY KEY AUTO_INCREMENT,
    `name` varchar(30) UNIQUE NOT NULL
);

INSERT INTO communitytags VALUES
(1, 'student'),
(2, 'office worker'),
(3, 'engineer'),
(4, 'hospitality industry'),
(5, 'medical industry'),
(6, 'financial industry'),
(7, 'primary industry'),
(8, 'child'),
(9, 'teenager'),
(10, 'adult'),
(11, 'naughty'),
(12, 'middle age'),
(13, 'elderly'),
(14, 'enthusiast'),
(15, 'athelete'),
(16, 'male'),
(17, 'female');


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
(1, 3),
(1, 17),
(2, 14),
(2, 16),
(3, 9),
(3, 17),
(4, 10),
(4, 16),
(5, 11),
(5, 16),
(6, 12),
(6, 17),
(7, 13),
(7, 16),
(8, 8),
(8, 17),
(9, 9),
(9, 16),
(10, 1),
(10, 10),
(10, 16),
(11, 1),
(11, 10),
(11, 16),
(12, 1),
(12, 10),
(12, 16),
(13, 1),
(13, 10),
(13, 16),
(14, 2),
(14, 10),
(14, 15),
(14, 17);



CREATE TABLE indices(
    id INT PRIMARY KEY AUTO_INCREMENT,
    `index` varchar(50) NOT NULL,
    questioner INT NOT NULL,
    language_id INT NOT NULL,
    `date` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (questioner)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id)
        REFERENCES languages(id) ON DELETE CASCADE
);

INSERT INTO indices(id, `index`, questioner, language_id) VALUES
(1, 'test', 1, 1),
(2, 'enjoy', 2, 1),
(3, 'stand', 2, 1),
(4, '草', 3, 2),
(5, 'なんでやねん', 3, 2),
(6, '乐趣', 4, 3),
(7, '재미', 5, 4),
(8, 'divertimento', 6, 5),
(9, 'amusant', 7, 6),
(10, 'divertida', 8, 7),
(11, 'ecc', 9, 1),
(12, '芝', 10, 2),
(13, 'スラング', 11, 2),
(14, 'hoge', 12, 2),
(15, '松', 13, 2),
(16, 'hybrid', 14, 1),
(17, 'Sup?', 10, 1),
(18, '三密', 11, 2),
(19, '台パン', 12, 2);

CREATE TABLE indices_users_communitytags(
    index_id INT,
    user_id INT,
    PRIMARY KEY(index_id, user_id),
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO indices_users_communitytags VALUES
(1, 1),
(1, 2),
(2, 2),
(2, 3),
(3, 2),
(3, 1),
(4, 3),
(5, 3),
(6, 4),
(7, 5),
(8, 6),
(9, 7),
(10, 8),
(11, 9),
(12, 11),
(12, 12),
(12, 13),
(13, 10),
(13, 12),
(13, 13),
(14, 10),
(14, 11),
(14, 13),
(15, 10),
(15, 11),
(15, 12),
(16, 14),
(16, 2),
(16, 3),
(16, 4),
(16, 5),
(16, 6),
(16, 7),
(16, 8),
(17, 10),
(18, 11),
(19, 10),
(19, 11),
(19, 13);

CREATE TABLE categorytags(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(30) UNIQUE NOT NULL
);

INSERT INTO categorytags VALUES
(1, 'slang'),
(2, 'formal'),
(3, 'polite'),
(4, 'casual'),
(5, 'offensive'),
(6, 'intelligent'),
(7, 'pedantic'),
(8, 'writtern language'),
(9, 'spoken language'),
(10, 'poetic'),
(11, 'proverb'),
(12, 'obsolete'),
(13, 'archaic'),
(14, 'science'),
(15, 'technical term');


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
(2, 9),
(3, 1),
(4, 1),
(5, 8),
(6, 8),
(7, 8),
(8, 8),
(9, 8),
(10, 8),
(11, 15),
(12, 2),
(13, 3),
(14, 4),
(15, 5),
(16, 6),
(17, 1),
(18, 4),
(19, 6);


CREATE TABLE answers(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    index_id INT NOT NULL,
    `definition` varchar(400) NOT NULL,
    origin varchar(300),
    note varchar(200),
    relevance INT NOT NULL default 30,
    `date` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE
);

INSERT INTO answers(id, user_id, index_id, `definition`, origin, note) VALUES
(1, 13, 1, 'お試し', 'わからん', 'テスト用だよ'),
(2, 1, 2, 'to get pleasure from something', '', ''),
(3, 14, 3, '立つ', '', ''),
(4, 3, 4, '葉っぱ、おもろい', 'わからんてぃうす', 'いっぱい意味あるよ'),
(5, 2, 5, 'なぜなのやの転', '', '大阪の方言かも'),
(6, 2, 6, 'enjoy', '', ''),
(7, 2, 7, 'enjoy', '', ''),
(8, 2, 8, 'enjoy', '', ''),
(9, 2, 9, 'enjoy', '', ''),
(10, 2, 10, 'enjoy', '', ''),
(11, 10, 11, '総合教育・生涯学習機関', '', 'いろんな種類の学校などがありますね'),
(12, 11, 12, '野原に自生する、いね科の多年生植物', '', '日当たりがいいと密です'),
(13, 12, 13, 'language of an informal register', '', ''),
(14, 13, 14, 'プログラムのサンプルコードなどで、特に意味がない、何を入れてもかまわないときに使う言葉', '', ''),
(15, 9, 15, 'まつ科の常緑樹の総称', '葉がまつ毛に似ているところから、まつ毛の「まつ」とする', '苗字でよくみますねぇ'),
(16, 10, 16, 'a plant or animal that has been produced from two different types of plant or animal, especially to get better characteristics', '', ''),
(17, 11, 17, 'やぁ。最近どう？何かあった？', '', 'メールやSNS上でよく見かける表現'),
(18, 12, 18, '集団感染防止のために避けるべきとされる密閉・密集・密接を指す。3つの「密」・三つの密とも表記され、一般に3密と略される。', '2020年（令和2年）の新型コロナウイルス感染症（COVID-19）拡大期に総理大臣官邸・厚生労働省が掲げた標語', '英語圏ではThree Cs・3Csとして普及'),
(19, 13, 19, 'アーケードゲームなどで、主に負けた腹いせなどとして、筐体を叩くなどの行為を意味する', '', '一般的に、迷惑行為とされるほか、筐体が破損した場合には器物損壊罪の適用もありうる');


CREATE TABLE answers_informative(
    answer_id INT,
    user_id INT,
    PRIMARY KEY(answer_id , user_id),
    FOREIGN KEY (answer_id )
        REFERENCES answers(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO answers_informative VALUES
(1, 2),
(4, 3),
(4, 5),
(11, 10),
(11, 11),
(11, 12),
(11, 13),
(13, 10),
(14, 2),
(14, 3),
(14, 4),
(14, 5),
(14, 6),
(14, 7),
(18, 10),
(18, 11);

CREATE TABLE answers_relevance(
    answer_id INT,
    user_id INT,
    PRIMARY KEY(answer_id , user_id),
    FOREIGN KEY (answer_id )
        REFERENCES answers(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO answers_relevance VALUES
(6, 9),
(7, 9),
(8, 9),
(9, 9),
(10, 9);

CREATE TABLE example_answer(
    id INT PRIMARY KEY AUTO_INCREMENT,
    example_sentence varchar(255) NOT NULL,
    answer_id INT NOT NULL,
    FOREIGN KEY (answer_id)
        REFERENCES answers(id) ON DELETE CASCADE
);

INSERT INTO example_answer VALUES
(1, 'これはtestです', 1),
(2, 'We enjoyed our dinner.', 2),
(4, '流石に草wwwww', 4),
(5, '草が生えるね', 4),
(6, 'ECCコンピュータ専門学校IT就職率100%!!??', 11),
(7, '松下玲司', 15),
(8, '３密を意識して過ごす。', 18);

CREATE TABLE favorite_indices(
    user_id INT NOT NULL,
    index_id INT NOT NULL,
    PRIMARY KEY(user_id, index_id),
    FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (index_id)
        REFERENCES indices(id) ON DELETE CASCADE
);

INSERT INTO favorite_indices VALUES
(1, 2),
(1, 3),
(2, 1),
(2, 16),
(2, 17),
(3, 4),
(10, 11),
(11, 11),
(12, 11),
(13, 11),
(14, 11),
(14, 12),
(14, 13),
(14, 14),
(14, 15); 

