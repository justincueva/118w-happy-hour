import os
from openai import OpenAI

class HappyHourExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def extract_happy_hour(self, page_text):
        prompt = """
        `You are an information‐extraction assistant. Your job is to scan the given text or HTML and pull out only the Happy Hour schedule lines.  Output **only** a plain text string, with each schedule on its own line, following this format:

            [days] [start]–[end]

            Rules:
            - If text says “Happy hour every day” or “daily,” use “everyday” for days.
            - If it lists specific weekdays, collapse them into a comma-separated list in order (e.g. “Mon, Tue, Wed”).
            - Always keep times to 12-hour format (e.g. “4pm–7pm”).
            - Don’t output anything that isn’t a happy-hour schedule (no venue names, no commentary).

            Examples:

            Input:
            \`\`\`
            Monday–Friday 4pm–7pm
            Live music nightly.
            Happy Hour daily from 3:30pm to 6:30pm
            \`\`\`
            
            Correct Output:
            \`\`\`
            Everyday 3:30 PM –6:30 PM
            \`\`\`
        """
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system","content": prompt},
                {"role": "user", "content": page_text}
            ]
        )
        return response.choices[0].message.content




