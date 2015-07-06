import arrow
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import *


class ReservationTestCase(TestCase):

    def setUp(self):
        u1 = Unit.objects.create(name='Unit 1', id='unit_1')
        u2 = Unit.objects.create(name='Unit 2', id='unit_2')
        rt = ResourceType.objects.create(name='Type 1', id='type_1', main_type='space')
        Resource.objects.create(name='Resource 1a', id='r1a', unit=u1, type=rt)
        Resource.objects.create(name='Resource 1b', id='r1b', unit=u1, type=rt)
        Resource.objects.create(name='Resource 2a', id='r2a', unit=u2, type=rt)
        Resource.objects.create(name='Resource 2b', id='r2b', unit=u2, type=rt)

        p1 = Period.objects.create(start='2015-06-01', end='2015-09-01', unit=u1, name='')
        p2 = Period.objects.create(start='2015-06-01', end='2015-09-01', unit=u2, name='')
        p3 = Period.objects.create(start='2015-06-01', end='2015-09-01', resource_id='r1a', name='')
        Day.objects.create(period=p1, weekday=0, opens='08:00', closes='22:00')
        Day.objects.create(period=p2, weekday=1, opens='08:00', closes='16:00')
        Day.objects.create(period=p3, weekday=0, opens='08:00', closes='18:00')

    def test_opening_hours(self):
        r1a = Resource.objects.get(id='r1a')
        r1b = Resource.objects.get(id='r1b')

        date = arrow.get('2015-06-01').date()
        hours = r1a.get_opening_hours(begin=date)  # Monday
        self.assertEqual(hours['opens'], datetime.time(8, 00))
        self.assertEqual(hours['closes'], datetime.time(18, 00))

        hours = r1b.get_opening_hours(begin=date)  # Monday
        self.assertEqual(hours['opens'], datetime.time(8, 00))
        self.assertEqual(hours['closes'], datetime.time(22, 00))

    def test_reservation(self):
        r1a = Resource.objects.get(id='r1a')
        r1b = Resource.objects.get(id='r1b')

        begin = arrow.get('2015-06-01T08:00:00+03:00')
        Reservation.objects.create(resource=r1a, begin=begin,
                                   end=begin + datetime.timedelta(hours=2))

        # Attempt overlapping reservation
        with self.assertRaises(ValidationError):
            Reservation.objects.create(resource=r1a, begin=begin,
                                       end=begin + datetime.timedelta(hours=2))

        # Make a reservation that ends when the resource closes
        begin = arrow.get('2015-06-01T16:00:00+03:00')
        Reservation.objects.create(resource=r1a, begin=begin,
                                   end=begin + datetime.timedelta(hours=2))

class DayTestCase(TestCase):
    """
    # Test case for day handler

    Creates a week of regular period with open hours and two day closed exceptional period

    Tests that day creation works as it should
    """

    def setUp(self):
        u1 = Unit.objects.create(name='Unit 1', id='unit_1')
        u2 = Unit.objects.create(name='Unit 2', id='unit_2')
        rt = ResourceType.objects.create(name='Type 1', id='type_1', main_type='space')
        Resource.objects.create(name='Resource 1a', id='r1a', unit=u1, type=rt)
        Resource.objects.create(name='Resource 1b', id='r1b', unit=u1, type=rt)
        Resource.objects.create(name='Resource 2a', id='r2a', unit=u2, type=rt)
        Resource.objects.create(name='Resource 2b', id='r2b', unit=u2, type=rt)

        # Regular hours for one week
        p1 = Period.objects.create(start='2015-08-03', end='2015-08-09', unit=u1, name='regular hours')
        Day.objects.create(period=p1, weekday=0, opens='08:00', closes='18:00')
        Day.objects.create(period=p1, weekday=1, opens='08:00', closes='18:00')
        Day.objects.create(period=p1, weekday=2, opens='08:00', closes='18:00')
        Day.objects.create(period=p1, weekday=3, opens='08:00', closes='18:00')
        Day.objects.create(period=p1, weekday=4, opens='08:00', closes='18:00')
        Day.objects.create(period=p1, weekday=5, opens='12:00', closes='16:00')
        Day.objects.create(period=p1, weekday=6, opens='12:00', closes='14:00')

        # Two shorter days as exception
        exp1 = Period.objects.create(start='2015-08-06', end='2015-08-07', unit=u1,
                                     name='exceptionally short days', exception=True, parent=p1)
        Day.objects.create(period=exp1, weekday=3, opens='12:00', closes='16:00')
        Day.objects.create(period=exp1, weekday=4, opens='12:00', closes='16:00')

        # Weekend is closed as an exception
        exp2 = Period.objects.create(start='2015-08-08', end='2015-08-09', unit=u1, name='weekend is closed',
                                     closed=True, exception=True, parent=p1)
