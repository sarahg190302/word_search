class EmailAddressAlreadyExistsError(Exception):
    message = "Email Already Exists"

class InvalidLoginDetails(Exception):
    message = "Invalid Login Details"

class WordNotFound(Exception):
    message = "Word Not Found"