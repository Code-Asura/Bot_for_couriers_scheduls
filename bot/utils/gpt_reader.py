import openai

from data import config


client = openai.OpenAI(
    api_key=config.api_key.get_secret_value(),
    base_url="https://api.proxyapi.ru/openai/v1"
)


async def extract_data_with_ai(message_text: str) -> list:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': "user",
             'content': f"Извлеки данные для расписания курьеров из следующего сообщения: {message_text}"}
        ]
    )
    return response['choices'][0]['message']['content']
