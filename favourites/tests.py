from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from productpage.models import Product, Favorite, Category
from storepage.models import Toko


class FavoritesViewTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password")
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpassword"
        )

        # Create a category and a product to work with
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="This is a test product.",
            min_price=10.0,
            max_price=20.0,
        )

        # Log in the user
        self.client.login(username="testuser", password="password")

    def test_toggle_favorite_add(self):
        """Test adding a product to favorites."""
        response = self.client.post(reverse("toggle", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Favorite.objects.filter(user=self.user, product=self.product).exists()
        )
        self.assertJSONEqual(
            response.content,
            {"success": True, "message": "Added to favorites!", "is_favorited": True},
        )

    def test_toggle_favorite_remove(self):
        """Test removing a product from favorites."""
        Favorite.objects.create(
            user=self.user, product=self.product
        )  # Add the product to favorites first
        response = self.client.post(reverse("toggle", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Favorite.objects.filter(user=self.user, product=self.product).exists()
        )
        self.assertJSONEqual(
            response.content,
            {
                "success": True,
                "message": "Removed from favorites!",
                "is_favorited": False,
            },
        )

    def test_view_favorites_by_another_user_id(self):
        """Test that a non-admin user cannot view another user's favorites."""
        other_user = User.objects.create_user(
            username="otheruser", password="otherpassword"
        )
        Favorite.objects.create(user=other_user, product=self.product)
        response = self.client.get(
            reverse("view_all_favorites_by_user_id", args=[other_user.id])
        )
        self.assertEqual(response.status_code, 403)  # Should return forbidden
