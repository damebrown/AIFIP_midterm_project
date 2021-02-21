# import csv
# import re
# import requests
# import wptools
# import wikidata
# import matplotlib.pyplot as plt


# good_ones = set([])
# bad_ones = []
# instances = []
#
#
# def something():
#     S = requests.Session()
#     URL = "https://en.wikipedia.org/w/api.php"
#     TITLE = "Gottfried Leibniz"
#     PARAMS = {
#         'action': "parse",
#         'page': TITLE,
#         'format': "json"
#     }
#     R = S.get(url = URL, params = PARAMS)
#     DATA = R.json()
#     print(DATA)
#
#
# def split(string):
#     string = string.strip("{{hlist")
#     splat = string.split(', ')
#     if len(splat) == 1:
#         splat = string.split(' |')
#     if len(splat) == 1:
#         splat = string.split('{{•}}')
#     return splat
#
#
# def get_page(line):
#     search = wikipedia.search(line)
#     if search:
#         p = wikipedia.page(search[0])
#         id = p.pageid
#         page = wptools.page(pageid = id).get_parse()
#         if not page.data or 'infobox' not in page.data.keys():
#             bad_ones.append(line)
#             bad_ones.append("\n")
#             return 0
#         return page
#     return 0
#
#
# def parse():
#     path = "western.txt"
#     f = open(path, 'r', encoding = "utf8")
#     philosophers = []
#     counter = 0
#     try:
#         for line in f:
#             counter += 1
#             m = re.match("(?P<name>[^,(]*).*", line)
#             if m.group(1) != '\n':
#                 philosophers.append(m.group(1))
#         path = "philosophers.txt"
#         f = open(path, 'w', encoding = "utf8", errors = 'ignore')
#         for p in philosophers:
#             f.write(p + "\n")
#         f.close()
#     except(UnicodeDecodeError):
#         print("ok")
#     return
#
#
# def wiki():
#     path = "western2.txt"
#     f = open(path, 'r', encoding = "utf8")
#     out = csv.writer(open("out2.csv", 'w', encoding = "utf8"), delimiter = ';')
#     try:
#         for line in f:
#             line = line.split('\n')[0]
#             if "ן»¿" in line:
#                 line = line.strip("ן»¿")
#             print(line)
#             page = get_page(line)
#             if not page:
#                 pass
#             else:
#                 if 'infobox' in page.data.keys():
#                     infobox = page.data.get('infobox')
#                     if infobox is None:
#                         pass
#                     else:
#                         infobox = page.data.get('infobox')
#                         if 'influences' in infobox.keys():
#                             good_ones.add(line)
#                             active = infobox['influences']
#                             splat_act = split(active)
#                             for i, w in enumerate(splat_act):
#                                 e = re.match("[ ]*\\[\\[(?P<name>[^|\\]]*)(|.*)?\\]\\][ ]*", w)
#                                 if e is not None:
#                                     g = e.group('name')
#                                     if g != '':
#                                         splat_act[i] = g
#                             print(splat_act)
#                         else:
#                             splat_act = []
#                         if 'influenced' in infobox.keys():
#                             good_ones.add(line)
#                             passive = infobox['influenced']
#                             splat_pass = split(passive)
#                             for i, w in enumerate(splat_pass):
#                                 e = re.match("[ ]*\\[\\[(?P<name>[^|\\]]*)(|.*)?\\]\\][ ]*", w)
#                                 if e is not None:
#                                     g = e.group('name')
#                                     if g != '':
#                                         splat_pass[i] = g
#                             print(splat_pass)
#                         else:
#                             splat_pass = []
#                         if len(splat_act) > 0 or len(splat_pass) > 0:
#                             out.writerow([line])
#                             out.writerow([splat_pass])
#                             out.writerow([splat_act])
#                             phil = Philosopher.Philosopher(line, splat_pass, splat_act)
#                             instances.append(phil)
#                         else:
#                             bad_ones.append(line + "\n")
#     except:
#         print("Bad ones: ", bad_ones)
#         f.close()
#
#
# def phil_factory():
#     philosophers = csv.reader(open("out.csv", 'r', encoding = "utf8"))
#     counter = 0
#     instance_list = []
#     name = ''
#     influenced, influences = [], []
#     current_philosopher = None
#     for row in philosophers:
#         if counter == 5:
#             phil = Philosopher.Philosopher(name, _influences = influences, _influenced = influenced)
#             instance_list.append(phil)
#             name = ''
#             influences, influenced = [], []
#             counter = 0
#         else:
#             if not counter:
#                 name = row[0]
#                 print(name)
#             elif counter == 2:
#                 for r in row:
#                     if ']' in r:
#                         r = r.strip(']')
#                         if '[' in r:
#                             influences = []
#                             break
#                         influences.append(r)
#                         break
#                     elif '[' in r:
#                         r = r.strip('[')
#                     influences.append(r)
#                 print(influences)
#             elif counter == 4:
#                 for r in row:
#                     if ']' in r:
#                         r = r.strip(']')
#                         if '[' in r:
#                             influenced = []
#                             break
#                         influenced.append(r)
#                         break
#                     elif '[' in r:
#                         r = r.strip('[')
#                     influenced.append(r)
#                 print(influenced)
#             counter += 1
#     return instance_list
#
#
# def graph_creator(phil_list):
#     g = networkx.DiGraph()
#     g.add_nodes_from(phil_list)
#
#     for phil in phil_list:
#         for name in phil.influenced_names:
#             # TODO create his influenced mushpaim list and have edges from phil to them
#             name = name.strip('\\')
#             mushpa = Philosopher.Philosopher.get_philosopher(name)
#             if mushpa:
#                 phil.influenced_nodes.append(mushpa)
#                 # g.add_weighted_edges_from()
#         # TODO update the influences's mashpi'im list
#         for name in phil.influences_names:
#             mashpia = Philosopher.Philosopher.get_philosopher(name)
#             if mashpia:
#                 mashpia.influenced_nodes.append(phil)
#                 mashpia.influenced_nodes = list(set(mashpia.influenced_nodes))
#     return

