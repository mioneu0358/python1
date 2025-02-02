from openai import OpenAI
from dotenv import load_dotenv
import base64
import os
from datetime import datetime

load_dotenv()
org = os.getenv('ORG_NAME')
key = os.getenv('OPEN_API_KEY')
client = OpenAI(
    organization=org,
    api_key=key,
)
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = f"{datetime.now()}.jpg"
base64_image = encode_image(image_path)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "이미지 안에 있는 글자들을 읽어서 요약본을 만들어서 보여줘. 코드는 필요없고 단순 텍스트로만 보여줘.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
)
text = response.choices[0].message.content
print(text)
from gtts import gTTS
tts = gTTS(text=text, lang='ko')
tts.save("summary_tts.mp3")
