from django.contrib.auth.models import AnonymousUser

import mock
from test_utils import RequestFactory, TestCase

from test_app import views
import waffle
from waffle.middleware import WaffleMiddleware


def get():
    request = RequestFactory().get('/foo')
    request.user = AnonymousUser()
    return request


def process_request(request, view):
    response = view(request)
    return WaffleMiddleware().process_response(request, response)


class WaffleTemplateTests(TestCase):
    def test_django_tags(self):
        request = get()
        response = process_request(request, views.flag_in_django)
        self.assertContains(response, 'flag off')
        self.assertContains(response, 'switch off')
        self.assertContains(response, 'sample')

    def test_jingo_tags(self):
        request = get()
        response = process_request(request, views.flag_in_jingo)
        self.assertContains(response, 'flag off')
        self.assertContains(response, 'switch off')
        self.assertContains(response, 'sample')

    @mock.patch.object(waffle, 'flag_is_active')
    @mock.patch.object(waffle, 'switch_is_active')
    @mock.patch.object(waffle, 'sample_is_active')
    def test_jingo_sugar(self, sample_is_active, switch_is_active,
                         flag_is_active):
        flag_is_active.return_value = True
        switch_is_active.return_value = True
        sample_is_active.return_value = True
        request = get()
        response = process_request(request, views.flag_in_jingo)
        self.assertContains(response, 'flag sugar on')
        self.assertContains(response, 'switch sugar on')
        self.assertContains(response, 'sample sugar on')
