# Use the official PostgreSQL image from the Docker Hub
FROM postgres:16.3

# Set environment variables for the database
ENV POSTGRES_DB=exampledb
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=

# Copy the SQL script to create the table and insert data
COPY init.sql /docker-entrypoint-initdb.d/
