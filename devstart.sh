#!/bin/bash

echo "Building..."

if command -v protoc &>/dev/null; then
    echo "Compiling proto"
else
    echo "protoc is not installed. Please install it to continue."
    exit
fi

protoc --python_out=. ./src/proto/web_monitor.proto

echo "Installing pip reqs"

python3 -m venv venv
echo "Activating venv"

source venv/bin/activate


while read package; do
    pip install "$package"
done < requirements.txt

exit 0