from InstagramAPI import InstagramAPI
import requests
import json

# simply helps you to know who've unsubbed from your Instagram account


def log_in(login, password):
    API = InstagramAPI(login, password)
    if API.login():
        return API
    else:
        return False


def get_total_followers(api, user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        followers_ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    for i in range(len(followers)):
        followers[i] = followers[i]['username']
    return followers


def get_subscribers_column(followers_list):
    # get list of followers in a column
    print('You have ' + str(len(followers_list)) + ' subscribers')
    print('Subscribers: ')
    for i in range(len(followers_list)):
        print(str(i+1) + '. ' + followers_list[i])
    print()


def spot_subs_difference(followers_list_was, api, user_id):
    unsubs = []
    new_subs = []
    followers_list_final = get_total_followers(api, user_id)
    for was in followers_list_was:
        if was not in followers_list_final:
            unsubs.append(was)
    for now in followers_list_final:
        if now not in followers_list_was:
            new_subs.append(now)
    if len(unsubs) == 0:
        unsubs = 'No unsubs'
    if len(new_subs) == 0:
        new_subs = 'No new subs'
    return [unsubs, new_subs]


def get_account_info(account_name):
    """get Instagram account info without authorization"""

    url = 'https://instagram.com/' + account_name

    response = requests.get(url).text
    response = response.split('window._sharedData = ')[1].split('<')[0]
    response = response[0:len(response) - 1]
    response = json.loads(response)
    user = response['entry_data']['ProfilePage'][0]['graphql']['user']
    bio = user['biography']
    followed_by = user['edge_followed_by']['count']
    follow = user['edge_follow']['count']
    username = user['username']
    return [username, bio, follow, followed_by]


def sort_by_subscribers(subs):
    subs_count = []
    for sub in subs:
        subs_count.append(get_account_info(sub)[3])
    for k in range(len(subs_count)):
        for i in range(len(subs_count)-1):
            if subs_count[i] < subs_count[i+1]:
                subs_count[i], subs_count[i+1] = subs_count[i+1], subs_count[i]
                subs[i], subs[i + 1] = subs[i + 1], subs[i]
    for i in range(len(subs)):
        subs[i] = subs[i] + ' (' + str(subs_count[i]) + ')'
    return subs


def display_subs(subs_list):
    if isinstance(subs_list, list) and len(subs_list) > 0:
        for i in range(len(subs_list)):
            print(str(i+1) + '. ' + subs_list[i])
    else:
        print(subs_list)


