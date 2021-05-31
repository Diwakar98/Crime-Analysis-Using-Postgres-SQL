
CREATE TABLE auto_theft
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Group_Name VARCHAR(60),
        Auto_Theft_Coordinated_Traced INTEGER,
        Auto_Theft_Recovered INTEGER,
        Auto_Theft_Stole INTEGER
    );

CREATE TABLE serious_fraud
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Group_Name VARCHAR(60),
        Loss_of_Property_1_10_Crores INTEGER,
        Loss_of_Property_10_25_Crores INTEGER,
        Loss_of_Property_25_50_Crores INTEGER,
        Loss_of_Property_50_100_Crores INTEGER,
        Loss_of_Property_Above_100_Crores INTEGER
    );

CREATE TABLE murder_victim_age_sex
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Group_Name VARCHAR(60),
        Victims_Upto_10_Yrs INTEGER,
        Victims_Upto_10_15_Yrs INTEGER,
        Victims_Upto_15_18_Yrs INTEGER,
        Victims_Upto_18_30_Yrs INTEGER,
        Victims_Upto_30_50_Yrs INTEGER,
        Victims_Above_50_Yrs INTEGER,
        Victims_Total INTEGER
    );


CREATE TABLE victims_of_rape
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Subgroup VARCHAR(60),
        Rape_Cases_Reported INTEGER,
        Victims_Above_50_Yrs INTEGER,
        Victims_Between_10_14_Yrs INTEGER,
        Victims_Between_14_18_Yrs INTEGER,
        Victims_Between_18_30_Yrs INTEGER,
        Victims_Between_30_50_Yrs INTEGER,
        Victims_of_Rape_Total INTEGER,
        Victims_Upto_10_Yr INTEGER
    );


CREATE TABLE cases_under_crime_against_women
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Group_Name VARCHAR(120),
        Sub_Group_Name VARCHAR(120),
        Cases_Acquitted_or_Discharged INTEGER,
        Cases_charge_sheets_were_not_laid_but_Final_Report_submitted INTEGER,
        Cases_Chargesheeted INTEGER,
        Cases_Compounded_or_Withdrawn INTEGER,
        Cases_Convicted INTEGER,
        Cases_Declared_False_on_Account_of_Mistake_of_Fact_or_of_Law INTEGER,
        Cases_Investigated_Chargesheets_FR_Submitted INTEGER,
        Cases_not_Investigated_or_in_which_investigation_was_refused INTEGER,
        Cases_Pending_Investigation_at_Year_End INTEGER,
        Cases_Pending_Investigation_from_previous_year INTEGER,
        Cases_Pending_Trial_at_Year_End INTEGER,
        Cases_Pending_Trial_from_the_previous_year INTEGER,
        Cases_Reported INTEGER,
        Cases_Sent_for_Trial INTEGER,
        Cases_Trials_Completed INTEGER,
        Cases_Withdrawn_by_the_Govt INTEGER,
        Cases_withdrawn_by_the_Govt_during_investigation INTEGER,
        Total_Cases_for_Trial INTEGER
    );

CREATE TABLE arrests_under_crime_against_women
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Group_Name VARCHAR(120),
        Sub_Group_Name VARCHAR(120),
        Persons_Acquitted INTEGER,
        Persons_against_whom_cases_Compounded_or_Withdrawn INTEGER,
        Persons_Arrested INTEGER,
        Persons_Chargesheeted INTEGER,
        Persons_Convicted INTEGER,
        Persons_in_Custody_or_on_Bail_during_Invest_at_Year_beginning INTEGER,
        Persons_in_Custody_or_on_Bail_during_Invest_at_Year_end INTEGER,
        Persons_in_Custody_or_on_Bail_during_Trial_at_Year_End INTEGER,
        Persons_Released_by_Police_before_Trial_for_want_of_evidence INTEGER,
        Persons_Trial_Completed INTEGER,
        Persons_under_Trial_at_Year_beginning INTEGER,
        Total_Persons_under_Trial INTEGER
    );



CREATE TABLE trial_of_violent_crimes_by_courts
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Sub_Group_Name VARCHAR(60),
        Trial_of_Violent_Crimes_by_Courts_By_Confession INTEGER,
        Trial_of_Violent_Crimes_by_Courts_By_trial INTEGER,
        Trial_of_Violent_Crimes_by_Courts_Total INTEGER
    );

CREATE TABLE period_of_trials_by_courts
    (
        Area_Name VARCHAR(60),
        Year INTEGER,
        Sub_Group_Name VARCHAR(60),
        PT_1_3_Years INTEGER,
        PT_3_5_Years INTEGER,
        PT_5_10_Years INTEGER,
        PT_6_12_Months INTEGER,
        PT_Less_than_6_Months INTEGER,
        PT_Over_10_Years INTEGER,
        PT_Total INTEGER
    );

CREATE TABLE users
(
    username VARCHAR(60),
    password VARCHAR(60)
);

\copy auto_theft from '30_Auto_theft.csv' delimiter ',' csv header;
\copy serious_fraud from '31_Serious_fraud.csv' delimiter ',' csv header;
\copy murder_victim_age_sex from '32_Murder_victim_age_sex.csv' delimiter ',' csv header;
\copy victims_of_rape from '20_Victims_of_rape.csv' delimiter ',' csv header;
\copy cases_under_crime_against_women from '42_Cases_under_crime_against_women.csv' delimiter ',' csv header;
\copy arrests_under_crime_against_women from '43_Arrests_under_crime_against_women.csv' delimiter ',' csv header;
\copy trial_of_violent_crimes_by_courts from '28_Trial_of_violent_crimes_by_courts.csv' delimiter ',' csv header;
\copy period_of_trials_by_courts from '29_Period_of_trials_by_courts.csv' delimiter ',' csv header;
