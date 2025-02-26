# Bergwerk Database

This file is responsible for building the **Bergwerk Database container**. It uses the latest MySQL image and initiates the setup with the `custom_init.sh` script, configuring the database for secure and efficient operation within the Bergwerk environment.

### Key Setup Details

- **Account Creation**: The `custom_init.sh` script creates necessary user accounts based on the credentials specified in the `config.env` file. This allows for secure access to the database by various Bergwerk components.
- **TLS Certificates**: To ensure secure remote connections to the MySQL server, the script generates TLS certificates, enhancing the security of data exchanges within the application.
- **Database Creation**: Two essential databases are created during the setup:
  - **Wiki Database**: Dedicated to the MediaWiki installation, this database stores all wiki-related content for managing the chatbot's knowledge base.
  - **Tracker Database**: Supports the tracker store, logging user interactions for review and further training of the chatbot.

This setup ensures that the Bergwerk Database container is optimized for secure and reliable performance, supporting the critical data needs of the Bergwerk application.


## docker-compose.yaml

```Dockerfile
--8<-- "db/Dockerfile"
```