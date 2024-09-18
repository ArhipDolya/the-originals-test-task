class UserAlreadyExistsError(Exception):
    """Raised when a user with the given username or email already exists."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when the provided credentials are invalid."""
    pass

class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    pass