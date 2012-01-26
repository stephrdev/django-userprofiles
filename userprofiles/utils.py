from django.db import models
from django.conf import settings
from userprofiles import settings as up_settings

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import SiteProfileNotAvailable

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def get_profile_model():
    if up_settings.USE_PROFILE:
        if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
            raise SiteProfileNotAvailable(
                'You need to set AUTH_PROFILE_MODULE in your project settings')

        try:
            app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        except ValueError:
            raise SiteProfileNotAvailable('app_label and model_name '
                'should be separated by a dot in the AUTH_PROFILE_MODULE '
                'setting')

        try:
            model = models.get_model(app_label, model_name)
            if model is None:
                raise SiteProfileNotAvailable('Unable to load the profile '
                    'model, check AUTH_PROFILE_MODULE in your project sett'
                    'ings')
            return model
        except (ImportError, ImproperlyConfigured):
            raise SiteProfileNotAvailable
    else:
        return None

UserProfile = get_profile_model()

def get_form_class(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error loading module %s: "%s"' % (module, e))
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a form named "%s"' % (module, attr))
    return form
