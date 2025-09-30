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
● What is the format of the data from each source (e.g., CSV, JSON, XML, database
tables)?
● Is the data streaming or can it be loaded in batches?
● What will the data look like on extraction?
● How do you verify the data's accuracy and completeness at the source?
● Are there any data access limitations or security constraints?
● How frequently is the data updated or changed at the source?
● Will you need to deal with incremental data extraction or full data loads?
● What are the volume and velocity of the data (e.g., terabytes per day, real-time
streams)?


## Designing a data pipeline: transformation
● What data cleansing steps are needed?
● Are there any business rules that need to be applied during transformation?
● Do you need to join or merge data from multiple sources?
● Are there any specific data formats or types that need to be converted?
● How will you handle any data inconsistencies or errors?
● Are there any dependencies between the transformation steps (e.g., one
transformation requires another to be completed first)?
● Do you need to enrich the data by adding additional calculated fields?
● How will you track the changes to the data for auditing purposes?
● Will transformation happen before or after loading?

## Designing a data pipeline: loading
● What is the target system for the data (e.g., data warehouse, data lake, database)?
● How often will the data be loaded (e.g., real-time, hourly, daily)?
● Should the data be appended to the existing dataset or replace it entirely?
● Are there any schema or structural requirements for the target system?
● How do you ensure data consistency and integrity during loading?
● What are the performance constraints?
● How will you handle schema changes in the target system?
● Is there a need for historical data tracking or versioning in the target?
● How will you monitor the loading process to ensure it runs successfully?


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