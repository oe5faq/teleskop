import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
     2 : {'name' : 'GPIO  2', 'state' : GPIO.LOW},
     3 : {'name' : 'GPIO  3', 'state' : GPIO.LOW},
     4 : {'name' : 'GPIO  4', 'state' : GPIO.LOW},
    17 : {'name' : 'GPIO 17', 'state' : GPIO.LOW}
}

# set each pin as output and make it low
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def index():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins' : pins
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('index.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name'] # get device name

    if action == "on":
        GPIO.output(changePin, GPIO.HIGH)
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."

    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    templateData = {
        'pins' : pins
    }

    return render_template('index.html', **templateData)

@app.route('/cakes')
def cakes():
    return render_template('cake.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


