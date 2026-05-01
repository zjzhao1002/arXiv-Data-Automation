import ollama
import json

class OllamaFunctions:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        if not self._ollama_model_checker():
            try:
                print(f"Model '{self.model_name}' not found in Ollama. Attempting to pull the model...")
                self._ollama_pull_model()
            except Exception as e:
                print(f"Error occurred while pulling the model: {e}")

    def _ollama_model_checker(self) -> bool:
        available_models = ollama.list()
        model_names = [model['model'] for model in available_models.models]
        if f"{self.model_name}:latest" in model_names:
            return True
        else:
            return False

    def _ollama_pull_model(self) -> None:
        ollama.pull(self.model_name)
        print(f"Model '{self.model_name}' pulled successfully.")

    def extract_keywords_ollama(self, title: str, abstract: str) -> list:

        print(f"Extracting keywords using {self.model_name} for title: {title}")
        prompt = f"""
        Extract 5 keywords from the following title and abstract:\n\n
        Title: {title}\n\n
        Abstract: {abstract}\n\n
        Respond in JSON format: {{\"keywords\": [\"kw1\", \"kw2\", ...]}}
        """
        response = ollama.chat(
            model=self.model_name, 
            format="json",
            messages=[{"role": "user", "content": prompt}])
        raw_content = response['message']['content']
        try:
            content_json = json.loads(raw_content)
            keywords = content_json.get("keywords", [])
        except json.JSONDecodeError:
            print(f"Error decoding JSON from Ollama response: {raw_content}")
            keywords = []
        return keywords
    
    def extract_contact_ollama(self, text: str) -> dict:

        prompt = f"""
        Extract the emails and affiliations from the following text:\n\n
        {text}\n\n
        Return the contact information in a JSON format: {{\"emails\": [], \"affiliations\": []}}. 
        The affiliations should be started by words like "University of", "Institute of", "Department of", etc. 
        Combine department and university names into one full string.
        Don't add any keys to the JSON object. Don't guess if you don't see any contact information in the text.
        """
        response = ollama.chat(
            model=self.model_name, 
            format="json", 
            messages=[{"role": "user", "content": prompt}], 
            options={"temperature": 0.0}
            )
        raw_content = response['message']['content']
        try:
            content_json = json.loads(raw_content)
            return content_json
        except json.JSONDecodeError:
            print(f"Error decoding JSON from Ollama response: {raw_content}")
            return {"emails": [], "affiliations": []}