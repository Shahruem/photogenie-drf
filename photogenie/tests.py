from rest_framework.test import APITestCase
from rest_framework import status
from photogenie.models import Category
from photogenie.api.serializers import CategorySerializer
from django.urls import reverse
from authentication.models import User
from photogenie.models import UserPost
from photogenie.api.serializers import PostSerializer


class CategoryViewSetTestCase(APITestCase):
    """ Test cases for Category Viewset containing list and retrieve methods """

    def setUp(self):
        """ Creates sample Category objects for testing """

        self.first_category = Category.objects.create(name="action")
        self.second_category = Category.objects.create(name="adventure")
        self.third_category = Category.objects.create(name="comedy")

    def test_list(self):
        """ Test listing all categories """

        url = reverse('category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Category.objects.count())
        expected_data = CategorySerializer(Category.objects.all(), many=True).data
        self.assertEqual(response.data['results'], expected_data)

    def test_retrieve(self):
        """ Test retrieving a category based on ID """

        url = reverse('category-detail', kwargs={'pk': self.first_category.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializer(self.first_category).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_non_existent(self):
        """ Test retrieving a category with non-existent ID """

        non_existent_pk = 400
        url = reverse('category-detail', kwargs={'pk': non_existent_pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserPostTestCase(APITestCase):
    """ Test cases for CRUD operations of UserPost model """

    def setUp(self):
        """ Creates sample UserPost objects for testing """

        self.first_user = User.objects.create(username='first_user', password='password1')
        self.second_user = User.objects.create(username='second_user', password='password2')

        self.first_category = Category.objects.create(name='action')
        self.second_category = Category.objects.create(name='adventure')

        self.first_post = UserPost.objects.create(
            published_by=self.first_user,
            description='Post 1 description',
            image='messi.jpg',
            views=10,
            downloads=5,
        )
        self.first_post.categories.add(self.first_category)
        self.first_post.tags.add('tag1', 'tag2')

        self.second_post = UserPost.objects.create(
            published_by=self.second_user,
            description='Post 2 description',
            image='superman.jpg',
            views=5,
            downloads=2,
        )
        self.second_post.categories.add(self.second_category)
        self.second_post.tags.add('tag3')

    def test_list_without_filters(self):
        """ Test listing all posts without any filters """

        url = reverse('userpost-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), UserPost.objects.count())

    def test_list_search_filter(self):
        """ Test listing all posts with search filter """

        url = reverse('userpost-list')
        response = self.client.get(url, {'search': 'action'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_count = UserPost.objects.filter(categories__name='action').count()
        self.assertEqual(len(response.data['results']), expected_count)

    def test_list_published_by_filter(self):
        """ Test listing all posts with published by (username) filter """

        url = reverse('userpost-list')
        response = self.client.get(url, {'published_by': self.first_user.username})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_count = UserPost.objects.filter(published_by=self.first_user).count()
        self.assertEqual(len(response.data['results']), expected_count)

    def test_list_category_filter(self):
        """ Test listing all posts with category (name) filter """

        url = reverse('userpost-list')
        response = self.client.get(url, {'category': self.first_category.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_count = UserPost.objects.filter(categories=self.first_category).count()
        self.assertEqual(len(response.data['results']), expected_count)

    def test_list_ordering_filter(self):
        """
        Tests listing all posts with ordering specified by downloads (can be views as well) and checks the first
        post of ordered response to have the download count equal to the lowest among all available posts
        """

        url = reverse('userpost-list')
        response = self.client.get(url, {'ordering': 'downloads'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['downloads'], self.second_post.downloads)

    def test_retrieve_by_author(self):
        """ Test retrieving a post published by the logged-in user so the views shouldn't increment """

        self.client.force_authenticate(user=self.first_user)
        url = reverse('userpost-detail', kwargs={'pk': self.first_post.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views'], 10)

    def test_retrieve_by_non_author(self):
        """ Test retrieving a post not published by the logged-in user so the views should increment """

        self.client.force_authenticate(user=self.second_user)
        url = reverse('userpost-detail', kwargs={'pk': self.first_post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views'], 11)

    def test_retrieve_non_existent(self):
        # Test retrieving a post that does not exist so expecting 404 Not Found

        url = reverse('userpost-detail', kwargs={'pk': 100})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
