from requests import get

result = get(
    url="http://localhost:8000/translate",
    params={'source_language': 'en', 'destination_language': 'de', 'text': 'hello world!'}
)

print(result.content)