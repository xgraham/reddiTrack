import re


def research(search_str, selftext):
    count = 0
    result = ""
    for char in search_str:
        if count == 0:
            result += char
        else:
            result += f"[{char.upper()}{char.lower()}]"
        count+=1
    print(result)
    return re.search(f"[^a-zA-Z]{result}[^a-zA-Z]", " " + selftext + " ") is not None



self_text = " Gme to the MOOON"
self_text1 = " GMe to the MOOON"
self_text2 = " GmE to the MOOON"
self_text3 = " Gme to the MOOON"
self_text4 = " GAEM to the moon"
self_text5 = " G m e to the MOOON"

ticker = "GE"

print(research(ticker,self_text))
print(research(ticker,self_text1))
print(research(ticker,self_text2))
print(research(ticker,self_text3))
print(research(ticker,self_text4))
print(research(ticker,self_text5))
