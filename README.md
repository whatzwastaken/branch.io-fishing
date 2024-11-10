
# 🌳 Branch.io Dashboard Panel

A powerful and intuitive dashboard panel for managing Branch.io integrations and analytics.

## ✨ Features

- Real-time analytics tracking
- Custom link management
- Campaign performance monitoring
- Deep linking configuration
- User journey visualization
- Advanced reporting tools

## 🚀 Getting Started

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Playwright (for browser automation)
- Flask (for web server)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Run the `setup.sh` script to set up the environment:

   ```bash
   bash setup.sh
   ```

   This will:
   - Update the package list and install necessary dependencies.
   - Set up a Python virtual environment.
   - Install required Python libraries (`Flask`, `Playwright`, etc.).
   - Install Playwright dependencies and Chromium.

3. Set up your credentials and configuration:
   - Modify the `settings.json` file with your Telegram Bot token and chat ID.
   - Make sure to place your proxy file (`proxy.txt`) in the root directory.

4. To start the application, run:

   ```bash
   python main.py
   ```

## Usage

- The Flask app serves an index page located in the `static` folder.
- You can send POST requests to `/validate` to trigger the scraping process, which will then notify you with the results via Telegram.

## Files

- `main.py`: Main Python script for running the web scraping process.
- `setup.sh`: Shell script for setting up the environment.
- `static/`: Folder containing static HTML and other assets.
- `proxy.txt`: File containing a list of proxies for the scraper.
- `settings.json`: Configuration file for Telegram bot and other settings.

## Notes

- The app uses Playwright to interact with a website and scrape data. Ensure that the target website's structure has not changed, as it may break the scraping logic.
- SSL certificates (`certificate.crt` and `certificate.key`) are required to run the app with HTTPS. Ensure they are placed in the appropriate directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

With love by: [@whatzwasthere](https://github.com/whatzwasthere)

