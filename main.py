import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QLabel, QVBoxLayout, QWidget
from nltk import WordNetLemmatizer
from textblob import TextBlob
import nltk
from nltk.corpus import wordnet
import re


# Указываем новый путь для данных NLTK
nltk.data.path.append('C:/python/9_analys_texts/data/nltk_data')

# Скачиваем нужные пакеты
nltk.download('wordnet', download_dir='C:/python/9_analys_texts/data/nltk_data')
nltk.download('omw-1.4')  # Чтобы WordNet мог работать с расширенным набором слов

lemmatizer = WordNetLemmatizer()


class TextAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Alexandria")
        self.setGeometry(450, 200, 1000, 600)

        # Create layout and widgets
        self.layout = QVBoxLayout()
        self.label = QLabel("Выберите файл/файлы для анализа:")
        self.button = QPushButton("Открыть файл/файлы")
        self.sentiment_button = QPushButton("Тональность текста")
        self.synonym_button = QPushButton("Синонимы")
        self.lexeme_button = QPushButton("Лексемы")
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)

        # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.sentiment_button)
        self.layout.addWidget(self.synonym_button)
        self.layout.addWidget(self.lexeme_button)
        self.layout.addWidget(self.result_display)

        # Set central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Connect buttons to functions
        self.button.clicked.connect(self.open_file)
        self.sentiment_button.clicked.connect(self.analyze_sentiment_from_text)
        self.synonym_button.clicked.connect(self.count_synonyms_from_text)
        self.lexeme_button.clicked.connect(self.count_lexemes_from_text)

        self.texts = []  # Список для хранения текста из нескольких файлов

    def open_file(self):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, "Open Text Files", "", "Text Files (*.txt)")

        if file_paths:
            self.texts = []  # Сброс списка текстов
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.texts.append(text)  # Добавляем текст в список
                    self.result_display.append(f"Loaded text from: {file_path}\n{text}\n")  # Отображаем загруженный текст

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return "Позитивный"
        elif sentiment < 0:
            return "Негативный"
        else:
            return "Нейтральный"

    def get_synonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
        return synonyms

    def count_synonyms(self, text, synonym_list):
        cleaned_text = re.sub(r"[^\w\s]", "", text.lower())
        word_list = cleaned_text.split()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in word_list]

        synonym_count = {synonym: 0 for synonym in synonym_list}
        for word in lemmatized_words:
            if word in synonym_count:
                synonym_count[word] += 1

        return synonym_count

    def count_lexemes(self, text):
        cleaned_text = re.sub(r"[^\w\s]", "", text.lower())
        word_list = cleaned_text.split()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in word_list]

        lexeme_count = {}
        for word in lemmatized_words:
            if word in lexeme_count:
                lexeme_count[word] += 1
            else:
                lexeme_count[word] = 1

        sorted_lexemes = sorted(lexeme_count.items(), key=lambda item: item[1], reverse=True)
        return sorted_lexemes

    def analyze_sentiment_from_text(self):
        results = []
        for text in self.texts:
            sentiment = self.analyze_sentiment(text)
            results.append(f"Sentiment: {sentiment}")
        self.result_display.setText("\n".join(results))

    def count_synonyms_from_text(self):
        synonym_list = self.get_synonyms('happy')
        synonym_list.update({'cheerful', 'joyful', 'blissful'})
        results = []

        for text in self.texts:
            synonym_counts = self.count_synonyms(text, synonym_list)
            result = f"Synonym counts in text:\n" + "\n".join([f"{synonym} ({count})" for synonym, count in synonym_counts.items() if count > 0])
            results.append(result)

        self.result_display.setText("\n\n".join(results))

    def count_lexemes_from_text(self):
        results = []
        for text in self.texts:
            lexeme_counts = self.count_lexemes(text)
            result = f"Lexeme counts in text:\n" + "\n".join([f"{lexeme} ({count})" for lexeme, count in lexeme_counts])
            results.append(result)

        self.result_display.setText("\n\n".join(results))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
