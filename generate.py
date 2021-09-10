""" generate html files """
import os
import requests
from jinja2 import Environment, FileSystemLoader
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
            "contact_name": "@tripofmice@friend.camp",
            "contact_link": "https://friend.camp/@tripofmice",
            "description": "Flagship instance, general purpose",
        },
        {
            "path": "https://wyrms.de/",
            "logo": "https://wyrms.de/images/logos/wyrm_bright_300.png",
            "contact_name": "@tofuwabohu@subversive.zone",
            "contact_link": "https://subversive.zone/@tofuwabohu",
            "description": "The Dispossessed (Le Guin) and everything else",
        },
        {
            "path": "https://cutebook.club/",
            "logo": "https://cutebook.club/images/logos/logo.png",
            "contact_name": "@allie@tech.lgbt",
            "contact_link": "https://tech.lgbt/@allie",
            "description": "General purpose",
        },
        {
            "path": "https://book.dansmonorage.blue/",
            "logo": "https://book.dansmonorage.blue/images/logos/BC12B463-A984-4E92-8A30-BC2E9280A331_1.jpg",
            "contact_name": "@faketaoist@mstd.dansmonorage.blue",
            "contact_link": "https://mstd.dansmonorage.blue/@faketaoist",
            "description": "General purpose",
        },
        {
            "path": "https://yyyyy.club/",
            "logo": "https://mastomedia.fra1.digitaloceanspaces.com/static/images/logo.png",
            "contact_name": "yyyyyadmin@protonmail.com",
            "contact_link": "mailto:yyyyyadmin@protonmail.com",
            "description": "General purpose",
        }
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
            instance["users"] = data["stats"]["user_count"]
            instance["open_registration"] = data["registrations"] and not data["approval_required"]
            instance["description"] = data["short_description"] or instance["description"]
            # right now there's a bug in how instances are serving logos on the api
            # page, so it's still hard-coded here
            instance["logo"] = instance["logo"] or data["thumbnail"]
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
            template_string = open(f"templates/{path}", "r").read()
            template = env.from_string(template_string)

            localized_dirs = ("%s%s" % (localized_site_path, path))
            localized_dirs = localized_dirs[:localized_dirs.rfind("/")]
            if not os.path.exists(localized_dirs):
                os.makedirs(localized_dirs)

            with open(f"{localized_site_path}{path}", "w+") as render_file:
                render_file.write(
                    template.render(
                        locale=locale,
                        locales_metadata=i18n.locales_metadata,
                        **data_loader(),
                    )
                )
