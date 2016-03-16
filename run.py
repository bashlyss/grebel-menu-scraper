#!/usr/bin/env python3

from app.server import app

if __name__ == "__main__":
    app.run('0.0.0.0', port=3001)
