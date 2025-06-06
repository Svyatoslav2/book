from book import recommend_books

def test_recommend_books_single_keyword():
    # Проверка для одного существующего ключевого слова
    result = recommend_books("программирование")
    assert "Рекомендуемые книги:" in result
    assert "Чистый код - Роберт Мартин" in result
    assert "Python. К вершинам мастерства - Лучано Рамальо" in result

def test_recommend_books_no_keyword():
    # Проверка для несуществующего ключевого слова
    result = recommend_books("несуществующее_слово")
    assert result == "Не нашел рекомендаций по вашим ключевым словам.\nПопробуйте: программирование, психология, наука, бизнес"

def test_recommend_books_multiple_keywords():
    # Проверка для нескольких ключевых слов
    result = recommend_books("программирование психология")
    assert "Рекомендуемые книги:" in result
    assert "Чистый код - Роберт Мартин" in result  # из категории "программирование"
    assert "Сила привычки - Чарльз Дахигг" in result  # из категории "психология"

def test_recommend_books_case_insensitive():
    # Проверка на регистронезависимость
    result = recommend_books("ПРОГРАММИРОВАНИЕ")
    assert "Рекомендуемые книги:" in result
    assert "Чистый код - Роберт Мартин" in result

def test_recommend_books_no_duplicates():
    # Проверка на отсутствие дубликатов
    # Добавим дубликат вручную (для теста)
    from book import book_recommendations
    original_value = book_recommendations["программирование"][:]
    book_recommendations["программирование"].append("Чистый код - Роберт Мартин")  # искусственный дубликат

    result = recommend_books("программирование")
    assert result.count("Чистый код - Роберт Мартин") == 1  # проверяем, что дубликат удален

    # Восстанавливаем исходные данные
    book_recommendations["программирование"] = original_value


def test_recommend_books_trim_spaces():
    result = recommend_books("  программирование  ")
    assert "Чистый код - Роберт Мартин" in result

def test_recommend_books_mixed_known_and_unknown():
    result = recommend_books("программирование неизвестное_слово")
    assert "Чистый код - Роберт Мартин" in result
    assert "Не нашел рекомендаций" not in result

def test_recommend_books_only_unknown_keywords():
    result = recommend_books("неизвестное1 неизвестное2")
    assert "Не нашел рекомендаций" in result

def test_recommend_books_with_multiple_spaces():
    result = recommend_books("   программирование   психология   ")
    assert "Чистый код - Роберт Мартин" in result
    assert "Сила привычки - Чарльз Дахигг" in result

def test_recommend_books_partial_match_should_fail():
    result = recommend_books("программирова")  # не должно сработать
    assert "Рекомендуемые книги" not in result
    assert "Не нашел рекомендаций" in result

def test_recommend_books_result_starts_correctly():
    result = recommend_books("психология")
    assert result.startswith("Рекомендуемые книги:")

def test_recommend_books_multiple_matches_count():
    result = recommend_books("психология наука")
    lines = result.strip().split("\n")[1:]  # пропускаем первую строку
    assert len(lines) >= 30  # т.к. по 15 книг в каждой категории

def test_recommend_books_strip_duplicates_between_categories():
    from book import book_recommendations
    # Искусственно вставим дубликат из одной категории в другую
    book_recommendations["психология"].append("Чистый код - Роберт Мартин")
    result = recommend_books("программирование психология")
    assert result.count("Чистый код - Роберт Мартин") == 1
    book_recommendations["психология"].remove("Чистый код - Роберт Мартин")  # cleanup

def test_recommend_books_return_type():
    result = recommend_books("наука")
    assert isinstance(result, str)

def test_recommend_books_keywords_with_mixed_case_and_spaces():
    result = recommend_books("  Психология   НАУКА ")
    assert "Сила привычки - Чарльз Дахигг" in result
    assert "Краткая история времени - Стивен Хокинг" in result
