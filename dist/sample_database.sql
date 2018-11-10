BEGIN;

DROP TABLE IF EXISTS Organization_demo;
DROP TABLE IF EXISTS Organizationinfo_demo;
DROP TABLE IF EXISTS SubOrganization_demo;
DROP TABLE IF EXISTS department_demo;

CREATE TABLE Organization_demo(
    OrgID NUMERIC NOT NULL PRIMARY KEY,
  OrgName TEXT    NOT NULL UNIQUE
);

CREATE UNIQUE INDEX Orgname_UNIQUE_idx
ON Organization_demo(OrgName);

CREATE TABLE Organizationinfo_demo(
    OrgID NUMERIC NOT NULL PRIMARY KEY REFERENCES Organization_demo(OrgID),
  Founded DATE    NULL,
     Goal TEXT    NULL
);

CREATE TABLE SubOrganization_demo(
     SID INTEGER NOT NULL PRIMARY KEY,
   OrgID NUMERIC NOT NULL REFERENCES Organizationinfo_demo(OrgID),
    Name TEXT    NOT NULL UNIQUE
);
CREATE UNIQUE INDEX names_UNIQUE_idx
  ON SubOrganization_demo (Name);

CREATE TABLE department_demo(
    DEPTID INTEGER NOT NULL PRIMARY KEY,
  SubOrgID INTEGER NOT NULL REFERENCES SubOrganization_demo(SID),
      Name TEXT    NOT NULL UNIQUE
);
CREATE UNIQUE INDEX namesdept_UNIQUE_idx
  ON department_demo(Name);

COMMIT;
