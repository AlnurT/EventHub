from testcontainers.community.postgres import PostgresContainer

with PostgresContainer("postgres:16-alpine", driver="acyncpg") as postgres:
    print(postgres.get_connection_url())
