import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()

def test_add_new_book_adds_book_without_genre(collector):
    collector.add_new_book('Гарри Поттер')
    assert collector.get_books_genre() == {'Гарри Поттер': ''}


def test_add_new_book_not_added_if_name_too_long(collector):
    long_name = 'A' * 41
    collector.add_new_book(long_name)
    assert long_name not in collector.get_books_genre()


def test_add_new_book_not_added_twice(collector):
    collector.add_new_book('Книга')
    collector.add_new_book('Книга')
    assert list(collector.get_books_genre().keys()).count('Книга') == 1


@pytest.mark.parametrize('genre', ['Фантастика', 'Комедии'])
def test_set_book_genre_sets_allowed_genre(collector, genre):
    collector.add_new_book('Книга')
    collector.set_book_genre('Книга', genre)
    assert collector.get_book_genre('Книга') == genre


def test_set_book_genre_does_not_set_if_book_not_exist(collector):
    collector.set_book_genre('Неизвестная книга', 'Фантастика')
    assert collector.get_book_genre('Неизвестная книга') is None


def test_set_book_genre_does_not_set_if_genre_not_allowed(collector):
    collector.add_new_book('Книга')
    collector.set_book_genre('Книга', 'Роман')
    assert collector.get_book_genre('Книга') == ''



def test_get_book_genre_returns_none_for_unknown_book(collector):
    assert collector.get_book_genre('Неизвестная книга') is None


def test_get_books_with_specific_genre_returns_only_matching(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    collector.add_new_book('Книга 3')

    collector.set_book_genre('Книга 1', 'Фантастика')
    collector.set_book_genre('Книга 2', 'Ужасы')
    collector.set_book_genre('Книга 3', 'Фантастика')

    result = collector.get_books_with_specific_genre('Фантастика')
    assert sorted(result) == ['Книга 1', 'Книга 3']


def test_get_books_with_specific_genre_returns_empty_if_genre_not_allowed(collector):
    collector.add_new_book('Книга 1')
    collector.set_book_genre('Книга 1', 'Фантастика')
    result = collector.get_books_with_specific_genre('Роман')
    assert result == []


def test_get_books_genre_returns_actual_dict(collector):
    collector.add_new_book('Книга 1')
    collector.set_book_genre('Книга 1', 'Фантастика')
    assert collector.get_books_genre() == {'Книга 1': 'Фантастика'}


def test_get_books_for_children_excludes_age_restricted_genres(collector):
    collector.add_new_book('Страшилки')
    collector.add_new_book('Смешарики')
    collector.add_new_book('Дело Пуаро')

    collector.set_book_genre('Страшилки', 'Ужасы')
    collector.set_book_genre('Смешарики', 'Мультфильмы')
    collector.set_book_genre('Дело Пуаро', 'Детективы')

    result = collector.get_books_for_children()
    assert result == ['Смешарики']


def test_get_books_for_children_ignores_books_without_genre(collector):
    collector.add_new_book('Без жанра')
    assert collector.get_books_for_children() == []



def test_add_book_in_favorites_adds_only_existing_book(collector):
    collector.add_new_book('Книга')
    collector.add_book_in_favorites('Книга')
    collector.add_book_in_favorites('Несуществующая')
    assert collector.get_list_of_favorites_books() == ['Книга']


def test_add_book_in_favorites_not_added_twice(collector):
    collector.add_new_book('Книга')
    collector.add_book_in_favorites('Книга')
    collector.add_book_in_favorites('Книга')
    assert collector.get_list_of_favorites_books() == ['Книга']



def test_delete_book_from_favorites_removes_if_exists(collector):
    collector.add_new_book('Книга')
    collector.add_book_in_favorites('Книга')
    collector.delete_book_from_favorites('Книга')
    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_does_nothing_if_not_in_favorites(collector):
    collector.add_new_book('Книга')
    collector.delete_book_from_favorites('Книга')
    assert collector.get_list_of_favorites_books() == []


def test_get_list_of_favorites_books_returns_current_list(collector):
    collector.add_new_book('Книга 1')
    collector.add_new_book('Книга 2')
    collector.add_book_in_favorites('Книга 1')
    assert collector.get_list_of_favorites_books() == ['Книга 1']
