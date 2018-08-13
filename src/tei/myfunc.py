prefix = ".//{http://www.tei-c.org/ns/1.0}"
prefix3 = "{http://www.w3.org/XML/1998/namespace}"

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
