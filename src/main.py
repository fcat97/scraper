import sys
from medex_dot_com.scraper import MedexScraper

if __name__ == "__main__":
    parse_next_n_url = 5
    print(sys.argv)
    if len(sys.argv) <= 1:
        print('-' * 20)
        print('parsing next 5 url. run "python /src/scraper.py 10" to parse next 10 url and so on..')
        print('-' * 20)
    else:
        parse_next_n_url = int(sys.argv[1])

    scraper = MedexScraper(
        base_url="https://medex.com.bd/brands",
        max_iter=parse_next_n_url
    )
    scraper.start_srcaping()