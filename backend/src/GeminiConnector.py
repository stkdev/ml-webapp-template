import google.generativeai as genai
from PIL import Image
from urllib.parse import urlparse
import requests, io


class GeminiConnector:

    def __init__(self, google_api_key=None, model_key="flash"):
        self.model_ids = {
            "embedding": {
                "id": 'models/embedding-001',
                "task_type": {
                    "RETRIEVAL_QUERY": "retrieval_query",
                    "RETRIEVAL_DOCUMENT": "retrieval_document",
                    "SEMANTIC_SIMILARITY": "semantic_similarity",
                    "CLASSIFICATION": "classification",
                    "CLUSTERING": "clustering",
                },
            },
            "flash": 'gemini-1.5-flash-001',
            "pro": 'gemini-pro-vision',
        }

        self.latest_message = None
        self.latest_query = None
        self.client = None

        self.set_secret(
            google_api_key,
            model_key,
        )

    def set_secret(self, google_api_key, model_key):
        genai.configure(api_key=google_api_key)

        self.client = genai.GenerativeModel(self.model_ids.get(model_key))
        return

    def __image_file_to_PIL(self, file_path, size_max=1000):
        # urlの場合
        if urlparse(file_path).scheme.startswith('http'):
            img = Image.open(io.BytesIO(requests.get(file_path).content))
        # ファイルの場合
        else:
            img = Image.open(file_path)

        # 大きすぎる場合リサイズ
        if (2*size_max) < sum(img.size):
            sp = 1 + (max(img.size) // size_max)
            img = img.resize((img.width // sp, img.height // sp))

        return img

    def query(self, user_input, images=[]):
        if isinstance(images, str):
            images = [images]

        content = []
        for image in images:
            if isinstance(image, str):
                content.append(self.__image_file_to_PIL(image))
            elif isinstance(image, Image.Image):
                content.append(image)
            else:
                content.append(image)
        content.append(user_input)

        q = content
        self.latest_query = q

        try:
            message = self.client.generate_content(q)
            self.latest_message = message

            return message.text
        except Exception as e:
            print(e)
            raise e

    def embed(self, user_input, model_key="embedding", type_key="RETRIEVAL_DOCUMENT"):
        if type(user_input) == str:
            user_input = [user_input]

        model_id = self.model_ids.get(model_key).get("id")
        type_id = self.model_ids.get(model_key).get("task_type").get(type_key)

        message = genai.embed_content(
            model=model_id,
            content=user_input,
            task_type=type_id
        )

        return message["embedding"]
