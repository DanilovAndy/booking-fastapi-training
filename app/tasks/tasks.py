from pathlib import Path

from app.tasks.celery_config import celery_app
from PIL import Image


@celery_app.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(path)
    im_resized = im.resize((1000, 500))
    im_resized_2 = im.resize((200, 100))
    im_resized.save(f"app/static/images/resized1_{im_path.name}")
    im_resized_2.save(f"app/static/images/resized2_{im_path.name}")

