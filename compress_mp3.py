import subprocess
import os
import sys

def get_duration(filepath):
    result = subprocess.run([
        'ffprobe', '-i', filepath, '-show_entries', 'format=duration',
        '-v', 'quiet', '-of', 'csv=p=0'
    ], capture_output=True, text=True)

    try:
        return float(result.stdout.strip())
    except ValueError:
        print("❗ Не удалось определить длительность файла.")
        return 0

def process_audio(filepath):
    if not os.path.exists(filepath):
        print(f"Файл не найден: {filepath}")
        return

    print(f"🔍 Проверка длительности файла: {filepath}")
    duration = get_duration(filepath)

    # Если длительность больше 2 минут (120 сек) — обрезаем до 90 сек
    temp_cut = filepath.replace(".mp3", "_cut.mp3")
    if duration > 120:
        print("✂️ Обрезка до 90 секунд...")
        subprocess.run(['ffmpeg', '-y', '-i', filepath, '-t', '90', '-c', 'copy', temp_cut])
    else:
        temp_cut = filepath

    output_clean = filepath.replace(".mp3", "_cleaned.mp3")
    print("🎛 Перекодировка в нормальный MP3 (96k)...")
    subprocess.run(['ffmpeg', '-y', '-i', temp_cut, '-b:a', '96k', output_clean])

    print(f"✅ Готово: {output_clean}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Использование: python compress_mp3.py путь_к_файлу.mp3")
    else:
        process_audio(sys.argv[1])
