# Nyla Fundraiser Copy CLI

A command-line tool that generates a 5-email drip campaign and 4 social media captions for Nyla, an NYC non-profit event coordinator. The tool uses OpenRouter AI API to generate the content based on the event name, date, and desired tone.

## Features

- Generates 5 fundraising emails with subject lines
- Creates 4 social media captions with hashtags
- Customizable event name, date, and tone
- Saves output to a markdown file for easy use
- Uses OpenRouter API for AI content generation

## Quick-start

```bash
git clone <your-repo-url>
cd <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENROUTER_API_KEY=sk-or-*****
python main.py --event "Spring Gala" --date "2025-05-30" --tone "upbeat"
```

## Usage Options

```
python main.py --event "Community Fundraiser" --date "2025-06-15" --tone "friendly"
python main.py --event "Charity Auction" --date "2025-08-22" --tone "formal"
python main.py --event "Holiday Food Drive" --date "2025-12-10" --tone "heartfelt"
```

Use the `--dry-run` flag to see the prompt without making an API call:

```
python main.py --event "Spring Gala" --date "2025-05-30" --tone "upbeat" --dry-run
```

## Output

The tool generates output in markdown format and:

1. Saves it to `out/campaign.md` 
2. Prints it to the console

## Implementation Details

- Uses OpenRouter API compatible with OpenAI's interface
- Default model: "openai/gpt-3.5-turbo"
- Implements error handling and timeout management
- Includes debugging utilities for API troubleshooting

## Requirements

- Python 3.6+
- OpenRouter API key (get one at https://openrouter.ai)
- Required packages: see requirements.txt

## License

MIT

_Implementation completed 2025-04-26_
