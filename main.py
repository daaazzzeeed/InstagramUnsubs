import datetime
from InstaSubsAPI import *
import threading


def menu():
    print("""1 - to show unsubscribed profiles
2 - to show new subscribed profiles
3 - to show your subscribers
4 - sort by subscribers number
5 - turn on followers auto-checking
6 - turn off followers auto-checking
q - exit from the application""")


# log into instagram account
username = 'login'
password = 'password'
# create class instance
account = InstaSubsAPI(username, password)
# separate API
API = account.API
# get username
user_id = account.user_id
# create log file
file = None
# create username_log.txt file
path = username + '_log.txt'
followers_list = []

if Path(path).exists():
    # print('File exists')
    with open(path, 'r') as file:
        for follower in file:
            followers_list.append(follower.replace('\n', ''))
else:
    # print('Created file')
    file = open(path, 'w')
    # get list of followers
    followers_list = account.get_total_followers(API, user_id)
    # write followers list to a log file
    for i in range(len(followers_list)):
        username = followers_list[i]['username']
        followers_list[i] = username
        file.write(username)
        file.write('\n')
    file.close()

# spot difference in subscribers in a loop
while 1:
    try:
        menu()
        selection = input('\nChoose an option: ')
        print()
        if selection == '1':
            print(datetime.datetime.now())
            account.display_subs(account.spot_subs_difference(followers_list, API, user_id)[0])
            print()
        elif selection == '2':
            print(datetime.datetime.now())
            account.display_subs(account.spot_subs_difference(followers_list, API, user_id)[1])
            print()
        elif selection == '3':
            print(datetime.datetime.now())
            account.get_subscribers_column(account.get_total_followers(API, user_id))
        elif selection == '4':
            print(datetime.datetime.now())
            account.display_subs(account.sort_by_subscribers(account.
                                                             spot_subs_difference(followers_list, API, user_id)[0]))
            print()
        elif selection == '5' or account.auto_checking:
            account.auto_checking = True
            timer = threading.Timer(60, account.auto_check, [followers_list])
            timer.start()
            print('Auto-checking enabled\nPlease check file "log.txt" \n')
        elif selection == '6':
            account.auto_checking = False
            print('Auto-checking disabled\n')
        elif selection == 'q':
            break
    except KeyboardInterrupt:
        exit(0)
