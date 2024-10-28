from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Rating
import uuid
import json

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(str(category), "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            name="Test Product",
            category=self.category,
            min_price=10.00,
            max_price=20.00,
            description="A test product description"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.min_price, 10.00)
        self.assertEqual(self.product.max_price, 20.00)

    def test_product_average_rating(self):
        user = User.objects.create_user(username="testuser", password="password")
        Rating.objects.create(user=user, product=self.product, rating=5)
        Rating.objects.create(user=user, product=self.product, rating=3)
        self.assertEqual(self.product.count_average_rating(), 4)

class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Sports")
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            name="Football",
            category=self.category,
            min_price=30.00,
            max_price=50.00,
            description="A test product for sports category"
        )

    def test_rating_creation(self):
        rating = Rating.objects.create(
            user=self.user,
            product=self.product,
            rating=4.5,
            review="Great product!"
        )
        self.assertEqual(rating.rating, 4.5)
        self.assertEqual(rating.review, "Great product!")
        self.assertEqual(str(rating), f'Rating: 4.5 by {self.user.username}')

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            id=uuid.uuid4(),
            name="Smartphone",
            category=self.category,
            min_price=100,
            max_price=200,
            description="Test smartphone product"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_product_page_view(self):
        response = self.client.get(reverse("product_page"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("products", response.context)

    def test_product_detail_view(self):
        response = self.client.get(reverse("product_detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("product", response.context)
        self.assertEqual(response.context["product"], self.product)

    def test_add_review_ajax(self):
        response = self.client.post(
            reverse("add_review_ajax", args=[self.product.id]),
            json.dumps({"review": "Great product!", "rating": 5}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.count(), 1)

    def test_edit_review_ajax(self):
        review = Rating.objects.create(user=self.user, product=self.product, rating=4, review="Nice")
        response = self.client.post(
            reverse("edit_review_ajax", args=[self.product.id, review.id]),
            json.dumps({"review": "Updated review", "rating": 4.5}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.review, "Updated review")
        self.assertEqual(review.rating, 4.5)

    def test_delete_review_ajax(self):
        review = Rating.objects.create(user=self.user, product=self.product, rating=4, review="Delete this")
        response = self.client.delete(
            reverse("delete_review_ajax", args=[self.product.id, review.id]),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rating.objects.count(), 0)