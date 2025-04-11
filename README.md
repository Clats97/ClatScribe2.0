# ClatScribe2.0
ClatScribe 2.0 is a variant of the original ClatScribe project, but uses the Google speech to text model. It is a speech-to-text tool that captures real-time audio and transcribes it in real time with the Google Transcription API. It has a CLI and a GUI.

![clatscribe2 0](https://github.com/user-attachments/assets/071495d2-89f1-4387-ba09-82190d6d4ecf)
![clatscribe2 0info](https://github.com/user-attachments/assets/a04541ed-a4a0-4d8a-8fc6-aa6ba74df0da)

# Speech-to-Text & Transcription Tool

This command-line tool captures audio from your microphone in real time, streams it to the Google Cloud Speech-to-Text API, and displays the transcription live in the terminal. Optionally, you can save the transcription log to a timestamped text file.

## Features

- **Real-Time Audio Capture:** Uses PyAudio to capture live audio.
- **Streaming Transcription:** Leverages Google Cloud Speech-to-Text for converting speech to text.
- **Live Display:** Updates and prints words as they are recognized.
- **Transcription Logging:** Optionally saves the full transcription log to a file.
- **Graceful Shutdown:** Stops audio capture when the user presses Enter.

## Requirements

- **Python 3.x**  
- **PyAudio:** [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/)  
- **Google Cloud Speech-to-Text:** [Google Cloud Speech-to-Text Documentation](https://cloud.google.com/speech-to-text/docs)  
- **google-auth**  

You can install the required packages using pip:

pip install pyaudio google-cloud-speech google-auth

## Setup

1. **Google Cloud Configuration:**
   - Enable the [Google Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text).
   - Create a service account with appropriate permissions.
   - Download the JSON key file

2. **Configure the Script:**
   - Verify the `service_account_info` dictionary in the script is set with your correct project details and credentials.
   - Adjust parameters such as sample rate, chunk size, and language code in the script if needed.

## Usage

1. **Run the Script:**

2. **Workflow:**
   - The script displays an ASCII banner and waits for your confirmation to start transcription.
   - Once started, it listens to your microphone input and streams the audio to the Speech-to-Text API.
   - Transcribed words are printed to the terminal as they are recognized.
   - At any point, press **Enter** to stop the recording.
   - After stopping, you will be prompted whether to save the transcription log to a file. If you choose to save, a file with a name like `transcription_log_YYYYMMDD_HHMMSS.txt` is generated.

## Code Structure

- **`capture_audio()`**  
  Captures audio from the microphone using PyAudio and places audio data into a queue.

- **`wait_for_enter()`**  
  Monitors user input and sets a flag to gracefully terminate the audio capture loop.

- **`request_generator()`**  
  A generator function that yields audio data chunks to the Google Cloud Speech API.

- **`print_banner()`**  
  Displays an ASCII banner along with version information when the script starts.

- **Main Execution Block:**  
  - Initializes audio and input threads.
  - Configures the Google Cloud Speech client with the provided credentials.
  - Manages streaming responses from the API and logs transcribed words.
  - Prompts the user to save the transcription log after stopping.

## Troubleshooting

- **Audio Issues:**  
  Ensure your microphone is correctly connected and that PyAudio is properly installed.

- **API Errors:**  
  Verify your Google Cloud credentials are accurate, and that the Speech-to-Text API is enabled in your project.

- **Dependencies:**  
  Double-check that all required Python packages are installed with compatible versions.

## Security Considerations

- **Credentials:**  
  Do not expose your private key. Use environment variables or secure configuration files for production deployments.

- **Data Privacy:**  
  Be aware that your audio is sent to Google Cloud for processing. Review Google’s privacy policy if you handle sensitive information.

## License

This project is licensed under the Apache 2.0 License

## Feedback and Contribution

Contributions and suggestions are welcome. Please open issues or submit pull requests if you encounter bugs or have ideas for enhancements.

**Author**

Joshua M Clatney (Clats97)

Ethical Pentesting Enthusiast

Copyright 2025 Joshua M Clatney (Clats97)


