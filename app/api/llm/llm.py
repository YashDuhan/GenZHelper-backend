import os
from groq import Groq
from pathlib import Path

class GenZTranslator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self):
        """Load the prompt template from prompt.txt"""
        prompt_path = Path(__file__).parent / "prompt.txt"
        with open(prompt_path, "r") as f:
            return f.read()

    def translate(self, request_data):
        """
        Translate regular text to GenZ style using Groq LLM
        
        Args:
            request_data (dict): Dictionary containing translation parameters
            
        Returns:
            dict: Translation response with GenZ text and analysis
        """
        try:
            # Construct the system prompt and user message
            messages = [
                {
                    "role": "system",
                    "content": self.prompt_template
                },
                {
                    "role": "user", 
                    "content": str(request_data)
                }
            ]

            # Call Groq API
            completion = self.client.chat.completions.create(
                model="mistral-saba-24b",  # Using Mixtral model for better performance
                messages=messages,
                temperature=0.7, # lower temperature for more consistent results
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )

            # Extract and parse response
            result = completion.choices[0].message.content
            
            # The LLM should return a JSON string that we can parse
            # If there's an error, return a null response
            try:
                return result
            except:
                return {
                    "response": None,
                    "analysis": {
                        "mood": "Error parsing response",
                        "likeability": 0,
                        "userInsights": {
                            "communicationStyle": "Error",
                            "emotionalTone": "Error",
                            "socialDynamics": "Error",
                            "languagePatterns": "Error",
                            "suggestedApproach": "Error processing request"
                        }
                    }
                }

        except Exception as e:
            return {
                "response": None,
                "analysis": {
                    "mood": f"Error: {str(e)}",
                    "likeability": 0,
                    "userInsights": {
                        "communicationStyle": "Error",
                        "emotionalTone": "Error",
                        "socialDynamics": "Error",
                        "languagePatterns": "Error",
                        "suggestedApproach": "An error occurred processing your request"
                    }
                }
            }
