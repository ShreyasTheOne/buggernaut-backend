import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buggernaut_backend.settings")
import django
django.setup()
from buggernaut.models import Tag


tags_list = ["Usability", "Content", "Visual", "Spelling", "Security", "Functional", "Forced"]

for tag_name in tags_list:
    try:
        t = Tag.objects.get(name=tag_name)
        print("A tag with the name", tag_name, "already exists.")
    except Tag.DoesNotExist:
        t = Tag(name=tag_name)
        t.save()
        print("A tag with the name", tag_name, "has been created.")


list = input("Input any more tags you want to add to the list, in the form of space separated words. If not simply press ENTER: ").split(" ")
if(len(list)==0):
    pass
else:
    for tag_name in list:
        if len(tag_name) == 0:
            continue
        try:
            t = Tag.objects.get(name=tag_name)
            print("A tag with the name", tag_name, "already exists.")
        except Tag.DoesNotExist:
            t = Tag(name=tag_name)
            t.save()
            print("A tag with the name", tag_name, "has been created.")
