import pubmed
from utils import *
import community
import networkx as net
import matplotlib.pyplot as plot

#articles = pubmed.get_articles('compu')
#open('articles.json','wb').write(json.dumps(articles))

articles = json.loads(open('articles.json','rb').read())

#articles2=[a for a in articles if parser.parse(a['DP'].replace('-',' ').split(' ')[0])>datetime.datetime(2000,1,1)]


aunet=pubmed.make_author_network(articles)

## removes single links; now will separate into research groups.
components=net.connected_component_subgraphs(trim_edges(aunet,2))

## separate the rest into communities. Plot the overall structure, individual clusters, macrostructure
community.plot_community(components[0], filename='images/largest_community.pdf')
subgraphs=community.plot_partitions(components[0],filename='images/community')

ind=community.induced_graph(community.best_partition(components[0]),components[0])
net.draw(ind)
plot.savefig('images/macrostructure.pdf')


