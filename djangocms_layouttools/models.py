from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from filer.fields.image import FilerImageField
from cms.models.pluginmodel import CMSPlugin
from cms.models import Page
from cms.models.fields import PageField
from ckeditor.fields import RichTextField
#from cmsplugin_filer_image import ThumbnailOption

from . import fields
from djangocms_attributes_field.fields import AttributesField

class Classes(models.TextField):
    default_field_class = fields.Classes

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = 'Classes'
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        if 'help_text' not in kwargs:
            kwargs['help_text'] = 'Space separated classes that are added to ' + \
            	'the class. See <a href="http://getbootstrap.com/css/" ' + \
            	'target="_blank">Bootstrap 3 documentation</a>.'
        super(Classes, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Classes, self).formfield(**defaults)

SIZE_CHOICES = (
    ('100% auto', 'fit width: 100% auto'),
    ('auto 100%', 'fit height: auto 100%'),
    ('cover', 'fill: cover '),
    ('auto', 'default: auto'),
)

REPEAT_CHOICES = (
    ('no-repeat', 'no-repeat'),
    ('repeat', 'repeat'),
    ('repeat-x', 'repeat-x'),
    ('repeat-y', 'repeat-y'),
)

ATTACHMENT_CHOICES = (
    ('scroll', 'scroll'),
    ('fixed', 'fixed'),
)

# Should pull these from django settings.py
CONTAINER_CHOICES = (
    ('', 'No container (full-width)'),
    ('container', '.container (smaller content width based on device size)'),
    ('container-fluid', '.container-fluid (full-width with slight padding on sides)'),
)

class Section(CMSPlugin):
    name = models.CharField('Section Name', max_length=25, default='', help_text='Descriptive name [not rendered on page]', blank=True, null=True)
    min_height = models.CharField('Minimum Section Height', max_length=25, default='0px', help_text='0 is default. Set it larger to expand height of section.')
    bg_image = FilerImageField(
        verbose_name=_('Background Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    bg_external_image = models.URLField(
        verbose_name=_('External URL Background Image'),
        blank=True,
        max_length=255,
        help_text=_('If provided, overrides the embedded image.')
    )
    bg_color = models.CharField('CSS Background Color', max_length=25, default='transparent', help_text='(e.g., #RRGGBB, rgba(120,120,120,0.3))')
    bg_size = models.CharField('Background Size', max_length=25, choices=SIZE_CHOICES, default='cover')
    bg_position = models.CharField('Background Position', max_length=25, default='center', blank=True)
    bg_repeat = models.CharField('Background Repeat', max_length=25, choices=REPEAT_CHOICES, default='no-repeat', blank=True)
    bg_attachment = models.CharField('Background Attachment', max_length=25, choices=ATTACHMENT_CHOICES, default='scroll', blank=True)
    container = models.CharField(
        verbose_name='Add nested .container or .container-fluid child element',
        max_length=25,
        choices=CONTAINER_CHOICES,
        blank=True,
        default='container',
        help_text=_('Adds a ".container" or ".container-fluid" element inside the section. '
            'Use it to have a full-page-width styled <section> with an inner container with '
            'a constrained width. All child plugins render inside the container.'),
    )

    classes = Classes()

    attributes = AttributesField(
        verbose_name='Attributes',
        blank=True,
        excluded_keys=['class'],
    )

    def __str__(self):
        return self.name + ' ' + self.container

    @property
    def bg_image_url(self):
        if self.bg_image:
            return self.bg_image.url
        else:
            return self.bg_external_image

    def clean(self):
        # you shall only set one image kind
        if self.bg_image and self.bg_external_image:
            raise ValidationError(
                ugettext('You need to add either an image or a URL '
                         'linking to an external image, not both.')
            )
