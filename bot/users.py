from users_data import users

users_ids = {}
users_topics = {}
for user in users:
    users_ids[users[user]['id']] = { 'name': user, 'topic': users[user]['topic'] }
    users_topics[users[user]['topic']] = { 'name': user, 'id': users[user]['id'] }
