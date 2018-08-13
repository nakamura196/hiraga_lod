import xml.etree.ElementTree as ET
from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib.namespace import DC, FOAF
import argparse
import sys
from bs4 import BeautifulSoup
import myfunc as mf


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'path_to_xml',
        action='store',
        type=str,
        help='Ful path to tei file.')

    return parser.parse_args(args)


def main(path_to_xml):

    inputpath = path_to_xml
    outputpath = inputpath+".rdf"

    prefix = ".//{http://www.tei-c.org/ns/1.0}"
    prefix3 = "{http://www.w3.org/XML/1998/namespace}"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    people_dict = mf.get_people(root)
    facs_dict = mf.getFacs(root)

    body = root.find(prefix+"body")

    g = Graph()

    ps = body.findall(prefix+"p")

    for p in ps:

        dates = p.findall(prefix + "date")
        if len(dates) > 0:

            pid = p.get("facs")

            s = URIRef("http://example.org"+pid)

            g.add((s, DC.date, Literal(dates[0].get("when"))))
            g.add((s, DC.title, Literal(dates[0].text)))

            text = str(BeautifulSoup(ET.tostring(p).decode(), "xml"))
            text = text.split("</ns0:date>")[1]
            text = text.replace("<ns0:lb/>", "<br/>")

            pers = p.findall(prefix + "persName")
            for per in pers:
                person_id = per.get("corresp").replace("#", "")

                person_dict = people_dict[person_id]

                person_text = per.text

                before_text = '<ns0:persName corresp="#' + person_id + '">' + person_text + '</ns0:persName>'
                title = person_dict["persName"] + person_dict["occupation"]
                after_text = "<a style='color : #c34528;' href='" + person_dict["dbpedia_url"].replace(
                    "http://ja.dbpedia.org/resource/",
                    "https://ja.wikipedia.org/wiki/") + "' title='" + title + "'>" + person_text + "</a>"

                text = text.replace(before_text, after_text)

                g.add((s, DC.subject, URIRef(person_dict["dbpedia_url"])))

            g.add((s, DC.description, Literal(text)))

            if p.get("facs") != None:
                facs_id = p.get("facs").replace("#", "")
                target_url = facs_dict[facs_id]
                g.add((s, FOAF.thumbnail, URIRef(target_url)))

    f = open(outputpath, "wb")
    f.write(g.serialize(format='xml'))
    f.close()


if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml)
