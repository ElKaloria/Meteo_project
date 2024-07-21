import json
import unittest
from unittest import mock

import requests
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
mock_response = [{
    'current_weather': {
        'temperature': 10
    }
}]


class MeteoTestCase(TestCase):
    def test_meteo_request_get(self):
        url = reverse('meteo_app:meteo_request_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meteo_app/city_form.html')

    # @unittest.expectedFailure
    # @mock.patch('requests.get', return_value=requests.Response)
    def test_meteo_request_post(self):
        url = reverse('meteo_app:meteo_request_view')
        response = self.client.post(url, {'city': 'Moscow'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meteo_app/weather.html')
        self.assertEqual(response.context['city'], 'Moscow')



