from flask import Flask ,request ,send_file
from scraper import scrape
import pandas as pd
from inference import inference
from utils.review_url import url_maker

app = Flask(__name__)

@app.route('/generate_pdf', methods = ['POST'])
def generate_pdf_route():
    data = request.json
    url = data['url']

    review_url = url_maker(url)
    reviews_df = scrape(review_url)
    df = pd.read_csv("ScrapedReviews/Review_Data.csv")
    inference(df)

    pdf_path = 'sample.pdf'

    #return send_file(pdf_path, as_attachment = True)
    return send_file(pdf_path, as_attachment=True, download_name="generated_pdf.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(host= "172.31.113.51" , debug=True)