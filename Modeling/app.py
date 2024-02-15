import argparse
from flask import Flask, render_template
from flask import request, jsonify, send_from_directory, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page2')
def page2():
    return '<h1>Welcome to Page 2!</h1>'

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user preferences from the request
    data = request.json
    user_preferences = data['userPreferences']

    # Get recommended image filename from the user preferences
    recommended_image_filename = 'images/1.png'

    # Get the URL of the recommended image
    image_url = url_for('static', filename=recommended_image_filename)

    # Return the recommended image URL as a JSON response
    return jsonify(imageUrl=image_url)

@app.route('/textSearch', methods=['POST'])
def text_search():
    # Get the query text from the request
    data = request.json
    query_text = data['searchText']

    # Return the search result as a JSON response
    # Generate image urls
    image1_url = url_for('static', filename='images/1.png')
    image2_url = url_for('static', filename='images/2.png')
    image3_url = url_for('static', filename='images/3.png')
    image4_url = url_for('static', filename='images/4.png')
    image5_url = url_for('static', filename='images/5.png')
    image6_url = url_for('static', filename='images/6.png')

    # Generate product information
    results = {}
    results['searchText'] = query_text
    results['searchImage'] = image1_url
    results['products'] = [
        {'productID': "0000001", 'productName': "스페이스 헤비코튼", "productImage": image2_url, "productBigcat": "상의", "productSmallcat": "후드 티셔츠", "productHashtag": ["후드티셔츠", "오버핏", "빈티지"]},
        {'productID': "0000002", 'productName': "코튼 트위드 자켓", "productImage": image3_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000003", 'productName': "코튼 트위드 자켓", "productImage": image4_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000004", 'productName': "코튼 트위드 자켓", "productImage": image5_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000005", 'productName': "코튼 트위드 자켓", "productImage": image6_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
    ]

    return jsonify(results)


@app.route('/imageSearch', methods=['POST'])
def image_search():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    image = request.files['image']
    prompt = request.form['description']

    # Save the image to the disk
    image.save('static/uploaded_image.jpg')

    # Use ImageSearchModel to segment and get top-k image file paths

    # Generate image urls
    image1_url = url_for('static', filename='images/1.png')
    image2_url = url_for('static', filename='images/2.png')
    image3_url = url_for('static', filename='images/3.png')
    image4_url = url_for('static', filename='images/4.png')
    image5_url = url_for('static', filename='images/5.png')
    image6_url = url_for('static', filename='images/6.png')

    results = {}
    results['searchText'] = prompt
    results['searchImage'] = ''
    results['products'] = [
        {'productID': "0000001", 'productName': "스페이스 헤비코튼", "productImage": image2_url, "productBigcat": "상의", "productSmallcat": "후드 티셔츠", "productHashtag": ["후드티셔츠", "오버핏", "빈티지"]},
        {'productID': "0000002", 'productName': "코튼 트위드 자켓", "productImage": image3_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000003", 'productName': "코튼 트위드 자켓", "productImage": image4_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000004", 'productName': "코튼 트위드 자켓", "productImage": image5_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000005", 'productName': "코튼 트위드 자켓", "productImage": image6_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
    ]

    return jsonify(results)

@app.route('/searchMoments', methods=['POST'])
def search_moments():
    # Get the query text from the request
    data = request.json
    video_url = data['videoUrl']
    prompt = data['prompt']

    # Use VideoSearchModel to get top-k moments from the video
    # Generate image urls
    visualization_url = url_for('static', filename='images/visualization.jpg')
    image1_url = url_for('static', filename='images/1.png')
    image2_url = url_for('static', filename='images/2.png')
    image3_url = url_for('static', filename='images/3.png')
    image4_url = url_for('static', filename='images/4.png')
    image5_url = url_for('static', filename='images/5.png')
    image6_url = url_for('static', filename='images/6.png')

    results = {}
    results['visualization'] = visualization_url
    results['selectedMoments'] = [
        {'image': image1_url},
        {'image': image2_url},
        {'image': image3_url},
        {'image': image4_url},
        {'image': image5_url},
    ]

    return jsonify(results)

@app.route('/videoSearch', methods=['POST'])
def video_search():
    data = request.json
    selected_moment = data['selectedMoment'] # integer index of the selected moment (0-4)
    prompt = data['prompt']

    # Generate image urls
    image1_url = url_for('static', filename='images/1.png')
    image2_url = url_for('static', filename='images/2.png')
    image3_url = url_for('static', filename='images/3.png')
    image4_url = url_for('static', filename='images/4.png')
    image5_url = url_for('static', filename='images/5.png')
    image6_url = url_for('static', filename='images/6.png')

    results = {}
    results['searchText'] = prompt
    results['searchImage'] = ''
    results['products'] = [
        {'productID': "0000001", 'productName': "스페이스 헤비코튼", "productImage": image2_url, "productBigcat": "상의", "productSmallcat": "후드 티셔츠", "productHashtag": ["후드티셔츠", "오버핏", "빈티지"]},
        {'productID': "0000002", 'productName': "코튼 트위드 자켓", "productImage": image3_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000003", 'productName': "코튼 트위드 자켓", "productImage": image4_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000004", 'productName': "코튼 트위드 자켓", "productImage": image5_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
        {'productID': "0000005", 'productName': "코튼 트위드 자켓", "productImage": image6_url, "productBigcat": "아우터", "productSmallcat": "자켓", "productHashtag": ["자켓", "트위드", "코튼"]},
    ]

    return jsonify(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=7777)
    parser.add_argument('--mode', type=str, default='local')
    args = parser.parse_args()

    if args.mode == 'local':
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=args.port)
