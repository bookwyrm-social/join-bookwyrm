# Join Bookwyrm

Static page about the bookwyrm network

## Development

After installing the required packages in your environment (or virtual environment), run the command `./serve.sh` to serve the `site` directory with the Python HTTP local server. Then, every time you update the template files, run the command `./bw-dev site:compile` from another terminal.

### Translating the website

The translation system uses `gettext`, with `.PO` (source) and `.MO` (compiled) files.

Two commands are available for the translation. Both need a locale to work.

```shell
./bw-dev messages:generate <locale>
```

This command will extract the translation keys from the `.html` files stored in the `templates/` directory, and create or update the `.PO` file for the locale. The locale files are located into the `locale/` directory. You will need to and update that file with the right message translations.

```shell
./bw-dev messages:compile <locale>
```

This second command will compile the `.PO` file into the corresponding `.MO` file.
