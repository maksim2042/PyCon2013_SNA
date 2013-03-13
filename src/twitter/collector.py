import tweetstream
from utils import *
import networkx as net


words = ["#Pope"]
##people = [123,124,125]
#locations = ["-122.75,36.8", "-121.75,37.8"] #, follow=people, locations=locations


retweets=net.DiGraph()
hashtag_net=net.Graph()

with tweetstream.FilterStream("ElectionGauge", "cssgmu", track=words) as stream:
    for js in stream:

        ### process tweet to extract information
        try:
            author=js['user']['screen_name']
            entities=js['entities']
            mentions=entities['user_mentions']
            hashtags=entities['hashtags']

            for rt in mentions:
            	alter=rt['screen_name']
            	retweets.add_edge(author,alter)

            tags=[tag['text'].lower() for tag in hashtags]
            for t1 in tags: 
            	for t2 in tags:
            		if t1 is not t2:
            			add_or_inc_edge(hashtag_net,t1,t2)      
        except :
            print ':-('
            continue


