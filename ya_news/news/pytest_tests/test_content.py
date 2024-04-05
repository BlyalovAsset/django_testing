import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(eleven_news, client):
    constant_url_news_home = reverse('news:home')
    response = client.get(constant_url_news_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(eleven_news, client):
    constant_url_news_home = reverse('news:home')
    response = client.get(constant_url_news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(news_with_ten_comments, client, news):
    constant_url_news_detail = reverse('news:detail', args=(news.id,))
    response = client.get(constant_url_news_detail)
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
def test_anonymous_client_has_no_form(client, news):
    constant_url_news_detail = reverse('news:detail', args=(news.id,))
    response = client.get(constant_url_news_detail)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news):
    constant_url_news_detail = reverse('news:detail', args=(news.id,))
    response = author_client.get(constant_url_news_detail)
    form = response.context.get('form')
    assert isinstance(form, CommentForm)
