import requests
from bs4 import BeautifulSoup as bs4


def scrap_page_links(curr_url, tag, tag_class):
    page = requests.get(curr_url)
    soup = bs4(page.text, 'html.parser')
    x = []
    for header in soup.findAll(tag, attrs={'class': tag_class}):
        if header.has_attr('href'):
            x.append(header['href'])
        else:
            x.append(header.find('a', href=True)['href'])
    return x


# Print iterations progress

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (

        - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def get_last_pagination_num():
    numbers = []
    main_url = 'https://smartybro.com/'
    page = requests.get(main_url)
    soup = bs4(page.text, 'html.parser')
    pagination_links = [a for a in soup.findAll('a', attrs={'class': 'page-numbers'})]
    for a in pagination_links:
        try:
            numbers.append(int(a.text.strip()))
        except Exception as e:
            print('--- Not a number --- ')
    return max(numbers)


# Main


temp_scrapped_links = []
print('---  ---- --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- --- --- ')
print('--- Getting Max number  --- ')
last_pagination_num = get_last_pagination_num()
print('---  ---- --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- --- --- ')
print('--- Scraping links from SmartyBro --- ')
print_progress_bar(0, last_pagination_num, prefix='Progress:', suffix='Complete', length=50)
for page_num in range(0, last_pagination_num):
    temp_scrapped_links.append(scrap_page_links('https://smartybro.com/page/'+str(page_num)+'/', 'h2', 'grid-tit'))
    print_progress_bar(page_num+1, last_pagination_num, prefix='Progress:', suffix='Complete', length=50)

flat_scrapped_links = [item for sublist in temp_scrapped_links for item in sublist]

print('--- Scraping Finished --- ')
print('---  ---- --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- --- --- ')
print('--- Scraping for Udemy links --- ')
temp_scrapped_links = []
count = 0
print_progress_bar(0, len(flat_scrapped_links), prefix='Progress:', suffix='Complete', length=50)
for url in flat_scrapped_links:
    count += 1
    temp_scrapped_links.append(scrap_page_links(url, 'a', 'fasc-button'))
    print_progress_bar(count, len(flat_scrapped_links), prefix='Progress:', suffix='Complete', length=50)

flat_scrapped_links = [item for sublist in temp_scrapped_links for item in sublist]

print('--- Scraping Finished --- ')
print('---  ---- --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- --- --- ')
print('--- Generating Udemy links --- ')
file = open("all_links.txt", "w+")
for brainy_link in flat_scrapped_links:
    file = open("all_links.txt", "a")
    file.write(brainy_link + "\n")
    file.close()
print('--- Writing Udemy links Finished --- ')
print('---  ---- --- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- --- --- ')


