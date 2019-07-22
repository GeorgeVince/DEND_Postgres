# UDACITY - DATA ENGINEERING NANODEGREE - PROJECT ONE

The aim of this project is to build a PostgresSQL database to house song and log data for an example company "Sparkify".
Currently there exists not way to query the data stored in log files and metadata files, and therefore an ETL script must be built to take data from these files, transform it and load it into the database. All data files are in JSON format.

## Usage Instructions:

* In order to run the project ensure log files and song data files are held in the current repository in data/log_data and data/song_data.
* Run *create_tables.py* to create the required tables.
* Run *etl.py* to process the files
* Verify files have been added using the *test.ipynb* workbook.

## Description of project files:

### Data:
* *log_data*: Monthly log files are stored containing infomation about the users' interaction with the Sparkify app.
* *song_data*: Metadata about the song files contained on the sparkify database.

### Python files:
* *sql_queries.py* - contains all required SQL statements for the project, including creating / deleting tables and selecting data.
* *create_tables.py* - Uses the creation statements in the *sql_queries.py* to create the required tables for the project.
* *etl.py* - used to process each of the log data and song data files contained in the data folder current directory folder.  e.g. data/log_data and data/song_data

### Notebooks:
* *etl.ipynb* - Skeleton workbook created to make each of the seperate ETL fucntions.
* *test.ipynb* - Workbook used to test and verify data has been added to DB.

