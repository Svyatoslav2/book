# -*- coding: windows-1251 -*-

from book import recommend_books

def test_recommend_books_single_keyword():
    # �������� ��� ������ ������������� ��������� �����
    result = recommend_books("����������������")
    assert "������������� �����:" in result
    assert "������ ��� - ������ ������" in result
    assert "Python. � �������� ���������� - ������ �������" in result

def test_recommend_books_no_keyword():
    # �������� ��� ��������������� ��������� �����
    result = recommend_books("��������������_�����")
    assert result == "�� ����� ������������ �� ����� �������� ������.\n����������: ����������������, ����������, �����, ������"

def test_recommend_books_multiple_keywords():
    # �������� ��� ���������� �������� ����
    result = recommend_books("���������������� ����������")
    assert "������������� �����:" in result
    assert "������ ��� - ������ ������" in result  # �� ��������� "����������������"
    assert "���� �������� - ������ ������" in result  # �� ��������� "����������"

def test_recommend_books_case_insensitive():
    # �������� �� ���������������������
    result = recommend_books("����������������")
    assert "������������� �����:" in result
    assert "������ ��� - ������ ������" in result

def test_recommend_books_no_duplicates():
    # �������� �� ���������� ����������
    # ������� �������� ������� (��� �����)
    from book import book_recommendations
    original_value = book_recommendations["����������������"][:]
    book_recommendations["����������������"].append("������ ��� - ������ ������")  # ������������� ��������

    result = recommend_books("����������������")
    assert result.count("������ ��� - ������ ������") == 1  # ���������, ��� �������� ������

    # ��������������� �������� ������
    book_recommendations["����������������"] = original_value


def test_recommend_books_trim_spaces():
    result = recommend_books("  ����������������  ")
    assert "������ ��� - ������ ������" in result

def test_recommend_books_mixed_known_and_unknown():
    result = recommend_books("���������������� �����������_�����")
    assert "������ ��� - ������ ������" in result
    assert "�� ����� ������������" not in result

def test_recommend_books_only_unknown_keywords():
    result = recommend_books("�����������1 �����������2")
    assert "�� ����� ������������" in result

def test_recommend_books_with_multiple_spaces():
    result = recommend_books("   ����������������   ����������   ")
    assert "������ ��� - ������ ������" in result
    assert "���� �������� - ������ ������" in result

def test_recommend_books_partial_match_should_fail():
    result = recommend_books("�������������")  # �� ������ ���������
    assert "������������� �����" not in result
    assert "�� ����� ������������" in result

def test_recommend_books_result_starts_correctly():
    result = recommend_books("����������")
    assert result.startswith("������������� �����:")

def test_recommend_books_multiple_matches_count():
    result = recommend_books("���������� �����")
    lines = result.strip().split("\n")[1:]  # ���������� ������ ������
    assert len(lines) >= 30  # �.�. �� 15 ���� � ������ ���������

def test_recommend_books_strip_duplicates_between_categories():
    from book import book_recommendations
    # ������������ ������� �������� �� ����� ��������� � ������
    book_recommendations["����������"].append("������ ��� - ������ ������")
    result = recommend_books("���������������� ����������")
    assert result.count("������ ��� - ������ ������") == 1
    book_recommendations["����������"].remove("������ ��� - ������ ������")  # cleanup

def test_recommend_books_return_type():
    result = recommend_books("�����")
    assert isinstance(result, str)

def test_recommend_books_keywords_with_mixed_case_and_spaces():
    result = recommend_books("  ����������   ����� ")
    assert "���� �������� - ������ ������" in result
    assert "������� ������� ������� - ������ ������" in result
