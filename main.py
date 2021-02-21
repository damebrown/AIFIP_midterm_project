import math
from tkinter import *
from tkinter.font import Font
from tkinter import Label
# import parsing
import sys
import wikipedia
import networkx
# from SPARQLWrapper import SPARQLWrapper, JSON
import SPARQLWrapper
import pywikibot


def get_influence():
    return e1.get()


def get_influenced():
    return e2.get()


def start():
    dy = 350
    first_label['text'] = "How did"
    first_label.place(x = dx, y = dy, anchor = N)
    dy += 50
    e1.place(x = dx, y = dy, anchor = N)
    dy += 50
    sec_label['text'] = "influence"
    sec_label.place(x = dx, y = dy, anchor = N)
    dy += 50
    e2.place(x = dx, y = dy, anchor = N)
    dy += 50
    gobutton['text'] = "?"
    gobutton['command'] = get
    gobutton['font'] = ("Courier", 30, 'bold')
    gobutton.place(x = dx, y = dy, anchor = N)


def get():
    first_label['text'] = 'Thinking...'
    x, y = get_influenced(), get_influence()
    e1.place_forget(), e2.place_forget()
    sec_label.place_forget()
    res = query(x, y)
    if not res:
        first_label['text'] = 'Who?! No input detected!'
        gobutton['text'] = "Again?"
        gobutton['command'] = start
        gobutton['font'] = ("Courier", 22, 'bold')
        gobutton.place(x = dx, y = 450, anchor = N)
        return
    gobutton.place_forget()
    if res == -1:
        first_label['text'] = 'He didn\'t!'
        start()
    if res == -2:
        first_label['text'] = 'Something went wrong'
        start()
    else:
        le = len(res)
        f3 = Font(family = "Courier", size = 24)
        h = root.winfo_height()
        first_label.place_forget()
        if le == 2:
            label = Label(root, text = res[0] + " influenced " + res[1] + " directly!", font = f3, foreground = color)
            label.place(x = dx, y = h / 2, anchor = N)
            return
        dy = math.floor(h / 2) - (math.floor(le / 2) * 50)
        for i in range(1, len(res)):
            if i == 1:
                label = Label(root, text = res[i - 1] + " influenced " + res[i] + "...", font = f3, foreground = color)
                label.place(x = dx, y = dy, anchor = N)
            else:
                if i == le - 1:
                    label = Label(root, text = "And " + res[i - 1] + " influenced " + res[i] + "!", font = f3,
                                  foreground = color)
                    label.place(x = dx, y = dy, anchor = N)
                else:
                    label = Label(root, text = "And " + res[i - 1] + " influenced " + res[i] + "...", font = f3,
                                  foreground = color)
                    label.place(x = dx, y = dy, anchor = N)
            dy += 50


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
        sparql = SPARQLWrapper.SPARQLWrapper(endpoint_url)
        sparql.setQuery(query)
        sparql.setReturnFormat(SPARQLWrapper.JSON)
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


# if __name__ == "__main__":
root = Tk()
x = 600
y = 800
root.geometry('{}x{}'.format(y, x))
frame = Frame(root)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
frame.place()
frame.winfo_toplevel().title("Philosopher's Influence")
color = 'Dodger Blue'
rel = "ridge"
root.configure(bg = color)
im = "fade.gif"
background_image = PhotoImage(file = im)
background_label = Label(root, image = background_image, borderwidth = 0, highlightthickness = 0)
background_label.pack()
root.bind('<Escape>', sys.exit)

dx = 660
dy = 350
f = Font(family = "Courier", size = 24, weight = 'bold')
first_label = Label(root, text = 'How did', font = f, foreground = color, borderwidth = 2, relief = rel)
first_label.place(x = dx, y = dy, anchor = N)
f1 = Font(family = "Courier", size = 18)
e1 = Entry(root, width = 40, justify = CENTER, font = f1)
dy += 50
e1.place(x = dx, y = dy, anchor = N)
dy += 50
sec_label = Label(root, text = 'influence', font = f, foreground = color, borderwidth = 2, relief = rel)
sec_label.place(x = dx, y = dy, anchor = N)
e2 = Entry(root, width = 40, justify = CENTER, font = f1)
dy += 50
e2.place(x = dx, y = dy, anchor = N)

gobutton = Button(root, text = "?", fg = color, font = ("Courier", 30, 'bold'), command = get, bd = 6)
dy += 50
gobutton.place(x = dx, y = dy, anchor = N)

root.mainloop()
