# This module gets information about Twitter friends of specified user
import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl


def get_friends_list(acct):
    """
    (str) -> list
    Return list of acct friends got from Twitter API
    """
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    friends = list()
    cursor = -1
    # friends info is got from Twitter in chunks of 200 friends by one request
    # keep sending requests until all friends info is got or request limit is
    # reached
    while cursor:
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '200',
                             'cursor': str(cursor)})
        print('Retrieving:', url)
        try:
            connection = urllib.request.urlopen(url, context=ctx)
        except urllib.error.HTTPError as message:
            if str(message) == 'HTTP Error 401: Authorization Required':
                print('Can\'t find the user! Check if name is correct' +
                      'or try again later')
                exit()
            else:
                print('Request limit reached!')
                break
        data = connection.read().decode()
        js = json.loads(data)
        friends.extend(js['users'])
        cursor = js['next_cursor']
        headers = dict(connection.getheaders())
        print('Remaining', headers['x-rate-limit-remaining'], 'request')

    return friends


def get_info_from_json(friends):
    """
    (list, int, str) -> None
    Writes to file or in the console(depending on the out_type parameter)
    information about first fr_number friends from friends list
    """
    print('Friends: ' + '  |  '.join([fr['screen_name'] for fr in friends]))

    while True:
        try:
            name = input('Friend name: ')
            iterator = iter(friends)
            i = 0
            while True:
                fr = next(iterator)
                i += 1
                if fr['screen_name'] == name:
                    break
            break
        except StopIteration:
            print('wrong friend name')
            continue
    print(f'Getting info from {friends[i - 1]["screen_name"]}')
    next_dct = friends[i - 1]
    while True:
        if type(next_dct) != dict:
            print(next_dct)
            break
        field = input('Choose field to output: ' +
                      '  |  '.join(next_dct.keys()) + '\n'+
                      '(press Enter to stop!)' + '\n')
        if not field:
            break
        while True:
            try:
                next_dct = next_dct[field]
                break
            except KeyError:
                print('wrong key')
                continue


if __name__ == '__main__':
    acct_name = input('Account name: ')
    friends = get_friends_list(acct_name)
    print(f'{len(friends)} friends were found')
    get_info_from_json(friends)

