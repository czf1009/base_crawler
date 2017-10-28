from base_crawler.spiders import test_crawler
import os
import re

def merge_page():
    print('start merge page')
    files = {}
    for file in os.listdir():
        if 'index' in file:
            index = int(re.findall('\d+', file)[0])
            files[index] = file 
    with open('page.html', 'w') as page:
        for index in sorted(files):
            with open(files[index], 'r') as file:
                page.write(file.read())
            os.remove(files[index])
    print('\033[1;32mmerge page complete\033[0m')
            

try:
    test_crawler.main()
except KeyboardInterrupt as e:
    print('\033[1;31m强行终止！\033[0m')

merge_page()