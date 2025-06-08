from tkinter import simpledialog, messagebox, Tk, Label, Button, Listbox, Scrollbar, Toplevel
import webbrowser
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pickle
import os
from collections import defaultdict
import random

class BookRecommender:
    def __init__(self):
        # Загрузка или создание базы данных книг
        self.book_db = self.load_or_create_db()
        
        # Инициализация модели машинного обучения
        self.model = self.train_model()
        
        # Создание GUI
        self.root = Tk()
        self.root.title("Умный рекомендатель книг")
        self.setup_ui()
        
    def load_or_create_db(self):
        """Загружает существующую базу данных или создает новую"""
        if os.path.exists('book_database.pkl'):
            with open('book_database.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            # Преобразуем вашу исходную базу в более удобный формат
            book_db = defaultdict(list)
            for genre, books in book_recommendations.items():
                for book in books:
                    title, author = book.split(' - ')
                    book_db['title'].append(title)
                    book_db['author'].append(author)
                    book_db['genre'].append(genre)
                    book_db['description'].append(f"{title} - книга в жанре {genre}")
            
            # Преобразуем в DataFrame
            book_db = pd.DataFrame(book_db)
            
            # Сохраняем для будущего использования
            with open('book_database.pkl', 'wb') as f:
                pickle.dump(book_db, f)
                
            return book_db
    
    def train_model(self):
        """Обучает модель машинного обучения для рекомендаций"""
        # Создаем TF-IDF матрицу на основе описаний книг
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.book_db['description'])
        
        # Обучаем модель k-ближайших соседей
        model = NearestNeighbors(n_neighbors=5, algorithm='brute', metric='cosine')
        model.fit(tfidf_matrix)
        
        return model
    
    def get_recommendations(self, query):
        """Получает рекомендации на основе пользовательского запроса"""
        # Векторизуем запрос
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.book_db['description'])
        query_vec = tfidf.transform([query])
        
        # Находим ближайшие книги
        distances, indices = self.model.kneighbors(query_vec)
        
        # Возвращаем рекомендации
        recommendations = []
        for idx in indices[0]:
            book = self.book_db.iloc[idx]
            recommendations.append(f"{book['title']} - {book['author']} ({book['genre']})")
        
        return recommendations
    
    def get_similar_books(self, book_title):
        """Находит похожие книги на основе выбранной"""
        idx = self.book_db[self.book_db['title'] == book_title].index[0]
        
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.book_db['description'])
        
        # Вычисляем косинусную схожесть
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Получаем пары (индекс, схожесть)
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Сортируем по схожести
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Берем топ-5 похожих книг (исключая саму книгу)
        sim_scores = sim_scores[1:6]
        
        # Получаем индексы книг
        book_indices = [i[0] for i in sim_scores]
        
        # Возвращаем рекомендации
        return self.book_db.iloc[book_indices]
    
    def search_books(self, keywords):
        """Поиск книг по ключевым словам"""
        keywords = keywords.lower()
        results = []
        
        # Поиск по жанру
        genre_matches = self.book_db[self.book_db['genre'].str.contains(keywords, case=False)]
        
        # Поиск по названию или автору
        text_matches = self.book_db[
            self.book_db['title'].str.contains(keywords, case=False) | 
            self.book_db['author'].str.contains(keywords, case=False)
        ]
        
        # Объединяем результаты
        results = pd.concat([genre_matches, text_matches]).drop_duplicates()
        
        if results.empty:
            return None
        else:
            return results
    
    def setup_ui(self):
        """Настраивает пользовательский интерфейс"""
        Label(self.root, text="Умный рекомендатель книг", font=('Helvetica', 16)).pack(pady=10)
        
        Button(self.root, text="Поиск по ключевым словам", 
              command=self.show_search_dialog).pack(pady=5)
        
        Button(self.root, text="Рекомендации по жанру", 
              command=self.show_genre_recommendations).pack(pady=5)
        
        Button(self.root, text="Похожие книги", 
              command=self.show_similar_books_dialog).pack(pady=5)
        
        Button(self.root, text="Случайная рекомендация", 
              command=self.random_recommendation).pack(pady=5)
        
        Button(self.root, text="Выход", 
              command=self.root.quit).pack(pady=5)
    
    def show_search_dialog(self):
        """Показывает диалог поиска книг"""
        search_window = Toplevel(self.root)
        search_window.title("Поиск книг")
        
        Label(search_window, text="Введите ключевые слова:").pack(pady=5)
        
        search_entry = simpledialog.Entry(search_window, width=50)
        search_entry.pack(pady=5)
        
        def on_search():
            query = search_entry.get()
            if query:
                results = self.search_books(query)
                if results is not None and not results.empty:
                    self.show_results(results, f"Результаты поиска: {query}")
                else:
                    messagebox.showinfo("Результат", "Ничего не найдено. Попробуйте другие ключевые слова.")
            search_window.destroy()
        
        Button(search_window, text="Поиск", command=on_search).pack(pady=5)
    
    def show_genre_recommendations(self):
        """Показывает рекомендации по жанрам"""
        genre_window = Toplevel(self.root)
        genre_window.title("Рекомендации по жанру")
        
        Label(genre_window, text="Выберите жанр:").pack(pady=5)
        
        genre_listbox = Listbox(genre_window, height=15, width=30)
        scrollbar = Scrollbar(genre_window, orient="vertical")
        scrollbar.config(command=genre_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        for genre in sorted(set(self.book_db['genre'])):
            genre_listbox.insert("end", genre)
        genre_listbox.pack(pady=5)
        
        def on_select():
            selected_genre = genre_listbox.get(genre_listbox.curselection())
            books = self.book_db[self.book_db['genre'] == selected_genre]
            self.show_results(books, f"Книги в жанре: {selected_genre}")
            genre_window.destroy()
        
        Button(genre_window, text="Выбрать", command=on_select).pack(pady=5)
    
    def show_similar_books_dialog(self):
        """Показывает диалог для поиска похожих книг"""
        similar_window = Toplevel(self.root)
        similar_window.title("Похожие книги")
        
        Label(similar_window, text="Введите название книги:").pack(pady=5)
        
        book_entry = simpledialog.Entry(similar_window, width=50)
        book_entry.pack(pady=5)
        
        def on_find_similar():
            book_title = book_entry.get()
            if book_title:
                try:
                    similar_books = self.get_similar_books(book_title)
                    self.show_results(similar_books, f"Книги, похожие на: {book_title}")
                except:
                    messagebox.showerror("Ошибка", "Книга не найдена. Проверьте название.")
            similar_window.destroy()
        
        Button(similar_window, text="Найти похожие", command=on_find_similar).pack(pady=5)
    
    def show_results(self, books, title):
        """Показывает результаты поиска/рекомендаций"""
        results_window = Toplevel(self.root)
        results_window.title(title)
        
        Label(results_window, text=title, font=('Helvetica', 12)).pack(pady=5)
        
        listbox = Listbox(results_window, height=15, width=80)
        scrollbar = Scrollbar(results_window, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        for _, book in books.iterrows():
            listbox.insert("end", f"{book['title']} - {book['author']} ({book['genre']})")
        listbox.pack(pady=5, padx=5)
        
        def on_search_online():
            selected = listbox.get(listbox.curselection())
            title = selected.split(' - ')[0]
            search_url = f"https://www.google.com/search?q=купить+{title.replace(' ', '+')}"
            webbrowser.open(search_url)
        
        Button(results_window, text="Найти в интернете", command=on_search_online).pack(pady=5)
    
    def random_recommendation(self):
        """Показывает случайную рекомендацию"""
        random_book = self.book_db.sample(1).iloc[0]
        answer = messagebox.askyesno(
            "Случайная рекомендация", 
            f"Попробуйте: {random_book['title']} - {random_book['author']}\n\nЖанр: {random_book['genre']}\n\nХотите найти эту книгу в интернете?"
        )
        
        if answer:
            search_url = f"https://www.google.com/search?q=купить+{random_book['title'].replace(' ', '+')}"
            webbrowser.open(search_url)
    
    def run(self):
        """Запускает приложение"""
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    # Здесь должна быть ваша исходная база данных book_recommendations
    # Я предполагаю, что она уже определена выше в вашем коде
    
    app = BookRecommender()
    app.run()