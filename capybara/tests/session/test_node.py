import pytest


class NodeTestCase:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")


class TestNode(NodeTestCase):
    def test_acts_like_a_session_object(self, session):
        session.visit("/form")
        form = session.find("css", "#get-form")
        form.click_button("med")

    def test_scopes_css_selectors(self, session):
        assert not session.find("css", "#second").has_css("h1")


class TestNodeText(NodeTestCase):
    def test_extracts_node_text(self, session):
        assert session.find("//a[1]").text == "labore"
        assert session.find("//a[2]").text == "ullamco"

    def test_returns_document_text_on_html_selector(self, session):
        session.visit("/with_simple_html")
        assert session.find("/html").text == "Bar"


class TestNodeAttribute(NodeTestCase):
    def test_extracts_node_attributes(self, session):
        assert session.find("//a[1]")["class"] == "simple"
        assert session.find("//a[2]")["id"] == "foo"
        assert session.find("//input[1]")["type"] == "text"

    def test_extracts_boolean_node_attributes(self, session):
        assert session.find("//input[@id='checked_field']")["checked"]


class TestNodeValue(NodeTestCase):
    def test_allows_retrieval_of_the_value(self, session):
        assert session.find("//textarea[@id='normal']").value == "banana"

    def test_does_not_swallow_extra_newlines_in_textarea(self, session):
        assert session.find("//textarea[@id='additional_newline']").value == "\nbanana"

    def test_defaults_to_on_for_checkboxes(self, session):
        session.visit("/form")
        assert session.find("//input[@id='valueless_checkbox']").value == "on"

    def test_defaults_to_on_for_radio_buttons(self, session):
        session.visit("/form")
        assert session.find("//input[@id='valueless_radio']").value == "on"


class TestNodeChecked(NodeTestCase):
    def test_extracts_node_checked_state(self, session):
        session.visit("/form")
        assert session.find("//input[@id='gender_female']").checked is True
        assert session.find("//input[@id='gender_male']").checked is False
        assert session.find("//h1").checked is False