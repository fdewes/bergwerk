
# Welcome to Bergwerk!

## Overview

**Bergwerk** is a user-friendly chatbot platform designed for easy setup and maintenance. It provides a simple way to manage chatbot content through a multi-user wiki system, making it accessible for non-technical users to contribute and update the chatbot’s knowledge base.

## Key Features

- **Simple Installation**: Easily set up via Docker Compose.
- **SSL Encryption**: Built-in support for SSL encryption using [Let's Encrypt](https://letsencrypt.org).
- **Content Management**: Based on [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki), ensuring robust and tested content management.
- **High Performance**: Powered by MySQL for efficient performance.
- **Conversation Logging**: Automatically logs conversations to wiki pages for seamless evaluation and review.
- **Multilingual Support**: Currently available in English and German, with the potential for further language expansion.
- **Open Source Software**: Free of charge, source code open to review. 

## How It Works

Bergwerk uses a wiki as its primary "database," allowing contributors to manage chatbot content similarly to editing a Wikipedia page. Non-technical users can add or modify information easily, and previous conversations can be reviewed and evaluated directly on the wiki.

## Quickstart Guide

Follow these steps to quickly set up Bergwerk:

### **1) Clone the Repository**:

Clone the Bergwerk repository and change into the newly created directory:

```
git clone https://github.com/HTW-Berlin-KI-Werkstatt/bergwerk
cd bergwerk
```

### **2) Configure Environment Variables**:  
   Edit the `config.env` file located in the root directory. Set the required passwords  (**minimum 10 characters**) for the following environment variables: `MEDIAWIKI_ADMIN_PASSWORD`, `BOT_PASSWORD`, and `SQL_PASSWORD`.

```
MEDIAWIKI_ADMIN=admin
MEDIAWIKI_ADMIN_PASSWORD=

BOT_USERNAME=bot
BOT_PASSWORD=

SQL_USERNAME=dbuser
SQL_PASSWORD=

SERVER=http://localhost
```

### **3) Start the Application**:
Run the following command to build and start all services:
```
docker compose up
```

### **4) Accessing the Chatbot**:
Open your browser and navigate to `http://localhost` to begin interacting with the chatbot.

To start building your own custom chatbot, log in to the wiki at `http://localhost/wiki` using the MediaWiki credentials you set earlier. Once logged in, you can easily modify content and experiment with creating your own assistant by editing the wiki pages—just like editing a Wikipedia article. Get creative and tailor the chatbot to suit your needs!

## Documentation

Further details can be found in the [documentation](https://bergwerk.readthedocs.io/en/latest/). You can also build the documentation locally by invoking these commands:

```
pip install -r requirements.txt
mkdocs serve
```

Then please proceed to `http://localhost:8000`
