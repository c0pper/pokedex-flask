from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from flask import Flask, url_for, render_template, request

national_dex_url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
national_dex_req = Request(national_dex_url, headers={'User-Agent': 'Mozilla/5.0'})
national_dex_soup = BeautifulSoup(urlopen(national_dex_req).read(), 'html.parser')

all_pkmn = {}
for g in range(1,9):
    generation = national_dex_soup.find('div', {'id': 'mw-content-text'}).select("tbody")[g]
    entries = generation.findChildren("tr", recursive=False)
    for entry in entries:
        pkmn_id = entry.contents[3].get_text().replace("\n","").replace("#","")
        pkmn_name = entry.contents[7].get_text().replace("\n","")
        all_pkmn[pkmn_id] = pkmn_name


class Pokemon:
    url = ""
    req = ""
    soup = ""

    def __init__(self, pkmn_id):
        self.name = all_pkmn[str(pkmn_id)]
        self.url = f"https://bulbapedia.bulbagarden.net/wiki/{self.name}_(Pok%C3%A9mon)"
        self.req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.soup = BeautifulSoup(urlopen(self.req).read(), 'html.parser')

        self.type1 = str(self.soup.select("#mw-content-text > div > table:nth-child(2) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(1) > a > span > b")[0].get_text())
        self.type2 = str(self.soup.select("#mw-content-text > div > table:nth-child(2) > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > a > span > b")[0].get_text())

        if self.type2 == "Unknown":
            self.type2 = ""
        print("Name: " + self.name)
        print(f"\nType(s): {self.type1} {self.type2}")







app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_id = request.form["pkmnid"]
        p = Pokemon(str(input_id))
    return render_template("index.html", name=p.name, type1=p.type1, type2=p.type2)

if __name__ == "__main__":
    app.run()