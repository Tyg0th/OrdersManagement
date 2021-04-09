import unittest

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ExampleTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
