import datetime
from pathlib import Path
from my_api import *


def menu():
    print("""1 - to show unsubscribed profiles
2 - to show new subscribed profiles
3 - to show your subscribers
4 - sort by subscribers number
q - exit from the application""")


# log into instagram account
username = 'YourInstagramLogin'
password = 'YourInstagramPassword'
API = log_in(username, password)
# get username
user_id = API.username_id
# create log file
file = None
path = username + '_log.txt'
followers_list = []
if Path(path).exists():
    print('File exists')
    with open(path, 'r') as file:
        for follower in file:
            followers_list.append(follower.replace('\n', ''))
else:
    print('Created file')
    file = open(path, 'w')
    # get list of followers
    followers_list = get_total_followers(API, user_id)
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
            display_subs(spot_subs_difference(followers_list, API, user_id)[0])
            print()
        elif selection == '2':
            print(datetime.datetime.now())
            display_subs(spot_subs_difference(followers_list, API, user_id)[1])
            print()
        elif selection == '3':
            print(datetime.datetime.now())
            get_subscribers_column(get_total_followers(API, user_id))
        elif selection == '4':
            print(datetime.datetime.now())
            display_subs(sort_by_subscribers(spot_subs_difference(followers_list, API, user_id)[0]))
            print()
        elif selection == 'q':
            break
    except KeyboardInterrupt:
        exit(0)
