class FileTypeException(Exception):
    """
    Custom Exception class responsible for
    unknown file type
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return 'Unkwonn file type\n'
