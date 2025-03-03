from flask import Flask, render_template, request, jsonify
import ctypes
import os
import tempfile
import subprocess
import platform

app = Flask(__name__)

# Morse code mappings
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

# Reverse dictionary for decoding
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

def encode_to_morse(message):
    """Convert text to Morse code"""
    morse = []
    for char in message.upper():
        if char == ' ':
            morse.append('/')
        elif char in MORSE_CODE_DICT:
            morse.append(MORSE_CODE_DICT[char])
    return ' '.join(morse)

def decode_from_morse(morse):
    """Convert Morse code to text"""
    # Split the morse code by space
    morse_words = morse.split(' / ')
    decoded_message = []
    
    for word in morse_words:
        morse_chars = word.split(' ')
        decoded_word = []
        
        for morse_char in morse_chars:
            if morse_char in REVERSE_MORSE_DICT:
                decoded_word.append(REVERSE_MORSE_DICT[morse_char])
            elif morse_char:  # If not empty
                decoded_word.append('?')
        
        decoded_message.append(''.join(decoded_word))
    
    return ' '.join(decoded_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.form
    operation = data.get('operation')
    text = data.get('text', '')
    
    if operation == 'encode':
        result = encode_to_morse(text)
    elif operation == 'decode':
        result = decode_from_morse(text)
    else:
        return jsonify({'error': 'Invalid operation'}), 400
    
    return jsonify({'result': result})

# Optional: C implementation integration (for demonstration purposes)
def compile_c_program():
    """Compile the C program and return the path to the executable"""
    c_code = """
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Function to encode a message to Morse code
void encodeToMorse(const char* message) {
    const char* Morse[26] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", 
                             ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", 
                             "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.."};
    
    for (size_t i = 0; i < strlen(message); i++) {
        if (isalpha(message[i])) {
            int j = tolower(message[i]) - 'a';
            printf("%s ", Morse[j]);
        }
        else if (message[i] == ' ') {
            // Add a slash to represent word spacing in Morse code
            printf("/ ");
        }
        else if (isdigit(message[i])) {
            // Morse code for numbers
            const char* digitMorse[10] = {"-----", ".----", "..---", "...--", "....-", 
                                          ".....", "-....", "--...", "---..", "----."};
            printf("%s ", digitMorse[message[i] - '0']);
        }
        else {
            // For non-alphabetic and non-digit characters
            printf("%c ", message[i]);
        }
    }
}

// Function to decode Morse code to text
void decodeMorse(const char* morse) {
    const char* Morse[36] = {".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", 
                             ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", 
                             "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..",
                             "-----", ".----", "..---", "...--", "....-", ".....", "-....", 
                             "--...", "---..", "----."};
    
    const char* characters = "abcdefghijklmnopqrstuvwxyz0123456789";
    
    char morseChar[10] = {0}; // To store individual Morse characters
    int morsePos = 0;
    
    for (size_t i = 0; i <= strlen(morse); i++) {
        if (morse[i] == ' ' || morse[i] == '\\0') {
            // End of a Morse character
            if (morsePos > 0) {
                morseChar[morsePos] = '\\0'; // Null-terminate
                
                if (strcmp(morseChar, "/") == 0) {
                    printf(" "); // Space between words
                } else {
                    // Look up the Morse code
                    int found = 0;
                    for (int j = 0; j < 36; j++) {
                        if (strcmp(morseChar, Morse[j]) == 0) {
                            printf("%c", characters[j]);
                            found = 1;
                            break;
                        }
                    }
                    if (!found) {
                        printf("?"); // Unknown Morse code
                    }
                }
                morsePos = 0; // Reset for next character
            }
        } else {
            // Building up a Morse character
            morseChar[morsePos++] = morse[i];
            
            // Protect against buffer overflow
            if (morsePos >= sizeof(morseChar) - 1) {
                morsePos = sizeof(morseChar) - 1;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        return 1;
    }
    
    int mode = atoi(argv[1]);
    char* input = argv[2];
    
    if (mode == 1) {
        encodeToMorse(input);
    } else if (mode == 2) {
        decodeMorse(input);
    }
    
    return 0;
}
    """
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    c_file_path = os.path.join(temp_dir, "morse.c")
    
    # Write the C code to a file
    with open(c_file_path, "w") as f:
        f.write(c_code)
    
    # Determine the executable extension based on the platform
    if platform.system() == "Windows":
        exe_path = os.path.join(temp_dir, "morse.exe")
        compile_cmd = ["gcc", c_file_path, "-o", exe_path]
    else:
        exe_path = os.path.join(temp_dir, "morse")
        compile_cmd = ["gcc", c_file_path, "-o", exe_path]
    
    # Compile the C program
    try:
        subprocess.run(compile_cmd, check=True)
        return exe_path
    except subprocess.CalledProcessError:
        return None

@app.route('/c_convert', methods=['POST'])
def c_convert():
    """Use the C implementation to convert"""
    data = request.form
    operation = data.get('operation')
    text = data.get('text', '')
    
    exe_path = compile_c_program()
    if not exe_path:
        return jsonify({'error': 'Failed to compile C program'}), 500
    
    mode = "1" if operation == "encode" else "2"
    try:
        result = subprocess.check_output([exe_path, mode, text], text=True)
        return jsonify({'result': result.strip()})
    except subprocess.CalledProcessError:
        return jsonify({'error': 'Failed to execute C program'}), 500

if __name__ == '__main__':
    app.run(debug=True)