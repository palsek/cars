from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
import json

from .models import TheCar
from .serializers import TheCarSerializer
from .facades import CarsDbFacade
from .setup import CARS_SERVICE_URL


class popular(APIView):

    def get(self, request, number=3, format=None):
        """Get the most popular cars from local db
        """        
        
        cars_db = CarsDbFacade()
        most_popular_cars = cars_db.get_most_popular_car(number)
        
        serializer = TheCarSerializer(most_popular_cars, many=True)

        return Response(serializer.data)


class cars(APIView):

    def get(self, request, format=None):
        """"Get all cars from local db
        """
        
        cars_db = CarsDbFacade()
        all_cars = cars_db.get_all_cars()

        serializer = TheCarSerializer(all_cars, many=True)

        # prepare average rate for each car
        for car in serializer.data:
            if car['rates'] != 0:
                car['average_rate'] = (car['rate1'] * 1 + car['rate2'] * 2 + car['rate3'] * 3 + car['rate4'] * 4 + car['rate5'] * 5) / car['rates']
            else:
                car['average_rate'] = 0

        return Response(serializer.data)
        

    def post(self, request, format=None):
        """Search car in external service and adds it to local db
        """
        
        try:
            wanted_car_make = request.data['car_make']
            wanted_car_name = request.data['model_name']
        except KeyError as e:
            content = {
                'Not found key in request body: ': str(e),
                'proper request example' : {
                    "car_make" : "Honda",
                    "model_name": "civic"
                    }                
                }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        # prepare url to external car service
        car_service_url = CARS_SERVICE_URL + wanted_car_make + r'?format=json'

        try:
            # call external service
            response = requests.get(car_service_url)
        except requests.exceptions.Timeout:
            error_detail = "Timeout exception raised during external service call"
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException:
            error_detail = "Unknown exception raised during external service call"
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        
        if response.status_code == 200:
            response_data = json.loads(response.content)

            response_data_results = response_data['Results']

            # search cars by car name (model)
            found_cars = [c for c in response_data_results if c['Model_Name'].upper() == wanted_car_name.upper()]

            if len(found_cars) > 0:
                found_car = found_cars[0]
            else:
                content = {'Eror': 'Car not found in external service.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            the_car = TheCar()
            the_car.make = found_car['Make_Name']
            the_car.model = found_car['Model_Name']

            # interaction with local db
            cars_db = CarsDbFacade()
            cars_db.add_car(the_car)
                        
            serializer = TheCarSerializer(the_car)
            return Response(serializer.data)
        else:
            error_detail = 'Error during call external service'
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        

class rate(APIView):

    def get(self, request, format=None):
        """Return error because this operation is forbidden
        """
        
        error_detail = 'This method is unsupported'
        return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, format=None):
        """Add a rate to a car from (range from 1 to 5)
        """
        
        try:
            wanted_car_make = request.data['car_make']
            wanted_car_name = request.data['model_name']
            wanted_car_rate = request.data['rate']
        except KeyError as e:
            content = {
                'Not found key in request body: ': str(e),
                'proper request example' : {
                    "car_make" : "Honda",
                    "model_name": "civic",
                    "rate" : 5
                    }                
                }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        if int(wanted_car_rate) < 1 or int(wanted_car_rate) > 5:
            return Response('Rate need to be between 1 and 5', status=status.HTTP_404_NOT_FOUND)

        cars_db = CarsDbFacade()
        if cars_db.rate_car(wanted_car_make, wanted_car_name, wanted_car_rate):
            return Response('', status=status.HTTP_200_OK)
        else:
            error_detail = 'Error during rating, probably no such car exists'
            return Response(error_detail, status=status.HTTP_404_NOT_FOUND)
