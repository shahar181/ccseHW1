class Error(Exception):
    """Base class for other exceptions"""
    pass

class MissingFieldsError(Error):
    """Raised when a required field is missing"""
    pass

class InvalidLoanIdException(Error):
    """Raised when an invalid loan id is used"""
    pass

class APIServiceError(Error):
    """Raised when there's a problem with an external API service"""
    pass


class NotFoundError(Error):
    """Raised when an ISBN is not found in Google Books"""
    pass

class BookNotInBooksError(Error):
    """Raised when a required book for loan is not in /books"""
    pass

