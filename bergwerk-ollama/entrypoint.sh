#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve model..."
ollama pull llama3.2:1b
echo "🟢 pull Done!"

# Wait for Ollama process to finish.
wait $pid