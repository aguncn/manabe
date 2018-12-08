from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.auth.models import User


class SeleniumLiveServerTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test', )
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('{}{}'.format(
            self.live_server_url,
            '/accounts/login/'
        ))
        username_input = \
            self.selenium.find_element_by_name("username")
        username_input.send_keys("test")
        password_input = \
            self.selenium.find_element_by_name("password")
        password_input.send_keys("test")
        self.selenium.find_element_by_xpath('//input[@name="login"]').click()
