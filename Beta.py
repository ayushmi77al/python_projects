import speech_recognition as sr
import pyttsx3
import pywhatkit
import time
import datetime
import wikipedia
import pyjokes
import webbrowser
import random
import requests
import json

recognizer = sr.Recognizer()

engine = pyttsx3.init('sapi5')

# saving stock prices
stockcount = 0

if stockcount == 0:
    nse = requests.get(
        "https://financialmodelingprep.com/api/v3/quotes/nse?apikey=71d86c5aaf112f1c746e9092e652b7c3").text
    nsdaq = requests.get(
        "https://financialmodelingprep.com/api/v3/quotes/nasdaq?apikey=71d86c5aaf112f1c746e9092e652b7c3").text

    stockdata = json.loads(nse)
    stockdata += json.loads(nsdaq)
    print('aaya')


def stockPrice(company, stockdata):
    for item in stockdata:
        if company == 'tcs':
            company = 'tata consultancy'
        if company == 'google':
            company = 'alphabet'
        if company in item['name'].lower():
            return f"Stock price of {item['name']} is {item['price']}."


def weatherDescription(city_name):
    api_key = "2f92968d4b299ff13d9c8d30239ded82"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found

    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]
        feels_like = y["feels_like"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        additional = ''

        description = f"Current temperature of {city_name} is {str(current_temperature - 273.15)[0:5]} degree celcius but it feels like {str(feels_like-273.15)[0:5]} degree celcius and it is {weather_description} outside"

        if 'rain' in weather_description:
            additional = '\nYou should carry umbrella if you are going outside'

        return (description + additional)
    else:
        return " City Not Found "


def talk(text):
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    # get command from the microphone
    with sr.Microphone() as source:
        print("listning...")

        # to handle ambient noise
        recognizer.adjust_for_ambient_noise(source)

        voice = recognizer.listen(source)

    # checking if there any error in error while listening
    try:
        # recognizer.recognize_google(voice, show_all=True) -> to show all alternatives
        command = recognizer.recognize_google(voice)
        command = command.lower()

    except sr.UnknownValueError:
        print("Could not understand command")
        talk("Could not understand command")
        runBeta()
    except sr.RequestError as e:
        print("Could not request wiki; {0}".format(e))
        runBeta()

    if command == None or command == '':
        runBeta()

    return command


def runBeta():
    try:
        command = takeCommand()
    except:
        exit()
    print('   >>>  ', command)

    stockcount = 0

    # to stop
    if 'rest' in command:
        talk('Thankyou')
        exit()

    # play on youtube
    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
        print(song)

    # show time
    elif 'time' in command:
        present_time = datetime.datetime.now().strftime('%I:%M %p')
        print(present_time)
        talk('current time is ' + present_time)

    # introduction
    elif 'who are you' in command:
        talk('I am beta, personal assistant made by Ayush Mittal')

    # searching on wikipedia
    elif 'wikipedia' in command:
        talk('Searching Wikipedia...')
        command = command.replace("wikipedia", "")
        try:
            wiki = wikipedia.summary(command, sentences=3)
            print(wiki)
            talk("According to Wikipedia")
            talk(wiki)
        except wikipedia.exceptions.PageError:
            talk(f'sorry! no information found for {command}')
        except:
            pass

        time.sleep(8)

    # for jokes
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        print(joke)

    # google search
    elif 'search' in command:
        command = command.replace("search", "")
        base_url = "http://www.google.com/?#q="
        final_url = base_url + command
        talk('here are some best results')
        webbrowser.get().open(final_url, new=1)

    # stock price
    elif ('stock price of') in command:
        print('Price of all companies of NASDAQ EXCHANCE in USD and of NSE in INR')
        command = command.replace("stock price of ", "")

        # if no data found
        try:
            result = stockPrice(command, stockdata)
        except AttributeError:
            result = 'unable to find!'

        print(result)
        talk(result)

    # weather detail
    elif 'weather of' in command:
        city = command.replace("weather of ", "")

        weather_description = weatherDescription(city)
        print(weather_description)
        talk(weather_description)

    # thank you reply
    elif 'thank you' == command:
        answer_thankyou = ["you're welcome", "happy to help",
                           "i aim to please", "you're very welcome", "i'm here to help you"]
        reply = random.sample(answer_thankyou, 1)
        print(reply)
        talk(reply)

    # if don't understand
    else:
        talk("Sorry! I didn't understand")


if __name__ == "__main__":
    print("Hello, I'm your personal assistant Beta, how can I help you?")
    talk("Hello, I'm your personal assistant Beta, how can I help you?")

    while True:
        runBeta()
