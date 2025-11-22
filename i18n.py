""" handle internationalization """
import os
import gettext as gettextlib
import threading

localedir = os.path.join(os.path.dirname(__file__), "locale")
DOMAIN = "messages"
thread_local_data = threading.local()
thread_local_data.locale = "en_US"

locales_metadata = [
    {"code": "en_US", "name": "English (US)", "slug": ""},
    {"code": "ca_ES", "name": "Català", "slug": "ca/"},
    {"code": "eo_UY", "name": "Esperanto", "slug": "eo/"},
    {"code": "de_DE", "name": "Deutsch", "slug": "de/"},
    {"code": "es_ES", "name": "Español", "slug": "es/"},
    {"code": "eu_ES", "name": "Euskara", "slug": "eu/"},
    {"code": "gl_ES", "name": "Galego", "slug": "gl/"},
    {"code": "it_IT", "name": "Italiano", "slug": "it/"},
    {"code": "fr_FR", "name": "Français", "slug": "fr/"},
    {"code": "lt_LT", "name": "Lietuvių", "slug": "lt/"},
    {"code": "no_NO", "name": "Norsk", "slug": "no/"},
    {"code": "pl_PL", "name": "Polski", "slug": "pl/"},
    {"code": "pt_PT", "name": "Português Europeu", "slug": "pt-pt/"},
    {"code": "pt_BR", "name": "Português do Brasil", "slug": "pt-br/"},
    {"code": "ro_RO", "name": "Română", "slug": "ro/"},
    {"code": "sv_SE", "name": "Svenska", "slug": "sv/"},
    {"code": "zh_Hans", "name": "简体中文", "slug": "zh/"},
]

default_locale = "en_US"  # pylint: disable=invalid-name

# find out all supported locales in locale directory
locales = []
for dirpath, dirnames, filenames in os.walk(localedir):
    for dirname in dirnames:
        locales.append(dirname)
    break

all_translations = {}
for locale_name in locales:
    try:
        all_translations[locale_name] = gettextlib.translation(
            DOMAIN, localedir, [locale_name]
        )
    except FileNotFoundError:
        print("Translate file not found for locale:", locale_name)


def gettext(message):
    """translate message based on current locale"""
    return all_translations[thread_local_data.locale].gettext(message)


# pylint: disable=invalid-name
def ngettext(singular, plural, n):
    """translation strings with plurals"""
    return all_translations[thread_local_data.locale].ngettext(singular, plural, n)


# pylint: disable=invalid-name
def setLocale(locale):
    """set thread data locale"""
    if locale in locales:
        thread_local_data.locale = locale


if __name__ == "__main__":
    # for test purpose
    for dirpath, dirnames, filenames in os.walk(localedir):
        for dirname in dirnames:
            print(dirname)
        break
