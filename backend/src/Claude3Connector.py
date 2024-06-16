from anthropic import AnthropicBedrock
import base64
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse
import requests, io


class Claude3Connector:

    def __init__(self, aws_access_key=None, aws_secret_key=None, aws_session_token=None, aws_region='us-west-2'):
        self.model_ids = {
            "haiku": 'anthropic.claude-3-haiku-20240307-v1:0',
            "sonnet": 'anthropic.claude-3-sonnet-20240229-v1:0',
            "opus": 'anthropic.claude-3-opus-20240229-v1:0',
        }

        self.latest_message = None
        self.latest_query = None
        self.client = None

        self.set_secret(
            aws_access_key,
            aws_secret_key,
            aws_session_token,
            aws_region
        )

    def set_secret(self, aws_access_key, aws_secret_key, aws_session_token, aws_region):
        self.client = AnthropicBedrock(
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_session_token=aws_session_token,
            aws_region=aws_region
        )
        return

    def __PIL_to_bytes(self, img, size_max=1000):
        # 大きすぎる場合リサイズ
        if (2*size_max) < sum(img.size):
            sp = 1 + (max(img.size) // size_max)
            img = img.resize((img.width // sp, img.height // sp))

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        data = base64.b64encode(buffered.getvalue())

        return data


    def __image_file_to_bytes(self, file_path, size_max=1000):
        # urlの場合
        if urlparse(file_path).scheme.startswith('http'):
            img = Image.open(io.BytesIO(requests.get(file_path).content))
        # ファイルの場合
        else:
            img = Image.open(file_path)

        data = self.__PIL_to_bytes(img, size_max=size_max)

        return data

    def __image_json_from_bytes(self, content):
        image_media_type = "image/png"
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_media_type,
                "data": content.decode('utf-8'),
            },
        }

    def __image_json_from_file(self, file_path, size_max=1000):
        content = self.__image_file_to_bytes(file_path, size_max)
        return self.__image_json_from_bytes(content)

    def __image_json_from_PIL(self, img, size_max=1000):
        content = self.__PIL_to_bytes(img, size_max=size_max)
        return self.__image_json_from_bytes(content)

    def __text_json(self, user_input):
        return {
            "type": "text",
            "text": user_input
        }

    def query(self, user_input, images=[], model_key="haiku", max_tokens=500):
        if isinstance(images, str) or isinstance(images, Image.Image):
            images = [images]

        content = []
        for image in images:
            if isinstance(image, str):
                content.append(self.__image_json_from_file(image))
            elif isinstance(image, bytes):
                content.append(self.__image_json_from_bytes(image))
            elif isinstance(image, Image.Image):
                content.append(self.__image_json_from_PIL(image))
        content.append(self.__text_json(user_input))

        q = [{"role": "user", "content": content}]
        self.latest_query = q

        try:
            message = self.client.messages.create(
                model=self.model_ids[model_key],
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": content}]
            )
            self.latest_message = message

            return message.content[0].text
        except Exception as e:
            print(e)
            raise e
