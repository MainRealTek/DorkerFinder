from colorama import Fore,Back,Style
from protocol.cmd_scanner import web_scraper
from time import sleep
from sys import exit
import os


banner = """
 ___                 _      ___    _             _              
(  _`\              ( )    (  _`\ (_)           ( )             
| | ) |   _    _ __ | |/') | (_(_)| |  ___     _| |   __   _ __ 
| | | ) /'_`\ ( '__)| , <  |  _)  | |/' _ `\ /'_` | /'__`\( '__)
| |_) |( (_) )| |   | |\`\ | |    | || ( ) |( (_| |(  ___/| |   
(____/'`\___/'(_)   (_) (_)(_)    (_)(_) (_)`\__,_)`\____)(_)   
Developed by MainRealTek
"""

def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def p_green(string):
    print(Fore.GREEN+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def p_red(string):
    print(Fore.RED+Style.BRIGHT+string+Fore.RESET+Style.RESET_ALL)

def main():

    p_green(banner)
    sleep(2.5)
    clear()
    try:
        keywrld = str(input('Choose the file name of keyworlds\n\n'))
        proxy = str(input('Choose the file name of proxy(only one proxy in file)\n\n'))
        dorks = str(input('Choose the file name of dorks\n\n'))
        output_file = str(input('Choose the file name of output\n\n'))
        clear()
    except Exception as i:
        p_red('\n\nSomething went wrong\n\nTRY AGAIN!')


    obj =  web_scraper(keyworlds_list=keywrld,list_proxy=proxy,list_dork=dorks,out_file=output_file)
    len_found = obj.main()
    

    p_green('\n\n\nFOUND --->'+str(len_found)+'\n\n\n')




if __name__ == '__main__':
    main()