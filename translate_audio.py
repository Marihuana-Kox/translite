import warnings

import whisper
import torch
from deep_translator import GoogleTranslator
import compress_mp3 as mp3
import sys
import os

def translate_audio_to_russian(audio_path):
    if not os.path.exists(audio_path):
        print(f"Файл не найден: {audio_path}")
        return
    try:
        audio_path = mp3.process_audio(audio_path)
        print("Компресс файла прошeл успешно")
    except ValueError as e:
        print(f"Ошибка процесса: {e}")

    print("🔍 Распознавание речи (немецкий)...")
    model = whisper.load_model("medium", device="cpu").to(torch.float32)  # избегаем FP16 # явно указываем CPU
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
    # model = whisper.load_model("medium")
    # Что бы оставить текст в исходном виде без перевода, надо в task оставить transcribe
    result_de = model.transcribe(audio_path, task="transcribe", language="de")
    # А что бы перевести на английский необходимо указать task = translete
    result = model.transcribe(audio_path, task="translate", language="de")
    deutche_text = result_de["text"]
    english_text = result["text"]

    # Перевод на русский
    russian_text = GoogleTranslator(source='en', target='ru').translate(english_text)
    # создаем пути сохранения файлов
    puth_file = ["_translated_ru.txt", "_deutche.txt"]
    result_text = [russian_text, deutche_text]

    for pth, restext in zip(puth_file, result_text):
        output_path = os.path.splitext(audio_path)[0] + pth
        read_text_to_file(output_path, restext)


def read_text_to_file(puth, text):
    with open(puth, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Использование: python translate_audio.py путь_к_аудиофайлу.mp3")
    else:
        translate_audio_to_russian(sys.argv[1])
