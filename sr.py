import speech_recognition as sr 
import datetime
import subprocess
import pywhatkit
import webbrowser
from gtts import gTTS
from pydub import AudioSegment
from playsound import playsound
import pyautogui
import time
import openai
import sched
import re
import threading
import os
import python_weather
import asyncio

hot_words = ['jervis', 'jarvis']
audio_file_path = 'path/to/your/audio_file.wav'
directory_path = '/home/leo/Assistant'

alarm_enabled = True
microphone_thread_enabled = True

api_key = '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'
openai.api_key = api_key

alarm_scheduler = sched.scheduler(time.time, time.sleep)
recognizer=sr.Recognizer()

'''
def convert(text, input_filename='speech.mp3'):
    # Convert text to speech and save as MP3
    modified = text + ", my lord"
    tts = gTTS(modified)
    tts.save(input_filename)

    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_filename)

    # Speed up the audio by 2x during export
    #modified_audio = audio.speedup(playback_speed=1.5)

    #modified_audio.export(input_filename, format="mp3")
    audio.export(input_filename, format="mp3")
    playsound(input_filename)'''

def convert(text, input_filename='speech.mp3'):
    modified = text 
    tts = gTTS(modified)
    tts.save(input_filename)
    audio = AudioSegment.from_mp3(input_filename)
    audio.export(input_filename, format="mp3")

    # Use threading to play the sound in the background
    play_thread = threading.Thread(target=playsound, args=(input_filename,))
    play_thread.start()

    # Optionally, wait for the sound to finish playing before returning
    play_thread.join()

    # Clean up the temporary MP3 file
    os.remove(input_filename)


def play_music(query):
    pywhatkit.playonyt(query)
    time.sleep(5)  # Adjust the sleep duration based on your system's performance and network speed
    pyautogui.press('space')  # Press the spacebar to play/pause the video
    print(query)

def play_alarm(sound_file):
    global alarm_enabled
    t_end = time.time() + 60 * 5
    with sr.Microphone() as source:
        while time.time() < t_end:
            print("Wake up!")
            playsound(sound_file)
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for stop command...")

            try:
                recordedaudio = recognizer.listen(source, timeout=1)
                text = recognizer.recognize_google(recordedaudio, language='en_US').lower()
                print('Your message:', format(text))

                if 'stop' in text or 'turn off' in text:
                    stop_alarm()
                    break
                else:
                    pass

            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
            except sr.RequestError as ex:
                print(f"Could not request results from Google Speech Recognition service; {ex}")
            except Exception as ex:
                print(f"An unexpected error occurred: {ex}")


        #asyncio.run(microphone_listener())
        
        
        # Stop the microphone thread when the alarm is turned off or time is up
    #microphone_thread_enabled = False
        #microphone_thread_instance.join()


def stop_alarm():
    global alarm_enabled
    alarm_enabled = False
    print("Alarm turned off...")
    convert("Turning off Alarm")

def set_alarm(hour, minute):
    # Get the current time
    global alarm_enabled
    current_time = time.localtime()
    current_hour, current_minute = current_time.tm_hour, current_time.tm_min

    # Calculate the time difference in seconds until the alarm
    time_difference = (hour - current_hour) * 3600 + (minute - current_minute) * 60

    # Check if the specified time is in the future
    if time_difference > 0:
        set_time = f"Alarm set for {hour:02d}:{minute:02d}"
        print(set_time)
        convert(set_time)
        
        # Schedule the alarm

        # Create a timer for the alarm
        alarm_timer = threading.Timer(time_difference, play_alarm, args=('alarm.wav',))
        #alarm_thread = threading.Thread(target=play_alarm)
        alarm_timer.start()
       # alarm_scheduler.enter(time_difference, 1, play_alarm, argument=('alarm.wav',))
        #alarm_scheduler.run()
        #stop_thread = threading.Thread(target=microphone_listener)
        #stop_thread.start()
    else:
        print("Please set an alarm for a future time.")
        convert("Please set an alarm for a future time.")

def chat_with_assistant(chat):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "you are a personal assistant called jarvis, provide any information that I ask in succinct "},
            {"role": "user", "content": chat},
        ],

        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    assistant_response = response['choices'][0]['message']['content']
    print("Assistant:", assistant_response)

    convert(assistant_response)
 
async def get_weather_attribute(attribute_name):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Liverpool')

        # Check if the attribute exists
        if hasattr(weather.current, attribute_name):
            # Access the attribute dynamically using getattr
            attribute_value = getattr(weather.current, attribute_name)
            print(f"{attribute_name}: {attribute_value}")
            return attribute_value
        else:
            print(f"{attribute_name} is not a valid attribute for weather.current")

async def get_temp():
    temperature = await get_weather_attribute("temperature")

    if temperature == 1:
        convert("It's, "+str(temperature)+" degree celcius outside")
    else:
        convert("It's, "+str(temperature)+" degrees celcius outside")

async def get_wind():
    spd = await get_weather_attribute("wind_speed")

    if spd == 1:
        convert("the wind is currently at "+str(spd)+" mile per hour")
    else:
        convert("the wind is currently at "+str(spd)+" miles per hour")

