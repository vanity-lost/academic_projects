
create table if not exists Location_on_Campus (
	building_name  character varying,
	region_on_campus character varying,
	open_time TIME,
	close_time TIME,
	floor_number integer,
	primary key(building_name)
);

create table if not exists Vending_Machine (
	v_id SERIAL,
	building_name character varying, 
	capacity integer,
	last_filled date,
	isAvailable boolean,
	hasCaseCase boolean,
	hasCreditCard boolean,
	hasCash boolean, 
	primary key(v_id),
	foreign key(building_name) REFERENCES Location_on_Campus
);

create table if not exists Snacks(
	s_id SERIAL,
	v_id integer,  
	s_name character varying NOT NULL,
	Price Money NOT NULL,	
    IsSweet Boolean,
 	IsSalty Boolean,
	IsDrink Boolean,
	Expiration_date Date  NOT NULL ,
	isAvailable Boolean  NOT NULL,
	Primary key (s_id),
 	foreign key(v_id) REFERENCES Vending_Machine 

);

create table if not exists Vending_Review (
	vreview_id SERIAL,
	v_id integer , 
	score integer,
	viewer_comments text,
	primary key(vreview_id),
  	foreign key(v_id) REFERENCES Vending_Machine  
);

create table if not exists Snack_Review (
	sreview_id SERIAL,
	s_id integer,
	score integer,
	viewer_comments text,
	primary key(sreview_id),
	foreign key(s_id) REFERENCES Snacks 

);


create table if not exists Nutrition (
	s_id integer ,
	calories integer,
	allergy_warns character varying,
	sugars integer,
	caffeine boolean,
	primary key(s_id),
	foreign key(s_id) REFERENCES Snacks 

);

create table if not exists Staff (
	SSN CHAR(11),
	company_name character varying,
	primary key(SSN)
);

create table if not exists Refills (
	SSN CHAR(11),
	r_id SERIAL, 
	s_id integer,
	date_refill DATE,
	quantity_refill integer,
	primary key(r_id),
	foreign key(SSN) REFERENCES Staff,
	foreign key(s_id) REFERENCES Snacks 
	
);

-- --inserting location on campus: buildingname, regiononcampus, opentime, closetime, floornumber, 
INSERT INTO Location_on_Campus VALUES ('Crawford Hall', 'Main Quad','08:00:00','18:00:00','1');
INSERT INTO Location_on_Campus VALUES ('KSL', 'Mather Quad','00:00:00','24:00:00','2');
INSERT INTO Location_on_Campus VALUES ('Sears Library', 'Main Quad','08:00:00','19:00:00','3');
INSERT INTO Location_on_Campus VALUES ('Nord Hall', 'Main Quad','08:00:00','19:00:00','3');
INSERT INTO Location_on_Campus VALUES ('Rockefeller Building', 'Main Quad','08:00:00','19:00:00','1');

--inserting vending machines:        vid building name, capacity, lastfilleddate, is avilabel, casecash, creidt, cash
INSERT INTO Vending_Machine VALUES (DEFAULT,'Crawford Hall','80','2019-09-11','true','true','true','true') ;
INSERT INTO Vending_Machine VALUES (DEFAULT,'Crawford Hall','80','2019-10-11','true','true','true','true') ;
INSERT INTO Vending_Machine VALUES (DEFAULT,'KSL',          '50','2019-10-11','true','true','true','true') ;
INSERT INTO Vending_Machine VALUES (DEFAULT,'KSL',          '50','2019-09-11','true','true','true','false') ;
INSERT INTO Vending_Machine VALUES (DEFAULT,'KSL',          '50','2019-10-11','true','true','true','false') ;

