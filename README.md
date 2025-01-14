# DatabasesProject

### Setup
To get started run the following commands:

```cmd
cp .env.example .env
```

```cmd
docker-compose up django mysql phpmyadmin
```

```cmd
docker exec -it mysql /bin/bash
```

```cmd
mysql -u user -psecret
```

```sql
USE project_database;
```

Copy and paste the contents of `/database/schema.sql` in the terminal to create the schema of MySQL database.

(TODO: automate schema and seed)
