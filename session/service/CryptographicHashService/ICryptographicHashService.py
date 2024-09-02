class ICryptographicHashService:
    def hash(self, data: str) -> (str, str):
        raise NotImplementedError()

    def is_match(self, data: str, hash_str: str) -> bool:
        raise NotImplementedError()
