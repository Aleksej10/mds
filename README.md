build container:
  docker compose build

run server:
  docker compose up -d app 

shut server down:
  docker compose down app


run tests:
  docker compose run --rm test
