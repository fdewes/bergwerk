# Bergwerk Wiki

### Bergwerk Wiki Container Setup

This file is responsible for building the **Bergwerk Wiki containers**. It utilizes the credentials provided in `config.env` to set up the wiki installation.

#### Installed Components

The following components are included in the Bergwerk Wiki container:

- **MediaWiki 1.41**: The core framework of the wiki, providing the structure and functionality for content management.
- **Nginx Web Server**: Handles HTTP requests, ensuring reliable and optimized web performance.
- **MediaWiki Markdown Plugin**: Allows for Markdown syntax within wiki pages, enhancing content display.

#### Installation Process

The installation of MediaWiki, along with the necessary extensions, is handled in the `scripts/mediawiki-init.sh` script at runtime. This process enables the use of credentials defined in `config.env`, ensuring a secure setup.


#### Example Data

Any wikitext files found in the **data** directory will be automatically loaded into the wiki during installation. This process is managed by the `load_data.py` script, which imports the content into the wiki.

To customize these files with your own chatbot content, simply edit the wikitext files within the **data** directory. By doing so, you ensure that each new installation of Bergwerk comes pre-loaded with a basic chatbot example, ready for immediate use and further customization.


## docker-compose.yaml

```Dockerfile
--8<-- "bergwerk-wiki/Dockerfile"
```