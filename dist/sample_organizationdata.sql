Begin;

-- Sample Organization --
Insert into Organization_demo
Values
 (1,'Big Store Inc');
Insert into Organizationinfo_demo
Values
  (1,'1972-06-02','Store');

Insert into Suborganization_demo
Values
  (10,1,'Xtra Big Store'),
  (11,1,'Big Store Groceries')
;
Insert into department_demo Values(100,10,'Electronics');
Insert into department_demo Values
((Select max(deptid)+1 From department_demo),10,'Groceries & Stocking'),
((Select max(deptid)+2 From department_demo),10,'Furniture & Appliances'),
((Select max(deptid)+3 From department_demo),10,'Clothing,Shoes'),
((Select max(deptid)+4 From department_demo),10,'Home,Patio and Garden'),
((Select max(deptid)+5 From department_demo),10,'Kitchen and Dining'),
((Select max(deptid)+6 From department_demo),10,'Toys & Video Games'),
((Select max(deptid)+7 From department_demo),10,'Movies, Books, & Music'),
((Select max(deptid)+8 From department_demo),10,'Sports and Outdoors'),
((Select max(deptid)+9 From department_demo),10,'Health and Medicine'),
((Select max(deptid)+10 From department_demo),10,'School and Office Supplies'),
((Select max(deptid)+11 From department_demo),10,'Matinence'),
((Select max(deptid)+12 From department_demo),10,'Management & Customer Service');

 Commit; 
 