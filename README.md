# Bio-Links Proxy Portal

A simple, fast, and elegant portal for accessing reverse-proxied bioinformatics web services. Designed for small teams and research groups, this project provides a clean user interface and a powerful automation script for easy deployment and management.

> **Powered by <img src="icons/google-gemini.svg" alt="Gemini Logo" width="100"/>**
> 
> This project was brought to life with the powerful assistance of Google's Gemini. From initial design and feature implementation to debugging and automation, Gemini played a crucial role in every step of the development process. 

---

## Features

- **Dynamic & Configurable**: Easily add, remove, or modify links by editing a single `config.json` file without touching the HTML.
- **Modern UI**: A clean, minimalist interface inspired by `hexo-theme-typo`, with automatic light and dark mode support based on your OS preference.
- **Live Search & Filtering**: Instantly find services by name using the search bar or filter by category with a dropdown menu.
- **Responsive Design**: Works beautifully on both desktop and mobile devices.
- **Nginx Automation**: Includes a Python script to automate the generation of robust Nginx reverse proxy configurations, saving time and preventing common errors.
- **No Dependencies**: The frontend is built with pure, dependency-free HTML, CSS, and vanilla JavaScript.

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend/Deployment**: Nginx (for reverse proxying) and Caddy (for web hosting and DNS-01 challenge)
- **Automation**: Python 3

## Project Structure

```
.
├── icons/                 # Icons for links
├── config.json            # Main configuration for links and categories
├── index.html             # The main portal page
├── script.js              # Frontend logic for search, filtering, and rendering
├── style.css              # All styles for the portal
├── generate_nginx_conf.py # Nginx configuration generator script
└── README.md              # You are here
```

## How to Use

### Adding a New Link

To add a new service to the portal, simply open `config.json` and add a new object to the array:

```json
{
  "name": "New Service",
  "url": "https://service.example.com/",
  "icon": "icons/new-icon.svg",
  "category": "New Category",
  "description": "Optional: A short description. If present, a confirmation dialog will appear before redirecting."
}
```

Or just give us an issue, we will add it soon!

### Generating an Nginx Configuration

To create a new reverse proxy configuration for a service, use the included Python script.

**Usage:**

Navigate to the project directory in your terminal and run:

```bash
python3 generate_nginx_conf.py --name <service_name> --url <target_url> --port <local_port>
```

**Arguments:**

- `--name`: A short, file-safe name for the service (e.g., `peanutbase`).
- `--url`: The full URL of the service you want to proxy (e.g., `https://www.peanutbase.org`).
- `--port`: The local port Nginx should listen on for this service (e.g., `2027`).
- `--output-dir` (Optional): The directory to save the `.conf` file. Defaults to the `./confs`.

**Example:**

```bash
python3 generate_nginx_conf.py --name peanutbase --url https://www.peanutbase.org --port 2027
```

The script will print the generated configuration and save it to `peanutbase.conf`. It will also provide you with the `mv` and `nginx` commands to deploy it.

## Future Development

- **Documentation Site**: For more extensive guides, consider setting up a dedicated static site generator (like Hexo or Hugo) in a `/docs` sub-directory.
- **CI/CD Automation**: Implement a CI/CD pipeline (e.g., with GitHub Actions) to automatically test and deploy the Nginx configurations upon changes to a repository.
