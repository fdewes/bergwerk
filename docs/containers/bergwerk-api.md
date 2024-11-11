# Bergwerk API

### Bergwerk API Container Setup

The **Bergwerk API container** is integral to the Bergwerk system, handling communication between various services within the application. It serves as the intermediary, facilitating smooth data flow and synchronization across Bergwerk components.

#### Important Services Installed

The API container includes key libraries and tools necessary for chatbot functionality:

- **PyTorch**: Supports building the intent classifier and interpreting user text input. PyTorch enables the API to handle natural language processing tasks.
- **Requests**: Facilitates HTTP requests to and from the wiki and other components, allowing for communications within the Bergwerk environment.


## docker-compose.yaml

```Dockerfile
--8<-- "bergwerk-api/Dockerfile"
```