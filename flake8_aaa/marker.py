import tokenize

from .exceptions import NotAMarker


class TokenWrapper:
    """
    A wrapper around tokens from ``tokenize.generate_tokens`` which can be
    ``tuple`` or ``TokenInfo``.

    Attributes:
        _token: Original token that is wrapped
        type (int): Type of Token
        string (str): Content of Token
    """

    def __init__(self, token):
        """
        Sorry this is horrible. Will be cleaned up when back on green.
        """
        self._token = token
        try:
            self.type = self._token.type
        except AttributeError:
            self.type = self._token[0]
        try:
            self.string = self._token.string
        except AttributeError:
            self.string = self._token[1]
        try:
            self.start = self._token.start
        except AttributeError:
            self.start = self._token[2]


class Marker:
    """
    A wrapper around comment tokens that are AAA markers.

    Attributes:
        token (TokenWrapper)
    """

    def __init__(self, token):
        self.token = token

    @classmethod
    def build(obj, token):
        """
        Args:
            token (TokenWrapper): Any type of token can be passed.

        Returns:
            Marker: Token is a comment and a flake8 AAA marker then a Marker is
                returned wrapping the token.

        Raises:
            NotAMarker: Token is not a comment and not an AAA marker.
        """
        token = TokenWrapper(token)
        if token.type == tokenize.COMMENT and token.string.lower() == '# aaa act':
            return obj(token)
        raise NotAMarker()
