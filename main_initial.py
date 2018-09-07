import logging
from flask import Flask

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked index()')

    return 'hello from Flask!'

if __name__ == '__main__':
    app.run(debug=True)
