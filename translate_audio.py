import whisper
from deep_translator import GoogleTranslator
import sys
import os

def translate_audio_to_russian(audio_path):
    if not os.path.exists(audio_path):
        print(f"Файл не найден: {audio_path}")
        return

    print("🔍 Распознавание речи (немецкий)...")
    model = whisper.load_model("medium")
    result = model.transcribe(audio_path, task="translate", language="de")
    english_text = result["text"]

    print("🌍 Перевод на русский...")
    russian_text = GoogleTranslator(source='en', target='ru').translate(english_text)

    output_path = os.path.splitext(audio_path)[0] + "_translated_ru.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(russian_text)

    print(f"\n✅ Перевод завершён. Сохранено в: {output_path}")
    print("\n📄 Переведённый текст:\n")
    print(russian_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Использование: python translate_audio.py путь_к_аудиофайлу.mp3")
    else:
        translate_audio_to_russian(sys.argv[1])
