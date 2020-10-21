from django.test import TestCase

# Create your tests here.

class CarviewTest(TestCase):

    def test_get_cars_status_code_200(self):
        response = self.client.get('/cars')
        self.assertEquals(response.status_code, 200)

    def test_post_cars_status_code_200(self):
        request_data = {'car_make':'Honda', 'model_name': 'cr-v'}
        response = self.client.post('/cars', request_data)
        self.assertEquals(response.status_code, 200)

    def test_post_cars_status_code_404(self):
        request_data = {'XXXXX':'Honda', 'model_name': 'cr-v'}
        response = self.client.post('/cars', request_data)
        self.assertEquals(response.status_code, 404)

    def test_post_cars_wrong_request_data(self):
        request_data = {'XXXXX':'Honda', 'model_name': 'cr-v'}
        response = self.client.post('/cars', request_data)
        expected = {'Not found key in request body: ': "'car_make'", 'proper request example': {'car_make': 'Honda', 'model_name': 'civic'}}
        self.assertEquals(response.data, expected)


class RateviewTest(TestCase):
    
    def test_get_rate_status_code_404(self):
        response = self.client.get('/rate')
        self.assertEquals(response.status_code, 404)

    def test_post_rate_status_code_404(self):
        request_data = {'car_make': 'Honda', 'model_name': 'civic', 'rate' : '5'}
        response = self.client.post('/rate', request_data)

        self.assertEquals(response.data, "Error during rating, probably no such car exists")

class PopularviewTest(TestCase):
    
    def test_get_popular_status_code_200(self):
        response = self.client.get('/popular')
        self.assertEquals(response.status_code, 200)
