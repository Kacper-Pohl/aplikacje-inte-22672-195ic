from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from bs4 import BeautifulSoup
from lxml import html
import requests


def home(request):
    page = requests.get("https://webscraper.io/test-sites/e-commerce/static")
    soup = BeautifulSoup(page.content, "html.parser")
    #1
    all_p_tags = []

    for element in soup.select("p"):
        all_p_tags.append(element.text)

    all_p_tagslen=len(all_p_tags)
    second_p_text = soup.select("p")[1].text
    #2

    soup = BeautifulSoup(page.content, "html.parser")
    top_items = []

    products = soup.select("div.thumbnail")
    for elem in products:
        title = elem.select("h4 > a.title")[0].text
        review_label = elem.select("div.ratings")[0].text
        info = {"title": title.strip(), "review": review_label.strip()}
        top_items.append(info)
    #3

    image_data = []
    images = soup.select("img")
    print("Liczba obrazków =", len(images))
    for image in images:
        src = image.get("src")
        alt = image.get("alt")
        image_data.append({"src": src, "alt": alt})
    #4
    all_products = []


    products = soup.select('div.thumbnail')
    for product in products:
        name = product.select('h4 > a')[0].text.strip()
        description = product.select('p.description')[0].text.strip()
        price = product.select('h4.price')[0].text.strip()
        reviews = product.select('div.ratings')[0].text.strip()
        image = product.select('img')[0].get('src')

        all_products.append({
            "name": name,
            "description": description,
            "price": price,
            "reviews": reviews,
            "image": image
        })
    return render(request,'home.html',{'top_items':top_items,'all_p_tagslen':all_p_tagslen,
        'second_p_text':second_p_text, 'image_data':image_data,'all_products':all_products})



def scraping (request):
    if request.method == "POST":
        allElements = []
        web_link = request.POST.get('web_link', None)
        element = request.POST.get('element', None)
        url = web_link
        source=requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        items = soup.find_all(element)
        amount = len(items)

        for i in items:

            findClass = i.get('class')
            if findClass is None:
                findClass = "Brak"

            findId = i.get('id')
            findId = findId.strip() if findId is not None else "Brak"

            findArticle = i.get('article')
            findArticle = findArticle.strip() if findArticle is not None else "Brak"

            find_alt = i.get('alt')
            find_alt = find_alt.strip() if find_alt is not None else "Brak"

            getText = i.text
            getText = getText.strip() if getText is not None else "Brak"

            findSpan = i.get('span')
            findSpan = findSpan.strip() if findSpan is not None else "Brak"

            findHref = i.get('href')
            findHref = findHref.strip() if findHref is not None else "Brak"

            allElements.append({"findId": findId, "findClass": findClass,"find_alt": find_alt, "findArticle": findArticle, "getText": getText,
            'findHref':findHref, 'findSpan': findSpan})
        return render(request, 'lab5.html', {'allElements':allElements, 'amount': amount, 'web_link': web_link, 'element':element})
    return render(request, 'lab5.html')


def xpath(request):

    url = 'https://webscraper.io/test-sites/e-commerce/static'
    path = '/html/body/div[1]/div[2]'
    response = requests.get(url)
    source = html.fromstring(response.content)
    tree = source.xpath(path)
    lxml1 = tree[0].text_content()

    url = 'https://pe.amw.gdynia.pl/Logowanie'
    path = '//*[@class="pb-4 text-right"]'
    response = requests.get(url)
    source = html.fromstring(response.content)
    tree = source.xpath(path)
    lxml2 = tree[0].text_content()

    return render(request, 'xpath.html', {'lxml1': lxml1,'lxml2': lxml2 })

