# Conference data guide

The calendar uses [`conferences.yml`](conferences.yml) as its single source of truth. The generated Markdown, web page and ICS files should not be edited directly.

People who do not want to edit repository files can use the guided issue forms to [suggest a conference or event](https://github.com/Nordic-Accessibility-Community-Group/en-301-549-resources-and-eaa-monitoring/issues/new?template=conference-addition.yml) or [report a correction](https://github.com/Nordic-Accessibility-Community-Group/en-301-549-resources-and-eaa-monitoring/issues/new?template=conference-correction.yml).

## Add or update an event

1. Check the dates and details against the official event website.
2. Add or edit the entry in `conferences.yml`.
3. Use inclusive `start_date` and `end_date` values in `YYYY-MM-DD` format.
4. Keep the `id` stable after publication. Calendar applications use it to identify updates.
5. Increase `sequence` whenever a published event changes.
6. Set `last_verified` to the date on which the official source was checked.
7. Regenerate the published files.

For a cancellation, keep the event in the data, set `status` to `cancelled` and increase `sequence`. Removing it immediately could leave the old event in subscribers' calendars.

Allowed `format` values are `Hybrid`, `In person` and `Online`. Allowed `status` values are `confirmed`, `tentative` and `cancelled`.

## Generate the files

Install the generator dependency:

```sh
python3 -m pip install -r .github/scripts/requirements-conferences.txt
```

Generate the Markdown list, web page, complete calendar and individual event files:

```sh
python3 .github/scripts/generate_conferences.py
```

Check that committed output matches the data without changing files:

```sh
python3 .github/scripts/generate_conferences.py --check
```

The conference calendar workflow runs the same check on pull requests. After a change reaches `main`, it publishes the contents of `calendar/` through GitHub Pages.

## Enable publishing

GitHub Pages must be enabled once by a repository administrator, with **GitHub Actions** selected as the source. A pull request cannot change that repository setting. After it is enabled, the workflow publishes the landing page and subscription feed at the `public_url` configured in `conferences.yml`.
