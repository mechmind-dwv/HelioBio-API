#!/bin/bash

# --- VARIABLES ---
# The command to start your server. Replace `your_server_command` with the actual command.
# For example: `node app.js`, `python -m http.server`, or `/path/to/your/server_executable`
SERVER_COMMAND="node server.js"

# --- FUNCTIONS ---

# Function to check if the server is already running
is_server_running() {
    # Check for a process with the same command. Adjust if necessary.
    pgrep -f "$SERVER_COMMAND" > /dev/null
    return $?
}

# --- SCRIPT LOGIC ---

# Check if the server is already running
if is_server_running; then
    echo "Server is already running."
    exit 1
fi

# Start the server in the background
echo "Starting server..."
nohup $SERVER_COMMAND > /dev/null 2>&1 &

# Optional: Add a small delay to allow the server to start
sleep 2

# Check if the server started successfully
if is_server_running; then
    echo "Server started successfully."
else
    echo "Failed to start server."
    exit 1
fi
