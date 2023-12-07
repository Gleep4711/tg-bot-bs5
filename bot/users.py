users = {
    'dark_bag':        {'id': 5082322795, 'topic': 4},
    'sock_of_destiny': {'id': 2013389248, 'topic': 2},
    'gleep':           {'id': 360573683,  'topic': 3104},
    'roxana':          {'id': 5184767380, 'topic': 7095},
    'goof':            {'id': 2049194365, 'topic': 30276},
}

users_ids = {}
users_topics = {}
for user in users:
    users_ids[users[user]['id']] = { 'name': user, 'topic': users[user]['topic'] }
    users_topics[users[user]['topic']] = { 'name': user, 'id': users[user]['id'] }
