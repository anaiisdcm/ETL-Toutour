# ETL-Toutour

## Prerequisite
This code requires SQL and PostGres installed.  
This code runs using Python 3.11+. The following libraries are required :

- numpy
- pandas
- streamlit
- sqlalchemy
- os

## Folder Structure
Folders in yellow are to be created. Files in green are code files. Folders in pink are code folders.
.  
└── ETL-Toutour  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:gold">data_in</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:gold">data_noisy</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:gold">data_out</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:pink">DataGeneration</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── <span style="color:green">...Python files</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:pink">EL_DB_Toutour</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── <span style="color:green">...Python files</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:pink">HotDog</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── <span style="color:green">...Python files</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:pink">Transform</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── <span style="color:green">...Python files</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── <span style="color:green">main.py</span>  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── README.md

## Quick start

To launch a quick demo of the code, proceed as follow :

0. Clone this git and install the required libraries.
1. Ensure the structure of the folder is correct.
    - Create data_in and data_out folders if necessary.
2. Set-up custom user in postgres:
    - [bash] sudo -u postgres psql
    - [PostGres] #CREATE ROLE usertoutour WITH LOGIN PASSWORD 'mdp';
    - [PostGres] #ALTER ROLE usertoutour WITH SUPERUSER;
    - [PostGres] #\du
3. Run main.py
4. Input "yes" when prompted
5. Copy the given url in a web browser.


## Project: Design a data pipeline
You are the 4 person data engineering team of a startup

- Startups to be defined in AI Business Models class
- 2 - 4 page report on ETL/ELT pipeline choices
    - Motivate and explain choices:
        - E: where are the data coming from?
        - T: how are the data being transformed?
        - L: how are the data loaded, stored, and used?
- Demo of example database
    - PostgreSQL, Mongo, other, your choice
    - Documented scripts to load and manipulate example data
    - Data should not be exhaustive, should demonstrate ETL choices

Report rigor /6
Report clarity /6
Demo data /4
Demo manipulation /4