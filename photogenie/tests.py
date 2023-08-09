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
            image='images/messi.jpg',
            views=10,
            downloads=5,
        )
        self.first_post.categories.add(self.first_category)
        self.first_post.tags.add('tag1', 'tag2')

        self.second_post = UserPost.objects.create(
            published_by=self.second_user,
            description='Post 2 description',
            image='images/superman.jpg',
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
        self.assertEqual(response.data['views'], self.first_post.views)

    def test_retrieve_by_non_author(self):
        """ Test retrieving a post not published by the logged-in user so the views should increment """

        self.client.force_authenticate(user=self.second_user)
        url = reverse('userpost-detail', kwargs={'pk': self.first_post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['views'], 11)

    def test_retrieve_non_existent(self):
        """ Test retrieving a post that does not exist so expecting 404 Not Found """

        url = reverse('userpost-detail', kwargs={'pk': 100})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_by_non_author(self):
        """ Tests updating the post with non-author """

        self.client.force_authenticate(user=self.first_user)
        url = reverse('userpost-detail', kwargs={'pk': self.second_post.id})

        new_data = {
            'description': 'Updated description',
            'categories': [self.second_category.id],
            'tags': ['tag4', 'tag5'],
            'image': 'images/superman.jpg'
        }

        response = self.client.put(url, new_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_unauthorized(self):
        """ Tests updating without authorization """

        url = reverse('userpost-detail', kwargs={'pk': self.first_post.id})

        new_data = {
            'description': 'Updated description',
        }

        response = self.client.put(url, new_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.first_post.refresh_from_db()
        self.assertNotEqual(self.first_post.description, new_data['description'])

    def test_destroy(self):
        """ Tests destroying User Post by its author """

        self.client.force_authenticate(user=self.first_user)

        url = reverse('userpost-detail', kwargs={'pk': self.first_post.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserPost.objects.filter(pk=self.first_post.id).exists())

    def test_destroy_unauthenticated(self):
        """ Tests destroying User post unauthenticated """

        url = reverse('userpost-detail', kwargs={'pk': self.first_post.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(UserPost.objects.filter(pk=self.first_post.id).exists())

    def test_destroy_by_non_author(self):
        """ Tests destroying User post from a non-author """

        self.client.force_authenticate(user=self.first_user)
        url = reverse('userpost-detail', kwargs={'pk': self.second_post.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_download_image_authenticated(self):
        """ Tests downloading the image of User Post with authenticated user """

        self.client.force_authenticate(user=self.first_user)

        url = reverse('download-image', kwargs={'pk': self.first_post.id})

        current_downloads = self.first_post.downloads
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/*')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.first_post.image.name}"')
        self.first_post.refresh_from_db()
        self.assertEqual(self.first_post.downloads, current_downloads + 1)

    def test_download_image_unauthenticated(self):
        """ Tests downloading the image of User Post without authenticated user """

        url = reverse('download-image', kwargs={'pk': self.first_post.id})

        current_downloads = self.first_post.downloads
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.first_post.refresh_from_db()
        self.assertEqual(self.first_post.downloads, current_downloads)
