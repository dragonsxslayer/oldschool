import requests,csv
from bs4 import BeautifulSoup as Soup
from pathlib import Path

class OldSchool:
    
    @staticmethod
    #return current dir  abs path
    def BASE_DIR():
        return Path(__file__).resolve().parent
    
    def __init__(self) :
        self.s = requests.session()
        self.user_agent =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        self.bosses_url =  "https://oldschool.runescape.wiki/w/Boss"
        self.bosses_list =  list()
        self.base_dir  = OldSchool.BASE_DIR()
        self.csv_file = Path(self.base_dir,"data.csv")
    
    
    def get_html(self,url):
        headers =  {"user_agent":self.user_agent}
        response = self.s.get(url,headers=headers)
        return response.content if  response.status_code == 200 else None
    
    def to_csv(self,data):
        fields = ['link', 'name', 'Released', 'Members', 'Combat level', 'Size','XP bonus','Attribute',
                 'Max hit', 'Aggressive', 'Poisonous', 'Attack style', 'Attack speed',
                 'combat_hitpoint', 'combat_attack', 'combat_strength', 'combat_defence',
                 'combat_magic', 'combat_ranged', 'aggressive_attack', 'aggressive_strength',
                 'aggressive_magic', 'aggressive_magic_damage', 'aggressive_ranged',
                 'aggressive_ranged_strenth', 'defensive_stab', 
                 'defensive_slash', 'defensive_crush', 'defensive_magic',
                 'defensive_ranged', 'Poison', 'Venom', 'Cannons', 'Thralls']
        
        with open(self.csv_file,"w") as file:
            writer = csv.DictWriter(file,fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
            
    def get_bosses_links(self):
        content  = self.get_html(self.bosses_url)
        
        if content:
            soup =  Soup(content,"html.parser")
            tables =  soup.find_all("table",{"class":"wikitable"})
            del tables[-1]
            del tables[-1]
            for table in tables:
                tr_tag =  table.find_all("tr")
                [self.bosses_list.append("https://oldschool.runescape.wiki"+tr.a["href"]) for tr in tr_tag if tr.a]
        return self.bosses_list
                
    def single_boss(self,url):
        content =  self.get_html(url)
        # print(content)
        boss_info  =  dict()
        
        """ if there any missing keyword just add it here 
             and in to_csv fields function too"""
        keywords =  ["Released","Members","Respawn time"
                     "Combat level","Size","Attribute"
                     "XP bonus","Max hit",
                     "Aggressive","Poisonous",
                     "Attack style","Attack speed","Poison","Venom","Cannons","Thralls"]
        if content:
            soup = Soup(content,"html.parser")
            table = soup.find("table",class_="infobox")
            boss_info["link"] = url
            if table:
                boss_info["name"] = table.find("th",class_="infobox-header").text.strip()
                trs = table.find_all("tr")
                loop  = 1
                for tr in trs:
                    th =  tr.find("th")
                    td = tr.find("td")
                    if th and td:
                        th_info = th.text.strip()
                        td_info  =  td.text.strip()
                        if th_info =="Attack speed":
                            #link without domain so have to add it 
                            td_info = "https://oldschool.runescape.wiki"+td.img["src"]
                        if th_info in keywords:
                            boss_info[th_info] =  td_info
                    stats  = tr.find_all("td","infobox-nested")

                    # 1 is attack , 2 is Aggressive ,3 is Defensive 
                    if stats:
                        
                        if loop==1:
                            boss_info["combat_hitpoint"] =  stats[0].text.strip()
                            boss_info["combat_attack"] = stats[1].text.strip()
                            boss_info["combat_strength"] =  stats[2].text.strip()
                            boss_info["combat_defence"] =  stats[3].text.strip()
                            boss_info["combat_magic"] =  stats[4].text.strip()
                            boss_info["combat_ranged"] =  stats[5].text.strip()
                        elif loop == 2:
                            boss_info["aggressive_attack"] =  stats[0].text.strip()
                            boss_info["aggressive_strength"] = stats[1].text.strip()
                            boss_info["aggressive_magic"] =  stats[2].text.strip()
                            boss_info["aggressive_magic_damage"] =  stats[3].text.strip()
                            boss_info["aggressive_ranged"] =  stats[4].text.strip()
                            boss_info["aggressive_ranged_strenth"] =  stats[5].text.strip()
                        elif loop ==3:
                            boss_info["defensive_stab"] =  stats[0].text.strip()
                            boss_info["defensive_slash"] = stats[1].text.strip()
                            boss_info["defensive_crush"] =  stats[2].text.strip()
                            boss_info["defensive_magic"] =  stats[3].text.strip()
                            boss_info["defensive_ranged"] =  stats[4].text.strip()
                        loop += 1
            else : boss_info["name"] = "not found"
        return boss_info
                    
                    
    def main(self):
        all_bosses  =  self.get_bosses_links()
        all_data =  list()
        for url in all_bosses:
            print("url => ",url)
            all_data.append(self.single_boss(url))
        
        self.to_csv(all_data)

        
        return all_data

if __name__ =="__main__":
    app  =  OldSchool()
    app.main()
    

#start =  OldSchool()  
#print(start.single_boss("https://oldschool.runescape.wiki/w/Nex"))