import pytest
from typing import Sequence
from ...VECTORSTORE.vectorstore import VectorStore  # type: ignore


@pytest.fixture
def vectorstore():
    return VectorStore()


def test_get_list_collections(vectorstore):
    assert isinstance(vectorstore.get_list_collections(), Sequence)


def test_is_alive(vectorstore):
    assert isinstance(vectorstore.is_alive(), int)