-- --inserting snacks: sid vid sname                                  price isWeet, isSalty, isDrink, EXPRIATION DATE, isavilable  
INSERT INTO Snacks VALUES (DEFAULT,'1','Rice Crispy Treat',           '2.5','true','false','false','2022-10-10','true') ;
INSERT INTO Snacks VALUES (DEFAULT,'1','Pop Tarts Frosted Strawberry','2.5','true','false','false','2022-10-10','true');
INSERT INTO Snacks VALUES (DEFAULT,'1','Doritos',                     '2.5','false','true','false','2022-10-10','true');
INSERT INTO Snacks VALUES (DEFAULT,'1','Skittles',                    '2.5','true','false','false','2022-10-10','false');
INSERT INTO Snacks VALUES (DEFAULT,'2','Rice Crispy Treat',           '2.5','true','false','false','2020-11-10','false');
INSERT INTO Snacks VALUES (DEFAULT,'2','Rice Crispy Treat',           '2.5','true','false','false','2020-10-10','true') ;
INSERT INTO Snacks VALUES (DEFAULT,'2','Pop Tarts Frosted Strawberry','2.5','true','false','false','2022-10-10','true');
INSERT INTO Snacks VALUES (DEFAULT,'2','Doritos',                     '2.5','false','true','false','2022-09-10','true');
INSERT INTO Snacks VALUES (DEFAULT,'3','Skittles',                    '2.5','true','false','false','2022-09-10','true');
INSERT INTO Snacks VALUES (DEFAULT,'4','Starbuck frappuccino Mocha',  '2.5','true','false','true','2020-06-15','true');
INSERT INTO Snacks VALUES (DEFAULT,'4','Starbuck frappuccino Coffee', '2.5','true','false','true','2020-06-15','false');

-- --inserting vending review:    reviewid vid score comment 
INSERT INTO Vending_Review VALUES (DEFAULT,'3','5','my favorite vending machine at ksl. This is the only one that accept debit card');
INSERT INTO Vending_Review VALUES (DEFAULT,'4','1','it eat my money and not giving me my candie, will never use this one');
INSERT INTO Vending_Review VALUES (DEFAULT,'5','1','my candies all melted ');
INSERT INTO Vending_Review VALUES (DEFAULT,'2','5','this is a good one because nobody know this machine so their always candy');
INSERT INTO Vending_Review VALUES (DEFAULT,'4','1','they need refill I NEED MY COFFEE');
INSERT INTO Vending_Review VALUES (DEFAULT,'4','5','the new melt chocolate mocha is really good');

-- --inserting nutrition: s_id calroies allgereis suger caffie 
INSERT INTO Nutrition VALUES ('1','160','true','18','0');
INSERT INTO Nutrition VALUES ('2','200','false','40','0');
INSERT INTO Nutrition VALUES ('3','250','false','0','0');
INSERT INTO Nutrition VALUES ('4','250','false','30','0');
 
--reviewid s_id score comments
INSERT INTO Snack_Review ( s_id, score,viewer_comments) 
SELECT  s_id ,1, 'too sweet not for me'
FROM Snacks
WHERE s_name ='Rice Crispy Treat';

INSERT INTO Snack_Review ( s_id, score,viewer_comments) 
SELECT  s_id ,5, 'loved the strawberry'
FROM Snacks
WHERE s_name ='Pop Tarts Frosted Strawberry';

INSERT INTO Snack_Review ( s_id, score,viewer_comments) 
SELECT  s_id ,4, 'rainbow color made me so happy '
FROM Snacks
WHERE s_name ='Skittles';

--inserting staff:     SSN company name 
INSERT INTO Staff VALUES ('123456789','A&M Vending Machine Sales');
INSERT INTO Staff VALUES ('223456789','A&M Vending Machine Sales');
INSERT INTO Staff VALUES ('323456789','A&M Vending Machine Sales');
INSERT INTO Staff VALUES ('423456789','D & S Vending Inc');
INSERT INTO Staff VALUES ('523456789','D & S Vending Inc.');
INSERT INTO Staff VALUES ('623456789','D & S Vending Inc.');
INSERT INTO Staff VALUES ('723456789','D & S Vending Inc.');

--- insert into refill tabel:SSN; refill id(serial), s_id, data_refill, quantity_refill, 
INSERT INTO Refills Values ('123456789',DEFAULT,'1','2019-12-11','20');
INSERT INTO Refills Values ('223456789',DEFAULT,'2','2019-12-11','20');
INSERT INTO Refills Values ('323456789',DEFAULT,'1','2019-12-10','20');

