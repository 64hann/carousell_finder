import requests,bs4,re,webbrowser

#code that asks the user what item he is looking for on carousell
#Then filter search results to those that include all the words the user typed
#opens those links
def web_scraper():
    global items,length,list_of_words,high
    words=str(input("Please enter the item you want to search on Carousell: "))
    high=float(input("What is your maximum price? $")) #ask user for thing to search
    list_of_words=words.split() #split into individual words
    length=len(list_of_words)
    URL='https://sg.carousell.com/search/'+ words
    page=requests.get(URL)
    page.raise_for_status() #check for error
    soup=bs4.BeautifulSoup(page.content,'html.parser')
    results=soup.find('div',class_='_2RJeLsMmpi') 
    items=results.find_all('div',class_='TpQXuJG_eo') 


def item_find(): #find name,price,link of item
    global name,price,link,item
    for item in items:
        name=item.find('p',class_='_1gJzwc_bJS _2rwkILN6KA mT74Grr7MA nCFolhPlNA lqg5eVwdBz uxIDPd3H13 _30RANjWDIv') #name of good
        price=item.find('p',class_='_1gJzwc_bJS _2rwkILN6KA mT74Grr7MA nCFolhPlNA lqg5eVwdBz _19l6iUes6V _3k5LISAlf6') #price of good
        
        if None in (name,price):
                    continue
        word_search(length)

def word_search(length):
    if length==0:
        price_filter()
        
    else:
        item_finder=re.compile(list_of_words[length-1],re.I)
        match_object=item_finder.findall(name.text)
        if match_object!=[]: #if word is present, continue searching
            length-=1
            word_search(length)

def price_filter():
    global price
    price=price.text.strip("S$")
    price=float(price) #change str to float
    if price<=high:
        link=item.find_all('a')[1]['href'] #get link
        full_link='https://sg.carousell.com'+link
        webbrowser.open(full_link)         #open link
        
    
def main():
    web_scraper()
    item_find()

main()


