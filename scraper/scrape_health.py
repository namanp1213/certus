import requests, bs4, json, time, argparse

def scrape(max_pages=50, out="public/health.json"):
    base="https://www.nhs.uk/conditions/"
    res=requests.get(base)
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,"lxml")
    links=[a['href'] for a in soup.select('a[href^="/conditions/"]')]
    seen=set()
    out_data=[]
    for href in links[:max_pages]:
        url="https://www.nhs.uk"+href
        if url in seen: continue
        seen.add(url)
        try:
            r=requests.get(url); r.raise_for_status()
            s=bs4.BeautifulSoup(r.text,"lxml")
            title=s.select_one("h1").get_text(strip=True)
            p=s.select_one("p")
            summary=p.get_text(" ",strip=True) if p else ""
            out_data.append({"title":title,"url":url,"summary":summary})
            time.sleep(0.4)
        except Exception as e:
            print("skip",url,e)
    with open(out,"w") as f: json.dump(out_data,f,indent=2)
    print("wrote",out)

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="public/health.json")
    ap.add_argument("--max-pages",type=int,default=50)
    args=ap.parse_args()
    scrape(args.max_pages,args.out)
