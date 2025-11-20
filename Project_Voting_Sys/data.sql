-- Active: 1759779716963@@127.0.0.1@3306@vote_data
CREATE DATABASE vote_data ; 

USE vote_data ; 


CREATE TABLE vote_details(
    Id INT AUTO_INCREMENT , 
    Name VARCHAR(50),
    Age INT ,
    Aadhaar BIGINT  UNIQUE,
    Mobile_no BIGINT ,
    selected_leader VARCHAR(30),
    PRIMARY KEY(Id , Aadhaar)
);


SELECT * FROM vote_details



SELECT selected_leader AS leader_name, COUNT(*) AS total_votes 
FROM vote_details 
GROUP BY selected_leader 
ORDER BY total_votes DESC;

SELECT selected_leader AS leader_name, COUNT(*) AS total_votes 
FROM vote_details 
WHERE selected_leader = 'modi';


TRUNCATE TABLE vote_details ;   -- this is to delete all the data from the table 



DROP DATABASE vote_data ;




-- UPDATE TABLE_NAME SET designation = (%s) , (new_designation) WHERE emp_id = 101 ;


-- cur.execute("""SELECT selected_leader AS leader_name, COUNT(*) AS total_votes 
-- FROM vote_details 
-- WHERE selected_leader = 'modi';""");