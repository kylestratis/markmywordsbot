import praw, time, re, json
r = praw.Reddit(user_agent='Mark My Words Bot 1.0 by /u/AchillesDev')

replied = set()
markString = """    Words:
    [ ] Unmarked  
    [x] Marked """
unmarkString = """    Words:
    [x] Unmarked
    [ ] Marked """
bottiquette = r.get_wiki_page('Bottiquette', 'robots_txt_json')
bansJson = json.loads(bottiquette.content_md)
bans = bansJson['disallowed']

r.login()
while(True):
    #subreddit = r.get_subreddit('bottest')
    #subreddit_comments = subreddit.get_comments()
    comments = r.get_comments('all')
    for comment in comments:
        if comment.subreddit not in bans:
            try:
                match = re.search(r'\bmark \D+ words?\b', comment.body, re.I)
                unMatch = re.search(r'\bunmark \D+ words?\b', comment.body, re.I)
                if match and comment.id not in replied:
                    print(comment.body) #testing
                    comment.reply(markString)
                    replied.add(comment.id)
                elif unMatch and comment.id not in replied:
                    print(comment.body) #testing
                    comment.reply(unmarkString)
                    replied.add(comment.id)
            except praw.errors.RateLimitExceeded, e:
                errmsg = e
                print("Rate limit exceeded, sleeping for {} minutes, {} seconds".format(int(errmsg.sleep_time / 60), int(errmsg.sleep_time % 60)))
                time.sleep(errmsg.sleep_time)
    time.sleep(2)