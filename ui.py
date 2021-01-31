import logging
import sys
import os

from bullet import Check, colors

# cli = Check(prompt = "Choose from the items below: ", 
#     choices = ['yes', 'no'])  # Create a Bullet or Check object
# result = cli.launch()  
# print (result)

def interrupt_dl():
    logging.info("Download aborted by Ctrl+c")
    try:
        return yesno("Do you like to mark item as played? (y/n) or quit? (Ctrl+c): ")
    except KeyboardInterrupt:
        print("\nQuitting")
        sys.exit()

def yesno(prompt):
    user_wish = input(prompt + ' [y/n]  ')
    return user_wish and 'yes'.startswith(user_wish.lower()) 

def mark_deletion(dir):
    filenames = sorted(os.listdir(dir), reverse=True)
    if filenames:
        cli = Check(choices = filenames, check='X ', check_color=colors.foreground['red'])
        return cli.launch()
