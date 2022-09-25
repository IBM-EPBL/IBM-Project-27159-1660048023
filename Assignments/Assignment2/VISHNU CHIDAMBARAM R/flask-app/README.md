### Initialise the Database
```flask initdb```

### Run the Application
```flask run```

### Table Structure (`users`)
| Column  | Type|
| ------------- | ------------- |
| `id`  | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `username`  | `TEXT NOT NULL`  |
| `password`  | `TEXT NOT NULL`  |
| `name`  | `TEXT NOT NULL` |
| `email`  | `TEXT NOT NULL`  |

`SQLite` is used for the database.
