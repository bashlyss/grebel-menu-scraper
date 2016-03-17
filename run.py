#!/usr/bin/env python3

from app.server import app

if __name__ == "__main__":
    app.run('127.0.0.1', port=3001)
