# SQLite cheatsheet

## 1. Open DB file / connect to an SQLite database
```bash
.open site.db

```

## 2. Show all available commands
```bash
.help

```

## 3. Show databases in the current database connection
```bash
.databases

```

## 4. Add additional database connection
```bash
ATTACH "site2.db" AS site2

```
```bash
.databases

seq  name             file
---  ---------------  ---------------------
0    main				site.db
2    site2				site2.db
```

## 5. Show tables in a database
```Bash
.tables

post user
```

## 6. Show the structure of a table
```bash
.schema user

CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(15) NOT NULL, 
	email VARCHAR(15) NOT NULL, 
	image_file VARCHAR(20) NOT NULL, 
	password VARCHAR(60) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
```
### show schema of all tables in db and contents of sqlite_stat 
```bash
.fullschema

CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(15) NOT NULL, 
	email VARCHAR(15) NOT NULL, 
	image_file VARCHAR(20) NOT NULL, 
	password VARCHAR(60) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE post (
	id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	content TEXT NOT NULL, 
	PRIMARY KEY (id)
);
/* No STAT tables available */
```

## 7. Show indexes of the current db
```bash
.indexes username

```

## 8. Save the result of a query into a file
```bash
.output users.txt
SELECT * From user;

```
### change file output type

```bash
.mode csv
.header open
.output users.txt
SELECT * From user;

```

## Automating the use of the SQLite shell
### 1. create the automation script -> automate.sql

```bash
.mode csv
.output results.csv
.open site.db
SELECT * from user;

```

### 2. Run the script
```bash
$ sqlite3 < commands.sql

```