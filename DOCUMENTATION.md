## Table of Contents
- [Quick Start](#quick-start)
- [PostgreSQL](#postgresql)

### Quick Start

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