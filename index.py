import g4f
from g4f.client import Client
import requests
import sched, time
import random

client = Client()
AUTHOR_TAG = 'cfxtimes'
AUTHOR_PASSWORD = 'oatmeal'
DELAY = 60

HASHTAG_PROB = 0.3
NEW_TOPIC_PROB = 0
EMOJI_PROB = 0.5

FUNNY_PROB = 0.4
SAD_PROB = 0.2
ANGRY_PROB = 0.4

KHERES_PROB = 0.1
ASK_REACTION_PROB = 0.1
CAPYBARA_PROB = 0.4


def ask_gpt(prompt):
    response = client.chat.completions.create(
        model=g4f.models.gpt_4,
        provider=g4f.Provider.FreeChatgpt,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def add_post(text, title='', html=''):
    if not text:
        print('Text is empty!')
        return
    
    requests.post('https://coffeetox.ru/addpostapi', json={
        'author_tag': AUTHOR_TAG,
        'author_password': AUTHOR_PASSWORD,
        'text': text,
        'title': title,
        'html': html
    }, verify=False)


with open('topics.txt', 'r', encoding='utf-8') as f:
    topics = f.read().splitlines()

def generate_topic():
    prompt = '''
    придумай интересную актуальную тему для очень короткой статьи в соцсети. 
    Она должна провоцировать дискуссии и споры. Эта тема может быть как обширной, так и связана с 
    разными мелочами в нашей жизни. Она должна вызывать реальные эмоции у читателя: 
    гнев, ярость, печаль или радость! Не пиши про природу и технологии. 
    Тема должна быть социальной. Одним предложением напиши придуманную статью'''

    return ask_gpt(prompt)

def choose_topic():
    return random.choice(topics)

def randbin(f):
    return random.uniform(0, 1) < f

def generate_prompt():
    topic = generate_topic() if randbin(NEW_TOPIC_PROB) else choose_topic()

    print(topic)

    prompt = f'''Ты -- умная капибара-редактор на сайте coffeetox.ru. Напиши публикацию на тему {topic}.
    Твоя публикация должна быть мотивирующей, интересной и воодушевляющей.
    Уложись в один маленький абзац, будто ты пишешь твит. Не пиши более 4 предложений.
    Помни, что ты пишешь его таким же капибарам, любящим кофе.
    Они должны поразиться, читая твой прекрасный пост, наполненный средствами выразительности. '''

    if randbin(ANGRY_PROB):
        prompt += ' Агрессивно, с яростью выскажи свое мнение об этом.'
    elif randbin(FUNNY_PROB):
        prompt += ' Разбавь статью юмором, сделай ее смешной.'
    elif randbin(SAD_PROB):
        prompt += ' С болью в душе, с грустью констатируй невеселые факты, о которых скажешь.'

    if randbin(KHERES_PROB):
        prompt += ' Не забудь упомянуть напиток херес!'
    if randbin(CAPYBARA_PROB):
        prompt += ' Не забудь упомянуть капибар!'

    if randbin(HASHTAG_PROB):
        prompt += ' Также добавь пару хештегов.'
    
    if randbin(EMOJI_PROB):
        prompt += ' Добавь эмоджи.'
    
    if randbin(ASK_REACTION_PROB):
        prompt += ' В конце поста необычно, изобретательно попроси читателей поставить лайк и написать комментарий.'

    return prompt


def schedule_post():
    scheduler.enter(max(DELAY, 1), 1, create_post)

def create_post():
    try:
        print('Generating post...')
        prompt = generate_prompt()
        response = ask_gpt(prompt)
        add_post(response.replace('**', ''))
        print('Added post!')
    except Exception as ex:
        print('Error:', ex)
    
    schedule_post()


scheduler = sched.scheduler(time.time, time.sleep)
create_post()
scheduler.run()

