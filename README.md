# Clash Royale Intelligent Deck Generator

An intelligent Clash Royale deck generator built in Python that learns from match results and continuously improves its deck recommendations.

Instead of generating completely random decks, the project uses historical performance and card synergy statistics to influence future deck generation. Every completed match updates the database, allowing the generator to gradually identify stronger card combinations over time.

## Features

* 🎯 Intelligent weighted deck generation.
* 🤝 Card synergy learning based on wins and losses.
* 📊 Statistical scoring system for every card combination.
* ⚖️ Dynamic average elixir balancing during deck generation.
* 📈 Adaptive card selection based on historical performance.
* 💾 Persistent database storing cards, decks and synergy statistics.
* ⚙️ Customizable generation settings and presets.

## How it works

Each generated deck is influenced by several factors:

* Individual card performance.
* Card-to-card synergy statistics.
* Desired average elixir cost.
* Historical win/loss records.
* Statistical confidence based on the number of recorded matches.

Rather than relying on predefined meta decks, the generator gradually improves its recommendations as more match data is added.

## Technologies

* Python
* Object-Oriented Programming (OOP)
* CSV-based statistical database

## Current Status

The project has accumulated thousands of recorded card synergies and continues to improve as more matches are played.

Planned features include:

* Clash Royale API integration.
* Match history analysis.
* Card usage trends.
* Matchup analysis.
* Improved deck recommendation algorithms.

This project explores data-driven deck building by combining probability, statistics, and adaptive learning techniques without using traditional machine learning models.
