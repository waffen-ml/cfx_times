import g4f
from g4f.client import Client

client = Client()


for d in dir(g4f.Provider):
    if d[0].upper() != d[0] or d[0] == '_':
        continue
    provider = getattr(g4f.Provider, d)
    print(d + ': ', end='')
    try:
        response = client.chat.completions.create(
            model=g4f.models.gpt_4,
            provider=provider,
            max_tokens=1000,
            messages=[{"role": "user", "content": 'hey'}]
        )
        print(response.choices[0].message.content[:50])
    
    except Exception as ex:
        print('Error:')
        print(ex)
    
    input()

# gpt_35_turbo: FlowGpt FreeChatgpt
# gpt_4: FreeChatgpt
