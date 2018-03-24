import tokenize

from .exceptions import NotAMarker


class Marker:
    """
    A wrapper around comment tokens that are AAA markers.

    Attributes:
        token (tokenize.TokenInfo)
    """

    def __init__(self, token):
        self.token = token

    @classmethod
    def build(obj, token):
        """
        Args:
            token (tokenize.TokenInfo): Any type of token can be passed.

        Returns:
            Marker: Token is a comment and a flake8 AAA marker then a Marker is
                returned wrapping the token.

        Raises:
            NotAMarker: Token is not a comment and not an AAA marker.
        """
        if token.type == tokenize.COMMENT and token.string.lower() == '# aaa act':
            return obj(token)
        raise NotAMarker()
