from bs4 import BeautifulSoup


class MedexParser:

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def parse(self) -> dict|None:
        data = dict()

        if not self.is_available():
            return None

        data['type'] = self.parse_type()
        data['name'] = self.parse_name()
        data['generic_group'] = self.parse_group()
        data['price'] = self.parse_price()
        data['pack_size_info'] = self.parse_pack_size()
        data['strip_price'] = self.parse_strip_price()
        data['indications'] = self.parse_section('indications')
        data['pharmacology'] = self.parse_section('mode_of_action')
        data['dosage'] = self.parse_section('dosage')
        data['interaction'] = self.parse_section('interaction')
        data['contraindications'] = self.parse_section('contraindications')
        data['side_effects'] = self.parse_section('side_effects')
        data['pregnancy_cat'] = self.parse_section('pregnancy_cat')
        data['precautions'] = self.parse_section('precautions')
        data['pediatric_uses'] = self.parse_section('pediatric_uses')
        data['drug_classes'] = self.parse_section('drug_classes')
        data['storage_conditions'] = self.parse_section('storage_conditions')

        return data

    def is_available(self) -> bool:
        code = self.soup.find('div', class_='code')
        if code:
            if code.text == '404':
                return False
        else:
            return True

    def parse_name(self) -> str:
        # Find the <small> tag
        small_tag = self.soup.find('small', class_='h1-subtitle')

        # If <small> tag exists, decompose it to remove it from the tree
        if small_tag:
            small_tag.decompose()

        # Find the <h1> tag and get its text, excluding any remaining child elements
        h1_tag = self.soup.find('h1', class_='page-heading-1-l brand')

        return h1_tag.text.strip()

    def parse_type(self) -> str:
        small_tag = self.soup.find('small', class_='h1-subtitle')
        return small_tag.text.strip()

    def parse_group(self) -> str:
        return self.soup.find('div', title='Generic Name').text.strip()

    def parse_manufacturer(self) -> str:
        return self.soup.find('div', title='Manufactured by').text.strip()

    def parse_price(self) -> str:
        unit_price_span = self.soup.find('span', string='Unit Price:')
        if unit_price_span is None:
            return ""
        else:
            return unit_price_span.find_next_sibling('span').text.strip()

    def parse_pack_size(self) -> str:
        return self.soup.find('span', class_='pack-size-info').text.strip()

    def parse_strip_price(self) -> str:
        strip_price_span = self.soup.find('span', string='Strip Price:')
        if strip_price_span is None:
            return ""
        else:
            return strip_price_span.find_next_sibling('span').text.strip()

    def parse_section(self, section: str) -> str:
        return self.soup.find(id=section).find_next_sibling().text.strip()
