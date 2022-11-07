""" generate html files """
import os
from packaging import version
from jinja2 import Environment, FileSystemLoader
from lxml import html
import requests
import i18n

env = Environment(loader=FileSystemLoader("templates/"), extensions=["jinja2.ext.i18n"])

env.install_gettext_translations(i18n)


def load_instances():
    """update the list of instances"""
    # pylint: disable=line-too-long
    instance_data = [
        {"path": "https://bookwyrm.social/"},
        {"path": "https://wyrms.de/"},
        {"path": "https://book.dansmonorage.blue/"},
        {"path": "https://yyyyy.club/"},
        {"path": "https://books.mxhdr.net/"},
        {"path": "https://ziurkes.group.lt/"},
        {"path": "https://kirja.casa/"},
        {"path": "https://books.solarpunk.moe/"},
        {"path": "https://masstoc.io/"},
        {"path": "https://velhaestante.com.br/"},
        {"path": "https://books.birdsonbicycles.racing/"},
        {"path": "https://books.theunseen.city/"},
        {"path": "https://bookrastinating.com/"},
        {"path": "https://bookwyrm.gatti.ninja/"},
    ]

    print("  Fetching instance statistics:")
    for instance in instance_data:
        instance_path = instance["path"]
        print(f"  - Fetching: {instance_path}")
        try:
            response = requests.get(f"{instance_path}api/v1/instance", timeout=15)
            data = response.json()
            version_number = data["version"]
            if version.parse(version_number) < version.parse("0.3.0"):
                raise Exception("Instance is out of date wiht version:", version_number)
            # pylint: disable=consider-using-f-string
            instance["users"] = "{:,}".format(data["stats"]["user_count"])
            instance["registration"] = (
                "open"
                if data["registrations"]
                else "invite"
                if data["approval_required"]
                else "closed"
            )
            description_text = data["short_description"] or ""
            if not description_text:
                description = data["description"]
                # pylint: disable=invalid-name
                for p in str(html.fromstring(description).text_content()).split("\n"):
                    description_text += f"<p>{p}</p>" if p else ""
                    if len(description_text) > 80:
                        break
            instance["description"] = description_text
            instance["logo"] = data["thumbnail"]
            instance["name"] = data["title"]
            instance["version"] = data["version"]
        except Exception as err:  # pylint: disable=broad-except
            print(f"    ! {err}")
            print("    - Site could possibly be down. Please check it manually:")
            print(f"    - Site url: {instance_path}")
            instance["skip"] = True
    return instance_data


if __name__ == "__main__":
    instances = load_instances()
    paths = [
        ["index.html", lambda: {}],
        ["instances/index.html", lambda: {"instances": instances}],
        ["get-involved/index.html", lambda: {}],
    ]

    for locale in i18n.locales_metadata:
        i18n.setLocale(locale["code"])

        LOCALIZED_SITE_PATH = "site/"
        if not locale["code"] == "en_US":
            LOCALIZED_SITE_PATH = f'site/{locale["slug"]}'

        for (path, data_loader) in paths:
            print("  Generating", f"{LOCALIZED_SITE_PATH}{path}")
            with open(f"templates/{path}", "r", encoding="utf-8") as template_file:
                template_string = template_file.read()
            template = env.from_string(template_string)

            localized_dirs = f"{LOCALIZED_SITE_PATH}{path}"
            localized_dirs = localized_dirs[: localized_dirs.rfind("/")]
            if not os.path.exists(localized_dirs):
                os.makedirs(localized_dirs)

            with open(
                f"{LOCALIZED_SITE_PATH}{path}", "w+", encoding="utf-8"
            ) as render_file:
                render_file.write(
                    template.render(
                        locale=locale,
                        locales_metadata=i18n.locales_metadata,
                        **data_loader(),
                    )
                )
