# resume/utils/groq_utils.py

from groq import Groq

class GroqClient:
    def __init__(self, api_key):
        """
        Initialize the Groq client.
        """
        self.client = Groq(api_key="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")
        print("Groq client initialized.")

    def send_prompt(self, system_message, user_prompt, model="qwen-2.5-coder-32b", temperature=0.7, max_tokens=1024):
        """
        Send a prompt to the Groq API and return the response.
        
        :param system_message: The system message to set the context.
        :param user_prompt: The user prompt to send to the API.
        :param model: The model to use (default is "llama-3.3-70b-versatile").
        :param temperature: The temperature for the response (default is 0.7).
        :param max_tokens: The maximum number of tokens in the response (default is 1024).
        :return: The response content from the Groq API.
        """
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return None