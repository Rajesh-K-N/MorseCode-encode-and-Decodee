# MorseCode-encode-and-Decodee
# Morse Code Converter

A full-featured web application for converting text to Morse code and vice versa, with both Python and C implementations.


## Features

- **Bidirectional Conversion**:
  - Text to Morse code encoding
  - Morse code to text decoding

- **Elegant User Interface**:
  - Clean, responsive design using Bootstrap
  - Tabbed interface for easy switching between encoding and decoding
  - Visual mode to display Morse code as graphical dots and dashes

- **Practical Tools**:
  - Copy to clipboard functionality
  - Clear inputs and results with one click
  - Built-in Morse code reference table

- **Dual Implementation**:
  - Pure Python implementation for portability
  - C implementation for performance
  - Flask web interface for accessibility

## Tech Stack

- **Backend**: Flask (Python), C
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **APIs**: RESTful JSON endpoints

## Getting Started

### Prerequisites

- Python 3.7 or higher
- GCC compiler (only needed for C implementation)
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/morse-code-converter.git
   cd morse-code-converter
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   flask run
   ```

5. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Text to Morse Code

1. Select the "Text to Morse" tab
2. Enter your text in the input field
3. Click "Convert to Morse"
4. View the result in the output area
5. Toggle "Visual Mode" to see dots and dashes as graphical elements
6. Click "Copy to Clipboard" to copy the result

### Morse Code to Text

1. Select the "Morse to Text" tab
2. Enter Morse code using dots (.) and dashes (-) with spaces between characters and slashes (/) between words
3. Click "Convert to Text"
4. View the decoded text in the output area
5. Click "Copy to Clipboard" to copy the result

## Morse Code Rules

- **Letters and Numbers**: Each letter and number has a unique pattern of dots and dashes
- **Character Separation**: Use a single space between Morse characters
- **Word Separation**: Use a slash (/) or three spaces between words
- **Example**: "HELLO WORLD" in Morse code is `.... . .-.. .-.. --- / .-- --- .-. .-.. -..`

## Project Structure

```
morse_flask_app/
│
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # HTML template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## C Implementation

The project includes a standalone C implementation that can be compiled and used separately:

```bash
# Compile
gcc morse.c -o morse

# Encode text to Morse
./morse 1 "Hello World"

# Decode Morse to text
./morse 2 ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
```

## API Usage

The application provides two API endpoints for programmatic access:

### Python Implementation

```bash
curl -X POST http://127.0.0.1:5000/convert \
  -d "operation=encode&text=Hello World"
```

### C Implementation

```bash
curl -X POST http://127.0.0.1:5000/c_convert \
  -d "operation=encode&text=Hello World"
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- International Morse Code standard
- Flask framework
- Bootstrap CSS framework
