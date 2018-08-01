import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import argparse
import sys

prefix = ".//{http://www.tei-c.org/ns/1.0}"
prefix2 = "{http://www.tei-c.org/ns/1.0}"
prefix3 = "{http://www.w3.org/XML/1998/namespace}"


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


def getFacs(root):
    facs_dict = {}

    surfaces = root.findall(prefix + "surface")
    for surface in surfaces:
        url = surface.find(prefix + "graphic").get("url")

        zones = surface.findall(prefix + "zone")
        for zone in zones:
            id = zone.get(prefix3 + "id")
            lry = int(zone.get("lry"))
            lrx = int(zone.get("lrx"))
            uly = int(zone.get("uly"))
            ulx = int(zone.get("ulx"))

            x = ulx
            y = uly
            dx = lrx - ulx
            dy = lry - uly

            area = str(x) + "," + str(y) + "," + str(dx) + "," + str(dy)

            target_url = url.replace("full/full", area + "/full")

            facs_dict[id] = target_url

    return facs_dict


def get_thumbnail_from_dbpedia(dbpedila_url):
    thumbnail = ""
    return thumbnail


def get_people(root):
    people_dict = {}

    people = root.findall(prefix + "person")
    for person in people:

        id = person.get(prefix3 + "id")

        # thumbnail = ""
        dbpedia_url = ""
        if person.find(prefix + "persName").get("ref") != None:
            dbpedia_url = person.find(prefix + "persName").get("ref")

            # thumbnail = get_thumbnail_from_dbpedia(dbpedia_url)

        occupation_list = []
        occupations = person.findall(prefix + "occupation")
        for occupation in occupations:
            occupation_list.append(occupation.text)

        occupation_str = ""
        if len(occupation_list) > 0:
            occupation_str = "〔"
            for i in range(len(occupation_list)):
                occupation_str += occupation_list[i]
                if i != len(occupation_list) - 1:
                    occupation_str += ", "
            occupation_str += "〕"

        person_dict = {}
        people_dict[id] = person_dict
        person_dict["persName"] = id
        person_dict["dbpedia_url"] = dbpedia_url
        person_dict["occupation"] = occupation_str

    return people_dict


def get_org(root):
    org_dict = {}

    orgs = root.findall(prefix + "org")
    for org in orgs:

        id = org.get(prefix3 + "id")
        note = ""
        if org.find(prefix + "note") != None:
            note = " 〔" + org.find(prefix + "note").text + "〕"

        org_dict[id] = id + note

    return org_dict


def main(path_to_xml):
    inputpath = path_to_xml
    outputpath = inputpath + ".csv"

    tree = ET.parse(inputpath)
    root = tree.getroot()

    body = root.find(prefix + "body")

    count = 1

    # 改行コード（\n）を指定しておく

    facs_dict = getFacs(root)
    people_dict = get_people(root)
    org_dict = get_org(root)
    print(org_dict)
    print(people_dict)

    ps = body.findall(prefix + "p")

    lines = []

    for p in ps:

        dates = p.findall(prefix + "date")
        if len(dates) > 0:

            date = dates[0].get("when")

            date = date.split("-")

            # ------------

            text = str(BeautifulSoup(ET.tostring(p).decode(), "xml"))
            print(text)
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

            orgs = p.findall(prefix + "orgName")
            for org in orgs:
                org_id = org.get("corresp").replace("#", "")

                org_title = org_dict[org_id]

                org_text = org.text

                before_text = '<ns0:orgName corresp="#' + org_id + '">' + org_text + '</ns0:orgName>'
                after_text = "<a style='color : #c34528;' title='" + org_title + "'>" + org_text + "</a>"

                text = text.replace(before_text, after_text)

            target_url = ""
            if p.get("facs") != None:
                facs_id = p.get("facs").replace("#", "")
                target_url = facs_dict[facs_id]

            line = []
            lines.append(line)
            line.append(int(date[0]))  # Year
            line.append(int(date[1]))  # Month
            line.append(int(date[2]))  # Day

            line.append("")
            line.append("")
            line.append("")
            line.append("")
            line.append("")
            line.append("")

            line.append(dates[0].text)  # Headline
            line.append(text)  # Text
            line.append(target_url)  # Media

            line.append("")
            line.append("")

            line.append(target_url)  # Thumbnail

    with open(outputpath, 'w') as f:

        writer = csv.writer(f, lineterminator='\n')

        for line in lines:
            writer.writerow(line)


if __name__ == "__main__":
    args = parse_args()

    main(
        args.path_to_xml)
