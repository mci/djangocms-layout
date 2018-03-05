# -*- coding: utf-8 -*-
from django.test import TestCase

from djangocms_layout.models import Section


EXAMPLE_IMAGE = 'https://www.google.com/images/logo.png'


class SectionTestCase(TestCase):

    def setUp(self):
        Section.objects.create(
            min_height='400px',
            bg_color='#ff00ff',
            container='.container',
            bg_external_image=EXAMPLE_IMAGE,
        )

    def test_section_instance(self):
        """Section instance has been created"""
        section = Section.objects.get(container='.container')
        self.assertEqual(section.container, '.container')
        self.assertEqual(section.bg_image_url, EXAMPLE_IMAGE)
