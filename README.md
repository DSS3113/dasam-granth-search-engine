# Dasam Granth Search Engine
A search engine for the Sri Dasam Granth - the book containing compositions attributed to the tenth Sikh Guru, Sri Guru Gobind Singh.

## Introduction
You might wonder why I decided to make this app even though a few search engines already exist for the Dasam Granth. The reason is that most of those search engines are either buggy or lack important search features. My goal was to create a search engine for the Dasam Granth that offers the same features as the popular search engine for the Sri Guru Granth Sahib available <a href="https://www.srigranth.org/">here</a>. I also hope that this app will aid people in the academia researching Sikh texts.

## How does it work?
This search engine is made in Flask and utilizes a SQLite <a href="https://github.com/shabados/database">database</a> of Sikh Bani and other Panthic texts created by the <a href="https://github.com/shabados">Shabad OS</a> team. For querying data, I have used the Flask-SQLAlchemy extension for Flask.

## How to run?
Firstly, we have to build the database. I am assuming that you have Node.js installed before beginning this. To do that, go <a href="https://github.com/shabados/database/tree/main">here</a> and clone the Shabad OS database. Next, `cd` into the root directory of the database project's local repo and run the following commands:
```
npm i
npm run build-sqlite
```
You will get a `database.sqlite` file in the `build` folder after the commands finish executing. Now, move the `database.sqlite` file to the local repo of this project in the `database` folder (create the folder if it doesn't exist).
Whew! The database setup is done.
Next, `cd` into the root directory of this project's local repo and run the following commands:<br />
For Unix:
```
pip3 install -r requirements.txt
python3 app.py
```
For Windows:
```
pip3 install -r requirements.txt
python app.py
```
## Planned features
+ There's minimal styling in this project and that needs to change; so that's definitely on the checklist.
+ Anything that comes to my mind later!

## Demonstration
Have a look at the pictures below:
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/1.jpg"></picture>
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/2.jpg"></picture>
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/3.jpg"></picture>
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/4.jpg"></picture>
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/5.jpg"></picture>
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/6.jpg"></picture>
 <picture><img src="https://github.com/DSS3113/dasam-granth-search-engine/blob/main/demo/7.jpg"></picture>

## Credits
I would like to thank the <a href="https://github.com/shabados">Shabad OS</a> team because this app wouldn't have been possible without their database. Also, the `to_ascii()` and `to_unicode()` functions used in this project's codebase have been inspired by the `toAscii()` and `toUnicode()` functions from another of <a href="https://github.com/shabados">Shabad OS</a>'s repos called <a href="https://github.com/shabados/gurmukhi-utils">Gurmukhi Utils</a>, which is a JavaScript library for converting, analyzing, and testing Gurmukhi strings.
