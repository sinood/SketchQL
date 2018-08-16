Begin;

Drop table if exists Organization_demo;
Drop table if exists Organizationinfo_demo;
Drop table if exists SubOrganization_demo;
Drop table if exists department_demo;

Create table Organization_demo(
OrgID Numeric Not Null Primary Key,
OrgName Text Not Null Unique
);
create unique index Orgname_unique_idx 
on Organization_demo(OrgName);

Create table Organizationinfo_demo(
OrgID Numeric Not Null Primary Key 
    References Organization_demo(OrgID),
Founded Date Null,
Goal Text Null
);

Create table SubOrganization_demo(
SID Integer Not Null Primary Key,
OrgID Numeric Not Null 
    References Organizationinfo_demo(OrgID),
Name TEXT Not Null Unique
);
create unique index names_unique_idx 
on SubOrganization_demo (Name);

Create table department_demo(
DEPTID Integer Not Null Primary Key,
SubOrgID Integer Not Null 
    References SubOrganization_demo(SID),
Name text Not Null Unique
);
create unique index namesdept_unique_idx 
on department_demo(Name);

Commit;

