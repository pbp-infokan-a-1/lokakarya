from django.test import TestCase
from django.urls import reverse
from landingpage.views import home

class LandingPageTests(TestCase):
    
    def test_home_page_status_code(self):
        """
        Test that the home page returns a 200 status code.
        """
        response = self.client.get(reverse('landingpage:home'))  # Assuming 'home' is the name of your URL pattern
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_template(self):
        """
        Test that the correct template is used for the home page.
        """
        response = self.client.get(reverse('landingpage:home'))
        self.assertTemplateUsed(response, 'main.html')  # Adjust based on your actual template file
    
    def test_home_page_context(self):
        """
        Test that the context data contains featured products or categories.
        """
        response = self.client.get(reverse('landingpage:home'))
        self.assertIn('featured_products', response.context)  # Replace 'featured_products' with your context variable
        self.assertIn('categories', response.context)  # Replace 'categories' with your context variable

    def test_search_functionality(self):
        """
        Test the search functionality on the landing page.
        """
        response = self.client.get(reverse('landingpage:home'), {'q': 'example search'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search Results')  # Make sure search results are being displayed
    
    def test_search_results_template(self):
        """
        Test that the correct template is used when displaying search results.
        """
        response = self.client.get(reverse('landingpage:home'), {'q': 'example'})
        self.assertTemplateUsed(response, 'search_results.html')

    def test_empty_search(self):
        """
        Test the behavior of an empty search query.
        """
        response = self.client.get(reverse('landingpage:home'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No results found')  # Make sure 'No results found' is shown for an empty search
