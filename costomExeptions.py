class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidGenreError(Error):
    """Raised when an invalid genre is provided"""
    pass


class MissingFieldsError(Error):
    """Raised when a required field is missing"""
    pass


class APIServiceError(Error):
    """Raised when there's a problem with an external API service"""
    pass


class NotFoundError(Error):
    """Raised when an ISBN is not found in Google Books"""
    pass


class BookAlreadyExistsError(Error):
    """Raised when a book already exists in the collection"""
    pass
