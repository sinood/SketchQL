BEGIN;

-- Sample Organization --
INSERT INTO Organization_demo
VALUES
 (1,'Big Store Inc')
;

INSERT INTO Organizationinfo_demo VALUES
  (1,'1972-06-02','Store')
;

INSERT INTO Suborganization_demo VALUES
  (10,1,'Xtra Big Store'),
  (11,1,'Big Store Groceries')
;

INSERT INTO department_demo VALUES
  (100,10,'Electronics')
;

INSERT INTO department_demo VALUES
((SELECT MAX(deptid)+1 FROM department_demo),10,'Groceries & Stocking'),
((SELECT MAX(deptid)+2 FROM department_demo),10,'Furniture & Appliances'),
((SELECT MAX(deptid)+3 FROM department_demo),10,'Clothing,Shoes'),
((SELECT MAX(deptid)+4 FROM department_demo),10,'Home,Patio and Garden'),
((SELECT MAX(deptid)+5 FROM department_demo),10,'Kitchen and Dining'),
((SELECT MAX(deptid)+6 FROM department_demo),10,'Toys & Video Games'),
((SELECT MAX(deptid)+7 FROM department_demo),10,'Movies, Books, & Music'),
((SELECT MAX(deptid)+8 FROM department_demo),10,'Sports and Outdoors'),
((SELECT MAX(deptid)+9 FROM department_demo),10,'Health and Medicine'),
((SELECT MAX(deptid)+10 FROM department_demo),10,'School and Office Supplies'),
((SELECT MAX(deptid)+11 FROM department_demo),10,'Matinence'),
((SELECT MAX(deptid)+12 FROM department_demo),10,'Management & Customer Service')
;

COMMIT;
