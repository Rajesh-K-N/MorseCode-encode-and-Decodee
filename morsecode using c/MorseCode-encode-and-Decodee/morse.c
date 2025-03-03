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
    printf("\n");
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
        if (morse[i] == ' ' || morse[i] == '\0') {
            // End of a Morse character
            if (morsePos > 0) {
                morseChar[morsePos] = '\0'; // Null-terminate
                
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
    printf("\n");
}

int main() {
    char input[500];
    int choice;
    
    printf("Morse Code Converter\n");
    printf("1. Encode (text to Morse)\n");
    printf("2. Decode (Morse to text)\n");
    printf("Enter your choice (1 or 2): ");
    
    if (scanf("%d", &choice) != 1) {
        printf("Invalid input\n");
        return 1;
    }
    
    // Clear input buffer
    while (getchar() != '\n');
    
    if (choice == 1) {
        printf("Enter text to encode: ");
        fgets(input, sizeof(input), stdin);
        
        // Remove trailing newline
        size_t len = strlen(input);
        if (len > 0 && input[len-1] == '\n') {
            input[len-1] = '\0';
        }
        
        printf("Morse code: ");
        encodeToMorse(input);
    }
    else if (choice == 2) {
        printf("Enter Morse code to decode (use spaces between characters and / between words):\n");
        fgets(input, sizeof(input), stdin);
        
        // Remove trailing newline
        size_t len = strlen(input);
        if (len > 0 && input[len-1] == '\n') {
            input[len-1] = '\0';
        }
        
        printf("Decoded text: ");
        decodeMorse(input);
    }
    else {
        printf("Invalid choice\n");
        return 1;
    }
    
    return 0;
}