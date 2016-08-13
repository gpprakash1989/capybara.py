from capybara.exceptions import ExpectationNotMet
from capybara.queries.selector_query import SelectorQuery
from capybara.queries.text_query import TextQuery


class MatchersMixin(object):
    def has_selector(self, *args, **kwargs):
        """
        Checks if a given selector is on the page or a descendant of the current node. ::

            session.has_selector("p#foo")
            session.has_selector("xpath", ".//p[@id='foo']")

        ``has_selector`` can also accept XPath expressions generated by the ``xpath-py`` package::

            from xpath import dsl as x

            session.has_selector("xpath", x.descendant("p"))

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            bool: If the expression exists.
        """

        try:
            self.assert_selector(*args, **kwargs)
            return True
        except ExpectationNotMet:
            return False

    def assert_selector(self, *args, **kwargs):
        """
        Asserts that a given selector is on the page or a descendant of the current node. ::

            session.assert_selector("p#foo")

        ``assert_selector`` can also accept XPath expressions generated by the ``xpath-py``
        package::

            from xpath import dsl as x

            session.assert_selector("xpath", x.descendant("p"))

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            True

        Raises:
            ExpectationNotMet: The given selector did not match.
        """

        query = SelectorQuery(*args, **kwargs)

        @self.synchronize
        def assert_selector():
            result = query.resolve_for(self)

            if not len(result):
                raise ExpectationNotMet(result.failure_message)

            return True

        return assert_selector()

    def has_xpath(self, query, **kwargs):
        """
        Checks if a given XPath expression is on the page or a descendant of the current node. ::

            session.has_xpath(".//p[@id='foo']")

        ``has_xpath`` can also accept XPath expressions generated by the ``xpath-py`` package::

            from xpath import dsl as x

            session.has_xpath(x.descendant("p"))

        Args:
            query (str): An XPath expression.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Return:
            bool: If the expression exists.
        """

        return self.has_selector("xpath", query, **kwargs)

    def has_css(self, path, **kwargs):
        """
        Checks if a given CSS selector is on the page or a descendant of the current node. ::

            session.has_css("p#foo")

        Args:
            path (str): A CSS selector.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Return:
            bool: If the selector exists.
        """

        return self.has_selector("css", path, **kwargs)

    def has_button(self, locator, **kwargs):
        """
        Checks if the page or current node has a button with the given text, value, or id.

        Args:
            locator (str): The text, value, or id of a button to check for.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            bool: Whether it exists.
        """

        return self.has_selector("button", locator, **kwargs)

    def has_link(self, locator, **kwargs):
        """
        Checks if the page or current node has a link with the given text or id.

        Args:
            locator (str): The text or id of a link to check for.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            bool: Whether it exists.
        """

        return self.has_selector("link", locator, **kwargs)

    def assert_text(self, *args, **kwargs):
        """
        Asserts that the page or current node has the given text content, ignoring any HTML tags.

        Args:
            *args: Variable length argument list for :class:`TextQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`TextQuery`.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the assertion hasn't succeeded during the wait time.
        """

        query = TextQuery(*args, **kwargs)

        @self.synchronize
        def assert_text():
            matches = query.resolve_for(self)

            if not matches:
                raise ExpectationNotMet(query.failure_message)

            return True

        return assert_text()

    def has_text(self, *args, **kwargs):
        """
        Checks if the page or current node has the given text content, ignoring any HTML tags.

        Whitespaces are normalized in both the node's text and the passed text parameter.

        Args:
            *args: Variable length argument list for :class:`TextQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`TextQuery`.

        Returns:
            bool: Whether it exists.
        """

        try:
            return self.assert_text(*args, **kwargs)
        except ExpectationNotMet:
            return False

    has_content = has_text
    """ Alias for :meth:`has_text`. """