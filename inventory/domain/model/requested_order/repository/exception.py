from pymongo.errors import DuplicateKeyError

from ....base.repository import EntityOutdated


class InvalidOrderIdException(Exception):
    pass


class OrderNotFoundException(Exception):
    pass


class OrderSubmittedException(Exception):
    pass


class InvalidOrderItemAmountException(Exception):
    pass
