import os
import unittest
from unittest.mock import patch, mock_open

import main


class MainTests(unittest.TestCase):
    def setUp(self):
        os.environ.setdefault("TELEGRAM_CHAT_ID", "12345")
        os.environ.setdefault("TELEGRAM_BOT_TOKEN", "bot:token")
        os.environ.setdefault("OPEN_ROUTER_API_KEY", "dummy")

    @patch("main.time.sleep", return_value=None)
    @patch("main.send_telegram_text")
    def test_main_sends_riddle_and_answer(self, mock_send, mock_sleep):
        # LLM returns riddle + Answer: separator
        sample_output = "Roses are red\nViolets are blue\nAnswer: You"

        with patch("main.ask_open_router", return_value=sample_output) as mock_ask:
            # patch prompt file read
            with patch("builtins.open", mock_open(read_data="Prompt {DATE}")):
                main.main()

        # ask_open_router should be called once
        self.assertTrue(mock_ask.called)

        # send_telegram_text should be called twice (riddle, then answer)
        self.assertEqual(mock_send.call_count, 2)

        first_msg = mock_send.call_args_list[0][0][0]
        second_msg = mock_send.call_args_list[1][0][0]

        # riddle text (first message) should not contain the literal 'Answer:'
        self.assertIn("Roses are red", first_msg)
        self.assertNotIn("Answer:", first_msg)

        # answer (second message) should include the parsed answer
        self.assertIn("You", second_msg)

    def test_main_raises_when_no_answer_separator(self):
        # If the LLM output lacks 'Answer:' the current code will raise ValueError
        with patch("main.ask_open_router", return_value="No separator here"):
            with patch("builtins.open", mock_open(read_data="Prompt {DATE}")):
                with self.assertRaises(ValueError):
                    main.main()


if __name__ == "__main__":
    unittest.main()
