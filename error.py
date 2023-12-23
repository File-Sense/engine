class AIEngineInitializationError(Exception):
    def __init__(self, message="AI ENGINE INITIALIZATION ERROR") -> None:
        self.message = message
        super().__init__(self.message)


class CaptionGenerationError(Exception):
    def __init__(self, message="CAPTION GENERATION ERROR") -> None:
        self.message = message
        super().__init__(self.message)


class ImageEmbeddingGenerationError(Exception):
    def __init__(self, message="IMAGE EMBEDDING GENERATION ERROR") -> None:
        self.message = message
        super().__init__(self.message)


class TextEmbeddingGenerationError(Exception):
    def __init__(self, message="TEXT EMBEDDING GENERATION ERROR") -> None:
        self.message = message
        super().__init__(self.message)
