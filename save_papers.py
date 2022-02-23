# ex) python save_papers.py --keywords generative,gan --conference ICCV2021
# ex) python save_papers.py --keywords lower --conference NeurIPS2021
import argparse
from tqdm import tqdm
import os
import requests
from bs4 import BeautifulSoup


def search_on_CVF(args):
    assert type(args.keywords) == tuple
    results = []

    url = 'https://openaccess.thecvf.com/{}?day=all'.format(args.conference)

    r = requests.get(url=url)

    bs = BeautifulSoup(r.text, 'lxml')

    paper_list = bs.find_all('dt', {'class': 'ptitle'})

    count = 0
    for paper_title in paper_list:
        for keyword in args.keywords:
            if keyword.lower() in paper_title.text.lower():
                split_href = paper_title.a['href'].split('/')
                split_href[3] = 'papers'
                href = '/'.join(split_href)
                href = href[:-4] + 'pdf'
                results.append((paper_title.text, href))
                count += 1
                break
    print('================================')
    print("FOUND [{}] papers with [{}] in [{}]".format(count, args.keywords, args.conference))
    print('================================')

    return results


# presentation_type, keyword_to_search
def search_on_openreview(args):
    presentation_type_limited = ['Poster', 'Oral', 'Spotlight', 'Submitted', 'Accepted']
    assert args.presentation_type in presentation_type_limited
    assert type(args.keywords) == tuple

    search_type = presentation_type_limited[:3] if args.presentation_type == 'Accepted' else [args.presentation_type]

    year = args.conference[-4:]
    venue = args.conference[:-4]

    results = []

    for search_type_each in search_type:

        url = 'https://api.openreview.net/notes?content.venue={}+{}+{}' \
              '&details=replyCount&offset=0&limit=5000' \
              '&invitation={}.cc%2F{}%2FConference%2F-%2FBlind_Submission'.format(venue, year, search_type_each, venue, year)

        header = {
            "authority": "api.openreview.net",
            "method": "GET",
            "path": url,
            "scheme": "https",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "access-control-allow-origin": "*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "_ga=GA1.2.1010458739.1641463521; _gid=GA1.2.627298767.1645402658; _gat_gtag_UA_108703919_1=1",
            "origin": "https://openreview.net",
            "referer": "https://openreview.net/",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.80 Safari/537.36"
        }

        r = requests.get(url, headers=header)

        tot_contents = r.json()
        print('================================')
        print("TOTAL [{}] papers in [{}]".format(len(tot_contents['notes']), search_type_each))

        count = 0
        for content in tot_contents['notes']:
            for keyword in args.keywords:
                if keyword.lower() in content['content']['title'].lower():
                    results.append((content['content']['title'], content['content']['pdf']))
                    count += 1
                    break

        print("FOUND [{}] papers with [{}] in [{}]".format(count, args.keywords, search_type_each))
        print('================================')

        r.close()

    print("FOUND [{}] papers with [{}]".format(len(results), args.keywords))

    return results


def save_as_pdf_files(args, conference_type, list_of_papers):
    url_prefix_dict = {'cvf': 'https://openaccess.thecvf.com', 'openreview': 'https://openreview.net'}
    url_prefix = url_prefix_dict[conference_type.lower()]

    save_dir = os.path.join('./', args.res_dir, args.keywords_as_str)
    print("PDFs will be saved in", save_dir)

    os.makedirs(save_dir, exist_ok=True)

    for paper in tqdm(list_of_papers):
        url_paper = url_prefix + paper[1]
        filename = os.path.join(save_dir, paper[0]+'.pdf')

        if os.path.exists(filename):
            print(filename, 'is already downloaded')
            continue

        with open(filename, "wb") as f:
            resp = requests.get(url_paper)
            f.write(resp.content)


parser = argparse.ArgumentParser(description='Conference paper save module')
parser.add_argument('--keywords')
parser.add_argument('--conference', default='ICCV2021')
parser.add_argument('--presentation_type', default='Accepted', choices=['Poster', 'Oral', 'Spotlight', 'Submitted', 'Accepted'])

args = parser.parse_args()

args.res_dir = args.conference

args.keywords_as_str = args.keywords

args.keywords = tuple(args.keywords.split(","))

cvf_dict = ['ICCV', 'CVPR', 'WACV', 'ACCV']

conference_type = 'openreview'
for cvf in cvf_dict:
    if cvf in args.conference:
        conference_type = 'cvf'

if conference_type == 'cvf':
    res = search_on_CVF(args)
else:
    res = search_on_openreview(args)

save_as_pdf_files(args, conference_type, res)
