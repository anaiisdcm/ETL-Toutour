# ETL-Toutour

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


## Designing a data pipeline: extraction

● What are the various data sources?
> The data comes from the users accounts on the application then put into sql tables
> For the demonstration data is generated

● What is the format of the data from each source (e.g., CSV, JSON, XML, database
tables)?
> Data is recieved via JSON from the app

● Is the data streaming or can it be loaded in batches?
> Data is loaded in batches since we don't need in real time following of the apps

● What will the data look like on extraction?
> In extraction the data will be presented in CSV files, one for each sql table

● How do you verify the data's accuracy and completeness at the source?
> TODO: define the data cleaning process

● Are there any data access limitations or security constraints?
> Not defined for now

● How frequently is the data updated or changed at the source?
> It is updated at least every time a user signs up in the app, then loaded each time a *tour* is requested and when the *hot dog* resume given to the user

● Will you need to deal with incremental data extraction or full data loads?
> Not defined for now 

● What are the volume and velocity of the data (e.g., terabytes per day, real-time
streams)?
> Not defined for now


## Designing a data pipeline: transformation

● What data cleansing steps are needed?
> Remove incorrect data types given by the users (e.g strings for the User's age or number for the dog name)

● Are there any business rules that need to be applied during transformation?
> Not defined for now

● Do you need to join or merge data from multiple sources?
> Yes since each user is a source of data

● Are there any specific data formats or types that need to be converted?
> JSON to CSV 

● How will you handle any data inconsistencies or errors?
> TODO⚙️

● Are there any dependencies between the transformation steps (e.g., one transformation requires another to be completed first)?
> TODO⚙️

● Do you need to enrich the data by adding additional calculated fields?
> It can happen for calculating the total walking time for the dogs in the *hot dog*

● How will you track the changes to the data for auditing purposes?
> Not defined

● Will transformation happen before or after loading?
> Not defined

## Designing a data pipeline: loading

● What is the target system for the data (e.g., data warehouse, data lake, database)?
> Not defined

● How often will the data be loaded (e.g., real-time, hourly, daily)?
> Not defined

● Should the data be appended to the existing dataset or replace it entirely?
> No

● Are there any schema or structural requirements for the target system?
> Not defined

● How do you ensure data consistency and integrity during loading?
> The cleaning process should have been made before

● What are the performance constraints?
> The loading should be fast enough for the consumer (seconds to find a course for their dog)

● How will you handle schema changes in the target system?
> Not defined

● Is there a need for historical data tracking or versioning in the target?
> Not sure

● How will you monitor the loading process to ensure it runs successfully?
> Not defined


## ETL or ELT
Data Format:

● ETL is needed for unstructured data to transform it into a
relational format.

● ELT can be used if the data is already in a relational or flat
format.
Data Size:

● ELT is suited for large datasets due to enhanced processing
capabilities.

● ETL is typically used for smaller datasets.
Cost:

● ETL can be expensive as it involves physically moving data for
processing.

● ELT can be more cost-effective, especially when leveraging
cloud-based parallel processing without moving data.
Data Source:

● ELT is better for large, batch-wise data from cloud sources.

● ETL is preferred for streaming or messaging data.
Data Destination:

● ETL is often used when the source and destination systems
differ.

● ELT is suitable when transferring data between identical
systems or products.
Transformation Intensity:

● ELT is preferred for simple transformations and scalability.

● ETL is chosen for more complex transformations that need
to be handled in smaller steps.
Transformation Location:

● In ETL, transformations occur before the data reaches the
warehouse.

● In ELT, transformations are performed after data import,
requiring more processing power but offering faster insights.
