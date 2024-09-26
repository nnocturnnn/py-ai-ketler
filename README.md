
# Instagram Profile Parser with OpenAI Integration

This project is designed to parse Instagram profile information (profile picture, biography, and recent posts) and generate a personalized message using OpenAI's GPT model. The project leverages the **Instaloader** library for scraping Instagram data and the **OpenAI** API for generating friendly messages based on the parsed content.

## Features

- **Parse Instagram Profile**: Fetch profile picture URL, biography, and the latest posts (up to 5).
- **Generate Personalized Message**: Use OpenAI's GPT to create a friendly message based on the parsed Instagram data (biography and posts).

## Prerequisites

Make sure you have the following installed:

- Python 3.x
- Instagram account credentials (for authorized scraping)
- OpenAI API Key

### Python Libraries

Install the necessary Python libraries by running:

```bash
pip install -r requirements.txt
```

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nnocturnnn/py-ai-ketler.git
   cd instagram-profile-parser
   ```

2. **Set up your environment:**

   - Replace `'your_username'` and `'your_password'` with your Instagram credentials.
   - Replace `'your-openai-api-key'` with your OpenAI API key in the script.

3. **Usage:**

   To run the script and fetch Instagram profile data, simply execute the following command:

   ```bash
   python main.py
   ```

## Project Structure

```
.
├── main.py                 # Main script for parsing Instagram profile and generating message
├── README.md               # Project documentation
└── requirements.txt        # List of Python dependencies
```