import wikipedia
import networkx
from SPARQLWrapper import SPARQLWrapper, JSON
import pywikibot


def query(mushpa, mashpia):
    if not mushpa and not mashpia:
        return 0
    target_name = wikipedia.search(mushpa)[0]
    src_name = wikipedia.search(mashpia)[0]
    site = pywikibot.Site("en", "wikipedia")
    page = pywikibot.Page(site, target_name)
    id = pywikibot.ItemPage.fromPage(page).id
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """PREFIX gas: <http://www.bigdata.com/rdf/gas#>

    SELECT ?itemLabel ?linkToLabel {
      SERVICE gas:service {
        gas:program gas:gasClass "com.bigdata.rdf.graph.analytics.SSSP" ;
                    gas:in wd:""" + id + """ ;
                    gas:traversalDirection "Forward" ;
                    gas:out ?item ;
                    gas:out1 ?depth ;
                    gas:maxIterations 150 ;
                    gas:maxVisited 150 ;
                    gas:linkType wdt:P737 .
      }
      OPTIONAL { ?item wdt:P737 ?linkTo }
      SERVICE wikibase:label {bd:serviceParam wikibase:language "en" }
    }"""

    def get_results(endpoint_url, query):
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    results = get_results(endpoint_url, query)
    g = networkx.DiGraph()
    for result in results["results"]["bindings"]:
        # print(result)
        if 'linkToLabel' in result:
            mushpa_name = result['itemLabel']['value']
            mashpia_name = result['linkToLabel']['value']
            # print(mushpa_name, "  ,  ", mashpia_name)
            g.add_edge(mashpia_name, mushpa_name)
    if not g.has_node(src_name) or not g.has_node(target_name):
        # print("Error")
        return -2
    else:
        try:
            y = networkx.astar_path(g, src_name, target_name)
            print(y)
            return y
        except networkx.NetworkXNoPath:
            # print("route not found")
            return -1
