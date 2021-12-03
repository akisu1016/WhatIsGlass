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
(9, 'ECC太郎', 'ecc@gmail.com', 'sha256$8Pdx42cZtoyQNTPg$2bb34128179cc84a7a080716cdb9188177c635f9e45e7dd0a4f748e8317da82e', null, 1), -- デフォルトのユーザー
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
(9, 1),
(9, 3),
(9, 7),
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
(9, 1),
(9, 3),
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
(1, 'brb', 1, 1),
(2, 'わろた', 2, 2),
(3, 'kewl', 2, 1),
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
(19, '台パン', 12, 2),
(20, 'Definitely', 10, 1),
(21, 'Oh dear', 9, 1),
(22, 'peace of cake', 9, 1),
(23, 'mashroom after rain', 13, 1),
(24, 'eat crow', 9, 1),
(25, 'spill the beans', 9, 1),
(26, 'when pigs fly', 11, 1),
(27, 'long story short', 9, 1),
(28, 'learn the rope', 10, 1),
(29, 'By the book', 9, 1),
(30, 'In a nutshell', 11, 1),
(31, 'Once in a blue moon', 9, 1),
(32, 'nasty', 2, 1),
(33, 'vice versa ', 9, 1),
(34, 'bucks', 10, 1),
(35, 'abs', 10, 1),
(36, 'lol', 11, 1),
(37, 'ASAP', 11, 1),
(38, 'R.I.P', 10, 1),
(39, 'Bullshit', 13, 1);

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
(1, 3),
(2, 2),
(2, 3),
(3, 2),
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
(16, 4),
(16, 5),
(16, 6),
(16, 7),
(16, 8),
(17, 10),
(18, 11),
(19, 10),
(19, 11),
(19, 13),
(23, 10),
(23, 11),
(23, 12),
(24, 2),
(24, 4),
(24, 5),
(25, 1),
(27, 3),
(28, 1),
(29, 1),
(30, 1),
(32, 2),
(32, 4),
(32, 5),
(33, 1),
(35, 3),
(36, 3),
(36, 10),
(36, 11),
(36, 12),
(36, 13);

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
(1, 1),
(1, 4),
(1, 9),
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
(19, 6),
(20, 8),
(20, 9),
(20, 4),
(21, 4),
(21, 9),
(22, 10),
(23, 8),
(23, 10),
(24, 8),
(24, 10),
(25, 8),
(25, 10),
(26, 10),
(27, 8),
(27, 9),
(28, 9),
(29, 9),
(30, 6),
(30, 8),
(30, 9),
(31, 10),
(32, 1),
(32, 4),
(32, 9),
(33, 8),
(33, 9),
(34, 1),
(34, 4),
(35, 14),
(36, 1),
(36, 4);

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
(1, 13, 1, 'brb stands for "be right back"', '', 'Informal. Only use this when talking to close friends'),
(2, 1, 2, 'indicate something is very funny', '', ''),
(3, 14, 3, 'cool', 'kewl when read out loud sounds like cool', 'This is a slang expression. You might wanna be careful when to use this.'),
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
(19, 13, 19, 'アーケードゲームなどで、主に負けた腹いせなどとして、筐体を叩くなどの行為を意味する', '', '一般的に、迷惑行為とされるほか、筐体が破損した場合には器物損壊罪の適用もありうる'),
(20, 2, 20, 'without doubt', '', ''),
(21, 2, 20, 'その通りだ！などと強く同意したい時の言葉', '', ''),
(22, 2, 20, '疑う余地もないくらい確かなこと', '', ''),
(23, 2, 21, 'synonym for "oh no"', '', 'you can also say "oh well" in similar context.'),
(24, 2, 21, 'なんてこった', '', ''),
(25, 2, 21, '「どうしましょう」の意味', '', '困ったことが起こった時に言います'),
(26, 2, 22, 'something very easy', '', ''),
(27, 2, 22, 'とても簡単なこと', '', '有名なイディオムだと思います'),
(28, 2, 23, '次々に、矢継ぎ早にといった意味', '雨が降った後にキノコが急激に育つことから', ''),
(29, 2, 24, 'to admit a humiliating error one has made', 'because crow is an unappetizing food', ''),
(30, 2, 24, '間違いを認める', '間違いを認めるのはカラスを食べるくらい苦痛を伴うことから', ''),
(31, 2, 25, 'to reveal secret information unintentionally', '', ''),
(32, 2, 25, '思いがけず秘密を漏らしてしまうこと', '', ''),
(33, 2, 26, '絶対にやりたくない、する予定は全くない', '「豚が飛ぶ時」は絶対に来ないことから', ''),
(34, 2, 27, 'to sum up', '', ''),
(35, 2, 28, 'コツを掴む', '', ''),
(36, 2, 28, '要領をつかむ', '新入りの船の乗組員が徐々にロープの結び方を覚えることから', '仕事とかでもよく使う表現ですね'),
(37, 2, 29, 'ルールに従うこと', 'ここでいうbookとはルールブックのこと', ''),
(38, 2, 30, 'explained using as few words as possible', '', ''),
(39, 2, 31, '滅多にないこと', 'ブルームーンはなかなか発生しないことから', ''),
(40, 2, 32, 'very unpleasant to see, smell or taste,', '', ''),
(41, 2, 32, '不快感がする, 汚い', '', 'dirtyよりもっときつい言い方だと思います'),
(42, 2, 33, '日本語で言う「逆もまた然り」といった意味です', '', ''),
(43, 2, 34, 'dollors', '', ''),
(44, 2, 34, 'ドル(dollor)の別の言い方', '', '主にアメリカで使う言葉だと思います'),
(45, 2, 35, '腹筋', 'abdominal musclesの略です', ''),
(46, 2, 36, '「laughing out loud」の略で日本語で言う「(笑)」みたいなものです', '', 'ネットで多用されてます'),
(47, 2, 36, 'abbreviation for laughing out loud', '', 'this word is slang'),
(48, 2, 1, 'すぐに戻るという意味です。', '', 'ネット上のチャットとかでよく見るイメージです'),
(49, 2, 1, '「be right back」の略', 'ネット用語', ''),
(50, 14, 3, 'coolのスラング的な表記', '', 'ネットスラングなのでフォーマルな場では使わない様にしましょう'),
(51, 14, 3, 'かっこいい', 'coolのスペルを崩して書いた単語ですね', ''),
(52, 2, 1, 'be right back = すぐに戻りますという意味', '', '');


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
(18, 11),
(20, 1),
(22, 1),
(22, 2),
(22, 3),
(23, 1),
(23, 2),
(23, 3),
(25, 1),
(25, 2),
(25, 3),
(25, 4),
(25, 5),
(27, 1),
(28, 1),
(28, 2),
(28, 3),
(29, 1),
(29, 2),
(30, 1),
(30, 2),
(30, 3),
(31, 1),
(33, 1),
(34, 1),
(35, 1),
(36, 1),
(36, 2),
(36, 3),
(36, 4),
(36, 5),
(41, 1),
(42, 1),
(42, 2),
(42, 3),
(44, 1),
(45, 1),
(46, 1),
(47, 1),
(47, 2),
(48, 1),
(1, 1),
(1, 2),
(1, 3),
(49, 1),
(49, 2),
(49, 3),
(50, 1),
(50, 2),
(51, 1),
(52, 1),
(52, 2),
(52, 3),
(52, 4),
(52, 5);

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
(1, 'I got a phone call, brb', 1),
(2, 'この画像面白すぎわろた', 2),
(4, 'それは流石に草', 4),
(5, '電車乗ったら変な人寝転がってて草生える', 4),
(6, 'ECCコンピュータ専門学校IT就職率100%!!??', 11),
(7, '松下玲司', 15),
(8, '３密を意識して過ごす。', 3),
(9, 'that is so kwel!', 3),
(10, 'Yes, definitely!', 20),
(11, 'This is defitely the best ice cream.', 20),
(12, 'Definitely not the best idea, but we have no other options.', 20),
(13, 'Oh dear, what do we do now.', 23),
(14, 'Oh dear, I think I''m in trouble.', 23),
(15, 'That''s a peace of cake.', 26),
(16, 'Waking up early in the morning is a peace of cake for me.', 26),
(17, 'He talks like mashrooms after rain.', 28),
(18, 'He had to eat crow when he broke the door.', 29),
(19, 'He was afraid she would spill the beans.', 31),
(20, 'It was careless of him to spill the beans.', 31),
(21, 'I will do it when pigs fly.', 33),
(22, 'I will do my homework when pigs fly!', 33),
(23, 'Long story short, I''m late for school.', 34),
(24, 'After weeks of practice, I''m finally learning the lope', 35),
(25, 'It did''t take long for him to learn the lope', 35),
(26, 'We should do this by the book', 37),
(27, 'This is how it works in a nutshell', 38),
(28, 'In a nutshell, she only wanted to make everyone happy', 38),
(29, 'Tell us about the plan in a nutshell', 38),
(30, 'I eat beef once in a blue moon', 39),
(31, 'Human can eat shark or vice versa', 42);

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

