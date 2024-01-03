<div align="center">
  
[![PyPI - Python Version](https://img.shields.io/badge/Python-%3E%3D%203.9-blue)](https://www.python.org/)
![OpenAI Badge](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=fff&style=for-the-badge)

</div>


https://github.com/leo007-htun/GPT3_Automated_Assistant_with_wake_word/assets/66962471/9524114d-1bd9-42cd-98dc-171db63401f8


## GPT3 Automated Assistant With Hot Word (Trigger Word)

``pyttsx3`` generates robotic voice which is not even understandable no matter how I tried to change language, speed and tone.

Thus, ``gtts`` is used and saved as ``speech.mp3``, which is again played by ``playsound`` module.

The script is run in the background, listening to any dialog. 

Once the ``hot-word``  or ``trigger-word``, ``JARVIS`` is heard, it will start responding. 

``set_alarm`` function is threaded so that other functions and commands can still be used while ``alarm`` is scheduling in background.

``GPT-3.5`` is utilized as assistant bot.

## Instructions
- Jarvis play (music)
- Jarvis what's the time
- Jarvis set alarm --:-- AM/PM
  - stop/turn off alarm
- Jarvis what's the temperature
- Jarvis how's the weather
- Jarvis save memo
- Jarvis show me the list of memo

## Installation

    $ git clone https://github.com/leo007-htun/GPT3_Automated_Assistant_with_wake_word.git
    

    $ pip install -r requirement.txt

replace ``YOUR_API_KEY`` with user's OpeanAI API key


## RUN
    $ source sr.sh to run in background



    
