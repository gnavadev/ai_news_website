from django.core.management.base import BaseCommand
from news.models import NewsPost
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Command(BaseCommand):
    help = "Generate and save a single Brainrot Daily post"

    def handle(self, *args, **kwargs):
        headline_res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": "Create a completely absurd, fake news headline. Examples: IShowSpeed becomes white, Asmongold grows hair, Epstein becomes a priest, Joe Biden becomes a dog, Adam Sandler becomes a remote control."
            }]
        )
        headline = headline_res.choices[0].message.content

        article_res = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": f"Write a 300-word comedic satirical fake news article about: {headline}"
            }]
        )
        content = article_res.choices[0].message.content

        image_res = client.images.generate(
            model="dall-e-3",
            prompt=f"Create a realistic illustration of this headline: {headline}, again, IT NEEDS TO LOOK REA, to the point of someone looking at it and think it is just a photo",
            n=1,
            size="1024x1024"
        )
        image_url = image_res.data[0].url

        post = NewsPost.objects.create(
            headline=headline,
            content=content,
            image_url=image_url
        )

        self.stdout.write(self.style.SUCCESS(f"✅ News post created: {post.headline}"))
