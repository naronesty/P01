# P01: The Hamster Wheel by Hamsters of Destiny

Our project is a random profile generator in which users can select from a variety of themes and genres to generate semi-randomized fictional profile pages.

### Made by:
PM: Noakai Aronesty  
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
  
  
  
## How to install and run our project:

### 1. Clone the repository in terminal:
```
$ git clone git@github.com:naronesty/P01.git
```

### 2. Create and activate a virtual enviroment:
```
$ python3 -m venv ~/hamster

$ source ~/hamster/bin/activate (for Linux)
$ source ~/hamster/Scripts/activate (for Windows)
```

### 3. Install dependencies:
```
(hamster)$ pip install -r requirements.txt  
```

### 4. Navigate to the directory and run:
```
(hamster)$ cd P01/app
(hamster)$ python3 __init__.py
```

### 5. Open up the url given by the terminal: [http://127.0.0.1:5000/]
