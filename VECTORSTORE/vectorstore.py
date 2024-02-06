from pathlib import Path
from os import path, mkdir
from typing import Dict, Sequence, Tuple, List
from error import VectorstoreInitializationError  # type: ignore
from chromadb import PersistentClient, Collection


class VectorStore(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(VectorStore, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        try:
            filesense_path = path.join(Path.home(), ".filesense")
            if not path.exists(filesense_path):
                mkdir(filesense_path)
            self.client = PersistentClient(path=path.join(filesense_path))
        except Exception as e:
            raise VectorstoreInitializationError(message=str(e))

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

    def get_img_path_list(
        self, collection: Collection, query_emb: List[float], limit: int
    ) -> List[str]:
        results = collection.query(query_embeddings=query_emb, n_results=limit)
        img_path_list = [
            value["path"] for result in results["metadatas"] for value in result  # type: ignore
        ]
        return img_path_list  # type: ignore

    def search_by_text(
        self, text_emb: List[float], collection_name: str, limit: int
    ) -> List[str]:
        text_collection = self.client.get_collection(name=f"{collection_name}_text")
        return self.get_img_path_list(text_collection, text_emb, limit)

    def search_by_image(
        self, img_emb: List[float], collection_name: str, limit: int
    ) -> List[str]:
        image_collection = self.client.get_collection(name=f"{collection_name}_image")
        return self.get_img_path_list(image_collection, img_emb, limit)

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(name=f"{collection_name}_text")
        self.client.delete_collection(name=f"{collection_name}_image")

    def is_alive(self) -> int:
        return self.client.heartbeat()

    def reset_all(self) -> None:
        self.client.reset()
