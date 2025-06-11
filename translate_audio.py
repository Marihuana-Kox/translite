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
    # Что бы оставить текст в исходном виде без перевода, надо в task оставить transcribe
    result_de = model.transcribe(audio_path, task="transcribe", language="de")
    # А что бы перевести на английский необходимо указать task = translete
    result = model.transcribe(audio_path, task="translate", language="de")
    deutche_text = result_de["text"]
    english_text = result["text"]

    # Перевод на русский
    russian_text = GoogleTranslator(source='en', target='ru').translate(english_text)
    # создаем пути сохранения файлов
    output_path = os.path.splitext(audio_path)[0] + "_translated_ru.txt"
    output_path_de = os.path.splitext(audio_path)[0] + "_deutche.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(russian_text)

    with open(output_path_de, "w", encoding="utf-8") as f:
        f.write(deutche_text)

    print(f"\n✅ Перевод завершён. Сохранено в: {output_path}")
    print("\n📄 Переведённый текст:\n")
    print(deutche_text)
    print(russian_text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Использование: python translate_audio.py путь_к_аудиофайлу.mp3")
    else:
        translate_audio_to_russian(sys.argv[1])
