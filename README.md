# Polygence work

## Requirements

```
docker (19.03.5>=)
git (2.14.3>=)
```

## Setup

#### List commands

```
make help
```

#### Set up project

```
make build
make install
```

#### Database setup

```
make database
make database-admin
```

```
localhost:8080 (admin@admin.org / admin)
database:5432 (admin / admin)
```

#### Start server

```
make migrate
make start (http://127.0.0.1:5000/api/spendings/)
```

- GET /api/spendings
```
curl -X GET "http://127.0.0.1:5000/api/spendings/"
```

- Filtering
```
curl -X GET "http://127.0.0.1:5000/api/spendings/?currency=HUF"
```

- POST /api/spendings
```
curl -d '{"amount": 1200, "currency": "HUF", "description": "food"}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:5000/api/spendings/"
```

- DELETE /api/spendings/<id>/
```
curl -X DELETE "http://127.0.0.1:5000/api/spendings/1/"
```

- PUT /api/spendings/<id>/
```
curl -d '{"amount": 1300, "currency": "HUF", "description": "food"}' -H "Content-Type: application/json" -X PUT "http://127.0.0.1:5000/api/spendings/1/"
```