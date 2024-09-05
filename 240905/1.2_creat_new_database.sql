IF EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = 'studb')
	DROP DATABASE studb
GO

CREATE DATABASE studb ON
	(NAME = 'studb',
	FILENAME = 'd:\studb.mdf',
	SIZE = 5,
	MAXSIZE = 10,
	FILEGROWTH = 1)
LOG ON
	(NAME = 'studb_log',
	FILENAME = 'd:\studb_log.LDF',
	SIZE = 1,
	FILEGROWTH = 10%)