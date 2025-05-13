
RUN = 'python3 main.py'

from pysrc.gen_html import generate_html_output
from pysrc.gen_json import generate_json_output
from pysrc.fetch_data import fetch_all_character
import sys

def help():
    print("Help: ")
    print(f"{RUN} clean\t\t clean the output.")
    print(f"{RUN} gen\t\t generate HTML and json.")
    print(f"{RUN} fetch\t\t fetch data from official site.")

if len(sys.argv) <= 1:
    help()
    exit()

para = sys.argv[1]

if para == 'gen':
    generate_json_output()
    generate_html_output()

elif para == 'fetch':
    fetch_all_character()

elif para == 'clean':
    pass

else:
    help()
