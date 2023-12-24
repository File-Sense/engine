from os import path
from settings import Settings  # type: ignore
from error import VectorStoreError  # type: ignore
from typing import Dict, Sequence, Tuple, List
from chromadb import PersistentClient, Collection


class VectorStore(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(VectorStore, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        try:
            self.settings = Settings()
            self.client = PersistentClient(
                path=path.join(self.settings.ROOT_DIR, "VECTORSTORE", "vdb")
            )
        except Exception as e:
            raise VectorStoreError(message=str(e))

    def get_list_collections(self) -> Sequence[Collection]:
        return self.client.list_collections()

    def __get_or_create_collection(
        self, collection_name
    ) -> Tuple[Collection, Collection]:
        text_collection = self.client.get_or_create_collection(
            name=f"{collection_name}_text"
        )
        image_collection = self.client.get_or_create_collection(
            name=f"{collection_name}_image"
        )
        return (text_collection, image_collection)

    def upsert_to_collections(
        self,
        id_list: List[str],
        caption_list: List[str],
        caption_emb_list: List[float],
        images_emb_list: List[float],
        metadata_list: List[Dict[str, str]],
        collection_name: str,
    ):
        (text_collection, image_collection) = self.__get_or_create_collection(
            collection_name
        )

        text_collection.upsert(
            ids=id_list,
            embeddings=caption_emb_list,
            metadatas=metadata_list,  # type: ignore
            documents=caption_list,
        )

        image_collection.upsert(
            ids=id_list,
            embeddings=images_emb_list,
            metadatas=metadata_list,  # type: ignore
            documents=caption_list,
        )

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(name=f"{collection_name}_text")
        self.client.delete_collection(name=f"{collection_name}_image")

    def is_alive(self) -> int:
        return self.client.heartbeat()

    def reset_all(self) -> None:
        self.client.reset()
