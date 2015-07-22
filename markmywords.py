import praw, time, re, json, sys, OAuth2Util
r = praw.Reddit(user_agent='Mark My Words v1.1 by /u/AchillesDev')
o = OAuth2Util.OAuth2Util(r)

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

start_time = time.time()
while(True):
    o.refresh()
    #subreddit = r.get_subreddit('bottesting')
    #comments = subreddit.get_comments()
    try:
	    comments = r.get_comments('all', limit=100)
	    for comment in comments:
	        if comment.subreddit not in bans:
	            print("In if!")
	            try:
	                match = re.search(r'\bmark \D+ words?\b', comment.body, re.I)
	                unMatch = re.search(r'\bunmark \D+ words?\b', comment.body, re.I)
	                if match and comment.id not in replied:
	                    print(comment.body) #for testing
	                    comment.reply(markString)
	                    replied.add(comment.id)
	                elif unMatch and comment.id not in replied:
	                    print(comment.body) #for testing
	                    comment.reply(unmarkString)
	                    replied.add(comment.id)
	            except (praw.errors.RateLimitExceeded, e):
	                errmsg = e
	                print("Rate limit exceeded, sleeping for {} minutes, {} seconds".format(int(errmsg.sleep_time / 60), int(errmsg.sleep_time % 60)))
	                time.sleep(errmsg.sleep_time)
    except KeyboardInterrupt:
        print("UPTIME: %s seconds" %(time.time() - start_time))
        sys.exit()
    
