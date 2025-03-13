import os
from openai import OpenAI

class HappyHourExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_happy_hour(self, page_text):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Extract only the Happy Hour schedule from the following restaurant webpage text."},
                {"role": "user", "content": page_text}
            ]
        )
        return response.choices[0].message.content





