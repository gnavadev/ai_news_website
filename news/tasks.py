from celery import shared_task
from .models import NewsPost
from dotenv import OPENAI_API_KEY
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

@shared_task
def generate_absurd_news():
    headline_res = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": "Create a completely absurd, fake news headline like 'BREAKING: TRUMP DOES A BACKFLIP IN CONGRESS' It doesn't need to be about trump, this is just an example, if possible, create it about one of the most popular topics of the day"
        }]
    )
    headline = headline_res['choices'][0]['message']['content']

    article_res = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Write a 300-word absurd and funny fake news article about: {headline}"
        }]
    )
    content = article_res['choices'][0]['message']['content']

    image_res = openai.Image.create(
        model="dall-e-3",
        prompt=f"Create the most realistic Absurd illustration of: {headline}",
        n=1,
        size="1024x1024"
    )
    image_url = image_res['data'][0]['url']

    NewsPost.objects.create(
        headline=headline,
        content=content,
        image_url=image_url
    )
