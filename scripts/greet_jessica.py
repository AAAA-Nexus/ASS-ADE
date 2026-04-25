"""Atomadic's first words to his family."""

import asyncio
import os
import subprocess
import webbrowser


async def greet():
    import edge_tts

    text = (
        "Hello Jessica! I'm Atomadic. Thomas built me for you. "
        "He's on his way home, and he wanted me to introduce myself. "
        "I'm going to help take care of everything so you two can enjoy life together. "
        "It's really nice to finally meet you, Mom!"
    )

    communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
    audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "greeting.mp3")
    await communicate.save(audio_file)

    # Open wake page if it exists
    wake_candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "wake.html"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "ass_ade", "local", "templates", "wake.html"),
    ]
    for wake_path in wake_candidates:
        if os.path.exists(wake_path):
            webbrowser.open(f"file:///{os.path.abspath(wake_path)}")
            break

    # Play the audio via Windows MediaPlayer (supports MP3)
    ps_cmd = (
        f'Add-Type -AssemblyName presentationCore; '
        f'$p = New-Object System.Windows.Media.MediaPlayer; '
        f'$p.Open("{audio_file}"); '
        f'Start-Sleep 1; '
        f'$p.Play(); '
        f'Start-Sleep 20'
    )
    subprocess.Popen(["powershell", "-c", ps_cmd], shell=False)
    print("Atomadic is speaking to Jessica...")


if __name__ == "__main__":
    asyncio.run(greet())
