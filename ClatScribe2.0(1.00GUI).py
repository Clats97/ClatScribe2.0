import pyaudio
import threading
import sys
import time
import string
import queue
from datetime import datetime
from google.cloud import speech
from google.oauth2 import service_account

service_account_info = {
    "project_id": "INSERT HERE",
    "private_key_id": "INSERT HERE",
    "private_key": "INSERT HERE",
    "client_email": "INSERT HERE",
    "client_id": "INSERT HERE",
    "auth_uri": "INSERT HERE",
    "token_uri": "INSERT HERE",
    "auth_provider_x509_cert_url": "INSERT HERE",
    "client_x509_cert_url": "INSERT HERE",
    "universe_domain": "googleapis.com"
}

credentials = service_account.Credentials.from_service_account_info(service_account_info)

stop_loop = False
transcription_log = []
audio_queue = queue.Queue()

def wait_for_enter():
    input("Press Enter at any time to stop recording...\n")
    global stop_loop
    stop_loop = True

def capture_audio(rate=16000, chunk=1024, channels=1):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk
    )
    try:
        while not stop_loop:
            try:
                data = stream.read(chunk, exception_on_overflow=False)
                audio_queue.put(data)
            except Exception as e:
                sys.stdout.write(f"\nAudio capture error: {e}\n")
                continue
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def request_generator(session_start_time, session_duration=290):
    while not stop_loop:
        if time.time() - session_start_time > session_duration:
            break
        try:
            data = audio_queue.get(timeout=0.1)
            yield speech.StreamingRecognizeRequest(audio_content=data)
        except queue.Empty:
            continue

def print_banner():
    red = "\033[31m"
    blue = "\033[34m"
    reset = "\033[0m"
    ascii_banner = f"""{red}
██████╗██╗      █████╗ ████████╗███████╗ ██████╗██████╗ ██╗██████╗ ███████╗
██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗██║██╔══██╗██╔════╝
██║     ██║     ███████║   ██║   ███████╗██║     ██████╔╝██║██████╔╝█████╗  
██║     ██║     ██╔══██║   ██║   ╚════██║██║     ██╔══██╗██║██╔══██╗██╔══╝  
╚██████╗███████╗██║  ██║   ██║   ███████║╚██████╗██║  ██║██║██████╔╝███████╗
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝
                                                                            
██████╗     ██████╗                                                         
╚════██╗   ██╔═████╗                                                        
 █████╔╝   ██║██╔██║                                                        
██╔═══╝    ████╔╝██║                                                        
███████╗██╗╚██████╔╝                                                        
╚══════╝╚═╝ ╚═════╝  
{reset}
{blue}SPEECH TO TEXT & TRANSCRIPTION TOOL{reset} {red}Version 1.00{reset}
"""
    print(ascii_banner)

if __name__ == "__main__":
    print_banner()
    input("Press Enter to start transcription...")

    sys.stdout.write("Listening... ")
    sys.stdout.flush()

    audio_thread = threading.Thread(target=capture_audio, daemon=True)
    audio_thread.start()

    exit_thread = threading.Thread(target=wait_for_enter, daemon=True)
    exit_thread.start()

    client = speech.SpeechClient(credentials=credentials)
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=False
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True
    )

    try:
        while not stop_loop:
            session_start_time = time.time()
            responses = client.streaming_recognize(
                streaming_config,
                request_generator(session_start_time)
            )
            printed_words = []
            for response in responses:
                if stop_loop:
                    break
                for result in response.results:
                    transcript = result.alternatives[0].transcript.strip()
                    words = transcript.split()
                    if len(words) > len(printed_words):
                        new_words = words[len(printed_words):]
                        for word in new_words:
                            clean_word = word.translate(str.maketrans('', '', string.punctuation))
                            sys.stdout.write(clean_word + " ")
                            sys.stdout.flush()
                            transcription_log.append(clean_word)
                        printed_words = words
                    if result.is_final:
                        printed_words = []
                        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"\nError during streaming recognition: {e}\n")
        sys.stdout.flush()

    user_choice = input("\nDo you want to save the transcription to a log file? (y/n): ")
    if user_choice.lower() in ['y', 'yes']:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcription_log_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(" ".join(transcription_log))
        sys.stdout.write(f"Log saved to {filename}\n")
    else:
        sys.stdout.write("Exiting without saving log.\n")