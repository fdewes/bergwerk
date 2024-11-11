import data.wiki as data
from model.section import Section
from model.sectionwikitext import SectionWikitext
from requests import ConnectionError
import responses
import json

M1 = json.loads(
    """
{
    "parse": {
        "pageid": 2,
        "title": "Start",
        "wikitext": {
            "*": "== Text ==\\nLorem ipsum dolor sit amet, consectetur adipiscing elit."
        }
    }
}
""")

M2 = json.loads(
    """
    {
    "parse": {
        "pageid": 2,
        "sections": [
            {
                "anchor": "Deutsch",
                "byteoffset": 0,
                "fromtitle": "Start",
                "index": "1",
                "level": "1",
                "line": "Deutsch",
                "linkAnchor": "Deutsch",
                "number": "1",
                "toclevel": 1
            },
            {
                "anchor": "Markdown",
                "byteoffset": 12,
                "fromtitle": "Start",
                "index": "2",
                "level": "2",
                "line": "Markdown",
                "linkAnchor": "Markdown",
                "number": "1.1",
                "toclevel": 2
            },
            {
                "anchor": "Text",
                "byteoffset": 449,
                "fromtitle": "Start",
                "index": "3",
                "level": "2",
                "line": "Text",
                "linkAnchor": "Text",
                "number": "1.2",
                "toclevel": 2
            },
            {
                "anchor": "Buttons",
                "byteoffset": 847,
                "fromtitle": "Start",
                "index": "4",
                "level": "2",
                "line": "Buttons",
                "linkAnchor": "Buttons",
                "number": "1.3",
                "toclevel": 2
            },
            {
                "anchor": "English",
                "byteoffset": 968,
                "fromtitle": "Start",
                "index": "5",
                "level": "1",
                "line": "English",
                "linkAnchor": "English",
                "number": "2",
                "toclevel": 1
            },
            {
                "anchor": "Markdown_2",
                "byteoffset": 980,
                "fromtitle": "Start",
                "index": "6",
                "level": "2",
                "line": "Markdown",
                "linkAnchor": "Markdown_2",
                "number": "2.1",
                "toclevel": 2
            },
            {
                "anchor": "Text_2",
                "byteoffset": 1313,
                "fromtitle": "Start",
                "index": "7",
                "level": "2",
                "line": "Text",
                "linkAnchor": "Text_2",
                "number": "2.2",
                "toclevel": 2
            },
            {
                "anchor": "Buttons_2",
                "byteoffset": 1779,
                "fromtitle": "Start",
                "index": "8",
                "level": "2",
                "line": "Buttons",
                "linkAnchor": "Buttons_2",
                "number": "2.3",
                "toclevel": 2
            },
            {
                "anchor": "Training_Questions",
                "byteoffset": 1893,
                "fromtitle": "Start",
                "index": "9",
                "level": "1",
                "line": "Training Questions",
                "linkAnchor": "Training_Questions",
                "number": "3",
                "toclevel": 1
            }
        ],
        "showtoc": "",
        "title": "Start"
    }
}
"""
)

M3 = """
{
    "error": {
        "*": "See http://10.10.1.9:80/mediawiki/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.",
        "code": "missingtitle",
        "info": "The page you specified doesn't exist."
    }
}
"""

def test_unknown_host():
    try:
        d = data.get_sections(
            host="http://www.nexistentgarbage.org", page="doesnotexist")
    except ConnectionError as e:
        assert True


@responses.activate
def test_get_mock_section():
    responses.add(responses.GET,
                  'http://chatbot.local/mediawiki/api.php?action=parse&format=json&page=start&prop=wikitext&section=7',
                  json=M1, status=200)
    wt = data.get_section_wikitext(
        host="http://chatbot.local", page="start", section=7)

    example_data = SectionWikitext(host="http://chatbot.local",
                                        page="start",
                                        pageid=2,
                                        section=7,
                                        wikitext="== Text ==\nLorem ipsum dolor sit amet, consectetur adipiscing elit.")
    assert wt == example_data

@responses.activate
def test_get_mock_sections():
    responses.add(responses.GET,
                  'http://chatbot.local/mediawiki/api.php?action=parse&format=json&page=start&prop=sections',
                  json=M2, status=200)
    sections = data.get_sections(host="http://chatbot.local", page="start")

    assert sections == [Section(page='start', pageid=2, line='Deutsch',
                    index=1, number='1', toclevel=1),
            Section(page='start', pageid=2, line='Markdown',
                    index=2, number='1.1', toclevel=2),
            Section(page='start', pageid=2, line='Text',
                    index=3, number='1.2', toclevel=2),
            Section(page='start', pageid=2, line='Buttons',
                    index=4, number='1.3', toclevel=2),
            Section(page='start', pageid=2, line='English',
                    index=5, number='2', toclevel=1),
            Section(page='start', pageid=2, line='Markdown',
                    index=6, number='2.1', toclevel=2),
            Section(page='start', pageid=2, line='Text',
                    index=7, number='2.2', toclevel=2),
            Section(page='start', pageid=2, line='Buttons',
                    index=8, number='2.3', toclevel=2),
            Section(page='start', pageid=2, line='Training Questions',
                    index=9, number='3', toclevel=1)]
