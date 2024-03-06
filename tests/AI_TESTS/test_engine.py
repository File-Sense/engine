from os import path
import pytest
from ...AI.engine import AIEngine  # type: ignore
from ...settings import Settings


@pytest.fixture
def ai_engine():
    return AIEngine()


@pytest.fixture
def settings():
    return Settings()


def test_generate_caption(ai_engine, settings):
    img_path = path.join(settings.ROOT_DIR, "static", "demo.jpg")
    caption = ai_engine.generate_caption(img_path)
    assert isinstance(caption, str)


def test_generate_text_embedding(ai_engine):
    text = ["This is a sample text"]
    embedding = ai_engine.generate_text_embedding(text)
    assert isinstance(embedding, list)


def test_generate_image_embedding(ai_engine, settings):
    img_path = path.join(settings.ROOT_DIR, "static", "demo.jpg")
    embedding = ai_engine.generate_image_embedding(img_path)
    assert isinstance(embedding, list)
