from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

# define our app
app = Flask(__name__)

# we define routes in Flask. they're routes that we would access on the web. the '/' is the homepage


@app.route('/')
# you should be able to access the home page if you to /index or /index.html for example, so I also want to add app.route('/index') so both '/' and '/index' will apply
@app.route('/index')
# following those 2 routes, we define a function that will return something for the route
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    if not bool(city.strip()):
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # If city is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


if __name__ == "__main__":
    # this makes it run on our local host
    # app.run(host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000)
