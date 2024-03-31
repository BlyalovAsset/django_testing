import pytest
from django.conf import settings
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(eleven_news, url_news_home, client):
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(eleven_news, url_news_home, client):
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(news_with_ten_comments, url_news_detail, client):
    response = client.get(url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    sorted_comments = sorted(all_comments,
                             key=lambda x: x.created,
                             reverse=True)
    assert [comment.id for
            comment in all_comments] == [comment.id
                                         for comment in sorted_comments[::-1]]


@pytest.mark.django_db
def test_anonymous_client_has_no_form(url_news_detail, client):
    response = client.get(url_news_detail)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(url_news_detail, author_client):
    response = author_client.get(url_news_detail)
    assert isinstance(response.context['form'], CommentForm)
