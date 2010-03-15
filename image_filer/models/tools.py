from django.db.models.query import CollectedObjects
from django.db.models.fields.related import ForeignKey
from django.forms.models import model_to_dict
from image_filer.models import Clipboard

def duplicate(obj, value=None, field=None, duplicate_order=None):
    """
    Duplicate all related objects of obj setting
    field to value. If one of the duplicate
    objects has an FK to another duplicate object
    update that as well. Return the duplicate copy
    of obj.

    duplicate_order is a list of models which specify how
    the duplicate objects are saved. For complex objects
    this can matter. Check to save if objects are being
    saved correctly and if not just pass in related objects
    in the order that they should be saved.

    """
    collected_objs = CollectedObjects()
    obj._collect_sub_objects(collected_objs)
    related_models = collected_objs.keys()
    root_obj = None

    # Sometimes it's good enough just to save in reverse deletion order.
    if duplicate_order is None:
        duplicate_order = reversed(related_models)

    for model in duplicate_order:
        # Find all FKs on model that point to a related_model.
        fks = []
        for f in model._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to in related_models:
                fks.append(f)
        # Replace each `sub_obj` with a duplicate.
        if model not in collected_objs:
            continue
        sub_obj = collected_objs[model]
        for pk_val, obj in sub_obj.iteritems():
            for fk in fks:
                fk_value = getattr(obj, "%s_id" % fk.name)
                # If this FK has been duplicated then point to the duplicate.
                if fk_value in collected_objs[fk.rel.to]:
                    dupe_obj = collected_objs[fk.rel.to][fk_value]
                    setattr(obj, fk.name, dupe_obj)
            # Duplicate the object and save it.
            obj.id = None
            if field is not None and value is not None:
                setattr(obj, field, value)
            obj.save()
            if root_obj is None:
                root_obj = obj
    return root_obj

def discard_clipboard(clipboard):
    clipboard.files.clear()

def delete_clipboard(clipboard):
    for file in clipboard.files.all():
        file.delete()

def get_user_clipboard(user):
    if user.is_authenticated():
        clipboard, was_clipboard_created = Clipboard.objects.get_or_create(user=user)
        return clipboard

def move_file_to_clipboard(files, clipboard):
    for file in files:
        clipboard.append_file(file)
        file.folder = None
        file.save()
    return True

def copy_file_to_clipboard(files, clipboard):
    for file in files:
        clipboard.append_file(file, is_copy=True)
        file.save()
    return True

def clone_files_from_clipboard_to_folder(clipboard, folder):
    for file in clipboard.files.all():
        cloned_file = file.clone()
        cloned_file.folder = folder
        cloned_file.save()

def move_files_from_clipboard_to_folder(clipboard, folder):
    return move_files_to_folder(clipboard, folder)

def move_files_to_folder(clipboard, folder):
    for item in clipboard.clipboarditem_set.all():
        if item.is_copy:
            file = duplicate(item.file)
            print "duplicating!", item.file, "as", file
        else:
            file = item.file
        file.folder = folder
        file.save()
    return True
