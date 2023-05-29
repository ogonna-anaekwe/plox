class Break(Exception):
    """Handles break."""

    def __init__(self, keyword):
        self.keyword = keyword
        super().__init__(self.keyword)
