from bs4 import BeautifulSoup
from medex_dot_com.utils import safe_run
from domain.parser import Parser

class MedexParser(Parser):
    def __init__(self):
        pass

    def parse(self, html) -> dict|None:
        soup = BeautifulSoup(html, 'html.parser')
        data = dict()

        if not self.is_available(soup):
            return None

        data['type'] = self.parse_type(soup)
        data['name'] = self.parse_name(soup)
        data['generic_group'] = self.parse_group(soup)
        data['price'] = self.parse_price(soup)
        data['pack_size_info'] = self.parse_pack_size(soup)
        data['strip_price'] = self.parse_strip_price(soup)
        data['indications'] = self.parse_section(soup, 'indications')
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

        return data

    def is_available(self, soup: BeautifulSoup) -> bool:
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
    def parse_type(self, soup: BeautifulSoup) -> str:
        small_tag = soup.find('small', class_='h1-subtitle')
        return small_tag.text.strip()

    @safe_run
    def parse_group(self, soup: BeautifulSoup) -> str:
        return soup.find('div', title='Generic Name').text.strip()

    @safe_run
    def parse_manufacturer(self, soup: BeautifulSoup) -> str:
        return soup.find('div', title='Manufactured by').text.strip()

    @safe_run
    def parse_price(self, soup: BeautifulSoup) -> str:
        unit_price_span = soup.select_one('.package-container > span:nth-of-type(2)')
        if unit_price_span is None:
            return ""
        else:
            return unit_price_span.text.strip()

    @safe_run
    def parse_pack_size(self, soup: BeautifulSoup) -> str:
        return soup.find('span', class_='pack-size-info').text.strip()

    @safe_run
    def parse_strip_price(self, soup: BeautifulSoup) -> str:
        strip_price_span = soup.select_one('.package-container div > span:nth-of-type(2)')
        if strip_price_span is None:
            return ""
        else:
            return strip_price_span.text.strip()

    @safe_run
    def parse_section(self, soup: BeautifulSoup, section: str) -> str:
        return soup.find(id=section).find_next_sibling().text.strip()
