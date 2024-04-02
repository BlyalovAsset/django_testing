from django.urls import reverse

NEWS_ID = 1

constant_url_news_detail = reverse('news:detail', args=(NEWS_ID,))
constant_url_news_home = reverse('news:home')
constant_url_news_detail = reverse('news:detail', args=(NEWS_ID,))
constant_url_comment_delete = reverse('news:delete', args=(NEWS_ID,))
constant_url_comment_edit = reverse('news:edit', args=(NEWS_ID,))
constant_url_news_detail = reverse('news:detail', args=(NEWS_ID,))
constant_url_comment_delete = reverse('news:delete', args=(NEWS_ID,))
constant_url_comment_edit = reverse('news:edit', args=(NEWS_ID,))
