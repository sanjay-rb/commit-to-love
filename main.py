"""
A GitHub Action that commits love daily,
delivering sweet riddles and reminders that some things are worth committing to 💖
"""

import os
import time
import random
import logging
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
import requests

TEXT_GENERATION_MODEL = "openrouter/free"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def ask_open_router(prompt: str) -> str:
    """Ask OpenRouter a question and return the answer."""

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    )

    completion = client.chat.completions.create(
        extra_body={"reasoning": {"enabled": True}},
        model=TEXT_GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    output = completion.choices[0].message.content.strip()
    return output.strip()


def send_telegram_text(text):
    """Send a text message to Telegram."""

    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    data = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": text,
        "parse_mode": "HTML",
    }
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    """Generate a riddle and sent to telegram chat."""

    logging.info("Starting the love riddle generator...")
    load_dotenv()

    # Read the prompt template
    logging.info("Reading the prompt template...")
    with open("prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Get today's date
    logging.info("Getting today's date...")
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Fill in the placeholder using format()
    logging.info("Filling in the prompt template with today's date...")
    prompt = prompt_template.format(DATE=today_date)

    # Now 'prompt' has today's date and is ready for the LLM
    logging.info("Prompt generated: %s", prompt)
    output = ask_open_router(prompt)

    # print the output
    logging.info("Output generated: %s", output)

    # split riddle and answer
    riddle, answer = output.split("Answer:")
    logging.info("Generated riddle: %s", riddle)
    logging.info("Generated answer: %s", answer)

    # send riddle to Love with a cute header and footer
    riddle_headers = [
        "💖 A little question for you 💖",
        "💕 Quick love puzzle 💕",
        "💌 One sweet question 💌",
        "💝 A tiny mystery 💝",
        "💗 A little riddle for you 💗",
    ]

    riddle_footers = [
        "Take your time to think about it 💕",
        "No rush, just enjoy the moment 💖",
        "Let it simmer in your heart 💌",
        "Feel free to ponder on it 💝",
        "Let the mystery unfold in your mind 💗",
    ]

    riddle = (
        f"{random.choice(riddle_headers)}\n\n"
        f"{riddle.strip()}\n\n"
        f"{random.choice(riddle_footers)}"
    )

    logging.info("Sending riddle to Love...")
    send_telegram_text(riddle)

    # wait for 30 seconds before sending the answer
    logging.info("Waiting for 30 seconds before sending the answer...")
    time.sleep(30)

    # send answer to Love with a cute header and footer
    answer_headers = [
        "💖 Love riddle answer 💖",
        "💌 Did you guess it? 💌",
        "💝 Here’s the answer 💝",
        "✨ Riddle solved! ✨",
        "🔥 Your answer is here 🔥",
    ]

    answer_footers = [
        "Always you ❤️",
        "You always make my day brighter 😍",
        "My heart chose you every single day 💞",
        "Keep smiling, love 💖",
        "Guess who’s stealing my heart today? 😏❤️",
    ]

    answer = (
        f"{random.choice(answer_headers)}\n\n"
        f"{answer.strip()}\n\n"
        f"{random.choice(answer_footers)}"
    )

    logging.info("Sending answer to Love...")
    send_telegram_text(answer)


if __name__ == "__main__":
    main()
