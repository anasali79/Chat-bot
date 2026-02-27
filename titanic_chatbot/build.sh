#!/bin/bash
# Build script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Copy dataset if needed
if [ ! -f "data/titanic.csv" ]; then
    echo "Dataset file not found, creating sample data..."
    # The dataset will be loaded from the repository
fi

echo "Build completed successfully!"