import os
import time
import requests
import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
from config import apikey


chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Sonu: {query}\nAwesome: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": "aeafdac344956ace31c5beae8cde7312",
        "units": "metric"  # You can change units to "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The weather in {city} is {weather_description}. Temperature: {temperature}°C. Humidity: {humidity}%"
    else:
        return "Unable to fetch weather information."

def get_news(category):
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": "a58f9d4e616f461ea6406d07e5206f47",
        "category": category,
        "country": "in"  # Change the country code as needed
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "ok":
        articles = data["articles"]
        news_text = ""
        for index, article in enumerate(articles):
            news_text += f"News {index + 1}: {article['title']}. {article['description']}. "
        return news_text
    else:
        return "Unable to fetch news."


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Awesome A.I"

def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Select a different voice (change the index as needed)
    engine.setProperty('rate', 150)  # Adjust the speech rate (default is 200)
    engine.setProperty('volume', 1)  # Adjust the volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    print('Welcome to Awesome A.I')
    say("Welcome to Awesome AI")
    while True:
        print("Listening...")
        query = takeCommand()

        # Opening Websites:
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                time.sleep(60)
                say(f"Thank you for using Awesome AI")
                exit()

        # playing music
        if "play" in query.lower():
            if "music" in query.lower():
                musicPath = "D:\music\Hey Dukh Bhanjan.mp3"
                os.startfile(musicPath)
                time.sleep(5*60 + 40)
            elif "song" in query.lower():
                musicPath = "D:\music\Dil Kyun Yeh Mera Shor Kare.mp3"
                os.startfile(musicPath)
                time.sleep(5*60 + 40)

        # Get weather information
        if "weather" in query.lower():
            city = query.split("in")[1].strip()
            weather_info = get_weather(city)
            say(weather_info)
            break

        # Get News information
        if "news" in query.lower():
            category = query.split("news")[1].strip()
            news_info = get_news(category)
            say(news_info)
            break


        if "Quit".lower() in query.lower():
            quit()

        else:
            print("Chatting...")
            chat(query)
