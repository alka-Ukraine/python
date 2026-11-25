from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import CityPost


class CityPostPermissionsTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.author = User.objects.create_user(username='author', password='safe-test-password-123')
        self.other = User.objects.create_user(username='other', password='safe-test-password-123')
        self.post = CityPost.objects.create(city='Львів', title='Прогулянка', body='Старе місто', author=self.author)

    def test_public_can_read_but_not_create(self):
        list_url = reverse('city-posts-list')
        self.assertEqual(self.client.get(list_url, {'city': 'львів'}).data[0]['id'], self.post.id)
        response = self.client.post(list_url, {'city': 'Львів', 'title': 'Новий', 'body': 'Текст'})
        self.assertIn(response.status_code, (401, 403))

    def test_only_author_can_edit_post(self):
        detail_url = reverse('city-posts-detail', args=[self.post.id])
        self.client.force_authenticate(user=self.other)
        self.assertEqual(self.client.patch(detail_url, {'title': 'Чужа зміна'}).status_code, 403)
        self.client.force_authenticate(user=self.author)
        self.assertEqual(self.client.patch(detail_url, {'title': 'Нова назва'}).status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Нова назва')

    def test_author_is_taken_from_authenticated_user(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.post(reverse('city-posts-list'), {
            'city': 'Львів', 'title': 'Мій маршрут', 'body': 'Деталі', 'author': self.author.username,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CityPost.objects.get(pk=response.data['id']).author, self.other)
