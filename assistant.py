import uuid
import requests
import json

api_key = "e1365358-9b2b-4973-b8b4-d31f2450c60c"


def get_response(text, contact, r):
    if r.get(contact) is None:
        r.set(contact, json.dumps({
            "messages": [],
            "chatbotId": "PL6svYtxs4Y3m2ZZ7o6kI",
            "stream": False,
            "temperature": 0,
            "conversationId": str(uuid.uuid4()),
        }))

    data = json.loads(r.get(contact))

    data["messages"].append({"role": "user", "content": text})

    response = requests.post('https://www.chatbase.co/api/v1/chat', headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }, data=json.dumps(data))

    response = response.json()['text']

    data["messages"].append({"role": "assistant", "content": response})

    r.set(contact, json.dumps(data))

    return response
