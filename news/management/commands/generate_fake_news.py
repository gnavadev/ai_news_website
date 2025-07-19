from django.core.management.base import BaseCommand
from news.models import NewsPost
from openai import OpenAI
import os
from django.core.files.storage import default_storage
import requests
from django.utils.text import slugify
from datetime import datetime
from django.core.files.base import ContentFile

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
            prompt=f"A high-resolution, ultra-realistic photograph of: {headline}. It should look like a real news photo taken by a professional journalist with a DSLR camera. Natural lighting, no illustration or painting style, just pure realism. People should think it's an actual photo from a news agency like Reuters or AP.",
            n=1,
            size="1024x1024"
        )
        temp_url = image_res.data[0].url
        response = requests.get(temp_url)
        if response.status_code == 200:
            image_name = f"{slugify(headline)}.png"
            image_file = ContentFile(response.content)
            image_file.name = image_name
        else:
            image_file = None  

        post = NewsPost.objects.create(
            headline=headline,
            content=content,
            image_url=image_file  
        )

        self.stdout.write(self.style.SUCCESS(f"✅ News post created: {post.headline}"))
