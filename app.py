#!/usr/bin/env python3
"""
Shiny E-Commerce Application Entry Point
"""

from shinyecomm import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)