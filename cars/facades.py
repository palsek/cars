from .models import TheCar


class CarsDbFacade:

    def add_car(self, car):
        """Add new car to db if already does not exists.
        """

        TheCar.objects.update_or_create(make=car.make, model=car.model.upper())


    def get_all_cars(self):
        """Get all cars from db.
        """

        all_cars = TheCar.objects.all()

        return all_cars

    def rate_car(self, make, model, rate):
        """Add new rate to specified car.
        """

        try:
            found_car = TheCar.objects.get(make=make.upper(), model=model.upper())
        except:
            return False
        else:
            found_car.rates += 1

            if rate == 1:
                found_car.rate1 = int(found_car.rate1) + 1 if found_car.rate1 is not None else 1
            elif rate == 2:
                found_car.rate2 = int(found_car.rate2) + 1 if found_car.rate1 is not None else 1
            elif rate == 3:
                found_car.rate3 = int(found_car.rate3) + 1 if found_car.rate1 is not None else 1
            elif rate == 4:
                found_car.rate4 = int(found_car.rate4) + 1 if found_car.rate1 is not None else 1
            elif rate == 5:
                found_car.rate5 = int(found_car.rate5) + 1 if found_car.rate1 is not None else 1

            found_car.save()

            return True


    def get_most_popular_car(self, car_number):
        """Get the car which has the most rates.
        """

        all_cars = TheCar.objects.all()
        most_popular_cars = sorted(all_cars, key=lambda c: c.rates, reverse=True)[:int(car_number)]

        return most_popular_cars
