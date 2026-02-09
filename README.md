# commit-to-love

A GitHub Action that commits love daily, delivering sweet riddles and reminders that some things are worth committing to 💖

## Description

This project is a GitHub Action that generates a daily love riddle and commits it to a repository. It aims to bring a little bit of love and positivity to the world of software development.

## Features

- Generates a daily love riddle using the OpenAI GPT-3 model.
- Sends the riddle to a specified Telegram chat.
- Commits the riddle to a repository with a cute header and footer.

## Prerequisites

- Python 3.x
- OpenAI API key
- Telegram bot token and chat ID

## Installation

1. Clone this repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your environment variables:
   - `OPEN_ROUTER_API_KEY`: Your OpenAI API key.
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID.

## Usage

1. Create a new GitHub Action workflow file in your repository's `.github/workflows` directory.
2. Add the following YAML code to the workflow file:

```yaml
name: Commit to Love

on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  commit-to-love:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Commit Love Riddle
        uses: <your_username>/commit-to-love@main
        with:
          riddle: ${{ secrets.RIDDLE }}