# P01: The Hamster Wheel by Hamsters of Destiny

Our project is a random profile generator in which users can select from a variety of themes and genres to generate semi-randomized fictional profile pages.

### Created by:
Noakai Aronesty (PM)  
Annabel Zhang  
Justin Zou  
Hebe Huang  

### Task Division:
Templates
- Home.html (Hebe, Justin)
- Login.html / Register.html (Noakai)
- Discover.html (Hebe)
- Profile.html (Justin)
  - Make sure each essential part of the profile is there (picture, bio, etc)
- CSS / Bootstrap (Noakai, Justin)  

Python
- Authentication (Noakai)
- db communication (Annabel)
- Slider for the different customization options (Annabel, Hebe)
- html communication / display (Noakai)
- Generate profiles (Justin, Hebe)
  - Taking information from the APIs and putting them on the profile
  - Different profiles based on Customization
  
  
## API Cards:
Text
- [Open Weather Map](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_OpenWeatherMap.md)
- [Joke](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_JokeAPI)
- [Cat Facts](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_CatFacts.md)
- [Random Word](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_RandomWord.md)
- [Twitter](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Twitter.md)
- [Meme](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_MemeAPI.md)
- [Fun Fact](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_FunFacts.md)

Images
- [NASA](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_NASA)
- [Random Duck](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_RandomDuck)
- [Dog](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_DogAPI.md)
- [Unsplash](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Unsplash.md)

  
## Launch Codes
- Install virtual environment <br>
$ ```python3 -m venv ~/hamster``` <br>
Linux: $ ```source ~/hamster/bin/activate``` <br>
Windows: $ ```source ~/hamster/Scripts/activate``` <br><br>
- Clone the Repository <br>
(hamster)$ ```git clone https://github.com/naronesty/P01.git ``` <br><br>
- Install Dependencies <br>
(hamster)$ ```cd P01 ``` <br>
(hamster)$ ```pip install -r requirements.txt``` <br><br> 
- Download the `keys` directory. Make sure it is in the `app` directory <br><br> 
- Run the app <br>
(hamster)$ ```cd app``` <br>
(hamster)$ ```python3 __init__.py``` <br><br>
- Open the website at http://127.0.0.1:5000/
