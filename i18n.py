""" handle internationalization """
import os
import gettext as gettextlib
import threading

localedir = os.path.join(os.path.dirname(__file__), "locale")
domain = "messages"
thread_local_data = threading.local()
thread_local_data.locale = "en_US"

locales_metadata = [
    {"code": "en_US", "name": "English (US)", "slug": ""},
    {"code": "de_DE", "name": "Deutsch", "slug": "de/"},
    {"code": "es_ES", "name": "Español", "slug": "es/"},
    {"code": "gl_ES", "name": "Galego", "slug": "gl/"},
    {"code": "it_IT", "name": "Italiano", "slug": "it/"},
    {"code": "fr_FR", "name": "Français", "slug": "fr/"},
    {"code": "lt_LT", "name": "Lietuvių", "slug": "lt/"},
    {"code": "no_NO", "name": "Norsk", "slug": "no/"},
    {"code": "pt_PT", "name": "Português Europeu", "slug": "pt-pt/"},
    {"code": "pt_BR", "name": "Português do Brasil", "slug": "pt-br/"},
    {"code": "sv_SE", "name": "Svenska", "slug": "sv/"},
    {"code": "zh_Hans", "name": "简体中文", "slug": "zh/"},
]
default_locale = "en_US"

# find out all supported locales in locale directory
locales = []
for dirpath, dirnames, filenames in os.walk(localedir):
    for dirname in dirnames:
        locales.append(dirname)
    break

all_translations = {}
for locale_name in locales:
    all_translations[locale_name] = gettextlib.translation(
        domain, localedir, [locale_name]
    )


def gettext(message):
    """translate message based on current locale"""
    return all_translations[thread_local_data.locale].gettextlib(message)


def ngettext(singular, plural, n):
    """translation strings with plurals"""
    return all_translations[thread_local_data.locale].ngettext(singular, plural, n)


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
