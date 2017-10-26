import urllib.request
import json
import csv

TBAauthkey = "MakeThisYourTBAAuthKey"
if TBAauthkey == "MakeThisYourTBAAuthKey":
    print("="*20)
    print("PLEASE SET THE TBA AUTH KEY. Goto thebluealliance.com, select account, scroll down to 'Read API Keys', add a new key and copy it in within the quotes of the fifth line of this file, which should look something like:")
    print("TBAauthkey = \"QsfHVwj95sdUIPYesd738asdfewkj89dsfEJKLDSF9ioj3ewf\"")
    print("="*20)
    input()

def makeRequest(extension):
    URL = "http://www.thebluealliance.com/api/v3/"
    request = urllib.request.Request(URL + extension)
    request.add_header("X-TBA-Auth-Key", "PUT YOUR TBA AUTH KEY HERE")
    request.add_header('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11")
    try:
        print("Making Request " + URL + extension)
        response = urllib.request.urlopen(request)
    except Exception as e:
        print(e.fp.read())
    jsonified = json.loads(response.read().decode("utf-8"))
    return jsonified

teams = makeRequest("teams/0")
fullOutput = csv.writer(open("TBATeamListOutputFull.csv", "w"), delimiter=",", lineterminator="\n")
websitesOnly = open("TBATeamListOutputWebsites.txt", "w")
counter = 0

rows = ["team_number","nickname","website","address","city","state_prov","country","rookie_year","name","postal_code","lat","lng"]
fullOutput.writerow(rows)

from unidecode import unidecode
def remove_non_ascii(text):
    if type(text) is str:
        return ''.join([i if ord(i) < 128 else ' ' for i in text])
        #return unidecode(unicode(text, encoding = "utf-8"))
    else:
        return text

def teamRequest(counter):
    try:
        return makeRequest("teams/" + str(counter))
    except Exception as e:
        print("Some mysterious error (all errors any error) occured while fetching the page. Cause tom is being super lazy, the response will just try again.")
        print("***THE ERROR:")
        print(e.fp.read())
        print("Retrying request...")
        return teamRequest(counter)

while teams is not []:
    print("Writing page " + str(counter))
    for team in teams:
        #print([(row + ":" + str(remove_non_ascii(team[row]))) for row in rows])
        fullOutput.writerow([remove_non_ascii(team[row]) for row in rows])
        if team["website"] is not None:
            websitesOnly.write(team["website"] + "\n")
    counter += 1
    teams = teamRequest(counter)

    if counter > 20:
        print("Please tell tom (@Cabey42) he is stupid and his conditional ending didn't work. (The program reached page 20 of teams (each page has 500 teams) and has stopped anyway, cause tom's code is broke and didn't stop when it should like he suspected but couldn't be bothered to check.)")
        break

fullOutput.close()
websitesOnly.close()
