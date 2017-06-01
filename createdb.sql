CREATE TABLE collisions(
  Borough TEXT,
  Contributing_Factor_1 TEXT,
  Contributing_Factor_2 TEXT,
  Contributing_Factor_3 TEXT,
  Contributing_Factor_4 TEXT,
  Contributing_Factor_5 TEXT,
  Cross_Street_Name TEXT,
  Date TEXT,
  Latitude REAL,
  Longitude REAL,
  Number_of_Cyclist_Injured INTEGER,
  Number_of_Cyclist_Killed  INTEGER,
  Number_of_Motorist_Injured  INTEGER,
  Number_of_Motorist_Killed INTEGER,
  Number_of_Pedestrians_Injured INTEGER,
  Number_of_Pedestrians_Killed  INTEGER,
  Number_of_Persons_Injured INTEGER,
  Number_of_Persons_Killed  INTEGER,
  Off_Street_Name TEXT,
  On_Street_Name  TEXT,
  Time  TEXT,
  Unique_Key  INTEGER NOT NULL UNIQUE,
  Vehicle_Type_Code1  TEXT,
  Vehicle_Type_Code2  TEXT,
  Vehicle_Type_Code3  TEXT,
  Vehicle_Type_Code4  TEXT,
  Vehicle_Type_Code5  TEXT,
  Zip_Code  INTEGER
);