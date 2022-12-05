""" generate html files """
import os
import json
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
    with open("instances.json", "r", encoding="utf-8") as list_file:
        instance_urls = json.load(list_file)

    print("  Fetching instance statistics:")
    instance_data = []
    for instance_url in instance_urls:
        print(f"  - Fetching: {instance_url}")
        try:
            response = requests.get(f"{instance_url}api/v1/instance", timeout=10)
            data = response.json()
            version_number = data["version"]
            if version.parse(version_number) < version.parse("0.3.0"):
                raise Exception("Instance is out of date wiht version:", version_number)
            # pylint: disable=consider-using-f-string
            instance = {"path": instance_url}
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
            print(f"    - Site url: {instance_url}")
            instance = {"path": instance_url, "skip": True}
        instance_data.append(instance)
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
