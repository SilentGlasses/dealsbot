# !!! THIS IS STILL A WORK IN PROGRESS !!!

> [!CAUTION]
> The `.env` template is **ONLY** there to help others build their file should they want to also use this app.
> - **Best Practice**:
>     - Rotate API keys regularly
>     - Keep the `.env` file out of version control
>     - Use a separate email for alerts

This is a Python-based deal scraper that pulls online deals from multiple sources. It supports:

- Secure OAuth2 authentication
- Multiple API sources (Amazon, eBay, Walmart, Target, Best Buy)
- Regex-based parsing for keyword-based searching
- Email notifications for new deals
- Logging and error handling for stability
- Scheduled execution using `cron` or `systemd`

## Features

- Queries major online stores using secure API authentication
- Configurable search terms and data sources
- Email alerts for new deals
- Logs all activity to a file
- Modular design with `.env` for secrets and `config.yaml` for settings

## Requirements

- Python 3.8+
- Internet Access
- Access to API keys for Amazon, eBay, Walmart, Target, and Best Buy

## Setup Instructions

- Clone the Repository
```
git clone https://github.com/SilentGlasses/dealsbot.git
cd dealsbot
```
- Set Up Virtual Environment
    - Create a Python virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
    - Install Dependencies
    ```
    pip install -r requirements.txt
    ```
- Make `.env` file and update it with production values:
```
mv .env_example .env
```

- Email Setup:
    - Use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if you have 2FA enabled on your email account.
    - For Gmail, enable "Allow less secure apps" (if not using App Password).
- API Key Setup:
    - Amazon: Get keys from [Amazon Developer Console](https://developer.amazon.com/)
    - eBay: Get keys from [eBay Developer Center](https://developer.ebay.com)
    - Walmart: Get keys from [Walmart Developer Portal](https://developer.walmart.com/)
    - Target: Get keys from [Target API Console](https://developer.target.com/)
    - Best Buy: Get keys from [Best Buy Developer](https://developer.bestbuy.com/)

## Running the Scraper

### Run Manually

To test the scraper manually:

```
python3 dealbot.py
```

### Option A: Schedule with cron

- Open the crontab file:
```
crontab -e
```
- Add the following line:
```
0 * * * * /path/to/venv/bin/python /path/to/dealsbot/dealbot.py
```

### Option B: Schedule with systemd

- Create a service file:
```
sudo nano /etc/systemd/system/dealsbot.service
```
- Add the following content:
```
[Unit]
Description=Deal Scraper
After=network.target

[Service]
User=username
WorkingDirectory=/path/to/dealsbot
ExecStart=/path/to/venv/bin/python /path/to/dealsbot/dealbot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
- Reload systemd:
```
sudo systemctl daemon-reload
```
- Enable the service:
```
sudo systemctl enable dealsbot
```
- Start the service:
```
sudo systemctl start dealsbot
```
- Check status:
```
sudo systemctl status dealsbot
```

## Logging and Monitoring

Logs are stored in logs/scraper.log:

```
tail -f logs/scraper.log
```

## Troubleshooting

| Issue | Solution |
|-------|----------| 
| Connection error | Check internet connection and API key settings
| Invalid credentials | Check the .env file for typos
| No emails sent | Check SMTP settings and permissions
| Token expired | Ensure OAuth2 token refresh is working


## Possible Future Improvements

- Add SQLite/MongoDB for storing historical deals
- Support more advanced filtering (price range, brand)
- Add a Telegram/Slack bot for instant notifications

## Contributing

Feel free to fork, modify, and submit pull requests!

## License

This project is licensed under the MIT License.
