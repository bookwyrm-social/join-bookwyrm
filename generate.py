""" generate html files """
import os
from jinja2 import Environment, FileSystemLoader
from lxml import html
import requests
import i18n

env = Environment(
    loader=FileSystemLoader("templates/"),
    extensions=['jinja2.ext.i18n']
)

env.install_gettext_translations(i18n)

def load_instances():
    """update the list of instances"""
    # TODO: get this properly
    # pylint: disable=line-too-long
    instance_data = [
        {
            "path": "https://bookwyrm.social/",
            "logo": "https://bookwyrm-social.sfo3.digitaloceanspaces.com/static/images/logo.png",
        },
        {
            "path": "https://wyrms.de/",
            "logo": "https://wyrms.de/images/logos/wyrm_bright_300.png",
        },
        {
            "path": "https://cutebook.club/",
            "logo": "https://cutebook.club/images/logos/logo.png",
        },
        {
            "path": "https://book.dansmonorage.blue/",
            "logo": "https://book.dansmonorage.blue/images/logos/BC12B463-A984-4E92-8A30-BC2E9280A331_1.jpg",
        },
        {
            "path": "https://yyyyy.club/",
            "logo": "https://mastomedia.fra1.digitaloceanspaces.com/static/images/logo.png",
        },
        {
            "path": "https://books.mxhdr.net/",
            "logo": "https://books.mxhdr.net/images/logos/owl-g6a1cbbee3_1280.png",
        },
    ]

    print("  Fetching instance statistics:")
    for instance in instance_data:
        print("  - Fetching: %s" % instance["path"])
        try:
            response = requests.get(
                "{:s}api/v1/instance".format(instance["path"]),
                timeout=15
            )
            data = response.json()
            instance["users"] = "{:,}".format(data["stats"]["user_count"])
            instance["open_registration"] = data["registrations"] and not data["approval_required"]
            description_text = data["short_description"] or ''
            if not description_text:
                description = data["description"]
                for p in str(html.fromstring(description).text_content()).split("\n"):
                    description_text += f"<p>{p}</p>" if p else ''
                    if len(description_text) > 80:
                        break
            instance["description"] = description_text
            # right now there's a bug in how instances are serving logos on the api
            # page, so it's still hard-coded here
            instance["logo"] = instance.get("logo", data["thumbnail"])
            instance["name"] = data["title"]
        except Exception as e: # pylint: disable=broad-except
            print("    ! %s" % str(e))
            print("    - Site could possibly be down. Please check it manually:")
            print("    - Site url: %s" % instance["path"])
            instance["skip"] = True
    return instance_data


if __name__ == "__main__":
    instances = load_instances()
    paths = [
        ["index.html", lambda: {}],
        ["instances/index.html", lambda: {"instances": instances}],
    ]

    for locale in i18n.locales_metadata:
        i18n.setLocale(locale['code'])

        localized_site_path = "site/"
        if not locale['code'] == "en_US":
            localized_site_path = "site/%s" % locale['slug']

        for (path, data_loader) in paths:
            print("  Generating", "%s%s" % (localized_site_path, path))
            with open(f"templates/{path}", "r", encoding="utf-8") as template_file:
                template_string = template_file.read()
            template = env.from_string(template_string)

            localized_dirs = ("%s%s" % (localized_site_path, path))
            localized_dirs = localized_dirs[:localized_dirs.rfind("/")]
            if not os.path.exists(localized_dirs):
                os.makedirs(localized_dirs)

            with open(f"{localized_site_path}{path}", "w+", encoding="utf-8") \
                    as render_file:
                render_file.write(
                    template.render(
                        locale=locale,
                        locales_metadata=i18n.locales_metadata,
                        **data_loader(),
                    )
                )
