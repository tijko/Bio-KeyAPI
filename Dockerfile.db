# Use an official SQLite image as a parent image
FROM alpine:latest

# Install SQLite
RUN apk add --no-cache sqlite

# Set the working directory in the container
WORKDIR /db

# Copy the SQLite database file into the container
COPY database.db /db

# Make the SQLite database file accessible
VOLUME /db

# Expose any ports the app is expecting
# (optional, depending on your use case)
# EXPOSE 5432

# Run SQLite when the container launches
CMD ["sqlite3", "/db/database.db"]
