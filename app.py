from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    urls = data['urls']
    keyword = data.get('keyword', '')
    min_price = data.get('minPrice', 0)
    max_price = data.get('maxPrice', float('inf'))
    location = data.get('location', '')
    date_filter = data.get('date', '30d')
    availability = data.get('availability', 'all')
    
    results = []
    
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Feltételek szerinti szűrés (példa szelektorokkal)
        for ad in soup.find_all('div', class_='ad'):
            title = ad.find('h2').text
            link = ad.find('a')['href']
            price = float(ad.find('span', class_='price').text.replace('$', ''))
            ad_date = ad.find('span', class_='date').text
            
            if keyword.lower() in title.lower() and min_price <= price <= max_price and location.lower() in ad.text.lower():
                results.append({'title': title, 'link': link, 'price': price, 'date': ad_date})
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
