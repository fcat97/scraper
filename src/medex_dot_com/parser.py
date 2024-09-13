from bs4 import BeautifulSoup
from medex_dot_com.utils import safe_run
from domain.parser import Parser

class MedexParser(Parser):
    def __init__(self):
        pass

    def parse(self, html) -> dict|None:
        soup = BeautifulSoup(html, 'html.parser')
        data = dict()

        if not self.__is_available(soup):
            return None

        data['type'] = self.parse_type(soup)
        data['name'] = self.parse_name(soup)
        data['generic_group'] = self.parse_title(soup, "Generic Name")
        data['manufacturer'] = self.parse_title(soup, "Manufactured by")
        data['strength'] = self.parse_title(soup, "Strength")
        data['price'] = self.parse_price(soup)
        data['pack_size_info'] = self.parse_pack_size(soup)
        data['strip_price'] = self.parse_strip_price(soup)
        data['indications'] = self.parse_section(soup, 'indications')
        data['composition'] = self.parse_section(soup, 'composition')
        data['pharmacology'] = self.parse_section(soup, 'mode_of_action')
        data['dosage'] = self.parse_section(soup, 'dosage')
        data['interaction'] = self.parse_section(soup, 'interaction')
        data['contraindications'] = self.parse_section(soup, 'contraindications')
        data['side_effects'] = self.parse_section(soup, 'side_effects')
        data['pregnancy_cat'] = self.parse_section(soup, 'pregnancy_cat')
        data['precautions'] = self.parse_section(soup, 'precautions')
        data['pediatric_uses'] = self.parse_section(soup, 'pediatric_uses')
        data['drug_classes'] = self.parse_section(soup, 'drug_classes')
        data['storage_conditions'] = self.parse_section(soup, 'storage_conditions')
        data['overdose_effects'] = self.parse_section(soup, 'overdose_effects')
        data['compound_summary'] = self.parse_section(soup, 'compound_summary', True)
        data['commonly_asked_questions'] = self.parse_section(soup, 'commonly_asked_questions', True)

        return data

    def __is_available(self, soup: BeautifulSoup) -> bool:
        code = soup.find('div', class_='code')
        if code:
            if code.text == '404':
                return False
        else:
            return True

    @safe_run
    def parse_name(self, soup: BeautifulSoup) -> str:
        # Find the <small> tag
        small_tag = soup.find('small', class_='h1-subtitle')

        # If <small> tag exists, decompose it to remove it from the tree
        if small_tag:
            small_tag.decompose()

        # Find the <h1> tag and get its text, excluding any remaining child elements
        h1_tag = soup.find('h1', class_='page-heading-1-l brand')

        return h1_tag.text.strip()

    @safe_run
    def parse_title(self, soup, title: str) -> str|None:
        div = soup.find('div', title=title)
        if div:
            return div.text.strip()
        else:
            return None

    @safe_run
    def parse_type(self, soup: BeautifulSoup) -> str|None:
        small_tag = soup.find('small', class_='h1-subtitle')
        if small_tag:
            return small_tag.text.strip()
        else:
            return None

    @safe_run
    def parse_price(self, soup: BeautifulSoup) -> str|None:
        unit_price_span = soup.select_one('.package-container > span:nth-of-type(2)')
        if unit_price_span is None:
            return None
        else:
            return unit_price_span.text.strip()

    @safe_run
    def parse_pack_size(self, soup: BeautifulSoup) -> str|None:
        span = soup.find('span', class_='pack-size-info')
        if span:
            return span.text.strip()
        else:
            return None

    @safe_run
    def parse_strip_price(self, soup: BeautifulSoup) -> str|None:
        strip_price_span = soup.select_one('.package-container div > span:nth-of-type(2)')
        if strip_price_span is None:
            return None
        else:
            return strip_price_span.text.strip()

    @safe_run
    def parse_section(self, soup: BeautifulSoup, section: str, as_html: bool = False) -> str|None:
        span = soup.find(id=section)
        if not span:
            return None

        if as_html:
            return span.find_next_sibling().decode_contents()
        else:
            return span.find_next_sibling().text.strip()
