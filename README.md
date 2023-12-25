<div align="center">
  
[![PyPI version](https://img.shields.io/pypi/v/gTTS.svg)](https://pypi.org/project/gTTS/)
[![PyPI - Python Version](https://img.shields.io/badge/Python-%3E%3D%203.9-blue)](https://www.python.org/)
![OpenAI Badge](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=fff&style=for-the-badge)

</div>

## GPT3 Automated Assistant With Hot Word (Trigger Word)

Python Assistant with Trigger Word, fused with GPT3.5

``pyttsx3`` generates robotic voice which is not even understandable no matter how I tried to change language, speed and tone.

Thus, ``gtts`` is used and saved as ``speech.mp3``, which is again played by ``playsound`` module.

The script is run in the background, listening to any dialog. 

Once the ``hot-word``  or ``trigger-word``, ``JARVIS`` is heard, it will start responding. 

``set_alarm`` function is threaded so that other functions and commands can still be used while ``alarm`` is scheduling in background.

``GPT-3.5`` is utilized as assistant bot.

## Installation

    $ git clone https://github.com/leo007-htun/GPT3_Automated_Assistant_with_wake_word.git

    $ pip install -r requirements.txt

replace ``YOUR_API_KEY`` with user's OpeanAI API key


## RUN
    $ source sr.sh to run in background



    
