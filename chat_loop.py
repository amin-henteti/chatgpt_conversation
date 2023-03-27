import openai
import importlib
from typing import Optional
import logging
from datetime import datetime
import os
import argparse

class MyChat:
    def __init__(
        self,
        api_key_file: str,
        chat_model: str,
        log_file: Optional[str] = None,
        console_color: Optional[str] = None,
    ):
        """
        initializes the class attributes, including the logger attribute that logs the conversation.
        If logger is not specified, then the conversation is printed to the console.
        """
        self.api_key_file = api_key_file
        self.chat_model = chat_model
        self.logger = None
        if log_file is not None and console_color is not None:
            # Import the MyLogger class and rename it to MyLogger
            MyLogger = importlib.import_module("my_logger").MyLogger
            # Create a MyLogger instance with a file name and console color scheme
            self.logger = MyLogger(logfile=log_file, console_color=console_color)

    def load_key(self):
        """
        return the content of the file that contains the openai key. 
        raise an error if file does not exist
        """
        if os.path.exists(self.api_key_file):
            return open(self.api_key_file, "r").read()
        else:
            raise FileNotFoundError(f"The file {self.api_key_file} does not exist.")
        
    def run_chat(self):
        """
        handles the conversation logic.
        Here, we added a try-except block to handle exceptions and errors that can occur during the conversation.
        If an error occurs, the conversation is terminated and an error message is logged or printed to the console.
        """
        openai.api_key = self.load_key()
        chat_log = []
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file_name = f"chat_log_{now}.log"
        while True:
            user_message = input("\nUser > ")
            if user_message.lower() == "q":
                if self.logger is not None:
                    self.logger.info("closing the conversation")
                    # Rename log file
                    new_log_file_name = input("Enter log file name or press enter to use the default name: ")
                    if new_log_file_name.strip():
                        os.rename(log_file_name, new_log_file_name)
                break
            chat_log.append({"role": "user", "content": user_message})
            try:
                response = openai.Completion.create(
                    engine=self.chat_model, prompt=chat_log, max_tokens=1024, n=1, stop=None, temperature=0.7,
                )
                assistant_response = response["choices"][0]["text"]
                assistant_response = assistant_response.strip()
                if self.logger is not None:
                    self.logger.info(
                        f"\nChatGPT > {assistant_response}", log_color="green"
                    )
                else:
                    print(f"\nChatGPT > {assistant_response}")
            except Exception as e: #pylint: disable 
                if self.logger is not None:
                    self.logger.error(f"An error occurred: {e}")
                else:
                    print(f"An error occurred: {e}")
                break

if __name__ == "__main__":
    # Add command-line arguments
    parser = argparse.ArgumentParser(description="MyChat - chat with GPT-3")
    parser.add_argument("-k", "--api_key_file", default="open_ai_key.json", help="API key for OpenAI")
    parser.add_argument("-m", "--chat_model", default="gpt-3.5-turbo", help="Chat model to use")
    parser.add_argument("-l", "--log_file", default="output.log", help="Log file name")
    parser.add_argument("-c", "--console_color", default="white", help="Console color scheme")
    args = parser.parse_args()

    # create an instance of MyChat 
    # and called the run_chat method to start the conversation.
    my_chat = MyChat(
        api_key_file=args.api_key_file,
        chat_model=args.chat_model,
        log_file=args.log_file,
        console_color=args.console_color,
    )
    my_chat.run_chat()
