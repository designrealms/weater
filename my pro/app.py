from flask import Flask, render_template, request
import requests
from email.message import EmailMessage
import ssl
import smtplib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_news', methods=['POST'])
def get_news():
    try:
        input_category = int(request.form['category'])
        email_receiver = request.form['email']

        # Replace 'YOUR_API_KEY' with your actual API key
        api_key = 'ccf2957a-5b99-498d-8903-1d9743480e59'

        # Define the base URL for The Guardian API
        base_url = 'https://content.guardianapis.com'

        # Specify the endpoint and any parameters you want to include
        endpoint = '/search'
        parameters = {
            'q': str(input_category),  # Replace with your desired search query
            'api-key': api_key,
        }

        # Make the API request
        response = requests.get(f'{base_url}{endpoint}', params=parameters)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and print relevant information
            news_list = []
            for result in data['response']['results']:
                title = result['webTitle']
                web_url = result['webUrl']
                news_list.append({'title': title, 'web_url': web_url})

            # Send email with news report
            send_email(email_receiver, news_list)

            return render_template('success.html', email=email_receiver, news_list=news_list)
        else:
            # Print an error message if the request was not successful
            return render_template('error.html')
    except:
        return render_template('error.html')

def send_email(email_receiver, news_list):
    email_admin = "ademide451@gmail.com"
    email_password = "tmwj hrrd hzbn duqn"
    subject = "Your News Report"
    body = "\n".join([f"Title: {news['title']}\nURL: {news['web_url']}" for news in news_list])

    msg = EmailMessage()
    msg['From'] = email_admin
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_admin, email_password)
        server.sendmail(email_admin, email_receiver, msg.as_string())
        print("Email sent")

if __name__ == '__main__':
    app.run(debug=True)
