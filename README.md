
# QuotesAPI

A RESTful API of quotes that provide humor, grief, insight, motivation, and inspiration.

## 🌟 Why This Exists

This project began as a simple frontend quote machine inspired by the freeCodeCamp curriculum. After completing that, I recreated the project in Python and stored hundreds of quotes in a CSV file. As I learned Django and Django REST Framework, I decided to turn the quotes into a fully accessible API for others to learn and build with.

## 🚀 Quick Start

Visit the live project here: https://www.quotesapi.paulrblack.com

## For Users and Developers

### 🌐 For Everyone (Home Page)
Visit the home page: https://www.quotessapi.paulrblack.com
Here, you can:
* Browse daily quotes.


* Get quote(s) by tag or author.


* Generate Instagram or TikTok-style images to share quotes visually.

### 👩‍💻 For Developers (API Access)
Base URL: https://www.quotessapi.paulrblack.com/api/v1/quotes

Access a growing dataset of quotes programmatically, filterable by tag or author. Great for practice, portfolio projects, or learning how to work with a REST API.


## 📌 Features
- ```/quotes/``` — Returns all quotes.
- ```/quotes/<str:tag>/``` — Returns quotes filtered by a specific tag.
- ```/quotes/author/<str:author_name> /``` — Returns quotes filtered by author name.

### 🔎 Example
**By Tag**
```quotes/president/``` — Returns quotes tagged with "president" (includes quotes from former/current presidents).

**By Author**
```/quotes/author/abraham-lincon``` — Returns quotes from Abraham Lincoln.


## 📘 Usage Guide
At this time, only HTTP GET requests are supported. The QuotesAPI is read-only and does not require authentication.

### 🧭 Fair Use Policy ### 
* This API is designed for educational and experimental purposes.


* There are no enforced rate limits, but to help reduce hosting costs, please avoid spamming requests.


* Abuse or denial-of-service attacks will result in permanent IP bans.

### 💡Developer Etiquette ###

* Be courteous and helpful to fellow developers.


* Use local caching where possible.


* Report any issues or vulnerabilities responsibly.


## 🛠️ Tech Stack ##

**Backend:** Django REST Framework

**Hosting:** Digital Ocean

## 📬 Contact ##

For questions, comments, or concerns, email me at pblackdevdemo@gmail.com.


