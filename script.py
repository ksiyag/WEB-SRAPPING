from flask import *
from web import WebScraper

app = Flask('scraper')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape',methods=['POST'])
def search():
    result = list()
    product_name = request.form['productname'].lower()
    # product_company = request.form['companyname'].lower()
    try:
        web_amazon = WebScraper()
        result = web_amazon.scrape(product_name=product_name,merchant='amazon')
        web_flipkart = WebScraper()
        result.extend(web_flipkart.scrape(product_name=product_name,merchant='flipkart'))
        print(result)
    except Exception as e:
        print(e)
    
    # print(result)
    return render_template('product_list.html',products=result,name=product_name)




    # print(result)

    # return render_template('product_list.html',products = result,name=product_name)


if __name__ == '__main__':

    app.run(debug=True,port=2000)
