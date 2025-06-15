import subprocess  # Для запуска внешних команд (ffprobe, ffmpeg)
import os          # Для работы с файловой системой

def get_duration(filepath):
    """
    Получает длительность аудиофайла с помощью ffprobe.
    Возвращает длительность в секундах (float).
    """
    result = subprocess.run([
        'ffprobe', '-i', filepath,
        '-show_entries', 'format=duration',
        '-v', 'quiet', '-of', 'csv=p=0'
    ], capture_output=True, text=True)

    try:
        return float(result.stdout.strip())  # Преобразуем результат в число
    except ValueError:
        return 0  # Возвращаем 0, если длительность не определена

def process_audio(filepath):
    """
    Обрабатывает MP3-файл:
    - Проверяет его длительность.
    - Если длительность > 2 минут, обрезает до 90 секунд.
    - Перекодирует в MP3 с битрейтом 96k.
    """
    if not os.path.exists(filepath):
        print(f"Файл не найден: {filepath}")
        return

    duration = get_duration(filepath)

    # Если длительность больше 120 секунд — обрезаем до 90 секунд
    needs_cut = duration > 120
    temp_cut = filepath.replace(".mp3", "_cut.mp3") if needs_cut else filepath

    if needs_cut:
        subprocess.run([
            'ffmpeg', '-y', '-i', filepath,
            '-t', '90', '-c', 'copy', temp_cut
        ])

    output_clean = filepath.replace(".mp3", "_cl.mp3")

    # Перекодируем в 96 kbps MP3
    subprocess.run([
        'ffmpeg', '-y', '-i', temp_cut,
        '-b:a', '96k', output_clean
    ])

    print(f"✅ Файл обработан: {output_clean}")
    return output_clean
