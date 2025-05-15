import os
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageSequence


class ASCIIVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Video Generator")
        self.root.configure(bg="#0d0d0d")

        self.root.bind("<Escape>", lambda e: self.root.quit())

        self.res_var = tk.StringVar(value="360p")
        self.fps_var = tk.IntVar(value=30)
        self.ascii_set_var = tk.StringVar(value="Standard")
        self.cleanup_var = tk.BooleanVar(value=True)
        self.fast_mode_var = tk.BooleanVar(value=False)
        self.lang_var = tk.StringVar(value="English")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Waiting...")

        self.ASCII_SETS = {
            "Standard": "@%#*+=-:. ",
            "Dense": "@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,^`'. ",
            "Minimal": " .:-=+*#%@",
            "Binary": "01",
            "Blocks": "█▓▒░ ",
            "Numbers": "0123456789",
            "Dots": " .•oO@",
            "Sharp": "$@B%&WM#*+=-:. ",
            "Smooth": " .:-=+*#%@",
            "Cubic": " ▖▘▝▗▚▞▛▜▟▙█",
            "Braille": "⠀⠁⠃⠇⠧⠷⠿",
            "ASCII Art": "#Wo-., ",
            "Emoji Mono": "⚪⚫",
            "Textured": "MWNXK0Okxdolc:;,'.. ",
            "Symbolic": "*&%#@!+=-:. ",
            "Runes": "ᚠᚢᚦᚨᚱᚲᚷᚹᚺᛉᛋ ",
            "Custom Bars": "█▇▆▅▄▃▂▁ "
        }

        self.LANGUAGES = [
            "English", "Spanish", "French", "German", "Italian", "Chinese (Simplified)", "Chinese (Traditional)",
            "Japanese", "Korean", "Russian", "Portuguese", "Arabic", "Hindi", "Bengali", "Turkish", "Vietnamese",
            "Polish", "Dutch", "Greek", "Hebrew", "Swedish", "Czech", "Hungarian", "Finnish", "Norwegian",
            "Danish", "Romanian", "Thai", "Indonesian", "Malay", "Ukrainian", "Catalan", "Slovak", "Croatian",
            "Serbian", "Bulgarian", "Lithuanian", "Latvian", "Slovenian", "Estonian"
        ]

        self.translations = {
            "English": {
                "title": "ASCII Video Generator",
                "resolution": "Resolution:",
                "fps": "FPS:",
                "ascii_style": "ASCII Style:",
                "fast_mode": "⚡ Fast loading (lower quality)",
                "cleanup": "🧹 Clean temp frames after export",
                "language": "Language:",
                "instructions": "📄 Instructions",
                "import_file": "🎬 Import MP4 / GIF / Image",
                "instructions_text": "1. Choose resolution, FPS, and style.\n2. Optionally enable fast mode.\n3. Import an MP4, GIF, or image to convert.\n4. Your ASCII export will be saved.",
                "waiting": "Waiting...",
                "extracting_frames": "🎞 Extracting frames...",
                "extracting_audio": "🔊 Extracting audio...",
                "converting_ascii": "⚙️ Converting to ASCII...",
                "creating_video": "💾 Creating final video...",
                "done": "✅ Done! Saved to:",
                "warning_high_res": "High resolutions may be slow. Continue?",
                "overwrite_audio": "already exists. Overwrite?",
                "yes": "Yes",
                "no": "No",
            },
            "Spanish": {
                "title": "Generador de Video ASCII",
                "resolution": "Resolución:",
                "fps": "FPS:",
                "ascii_style": "Estilo ASCII:",
                "fast_mode": "⚡ Carga rápida (menor calidad)",
                "cleanup": "🧹 Limpiar frames temporales tras exportar",
                "language": "Idioma:",
                "instructions": "📄 Instrucciones",
                "import_file": "🎬 Importar MP4 / GIF / Imagen",
                "instructions_text": "1. Elija resolución, FPS y estilo.\n2. Opcionalmente active el modo rápido.\n3. Importe un MP4, GIF o imagen para convertir.\n4. Su exportación ASCII se guardará.",
                "waiting": "Esperando...",
                "extracting_frames": "🎞 Extrayendo frames...",
                "extracting_audio": "🔊 Extrayendo audio...",
                "converting_ascii": "⚙️ Convirtiendo a ASCII...",
                "creating_video": "💾 Creando video final...",
                "done": "✅ ¡Hecho! Guardado en:",
                "warning_high_res": "Las altas resoluciones pueden ser lentas. ¿Continuar?",
                "overwrite_audio": "ya existe. ¿Sobrescribir?",
                "yes": "Sí",
                "no": "No",
            },
            "French": {
                "title": "Générateur de Vidéo ASCII",
                "resolution": "Résolution :",
                "fps": "FPS :",
                "ascii_style": "Style ASCII :",
                "fast_mode": "⚡ Chargement rapide (qualité inférieure)",
                "cleanup": "🧹 Nettoyer les frames temporaires après export",
                "language": "Langue :",
                "instructions": "📄 Instructions",
                "import_file": "🎬 Importer MP4 / GIF / Image",
                "instructions_text": "1. Choisissez la résolution, FPS, et style.\n2. Activez éventuellement le mode rapide.\n3. Importez un MP4, GIF ou image à convertir.\n4. Votre export ASCII sera sauvegardé.",
                "waiting": "En attente...",
                "extracting_frames": "🎞 Extraction des frames...",
                "extracting_audio": "🔊 Extraction de l'audio...",
                "converting_ascii": "⚙️ Conversion en ASCII...",
                "creating_video": "💾 Création de la vidéo finale...",
                "done": "✅ Terminé ! Enregistré dans :",
                "warning_high_res": "Les hautes résolutions peuvent être lentes. Continuer ?",
                "overwrite_audio": "existe déjà. Écraser ?",
                "yes": "Oui",
                "no": "Non",
            },
            "German": {
                "title": "ASCII Video Generator",
                "resolution": "Auflösung:",
                "fps": "FPS:",
                "ascii_style": "ASCII-Stil:",
                "fast_mode": "⚡ Schnelles Laden (geringere Qualität)",
                "cleanup": "🧹 Temporäre Frames nach dem Export löschen",
                "language": "Sprache:",
                "instructions": "📄 Anweisungen",
                "import_file": "🎬 MP4 / GIF / Bild importieren",
                "instructions_text": "1. Wählen Sie Auflösung, FPS und Stil.\n2. Optional den Schnellmodus aktivieren.\n3. Importieren Sie eine MP4, GIF oder ein Bild zum Konvertieren.\n4. Ihr ASCII-Export wird gespeichert.",
                "waiting": "Warten...",
                "extracting_frames": "🎞 Frames werden extrahiert...",
                "extracting_audio": "🔊 Audio wird extrahiert...",
                "converting_ascii": "⚙️ Konvertiere zu ASCII...",
                "creating_video": "💾 Erstelle das endgültige Video...",
                "done": "✅ Fertig! Gespeichert unter:",
                "warning_high_res": "Hohe Auflösungen können langsam sein. Fortfahren?",
                "overwrite_audio": "existiert bereits. Überschreiben?",
                "yes": "Ja",
                "no": "Nein",
            },
            "Italian": {
                "title": "Generatore di Video ASCII",
                "resolution": "Risoluzione:",
                "fps": "FPS:",
                "ascii_style": "Stile ASCII:",
                "fast_mode": "⚡ Caricamento veloce (qualità inferiore)",
                "cleanup": "🧹 Pulisci frame temporanei dopo l'esportazione",
                "language": "Lingua:",
                "instructions": "📄 Istruzioni",
                "import_file": "🎬 Importa MP4 / GIF / Immagine",
                "instructions_text": "1. Scegli risoluzione, FPS e stile.\n2. Opzionalmente abilita la modalità veloce.\n3. Importa un MP4, GIF o immagine da convertire.\n4. La tua esportazione ASCII sarà salvata.",
                "waiting": "In attesa...",
                "extracting_frames": "🎞 Estrazione dei frame...",
                "extracting_audio": "🔊 Estrazione audio...",
                "converting_ascii": "⚙️ Conversione in ASCII...",
                "creating_video": "💾 Creazione del video finale...",
                "done": "✅ Fatto! Salvato in:",
                "warning_high_res": "Le alte risoluzioni potrebbero essere lente. Continuare?",
                "overwrite_audio": "esiste già. Sovrascrivere?",
                "yes": "Sì",
                "no": "No",
            },
            "Chinese (Simplified)": {
                "title": "ASCII视频生成器",
                "resolution": "分辨率：",
                "fps": "帧率：",
                "ascii_style": "ASCII风格：",
                "fast_mode": "⚡ 快速加载（较低质量）",
                "cleanup": "🧹 导出后清理临时帧",
                "language": "语言：",
                "instructions": "📄 说明",
                "import_file": "🎬 导入MP4 / GIF / 图片",
                "instructions_text": "1. 选择分辨率、帧率和风格。\n2. 可选启用快速模式。\n3. 导入MP4、GIF或图片进行转换。\n4. ASCII导出文件将被保存。",
                "waiting": "等待中...",
                "extracting_frames": "🎞 正在提取帧...",
                "extracting_audio": "🔊 正在提取音频...",
                "converting_ascii": "⚙️ 转换为ASCII...",
                "creating_video": "💾 正在创建最终视频...",
                "done": "✅ 完成！保存至：",
                "warning_high_res": "高分辨率可能较慢。是否继续？",
                "overwrite_audio": "已存在。是否覆盖？",
                "yes": "是",
                "no": "否",
            },
            "Chinese (Traditional)": {
                "title": "ASCII影片產生器",
                "resolution": "解析度：",
                "fps": "FPS：",
                "ascii_style": "ASCII風格：",
                "fast_mode": "⚡ 快速載入（較低品質）",
                "cleanup": "🧹 匯出後清理暫存幀",
                "language": "語言：",
                "instructions": "📄 操作說明",
                "import_file": "🎬 匯入MP4 / GIF / 圖片",
                "instructions_text": "1. 選擇解析度、FPS和風格。\n2. 可選啟用快速模式。\n3. 匯入MP4、GIF或圖片進行轉換。\n4. ASCII匯出將會保存。",
                "waiting": "等待中...",
                "extracting_frames": "🎞 擷取影格中...",
                "extracting_audio": "🔊 擷取音訊中...",
                "converting_ascii": "⚙️ 轉換為ASCII...",
                "creating_video": "💾 建立最終影片中...",
                "done": "✅ 完成！保存於：",
                "warning_high_res": "高解析度可能較慢。是否繼續？",
                "overwrite_audio": "已存在。是否覆寫？",
                "yes": "是",
                "no": "否",
            },
            "Japanese": {
                "title": "ASCIIビデオジェネレーター",
                "resolution": "解像度：",
                "fps": "FPS：",
                "ascii_style": "ASCIIスタイル：",
                "fast_mode": "⚡ 高速読み込み（低品質）",
                "cleanup": "🧹 エクスポート後に一時フレームを削除",
                "language": "言語：",
                "instructions": "📄 使用説明",
                "import_file": "🎬 MP4 / GIF / 画像をインポート",
                "instructions_text": "1. 解像度、FPS、スタイルを選択します。\n2. オプションで高速モードを有効にします。\n3. 変換するMP4、GIF、または画像をインポートします。\n4. ASCIIエクスポートが保存されます。",
                "waiting": "待機中...",
                "extracting_frames": "🎞 フレームを抽出中...",
                "extracting_audio": "🔊 オーディオを抽出中...",
                "converting_ascii": "⚙️ ASCIIに変換中...",
                "creating_video": "💾 最終ビデオを作成中...",
                "done": "✅ 完了！保存先：",
                "warning_high_res": "高解像度は遅くなる場合があります。続行しますか？",
                "overwrite_audio": "すでに存在します。上書きしますか？",
                "yes": "はい",
                "no": "いいえ",
            },
            "Korean": {
                "title": "ASCII 비디오 생성기",
                "resolution": "해상도:",
                "fps": "FPS:",
                "ascii_style": "ASCII 스타일:",
                "fast_mode": "⚡ 빠른 로딩 (낮은 품질)",
                "cleanup": "🧹 내보낸 후 임시 프레임 정리",
                "language": "언어:",
                "instructions": "📄 사용 설명",
                "import_file": "🎬 MP4 / GIF / 이미지 가져오기",
                "instructions_text": "1. 해상도, FPS 및 스타일을 선택하세요.\n2. 빠른 모드를 선택할 수 있습니다.\n3. 변환할 MP4, GIF 또는 이미지를 가져오세요.\n4. ASCII 내보내기가 저장됩니다.",
                "waiting": "대기 중...",
                "extracting_frames": "🎞 프레임 추출 중...",
                "extracting_audio": "🔊 오디오 추출 중...",
                "converting_ascii": "⚙️ ASCII로 변환 중...",
                "creating_video": "💾 최종 비디오 생성 중...",
                "done": "✅ 완료! 저장 위치:",
                "warning_high_res": "고해상도는 느릴 수 있습니다. 계속하시겠습니까?",
                "overwrite_audio": "이미 존재합니다. 덮어쓰시겠습니까?",
                "yes": "예",
                "no": "아니오",
            },
            "Russian": {
                "title": "Генератор ASCII Видео",
                "resolution": "Разрешение:",
                "fps": "FPS:",
                "ascii_style": "Стиль ASCII:",
                "fast_mode": "⚡ Быстрая загрузка (низкое качество)",
                "cleanup": "🧹 Очистить временные кадры после экспорта",
                "language": "Язык:",
                "instructions": "📄 Инструкции",
                "import_file": "🎬 Импорт MP4 / GIF / изображения",
                "instructions_text": "1. Выберите разрешение, FPS и стиль.\n2. По желанию включите быстрый режим.\n3. Импортируйте MP4, GIF или изображение для конвертации.\n4. Ваш ASCII экспорт будет сохранён.",
                "waiting": "Ожидание...",
                "extracting_frames": "🎞 Извлечение кадров...",
                "extracting_audio": "🔊 Извлечение аудио...",
                "converting_ascii": "⚙️ Конвертация в ASCII...",
                "creating_video": "💾 Создание финального видео...",
                "done": "✅ Готово! Сохранено в:",
                "warning_high_res": "Высокое разрешение может работать медленно. Продолжить?",
                "overwrite_audio": "уже существует. Перезаписать?",
                "yes": "Да",
                "no": "Нет",
            },
            "Portuguese": {
                "title": "Gerador de Vídeo ASCII",
                "resolution": "Resolução:",
                "fps": "FPS:",
                "ascii_style": "Estilo ASCII:",
                "fast_mode": "⚡ Carregamento rápido (qualidade inferior)",
                "cleanup": "🧹 Limpar frames temporários após exportar",
                "language": "Idioma:",
                "instructions": "📄 Instruções",
                "import_file": "🎬 Importar MP4 / GIF / Imagem",
                "instructions_text": "1. Escolha resolução, FPS e estilo.\n2. Opcionalmente ative o modo rápido.\n3. Importe um MP4, GIF ou imagem para converter.\n4. Sua exportação ASCII será salva.",
                "waiting": "Aguardando...",
                "extracting_frames": "🎞 Extraindo frames...",
                "extracting_audio": "🔊 Extraindo áudio...",
                "converting_ascii": "⚙️ Convertendo para ASCII...",
                "creating_video": "💾 Criando vídeo final...",
                "done": "✅ Concluído! Salvo em:",
                "warning_high_res": "Altas resoluções podem ser lentas. Continuar?",
                "overwrite_audio": "já existe. Sobrescrever?",
                "yes": "Sim",
                "no": "Não",
            },
            "Arabic": {
                "title": "مولد فيديو ASCII",
                "resolution": "الدقة:",
                "fps": "معدل الإطارات:",
                "ascii_style": "أسلوب ASCII:",
                "fast_mode": "⚡ تحميل سريع (جودة أقل)",
                "cleanup": "🧹 تنظيف الإطارات المؤقتة بعد التصدير",
                "language": "اللغة:",
                "instructions": "📄 التعليمات",
                "import_file": "🎬 استيراد MP4 / GIF / صورة",
                "instructions_text": "1. اختر الدقة، FPS، والأسلوب.\n2. قم بتمكين الوضع السريع إذا أردت.\n3. استورد ملف MP4 أو GIF أو صورة للتحويل.\n4. سيتم حفظ التصدير ASCII الخاص بك.",
                "waiting": "جار الانتظار...",
                "extracting_frames": "🎞 استخراج الإطارات...",
                "extracting_audio": "🔊 استخراج الصوت...",
                "converting_ascii": "⚙️ التحويل إلى ASCII...",
                "creating_video": "💾 إنشاء الفيديو النهائي...",
                "done": "✅ تم! تم الحفظ في:",
                "warning_high_res": "الدقة العالية قد تكون بطيئة. هل تستمر؟",
                "overwrite_audio": "موجود مسبقاً. هل تستبدل؟",
                "yes": "نعم",
                "no": "لا",
            },
            "Hindi": {
                "title": "ASCII वीडियो जनरेटर",
                "resolution": "रिज़ॉल्यूशन:",
                "fps": "FPS:",
                "ascii_style": "ASCII स्टाइल:",
                "fast_mode": "⚡ तेज़ लोडिंग (कम गुणवत्ता)",
                "cleanup": "🧹 निर्यात के बाद अस्थायी फ़्रेम साफ़ करें",
                "language": "भाषा:",
                "instructions": "📄 निर्देश",
                "import_file": "🎬 MP4 / GIF / छवि आयात करें",
                "instructions_text": "1. रिज़ॉल्यूशन, FPS, और स्टाइल चुनें।\n2. वैकल्पिक रूप से तेज़ मोड सक्षम करें।\n3. कन्वर्ट करने के लिए MP4, GIF, या छवि आयात करें।\n4. आपका ASCII निर्यात सहेजा जाएगा।",
                "waiting": "प्रतीक्षा कर रहे हैं...",
                "extracting_frames": "🎞 फ़्रेम निकाल रहे हैं...",
                "extracting_audio": "🔊 ऑडियो निकाल रहे हैं...",
                "converting_ascii": "⚙️ ASCII में कन्वर्ट कर रहे हैं...",
                "creating_video": "💾 अंतिम वीडियो बना रहे हैं...",
                "done": "✅ पूरा! यहाँ सहेजा गया:",
                "warning_high_res": "उच्च रिज़ॉल्यूशन धीमा हो सकता है। जारी रखें?",
                "overwrite_audio": "पहले से मौजूद है। अधिलेखित करें?",
                "yes": "हाँ",
                "no": "नहीं",
            },
            "Bengali": {
                "title": "ASCII ভিডিও জেনারেটর",
                "resolution": "রেজোলিউশন:",
                "fps": "FPS:",
                "ascii_style": "ASCII স্টাইল:",
                "fast_mode": "⚡ দ্রুত লোডিং (কম মানের)",
                "cleanup": "🧹 রফতানির পর অস্থায়ী ফ্রেম পরিষ্কার করুন",
                "language": "ভাষা:",
                "instructions": "📄 নির্দেশাবলী",
                "import_file": "🎬 MP4 / GIF / ছবি আমদানি করুন",
                "instructions_text": "1. রেজোলিউশন, FPS এবং স্টাইল নির্বাচন করুন।\n2. অপশনাল দ্রুত মোড সক্রিয় করুন।\n3. রূপান্তরের জন্য MP4, GIF বা ছবি আমদানি করুন।\n4. আপনার ASCII রপ্তানি সংরক্ষিত হবে।",
                "waiting": "অপেক্ষা চলছে...",
                "extracting_frames": "🎞 ফ্রেম বের করা হচ্ছে...",
                "extracting_audio": "🔊 অডিও বের করা হচ্ছে...",
                "converting_ascii": "⚙️ ASCII তে রূপান্তরিত হচ্ছে...",
                "creating_video": "💾 চূড়ান্ত ভিডিও তৈরি হচ্ছে...",
                "done": "✅ সম্পন্ন! সংরক্ষিত:",
                "warning_high_res": "উচ্চ রেজোলিউশন ধীর হতে পারে। চালিয়ে যেতে চান?",
                "overwrite_audio": "আগেই আছে। ওভাররাইট করবেন?",
                "yes": "হ্যাঁ",
                "no": "না",
            },
            "Turkish": {
                "title": "ASCII Video Oluşturucu",
                "resolution": "Çözünürlük:",
                "fps": "FPS:",
                "ascii_style": "ASCII Stili:",
                "fast_mode": "⚡ Hızlı yükleme (daha düşük kalite)",
                "cleanup": "🧹 Dışa aktarma sonrası geçici kareleri temizle",
                "language": "Dil:",
                "instructions": "📄 Talimatlar",
                "import_file": "🎬 MP4 / GIF / Resim içe aktar",
                "instructions_text": "1. Çözünürlük, FPS ve stil seçin.\n2. İsteğe bağlı hızlı modu etkinleştirin.\n3. Dönüştürmek için MP4, GIF veya resim içe aktarın.\n4. ASCII dışa aktarımınız kaydedilecektir.",
                "waiting": "Bekleniyor...",
                "extracting_frames": "🎞 Kareler çıkarılıyor...",
                "extracting_audio": "🔊 Ses çıkarılıyor...",
                "converting_ascii": "⚙️ ASCII'ye dönüştürülüyor...",
                "creating_video": "💾 Son video oluşturuluyor...",
                "done": "✅ Tamamlandı! Kaydedildi:",
                "warning_high_res": "Yüksek çözünürlükler yavaş olabilir. Devam edilsin mi?",
                "overwrite_audio": "zaten var. Üzerine yazılsın mı?",
                "yes": "Evet",
                "no": "Hayır",
            },
            "Dutch": {
                "title": "ASCII Video Generator",
                "resolution": "Resolutie:",
                "fps": "FPS:",
                "ascii_style": "ASCII-stijl:",
                "fast_mode": "⚡ Snelle laadtijd (lagere kwaliteit)",
                "cleanup": "🧹 Tijdelijke frames opschonen na export",
                "language": "Taal:",
                "instructions": "📄 Instructies",
                "import_file": "🎬 MP4 / GIF / Afbeelding importeren",
                "instructions_text": "1. Kies resolutie, FPS en stijl.\n2. Schakel optioneel de snelle modus in.\n3. Importeer een MP4, GIF of afbeelding om te converteren.\n4. Je ASCII-export wordt opgeslagen.",
                "waiting": "Wachten...",
                "extracting_frames": "🎞 Frames aan het extraheren...",
                "extracting_audio": "🔊 Audio aan het extraheren...",
                "converting_ascii": "⚙️ Converteren naar ASCII...",
                "creating_video": "💾 Eindvideo aan het maken...",
                "done": "✅ Klaar! Opgeslagen in:",
                "warning_high_res": "Hoge resoluties kunnen traag zijn. Doorgaan?",
                "overwrite_audio": "bestaat al. Overschrijven?",
                "yes": "Ja",
                "no": "Nee",
            },
            "Polish": {
                "title": "Generator Wideo ASCII",
                "resolution": "Rozdzielczość:",
                "fps": "FPS:",
                "ascii_style": "Styl ASCII:",
                "fast_mode": "⚡ Szybkie ładowanie (niższa jakość)",
                "cleanup": "🧹 Czyszczenie tymczasowych klatek po eksporcie",
                "language": "Język:",
                "instructions": "📄 Instrukcje",
                "import_file": "🎬 Importuj MP4 / GIF / Obraz",
                "instructions_text": "1. Wybierz rozdzielczość, FPS i styl.\n2. Opcjonalnie włącz szybki tryb.\n3. Zaimportuj MP4, GIF lub obraz do konwersji.\n4. Twój eksport ASCII zostanie zapisany.",
                "waiting": "Oczekiwanie...",
                "extracting_frames": "🎞 Ekstrakcja klatek...",
                "extracting_audio": "🔊 Ekstrakcja audio...",
                "converting_ascii": "⚙️ Konwersja do ASCII...",
                "creating_video": "💾 Tworzenie końcowego wideo...",
                "done": "✅ Gotowe! Zapisano w:",
                "warning_high_res": "Wysokie rozdzielczości mogą być wolne. Kontynuować?",
                "overwrite_audio": "już istnieje. Nadpisać?",
                "yes": "Tak",
                "no": "Nie",
            },
            "Swedish": {
                "title": "ASCII Videogenerator",
                "resolution": "Upplösning:",
                "fps": "FPS:",
                "ascii_style": "ASCII-stil:",
                "fast_mode": "⚡ Snabb laddning (lägre kvalitet)",
                "cleanup": "🧹 Rensa temporära ramar efter export",
                "language": "Språk:",
                "instructions": "📄 Instruktioner",
                "import_file": "🎬 Importera MP4 / GIF / Bild",
                "instructions_text": "1. Välj upplösning, FPS och stil.\n2. Aktivera eventuellt snabb läge.\n3. Importera en MP4, GIF eller bild för konvertering.\n4. Din ASCII-export sparas.",
                "waiting": "Väntar...",
                "extracting_frames": "🎞 Extraherar ramar...",
                "extracting_audio": "🔊 Extraherar ljud...",
                "converting_ascii": "⚙️ Konverterar till ASCII...",
                "creating_video": "💾 Skapar slutgiltig video...",
                "done": "✅ Klart! Sparat i:",
                "warning_high_res": "Höga upplösningar kan vara långsamma. Fortsätta?",
                "overwrite_audio": "finns redan. Skriv över?",
                "yes": "Ja",
                "no": "Nej",
            },
            "Greek": {
                "title": "Γεννήτρια ASCII Βίντεο",
                "resolution": "Ανάλυση:",
                "fps": "FPS:",
                "ascii_style": "Στυλ ASCII:",
                "fast_mode": "⚡ Γρήγορη φόρτωση (χαμηλότερη ποιότητα)",
                "cleanup": "🧹 Καθαρισμός προσωρινών καρέ μετά την εξαγωγή",
                "language": "Γλώσσα:",
                "instructions": "📄 Οδηγίες",
                "import_file": "🎬 Εισαγωγή MP4 / GIF / Εικόνας",
                "instructions_text": "1. Επιλέξτε ανάλυση, FPS και στυλ.\n2. Προαιρετικά ενεργοποιήστε τη γρήγορη λειτουργία.\n3. Εισάγετε ένα MP4, GIF ή εικόνα για μετατροπή.\n4. Η εξαγωγή ASCII θα αποθηκευτεί.",
                "waiting": "Αναμονή...",
                "extracting_frames": "🎞 Εξαγωγή καρέ...",
                "extracting_audio": "🔊 Εξαγωγή ήχου...",
                "converting_ascii": "⚙️ Μετατροπή σε ASCII...",
                "creating_video": "💾 Δημιουργία τελικού βίντεο...",
                "done": "✅ Ολοκληρώθηκε! Αποθηκεύτηκε σε:",
                "warning_high_res": "Οι υψηλές αναλύσεις μπορεί να είναι αργές. Να συνεχίσω;",
                "overwrite_audio": "υπάρχει ήδη. Να αντικατασταθεί;",
                "yes": "Ναι",
                "no": "Όχι",
            },
            "Czech": {
                "title": "Generátor ASCII videa",
                "resolution": "Rozlišení:",
                "fps": "FPS:",
                "ascii_style": "Styl ASCII:",
                "fast_mode": "⚡ Rychlé načítání (nižší kvalita)",
                "cleanup": "🧹 Vyčistit dočasné snímky po exportu",
                "language": "Jazyk:",
                "instructions": "📄 Instrukce",
                "import_file": "🎬 Import MP4 / GIF / obrázku",
                "instructions_text": "1. Vyberte rozlišení, FPS a styl.\n2. Volitelně zapněte rychlý režim.\n3. Importujte MP4, GIF nebo obrázek k převodu.\n4. Váš ASCII export bude uložen.",
                "waiting": "Čekání...",
                "extracting_frames": "🎞 Extrahují se snímky...",
                "extracting_audio": "🔊 Extrahuje se zvuk...",
                "converting_ascii": "⚙️ Převod do ASCII...",
                "creating_video": "💾 Vytváří se konečné video...",
                "done": "✅ Hotovo! Uloženo do:",
                "warning_high_res": "Vysoká rozlišení mohou být pomalá. Pokračovat?",
                "overwrite_audio": "už existuje. Přepsat?",
                "yes": "Ano",
                "no": "Ne",
            },
            "Hungarian": {
                "title": "ASCII Videó Generátor",
                "resolution": "Felbontás:",
                "fps": "FPS:",
                "ascii_style": "ASCII Stílus:",
                "fast_mode": "⚡ Gyors betöltés (alacsonyabb minőség)",
                "cleanup": "🧹 Ideiglenes képkockák törlése export után",
                "language": "Nyelv:",
                "instructions": "📄 Útmutató",
                "import_file": "🎬 MP4 / GIF / Kép importálása",
                "instructions_text": "1. Válassza ki a felbontást, FPS-t és a stílust.\n2. Opcionálisan engedélyezze a gyors módot.\n3. Importáljon MP4-et, GIF-et vagy képet konvertáláshoz.\n4. Az ASCII export mentve lesz.",
                "waiting": "Várakozás...",
                "extracting_frames": "🎞 Képkockák kinyerése...",
                "extracting_audio": "🔊 Hang kinyerése...",
                "converting_ascii": "⚙️ Átalakítás ASCII-re...",
                "creating_video": "💾 Végső videó létrehozása...",
                "done": "✅ Kész! Mentve ide:",
                "warning_high_res": "A magas felbontás lassú lehet. Folytatja?",
                "overwrite_audio": "már létezik. Felülírja?",
                "yes": "Igen",
                "no": "Nem",
            },
            "Finnish": {
                "title": "ASCII Video Generaattori",
                "resolution": "Resoluutio:",
                "fps": "FPS:",
                "ascii_style": "ASCII-tyyli:",
                "fast_mode": "⚡ Nopeampi lataus (alhaisempi laatu)",
                "cleanup": "🧹 Poista väliaikaiset kehykset vientiin jälkeen",
                "language": "Kieli:",
                "instructions": "📄 Ohjeet",
                "import_file": "🎬 Tuo MP4 / GIF / Kuva",
                "instructions_text": "1. Valitse resoluutio, FPS ja tyyli.\n2. Ota valinnainen nopea tila käyttöön.\n3. Tuo MP4, GIF tai kuva muunnosta varten.\n4. ASCII-vientisi tallennetaan.",
                "waiting": "Odottamassa...",
                "extracting_frames": "🎞 Kehysten poisto...",
                "extracting_audio": "🔊 Äänen poisto...",
                "converting_ascii": "⚙️ Muunnos ASCII:ksi...",
                "creating_video": "💾 Lopullisen videon luonti...",
                "done": "✅ Valmis! Tallennettu:",
                "warning_high_res": "Korkeat resoluutiot voivat olla hitaita. Jatketaanko?",
                "overwrite_audio": "on jo olemassa. Ylikirjoitetaanko?",
                "yes": "Kyllä",
                "no": "Ei",
            },
            "Norwegian": {
                "title": "ASCII Videogenerator",
                "resolution": "Oppløsning:",
                "fps": "FPS:",
                "ascii_style": "ASCII-stil:",
                "fast_mode": "⚡ Rask lasting (lavere kvalitet)",
                "cleanup": "🧹 Rydd opp midlertidige bilder etter eksport",
                "language": "Språk:",
                "instructions": "📄 Instruksjoner",
                "import_file": "🎬 Importer MP4 / GIF / Bilde",
                "instructions_text": "1. Velg oppløsning, FPS og stil.\n2. Aktiver hurtigmodus om ønskelig.\n3. Importer MP4, GIF eller bilde for konvertering.\n4. Din ASCII-eksport lagres.",
                "waiting": "Venter...",
                "extracting_frames": "🎞 Henter bilder...",
                "extracting_audio": "🔊 Henter lyd...",
                "converting_ascii": "⚙️ Konverterer til ASCII...",
                "creating_video": "💾 Lager ferdig video...",
                "done": "✅ Ferdig! Lagret til:",
                "warning_high_res": "Høye oppløsninger kan være tregt. Fortsette?",
                "overwrite_audio": "finnes allerede. Overskrive?",
                "yes": "Ja",
                "no": "Nei",
            },

            "Danish": {
                "title": "ASCII Video Generator",
                "resolution": "Opløsning:",
                "fps": "FPS:",
                "ascii_style": "ASCII Stil:",
                "fast_mode": "⚡ Hurtig indlæsning (lavere kvalitet)",
                "cleanup": "🧹 Ryd op i midlertidige frames efter eksport",
                "language": "Sprog:",
                "instructions": "📄 Instruktioner",
                "import_file": "🎬 Importer MP4 / GIF / Billede",
                "instructions_text": "1. Vælg opløsning, FPS og stil.\n2. Aktivér eventuelt hurtig tilstand.\n3. Importér MP4, GIF eller billede til konvertering.\n4. Din ASCII eksport gemmes.",
                "waiting": "Venter...",
                "extracting_frames": "🎞 Udtrækker frames...",
                "extracting_audio": "🔊 Udtrækker lyd...",
                "converting_ascii": "⚙️ Konverterer til ASCII...",
                "creating_video": "💾 Opretter slutvideo...",
                "done": "✅ Færdig! Gemt til:",
                "warning_high_res": "Høje opløsninger kan være langsomme. Fortsæt?",
                "overwrite_audio": "eksisterer allerede. Overskriv?",
                "yes": "Ja",
                "no": "Nej",
            },

            "Romanian": {
                "title": "Generator Video ASCII",
                "resolution": "Rezoluție:",
                "fps": "FPS:",
                "ascii_style": "Stil ASCII:",
                "fast_mode": "⚡ Încărcare rapidă (calitate mai mică)",
                "cleanup": "🧹 Curăță cadre temporare după export",
                "language": "Limba:",
                "instructions": "📄 Instrucțiuni",
                "import_file": "🎬 Importă MP4 / GIF / Imagine",
                "instructions_text": "1. Alege rezoluția, FPS-ul și stilul.\n2. Opțional activează modul rapid.\n3. Importă un MP4, GIF sau imagine pentru conversie.\n4. Exportul tău ASCII va fi salvat.",
                "waiting": "Așteptare...",
                "extracting_frames": "🎞 Extrage cadre...",
                "extracting_audio": "🔊 Extrage audio...",
                "converting_ascii": "⚙️ Conversie în ASCII...",
                "creating_video": "💾 Creează video final...",
                "done": "✅ Gata! Salvat în:",
                "warning_high_res": "Rezoluțiile mari pot fi lente. Continuă?",
                "overwrite_audio": "există deja. Rescrie?",
                "yes": "Da",
                "no": "Nu",
            },

            "Thai": {
                "title": "โปรแกรมสร้างวิดีโอ ASCII",
                "resolution": "ความละเอียด:",
                "fps": "FPS:",
                "ascii_style": "สไตล์ ASCII:",
                "fast_mode": "⚡ โหลดเร็ว (คุณภาพต่ำกว่า)",
                "cleanup": "🧹 ลบภาพชั่วคราวหลังส่งออก",
                "language": "ภาษา:",
                "instructions": "📄 คำแนะนำ",
                "import_file": "🎬 นำเข้า MP4 / GIF / รูปภาพ",
                "instructions_text": "1. เลือกความละเอียด, FPS และสไตล์\n2. เปิดโหมดเร็วถ้าต้องการ\n3. นำเข้า MP4, GIF หรือรูปภาพเพื่อแปลง\n4. ไฟล์ ASCII ที่ส่งออกจะถูกบันทึก",
                "waiting": "รอ...",
                "extracting_frames": "🎞 กำลังดึงภาพจากวิดีโอ...",
                "extracting_audio": "🔊 กำลังดึงเสียง...",
                "converting_ascii": "⚙️ กำลังแปลงเป็น ASCII...",
                "creating_video": "💾 กำลังสร้างวิดีโอสุดท้าย...",
                "done": "✅ เสร็จสิ้น! บันทึกที่:",
                "warning_high_res": "ความละเอียดสูงอาจทำให้ช้า ดำเนินการต่อหรือไม่?",
                "overwrite_audio": "มีอยู่แล้ว ต้องการเขียนทับหรือไม่?",
                "yes": "ใช่",
                "no": "ไม่",
            },

            "Indonesian": {
                "title": "Generator Video ASCII",
                "resolution": "Resolusi:",
                "fps": "FPS:",
                "ascii_style": "Gaya ASCII:",
                "fast_mode": "⚡ Pemuatan cepat (kualitas lebih rendah)",
                "cleanup": "🧹 Bersihkan frame sementara setelah ekspor",
                "language": "Bahasa:",
                "instructions": "📄 Instruksi",
                "import_file": "🎬 Impor MP4 / GIF / Gambar",
                "instructions_text": "1. Pilih resolusi, FPS, dan gaya.\n2. Opsional aktifkan mode cepat.\n3. Impor MP4, GIF, atau gambar untuk konversi.\n4. Ekspor ASCII Anda akan disimpan.",
                "waiting": "Menunggu...",
                "extracting_frames": "🎞 Mengekstrak frame...",
                "extracting_audio": "🔊 Mengekstrak audio...",
                "converting_ascii": "⚙️ Mengonversi ke ASCII...",
                "creating_video": "💾 Membuat video akhir...",
                "done": "✅ Selesai! Disimpan di:",
                "warning_high_res": "Resolusi tinggi mungkin lambat. Lanjutkan?",
                "overwrite_audio": "sudah ada. Timpa?",
                "yes": "Ya",
                "no": "Tidak",
            },

            "Malay": {
                "title": "Penjana Video ASCII",
                "resolution": "Resolusi:",
                "fps": "FPS:",
                "ascii_style": "Gaya ASCII:",
                "fast_mode": "⚡ Muat naik pantas (kualiti lebih rendah)",
                "cleanup": "🧹 Bersihkan bingkai sementara selepas eksport",
                "language": "Bahasa:",
                "instructions": "📄 Arahan",
                "import_file": "🎬 Import MP4 / GIF / Imej",
                "instructions_text": "1. Pilih resolusi, FPS dan gaya.\n2. Aktifkan mod pantas jika mahu.\n3. Import MP4, GIF atau imej untuk penukaran.\n4. Eksport ASCII anda akan disimpan.",
                "waiting": "Menunggu...",
                "extracting_frames": "🎞 Mengekstrak bingkai...",
                "extracting_audio": "🔊 Mengekstrak audio...",
                "converting_ascii": "⚙️ Menukar ke ASCII...",
                "creating_video": "💾 Membuat video akhir...",
                "done": "✅ Selesai! Disimpan di:",
                "warning_high_res": "Resolusi tinggi mungkin perlahan. Teruskan?",
                "overwrite_audio": "sudah wujud. Ganti?",
                "yes": "Ya",
                "no": "Tidak",
            },

            "Ukrainian": {
                "title": "Генератор ASCII Відео",
                "resolution": "Роздільна здатність:",
                "fps": "FPS:",
                "ascii_style": "Стиль ASCII:",
                "fast_mode": "⚡ Швидке завантаження (нижча якість)",
                "cleanup": "🧹 Очищення тимчасових кадрів після експорту",
                "language": "Мова:",
                "instructions": "📄 Інструкції",
                "import_file": "🎬 Імпорт MP4 / GIF / Зображення",
                "instructions_text": "1. Виберіть роздільну здатність, FPS та стиль.\n2. За бажанням увімкніть швидкий режим.\n3. Імпортуйте MP4, GIF або зображення для конвертації.\n4. Ваш ASCII експорт буде збережено.",
                "waiting": "Очікування...",
                "extracting_frames": "🎞 Витяг кадрів...",
                "extracting_audio": "🔊 Витяг аудіо...",
                "converting_ascii": "⚙️ Конвертація в ASCII...",
                "creating_video": "💾 Створення фінального відео...",
                "done": "✅ Готово! Збережено в:",
                "warning_high_res": "Високі роздільні здатності можуть бути повільними. Продовжити?",
                "overwrite_audio": "вже існує. Перезаписати?",
                "yes": "Так",
                "no": "Ні",
            },

            "Catalan": {
                "title": "Generador de Vídeo ASCII",
                "resolution": "Resolució:",
                "fps": "FPS:",
                "ascii_style": "Estil ASCII:",
                "fast_mode": "⚡ Càrrega ràpida (qualitat inferior)",
                "cleanup": "🧹 Neteja fotogrames temporals després d'exportar",
                "language": "Idioma:",
                "instructions": "📄 Instruccions",
                "import_file": "🎬 Importa MP4 / GIF / Imatge",
                "instructions_text": "1. Trieu resolució, FPS i estil.\n2. Opcionalment activeu el mode ràpid.\n3. Importeu un MP4, GIF o imatge per convertir.\n4. La vostra exportació ASCII es desarà.",
                "waiting": "Esperant...",
                "extracting_frames": "🎞 Extraient fotogrames...",
                "extracting_audio": "🔊 Extraient àudio...",
                "converting_ascii": "⚙️ Convertint a ASCII...",
                "creating_video": "💾 Creant vídeo final...",
                "done": "✅ Fet! Desat a:",
                "warning_high_res": "Les altes resolucions poden ser lentes. Continuar?",
                "overwrite_audio": "ja existeix. Sobrescriure?",
                "yes": "Sí",
                "no": "No",
            },

            "Slovak": {
                "title": "Generátor ASCII videa",
                "resolution": "Rozlíšenie:",
                "fps": "FPS:",
                "ascii_style": "ASCII štýl:",
                "fast_mode": "⚡ Rýchle načítanie (nižšia kvalita)",
                "cleanup": "🧹 Vyčistiť dočasné snímky po exporte",
                "language": "Jazyk:",
                "instructions": "📄 Inštrukcie",
                "import_file": "🎬 Importovať MP4 / GIF / Obrázok",
                "instructions_text": "1. Vyberte rozlíšenie, FPS a štýl.\n2. Voliteľne zapnite rýchly režim.\n3. Importujte MP4, GIF alebo obrázok na konverziu.\n4. ASCII export bude uložený.",
                "waiting": "Čaká sa...",
                "extracting_frames": "🎞 Extrahovanie snímok...",
                "extracting_audio": "🔊 Extrahovanie zvuku...",
                "converting_ascii": "⚙️ Konvertovanie na ASCII...",
                "creating_video": "💾 Vytváranie finálneho videa...",
                "done": "✅ Hotovo! Uložené v:",
                "warning_high_res": "Vysoké rozlíšenia môžu byť pomalé. Pokračovať?",
                "overwrite_audio": "už existuje. Prepísať?",
                "yes": "Áno",
                "no": "Nie",
            },

            "Croatian": {
                "title": "ASCII Generator Videа",
                "resolution": "Rezolucija:",
                "fps": "FPS:",
                "ascii_style": "ASCII stil:",
                "fast_mode": "⚡ Brzo učitavanje (niža kvaliteta)",
                "cleanup": "🧹 Očisti privremene okvire nakon izvoza",
                "language": "Jezik:",
                "instructions": "📄 Upute",
                "import_file": "🎬 Uvezi MP4 / GIF / Slika",
                "instructions_text": "1. Odaberite rezoluciju, FPS i stil.\n2. Opcionalno omogućite brz način.\n3. Uvezite MP4, GIF ili sliku za konverziju.\n4. Vaš ASCII izvoz bit će spremljen.",
                "waiting": "Čeka se...",
                "extracting_frames": "🎞 Izvlačenje okvira...",
                "extracting_audio": "🔊 Izvlačenje zvuka...",
                "converting_ascii": "⚙️ Pretvaranje u ASCII...",
                "creating_video": "💾 Kreiranje konačnog videa...",
                "done": "✅ Gotovo! Spremljeno na:",
                "warning_high_res": "Visoke rezolucije mogu biti spore. Nastaviti?",
                "overwrite_audio": "već postoji. Prepiši?",
                "yes": "Da",
                "no": "Ne",
            },

            "Serbian": {
                "title": "ASCII Генератор Видео",
                "resolution": "Резолуција:",
                "fps": "FPS:",
                "ascii_style": "ASCII стил:",
                "fast_mode": "⚡ Брзо учитавање (нижи квалитет)",
                "cleanup": "🧹 Чишћење привремених кадрова након извоза",
                "language": "Језик:",
                "instructions": "📄 Упутства",
                "import_file": "🎬 Увези MP4 / GIF / Слику",
                "instructions_text": "1. Изаберите резолуцију, FPS и стил.\n2. По потреби омогућите брзи режим.\n3. Увезите MP4, GIF или слику за конверзију.\n4. Ваш ASCII извоз ће бити сачуван.",
                "waiting": "Чекање...",
                "extracting_frames": "🎞 Извлачење кадрова...",
                "extracting_audio": "🔊 Извлачење звука...",
                "converting_ascii": "⚙️ Конвертовање у ASCII...",
                "creating_video": "💾 Креирање финалног видеа...",
                "done": "✅ Готово! Сачувано у:",
                "warning_high_res": "Високе резолуције могу бити споре. Наставити?",
                "overwrite_audio": "већ постоји. Преписати?",
                "yes": "Да",
                "no": "Не",
            },

            "Bulgarian": {
                "title": "Генератор на ASCII видео",
                "resolution": "Резолюция:",
                "fps": "FPS:",
                "ascii_style": "ASCII стил:",
                "fast_mode": "⚡ Бързо зареждане (по-ниско качество)",
                "cleanup": "🧹 Почистване на временни кадри след експортиране",
                "language": "Език:",
                "instructions": "📄 Инструкции",
                "import_file": "🎬 Импортиране на MP4 / GIF / Изображение",
                "instructions_text": "1. Изберете резолюция, FPS и стил.\n2. По желание активирайте бърз режим.\n3. Импортирайте MP4, GIF или изображение за конвертиране.\n4. Вашият ASCII експорт ще бъде запазен.",
                "waiting": "Изчакване...",
                "extracting_frames": "🎞 Извличане на кадри...",
                "extracting_audio": "🔊 Извличане на аудио...",
                "converting_ascii": "⚙️ Конвертиране в ASCII...",
                "creating_video": "💾 Създаване на финалното видео...",
                "done": "✅ Готово! Запазено в:",
                "warning_high_res": "Високите резолюции може да са бавни. Продължавате ли?",
                "overwrite_audio": "вече съществува. Презапис?",
                "yes": "Да",
                "no": "Не",
            },

            "Lithuanian": {
                "title": "ASCII Vaizdo Generatorius",
                "resolution": "Rezoliucija:",
                "fps": "FPS:",
                "ascii_style": "ASCII Stilius:",
                "fast_mode": "⚡ Greitas įkėlimas (žemesnė kokybė)",
                "cleanup": "🧹 Išvalyti laikinas kadrus po eksporto",
                "language": "Kalba:",
                "instructions": "📄 Instrukcijos",
                "import_file": "🎬 Importuoti MP4 / GIF / Vaizdą",
                "instructions_text": "1. Pasirinkite rezoliuciją, FPS ir stilių.\n2. Pasirinktinai įjunkite greitą režimą.\n3. Importuokite MP4, GIF ar vaizdą konvertavimui.\n4. Jūsų ASCII eksportas bus išsaugotas.",
                "waiting": "Laukiama...",
                "extracting_frames": "🎞 Išgaunama kadrų...",
                "extracting_audio": "🔊 Išgaunama garso...",
                "converting_ascii": "⚙️ Konvertuojama į ASCII...",
                "creating_video": "💾 Kuriamas galutinis video...",
                "done": "✅ Baigta! Išsaugota:",
                "warning_high_res": "Didelės rezoliucijos gali sulėtinti. Tęsti?",
                "overwrite_audio": "jau egzistuoja. Perrašyti?",
                "yes": "Taip",
                "no": "Ne",
            },

            "Latvian": {
                "title": "ASCII Video Ģenerators",
                "resolution": "Izšķirtspēja:",
                "fps": "FPS:",
                "ascii_style": "ASCII Stils:",
                "fast_mode": "⚡ Ātra ielāde (zemāka kvalitāte)",
                "cleanup": "🧹 Tīrīt pagaidu kadrus pēc eksporta",
                "language": "Valoda:",
                "instructions": "📄 Norādījumi",
                "import_file": "🎬 Importēt MP4 / GIF / Attēlu",
                "instructions_text": "1. Izvēlies izšķirtspēju, FPS un stilu.\n2. Pēc izvēles ieslēdz ātro režīmu.\n3. Importē MP4, GIF vai attēlu konvertēšanai.\n4. Tavs ASCII eksports tiks saglabāts.",
                "waiting": "Gaidīšana...",
                "extracting_frames": "🎞 Izvelk kadrus...",
                "extracting_audio": "🔊 Izvelk audio...",
                "converting_ascii": "⚙️ Konvertē uz ASCII...",
                "creating_video": "💾 Veido galīgo video...",
                "done": "✅ Gatavs! Saglabāts:",
                "warning_high_res": "Augstas izšķirtspējas var būt lēnas. Turpināt?",
                "overwrite_audio": "jau eksistē. Pārrakstīt?",
                "yes": "Jā",
                "no": "Nē",
            },

            "Slovenian": {
                "title": "ASCII Video Generator",
                "resolution": "Ločljivost:",
                "fps": "FPS:",
                "ascii_style": "ASCII Slog:",
                "fast_mode": "⚡ Hitra nalaganja (nižja kakovost)",
                "cleanup": "🧹 Po izvozu počisti začasne slike",
                "language": "Jezik:",
                "instructions": "📄 Navodila",
                "import_file": "🎬 Uvozi MP4 / GIF / Sliko",
                "instructions_text": "1. Izberi ločljivost, FPS in slog.\n2. Po želji omogoči hitri način.\n3. Uvozi MP4, GIF ali sliko za pretvorbo.\n4. ASCII izvoz bo shranjen.",
                "waiting": "Čakam...",
                "extracting_frames": "🎞 Pridobivanje slik...",
                "extracting_audio": "🔊 Pridobivanje zvoka...",
                "converting_ascii": "⚙️ Pretvarjanje v ASCII...",
                "creating_video": "💾 Ustvarjanje končnega videa...",
                "done": "✅ Končano! Shranjeno v:",
                "warning_high_res": "Visoke ločljivosti so lahko počasne. Nadaljujem?",
                "overwrite_audio": "že obstaja. Prepišem?",
                "yes": "Da",
                "no": "Ne",
            },

            "Estonian": {
                "title": "ASCII Video Generaator",
                "resolution": "Resolutsioon:",
                "fps": "FPS:",
                "ascii_style": "ASCII Stiil:",
                "fast_mode": "⚡ Kiire laadimine (madalam kvaliteet)",
                "cleanup": "🧹 Puhasta ajutised kaadrid pärast eksporti",
                "language": "Keel:",
                "instructions": "📄 Juhised",
                "import_file": "🎬 Impordi MP4 / GIF / Pilt",
                "instructions_text": "1. Vali resolutsioon, FPS ja stiil.\n2. Soovi korral aktiveeri kiire režiim.\n3. Impordi MP4, GIF või pilt teisendamiseks.\n4. Sinu ASCII eksport salvestatakse.",
                "waiting": "Ootan...",
                "extracting_frames": "🎞 Kaadrite eraldamine...",
                "extracting_audio": "🔊 Helifaili eraldamine...",
                "converting_ascii": "⚙️ ASCII-ks teisendamine...",
                "creating_video": "💾 Lõpliku video loomine...",
                "done": "✅ Valmis! Salvestatud siia:",
                "warning_high_res": "Kõrge resolutsioon võib olla aeglane. Jätkata?",
                "overwrite_audio": "eksisteerib juba. Kas kirjutada üle?",
                "yes": "Jah",
                "no": "Ei",
            },
        }

        for lang in self.LANGUAGES:
            if lang not in self.translations:
                self.translations[lang] = self.translations["English"]

        self.widgets = {}

        self.setup_styles()
        self.setup_ui()
        self.apply_language()

        self.lang_var.trace_add("write", lambda *args: self.apply_language())

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar",
                        troughcolor="#1a1a1a",
                        bordercolor="#1a1a1a",
                        background="#ffffff",
                        lightcolor="#ffffff",
                        darkcolor="#aaaaaa")
        style.configure("TButton",
                        background="#222222",
                        foreground="#ffffff",
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor="none")

    def neon_label(self, text, name=None):
        label = tk.Label(self.root, text=text, fg="#ffffff", bg="#0d0d0d", font=("Consolas", 10, "bold"))
        if name:
            self.widgets[name] = label
        return label

    def neon_optionmenu(self, variable, choices, name=None):
        menu = ttk.OptionMenu(self.root, variable, variable.get(), *choices)
        menu.config(style="TButton")
        if name:
            self.widgets[name] = menu
        return menu

    def neon_spinbox(self, variable, from_, to, name=None):
        spinbox = tk.Spinbox(self.root, from_=from_, to=to, textvariable=variable,
                             fg="#ffffff", bg="#1a1a1a", insertbackground="#ffffff",
                             highlightthickness=0, font=("Consolas", 10), width=6)
        if name:
            self.widgets[name] = spinbox
        return spinbox

    def neon_button(self, text, command, name=None):
        btn = tk.Button(self.root, text=text, command=command,
                        fg="#ffffff", bg="#1a1a1a", activebackground="#ffffff", activeforeground="#0d0d0d",
                        relief="flat", font=("Consolas", 11, "bold"), padx=10, pady=5)
        if name:
            self.widgets[name] = btn
        return btn

    def update_preview(self, *args):
        ascii_chars = self.ASCII_SETS.get(self.ascii_set_var.get(), "@%#*+=-:. ").strip()
        if len(ascii_chars) < 2:
            ascii_chars += ascii_chars

        size = 20
        ascii_art = ""
        center = (size - 1) / 2

        for y in range(size):
            line = ""
            for x in range(size):
                dist_x = abs(x - center)
                dist_y = abs(y - center)
                gradient_value = 1 - ((dist_x + dist_y) / (2 * center))
                index = int(gradient_value * (len(ascii_chars) - 1))
                line += ascii_chars[index]
            ascii_art += line.center(60) + "\n"

        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, ascii_art)
        self.preview_text.config(state="disabled")

    def setup_ui(self):
        self.neon_label("", "lbl_resolution").pack(pady=(10, 0))
        self.neon_optionmenu(self.res_var, ["144p", "360p", "480p", "720p", "1080p", "1440p", "2K", "4K"],
                             "opt_resolution").pack(pady=2)

        self.neon_label("", "lbl_fps").pack(pady=(10, 0))
        self.neon_spinbox(self.fps_var, 10, 144, "spin_fps").pack(pady=2)

        self.neon_label("", "lbl_ascii_style").pack(pady=(10, 0))
        self.neon_optionmenu(self.ascii_set_var, list(self.ASCII_SETS.keys()), "opt_ascii_style").pack(pady=2)

        self.preview_text = tk.Text(self.root, height=10, width=40, bg="#0d0d0d", fg="#ffffff",
                                    font=("Consolas", 10, "bold"), bd=0, relief="flat")
        self.preview_text.pack(pady=(5, 10))
        self.preview_text.insert(tk.END, "(Preview will appear here)")
        self.preview_text.config(state="disabled")

        self.fast_mode_chk = tk.Checkbutton(self.root, text="", variable=self.fast_mode_var,
                                            bg="#0d0d0d", fg="#ffffff", selectcolor="#1a1a1a",
                                            activebackground="#0d0d0d", activeforeground="#ffffff")
        self.fast_mode_chk.pack(pady=(5, 0))

        self.cleanup_chk = tk.Checkbutton(self.root, text="", variable=self.cleanup_var,
                                          bg="#0d0d0d", fg="#ffffff", selectcolor="#1a1a1a",
                                          activebackground="#0d0d0d", activeforeground="#ffffff")
        self.cleanup_chk.pack(pady=(0, 10))

        self.neon_label("", "lbl_language").pack(pady=(5, 0))
        self.neon_optionmenu(self.lang_var, self.LANGUAGES, "opt_language").pack(pady=2)

        self.neon_button("", self.show_instructions, "btn_instructions").pack(pady=(0, 5))
        self.neon_button("", self.import_file, "btn_import").pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.root, maximum=100, variable=self.progress_var, length=300)
        self.progress_bar.pack(pady=5)

        self.status_lbl = tk.Label(self.root, textvariable=self.status_var, fg="#ffffff", bg="#0d0d0d",
                                   font=("Consolas", 10, "bold"))
        self.status_lbl.pack(pady=(5, 10))

        self.ascii_set_var.trace_add("write", self.update_preview)
        self.update_preview()

    def apply_language(self):
        lang = self.lang_var.get()
        t = self.translations.get(lang, self.translations["English"])

        self.root.title(t["title"])

        self.widgets["lbl_resolution"].config(text=t["resolution"])
        self.widgets["lbl_fps"].config(text=t["fps"])
        self.widgets["lbl_ascii_style"].config(text=t["ascii_style"])

        self.fast_mode_chk.config(text=t["fast_mode"])
        self.cleanup_chk.config(text=t["cleanup"])

        self.widgets["lbl_language"].config(text=t["language"])

        self.widgets["btn_instructions"].config(text=t["instructions"])
        self.widgets["btn_import"].config(text=t["import_file"])

        self.status_var.set(t["waiting"])

    def show_instructions(self):
        lang = self.lang_var.get()
        t = self.translations.get(lang, self.translations["English"])
        messagebox.showinfo(t["instructions"], t["instructions_text"])

    def import_file(self):
        lang = self.lang_var.get()
        t = self.translations.get(lang, self.translations["English"])

        file_path = filedialog.askopenfilename(filetypes=[
            ("Supported Files", "*.mp4 *.gif *.png *.jpg *.jpeg")
        ])
        if not file_path:
            return

        if self.res_var.get() in ["1440p", "2K", "4K"]:
            if not messagebox.askyesno(t["title"], t["warning_high_res"]):
                return

        base_folder = Path("project_frames")
        base_folder.mkdir(exist_ok=True)
        output_audio = base_folder / "audio_temp.aac"
        output_video = self.get_next_video_name(base_folder)

        if output_audio.exists():
            if not messagebox.askyesno(t["title"], f"{output_audio} {t['overwrite_audio']}"):
                return
            os.remove(output_audio)

        fps = self.fps_var.get()
        width = 80 if self.fast_mode_var.get() else self.get_width_from_resolution(self.res_var.get())

        ext = Path(file_path).suffix.lower()

        if ext == ".mp4":
            self.process_video(file_path, fps, width, base_folder, output_audio, output_video)
        elif ext == ".gif":
            self.process_gif(file_path, width, output_video)
        elif ext in [".png", ".jpg", ".jpeg"]:
            self.process_image(file_path, width, output_video)

    def process_video(self, file_path, fps, width, base_folder, output_audio, output_video):
        extracted_frames = base_folder / "extracted_frames"
        ascii_frames = base_folder / "ascii_frames"

        self.status_var.set(self.translations[self.lang_var.get()]["extracting_frames"])
        self.root.update()
        self.extract_frames(file_path, extracted_frames, fps)

        self.status_var.set(self.translations[self.lang_var.get()]["extracting_audio"])
        self.root.update()
        self.extract_audio(file_path, output_audio)

        self.status_var.set(self.translations[self.lang_var.get()]["converting_ascii"])
        self.root.update()
        self.generate_ascii_frames(extracted_frames, ascii_frames, width)

        self.status_var.set(self.translations[self.lang_var.get()]["creating_video"])
        self.root.update()
        self.create_ascii_video(ascii_frames, output_audio, output_video, fps)

        os.remove(output_audio)
        self.progress_var.set(100)
        self.status_var.set(self.translations[self.lang_var.get()]["done"])
        self.create_clickable_path(output_video)

        if self.cleanup_var.get():
            import shutil
            shutil.rmtree(extracted_frames)
            shutil.rmtree(ascii_frames)

    def process_gif(self, path, width, output_path):
        img = Image.open(path)
        ascii_frames = []
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            ascii_art = self.convert_image_to_ascii(frame, width)
            img_out = self.render_ascii_to_image(ascii_art)
            ascii_frames.append(img_out)
        ascii_frames[0].save(output_path, save_all=True, append_images=ascii_frames[1:], loop=0, duration=img.info.get("duration", 100))
        self.status_var.set(self.translations[self.lang_var.get()]["done"])
        self.create_clickable_path(output_path)

    def process_image(self, path, width, output_path):
        img = Image.open(path)
        ascii_art = self.convert_image_to_ascii(img, width)
        img_out = self.render_ascii_to_image(ascii_art)
        img_out.save(output_path)
        self.status_var.set(self.translations[self.lang_var.get()]["done"])
        self.create_clickable_path(output_path)

    def extract_frames(self, video_path, out_folder, fps):
        out_folder.mkdir(parents=True, exist_ok=True)
        cmd = [
            "bin/ffmpeg.exe", "-i", video_path, "-vf",
            f"fps={fps}", str(out_folder / "frame_%06d.png")
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def extract_audio(self, video_path, output_audio):
        cmd = [
            "bin/ffmpeg.exe", "-i", video_path, "-vn",
            "-acodec", "copy", str(output_audio)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def generate_ascii_frames(self, input_folder, output_folder, width):
        output_folder.mkdir(parents=True, exist_ok=True)
        frames = sorted(input_folder.glob("frame_*.png"))
        total = len(frames)
        for idx, frame_path in enumerate(frames):
            img = Image.open(frame_path)
            ascii_art = self.convert_image_to_ascii(img, width)
            img_out = self.render_ascii_to_image(ascii_art)
            img_out.save(output_folder / f"ascii_{idx:06d}.png")
            self.progress_var.set((idx + 1) / total * 100)
            self.root.update()

    def create_ascii_video(self, ascii_folder, audio_path, output_path, fps):
        temp_video = ascii_folder / "temp_no_audio.mp4"
        cmd = [
            "bin/ffmpeg.exe", "-framerate", str(fps), "-i",
            str(ascii_folder / "ascii_%06d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(temp_video)
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmd_audio = [
            "bin/ffmpeg.exe", "-i", str(temp_video), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
            str(output_path)
        ]
        subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        temp_video.unlink()

    def convert_image_to_ascii(self, img, width):
        w, h = img.size
        aspect_ratio = h / w
        new_height = int(aspect_ratio * width * 0.55)
        img = img.convert("L").resize((width, new_height))

        pixels = img.getdata()
        ascii_chars = self.ASCII_SETS[self.ascii_set_var.get()]
        chars_len = len(ascii_chars)
        ascii_str = ""
        for i, pixel in enumerate(pixels):
            ascii_str += ascii_chars[int(pixel / 255 * (chars_len - 1))]
            if (i + 1) % width == 0:
                ascii_str += "\n"
        return ascii_str

    def render_ascii_to_image(self, ascii_str):
        font = ImageFont.load_default()
        lines = ascii_str.splitlines()
        width = max(len(line) for line in lines)
        height = len(lines)

        img = Image.new("L", (width * 6, height * 10), color=0)
        draw = ImageDraw.Draw(img)
        for i, line in enumerate(lines):
            draw.text((0, i * 10), line, fill=255, font=font)
        return img

    def get_width_from_resolution(self, res):
        mapping = {
            "144p": 40,
            "360p": 80,
            "480p": 100,
            "720p": 140,
            "1080p": 180,
            "1440p": 220,
            "2K": 260,
            "4K": 320
        }
        return mapping.get(res, 80)

    def get_next_video_name(self, folder):
        base_name = folder / "ascii_video"
        for i in range(1, 1000):
            candidate = base_name.with_name(f"ascii_video_{i:03d}.mp4")
            if not candidate.exists():
                return candidate
        return base_name.with_name("ascii_video.mp4")

    def create_clickable_path(self, path):
        def open_file(event=None):
            import webbrowser
            webbrowser.open(str(path.resolve()))

        self.status_lbl.config(fg="#00ff00")
        self.status_lbl.bind("<Button-1>", open_file)
        self.status_var.set(f"{self.translations[self.lang_var.get()]['done']} {path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIVideoApp(root)
    root.geometry("400x700")
    root.minsize(400, 700)
    root.mainloop()
