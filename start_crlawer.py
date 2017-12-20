from base_crawler.spiders.xinli001 import main
import os
import re

try:
    main()
except KeyboardInterrupt as e:
    print('\033[1;31m强行终止！\033[0m')
