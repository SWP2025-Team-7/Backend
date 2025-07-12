# Table of Contents
- [Quick Start](#quick-start)
- [PostgreSQL](#postgresql)

## Quick Start

## API Descriprion
### Bot Users ```/bot_users```
```
/register
```
```
/login
```

## Users ```/users```

## Database

### Tables
**<center>bot_users</center>**

|Column|Type|Collation|Nullable|Default|Storage|Compression|Stats target|Description|
|-|-|-|-|-|-|-|-|-|
|id|integer||not null|nextval('bot_users_id_seq'::regclass)|plain||||
|user_id|integer||not null||plain||||
|username|character varying||not null||extended||||
|login_date|date||not null||plain||||
|login_time|time||not null||plain||||
|last_used_date|date||not null||plain||||
|last_used_time|time||not null||plain||||

**<center>users</center>**
|Column|Type|Collation|Nullable|Default|Storage|Compression|Stats target|Description|
|-|-|-|-|-|-|-|-|-|
### PostgreSQl
To run psql execution inside postgres container:
```
docker exec -it {container id} psql -U {POSGRES_USER=postgres}
```
example:
```
docker exec -it 605c4d78beb4 psql -U postgres
```
To view list ofdatabases:
```
\l
```

To connect to database:
```
\c postgres
```

To view database tables (after connection):
```
\dt
```

To view table data:
```
TABLE {table name};
```