async def get_rain():
    rain = await get_weather_attribute("description")
    cond = 'light rain'
    if cond in rain.lower():
        print(str(rain))
        convert("Drizzles maybe detected in certain areas")
    else :
        convert(rain)

def cmd():

    with sr.Microphone() as source:
        print("Clearing background noises...Please wait")
        recognizer.adjust_for_ambient_noise(source,duration=0.5)
        print('Ask me anything..')
        recordedaudio=recognizer.listen(source)

    try:
        text=recognizer.recognize_google(recordedaudio,language='en_US')
        text=text.lower()
        print('Your message:',format(text))

        if any(word in text for word in hot_words):  
            if 'firefox' in text:
                c='Opening firefox..'
                convert(c)
                programName = "/usr/bin/firefox"
                subprocess.Popen([programName])

            elif 'time' in text:
                time = datetime.datetime.now().strftime('%I:%M %p')
                print(time)
                convert(time)
                #chat_with_assistant(time)

            elif 'play' in text:
                omit_words = ['jarvis', 'jervis', 'play']
                words = text.split()
                filtered_words = [word for word in words if word.lower() not in omit_words]
                filtered_text = ' '.join(filtered_words)
                filtered_text_ = 'playing'+filtered_text
                convert(filtered_text_)
                play_music(filtered_text  )
                

            elif 'set alarm' in text:
                numbers = re.findall(r'\b\d+\b', text)
                numbers = "".join(numbers)
                if len(numbers) == 3:
                    hours = int(numbers[0])
                    minutes = int(numbers[1:])
                elif len(numbers) == 4:
                    hours = int(numbers[:2])
                    minutes = int(numbers[2:])
                else:
                    hours = None
                    minutes = None

                if 'p.m' in text or 'pm' in text.lower():
                    # Convert to 24-hour format
                    if hours != 12:
                        hours += 12
                elif 'a.m' in text or 'am' in text.lower():
                    # Handle 12 am case
                    if hours == 12:
                        hours = 0
                print("Hours:", hours, "\nMinutes:", minutes)
                set_alarm(hours,minutes)

            elif 'temperature' in text:
                asyncio.run(get_temp())


            elif any(keyword in text for keyword in ['windy', 'wind speed', 'wind']):
                asyncio.run(get_wind())

            elif any(keyword in text for keyword in ['rain', 'weather']):
                asyncio.run(get_rain())

            elif 'youtube' in text:
                b='opening youtube'
                convert(b)
                webbrowser.open('www.youtube.com')

            #if 'create memo' in text:
            elif any(keyword in text for keyword in ['create memo', 'creating memo', 'save memo', 'safe memo']):
                save_text(text)

            elif any(keyword in text for keyword in ['list', 'many memo', 'money memo', 'current memo']):
                list_txt_files(directory_path)

            else:
                chat_with_assistant(text)
            
            #if 'ask' or 'chat' in text:
                #chat_with_assistant(text)

    except Exception as ex:
        print(ex)

def list_txt_files(directory_path):
    try:
        # Get the list of files in the specified directory
        file_list = os.listdir(directory_path)

        # Filter out only the .txt files
        txt_files = [file for file in file_list if file.endswith(".txt")]

        if txt_files:
            print(f"Number of .txt files: {len(txt_files)}")
            num_txt = len(txt_files)
            if num_txt > 1:
                convert('There are'+ str(num_txt) + 'text files in the directory')

            elif num_txt == 1:
                convert('There is only'+ str(num_txt) + 'text file in the directory')
            print("List of .txt files:")

            convert("Would you like to know the names?")
            with sr.Microphone() as source:
                print("Clearing background noises...Please wait")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("YES OR NO?")
                recorded_audio = recognizer.listen(source)

            try:
                name = recognizer.recognize_google(recorded_audio, language='en_US')
                name = name.lower()
                print('Your memo name:', format(name))
                if 'yes' in name:
                    for txt_file in txt_files:
                        print(txt_file)
                        convert(txt_file)
                else:
                    pass
            except Exception as ex:
                print(ex)
        
        else:
            print("No .txt files found in the directory.")
            convert("No text files found in the directory.")

    except Exception as e:
        print(f"An error occurred: {e}")

def save_text(content_prompt="Ready for memo..."):
    g = "What would you like to name your memo"
    convert(g)
    with sr.Microphone() as source:
        print("Clearing background noises...Please wait")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("content_prompt")
        recorded_audio = recognizer.listen(source)

    try:
        name = recognizer.recognize_google(recorded_audio, language='en_US')
        name = name.lower()
        print('Your memo name:', format(name))

        content_prompt = "What content you like to save in " + name + "?"
        print(content_prompt)
        convert(content_prompt)
        with sr.Microphone() as source:
            print("Clearing background noises...Please wait")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print('Ready for memo content...')
            recorded_audio = recognizer.listen(source)

        try:
            content = recognizer.recognize_google(recorded_audio, language='en_US')
            content = content.lower()
            print('Your memo content:', format(content))

            with open(f'{name}.txt', 'a') as f:
                f.write("\n" + content )
                print(f"{name}.txt created or updated...")
                create = "Memo saved"
                convert(create)
        except Exception as ex:
            print(ex)
    except Exception as ex:
        print(ex)



if __name__ == "__main__":

    while True:
        
        cmd()















