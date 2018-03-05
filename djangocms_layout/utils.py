from cms.models import CMSPlugin
from bootstrap_layout.models import Section
from djangocms_layout.models import Section as LSection
from cms.utils.plugins import copy_plugins_to_placeholder
import time

'''
First edit djangocms_layout.cms_plugins and set SectionPlugin.__name__ = 'LayoutSectionPlugin'
before registering plugin.
Change this back to 'SectionPlugin' once plugins have been migrated.
'''

def get_fresh_instance(model, instance_pk, retries=3):
    try:
        fresh = model.objects.get(pk=instance_pk)
        return fresh
    except:
        print('Error getting fresh copy of plugin', instance_pk)
        if retries > 0:
            print('...sleeping for 0.5 seconds before retrying')
            time.sleep(0.5)
            return get_fresh_instance(model=model, instance_pk=instance_pk, retries=retries-1)
        else:
            print('...giving up')
            raise

def migrateSection(old_plugin):
    old_plugin = old_plugin.get_bound_plugin()
    children = old_plugin.get_children()
    
    new_plugin = LSection(
        language = old_plugin.language,
        placeholder = old_plugin.placeholder,
        position = old_plugin.position,
        plugin_type = 'LayoutSectionPlugin',

        name = old_plugin.name,
        min_height = old_plugin.min_height,
        bg_image = old_plugin.bg_image,
        bg_external_image = '', # bootstrap_layout didn't have this field
        bg_color = old_plugin.bg_color,
        bg_size = old_plugin.bg_size,
        bg_position = old_plugin.bg_position,
        bg_repeat = old_plugin.bg_repeat,
        bg_attachment = old_plugin.bg_attachment,
        container = old_plugin.container,
        classes = old_plugin.classes,
        attributes = old_plugin.attributes,
    )

    try:
        new_plugin.parent = old_plugin.parent
    except:
        pass

    # insert new plugin into tree at original position, shifting original to right
    new_plugin = old_plugin.add_sibling(pos='left', instance=new_plugin)

    # This does not seem to stick for some reason
    #for child in children:
    #    child.move(target=new_plugin, pos='last-child')
    
    try:
        new_plugin = get_fresh_instance(model=LSection, instance_pk=new_plugin.pk, retries=3)
    except:
        print("Couldn't get fresh copy of new_plugin")
    try:
        new_plugin = get_fresh_instance(model=Section, instance_pk=old_plugin.pk, retries=3)
    except:
        print("Couldn't get fresh copy of old_plugin")
    
    copy_plugins_to_placeholder(plugins=old_plugin.get_descendants(), placeholder=old_plugin.placeholder, root_plugin=new_plugin)
    
    new_plugin.copy_relations(old_plugin)
    # new_plugin.post_copy(old_plugin, [(new_plugin, old_plugin),])
    
    # in case this is a child of a TextPlugin that needs
    # its content updated with the newly copied plugin
    # if new_plugin.parent:
    #     new_plugin.parent.post_copy(new_plugin.parent, [(new_plugin, old_plugin),])
        
    old_plugin.delete()

    return new_plugin

def convert_bootstrap_to_djangocms_layout():
    numsections = Section.objects.count() # get initial count
    for i in range(0, numsections * 2):
        # give ourselves 2x as many chances to get this right
        section = Section.objects.first()
        if section:
            # still have Sections to migrate
            print('old section id:', section.pk)
            new_plugin = migrateSection(section)
            print('new layoutsection id:', new_plugin.pk)
        else:
            break
    # for section in Section.objects.all():
    #     print('old section id:', section.pk)
    #     new_plugin = migrateSection(section)
    #     print('new layoutsection id:', new_plugin.pk)
    lsections = CMSPlugin.objects.filter(plugin_type='LayoutSectionPlugin')
    for ls in lsections:
        ls.plugin_type = 'SectionPlugin'
        ls.save()
