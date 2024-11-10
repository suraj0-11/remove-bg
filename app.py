from flask import Flask, request, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
REMOVE_BG_API_KEY = '9gTuMbsUeJQhvAodEjPFa2nZ'

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['image']
        if file:
            # Save the uploaded image temporarily
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_path)

            # Send the image to RemoveBG API
            with open(input_path, 'rb') as image_file:
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': image_file},
                    data={'size': 'auto'},
                    headers={'X-Api-Key': REMOVE_BG_API_KEY}
                )

            # Check if the request was successful
            if response.status_code == 200:
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'no_bg_' + file.filename)
                with open(output_path, 'wb') as output_file:
                    output_file.write(response.content)
                
                # Redirect to display the processed image
                return redirect(url_for('display_image', filename='no_bg_' + file.filename))
            else:
                return f"Error: {response.status_code}, {response.text}"

    return render_template('index.html')

@app.route('/display/<filename>')
def display_image(filename):
    return render_template('display.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
