#!/usr/bin/env python3
"""Generate the human-readable conference list, calendar feed and web page."""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "conferences.yml"
MARKDOWN_FILE = ROOT / "conferences.md"
CALENDAR_DIRECTORY = ROOT / "calendar"
FEED_FILE = CALENDAR_DIRECTORY / "conferences.ics"
PAGE_FILE = CALENDAR_DIRECTORY / "index.html"
EVENT_DIRECTORY = CALENDAR_DIRECTORY / "events"

REPOSITORY_URL = (
    "https://github.com/Nordic-Accessibility-Community-Group/"
    "en-301-549-resources-and-eaa-monitoring"
)
ADDITION_FORM_URL = f"{REPOSITORY_URL}/issues/new?template=conference-addition.yml"
CORRECTION_FORM_URL = f"{REPOSITORY_URL}/issues/new?template=conference-correction.yml"
UID_DOMAIN = "nordic-accessibility-community-group.github.io"

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FORMATS = {"Hybrid", "In person", "Online"}
ALLOWED_STATUSES = {"cancelled", "confirmed", "tentative"}
REQUIRED_EVENT_FIELDS = {
    "description",
    "end_date",
    "format",
    "id",
    "last_verified",
    "location",
    "name",
    "sequence",
    "start_date",
    "status",
    "url",
}
OPTIONAL_EVENT_FIELDS = {"language", "organizer"}


class DataError(ValueError):
    """Raised when conference source data is invalid."""


@dataclass(frozen=True)
class CalendarDetails:
    name: str
    description: str
    public_url: str

    @property
    def feed_url(self) -> str:
        return f"{self.public_url}conferences.ics"

    @property
    def webcal_url(self) -> str:
        return self.feed_url.replace("https://", "webcal://", 1)


@dataclass(frozen=True)
class Conference:
    id: str
    name: str
    start_date: date
    end_date: date
    location: str
    format: str
    url: str
    description: str
    status: str
    sequence: int
    last_verified: date
    language: str | None = None
    organizer: str | None = None

    @property
    def event_feed_url(self) -> str:
        return f"events/{self.id}.ics"


def require_non_empty_string(value: object, field: str, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DataError(f"{context}: {field} must be a non-empty string")
    return value.strip()


def parse_iso_date(value: object, field: str, context: str) -> date:
    text = require_non_empty_string(value, field, context)
    try:
        return date.fromisoformat(text)
    except ValueError as error:
        raise DataError(f"{context}: {field} must use YYYY-MM-DD") from error


def validate_https_url(value: object, field: str, context: str) -> str:
    text = require_non_empty_string(value, field, context)
    parsed = urlparse(text)
    if parsed.scheme != "https" or not parsed.netloc:
        raise DataError(f"{context}: {field} must be an absolute HTTPS URL")
    return text


def load_data(path: Path = DATA_FILE) -> tuple[CalendarDetails, list[Conference]]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise DataError(f"Could not read {path}: {error}") from error

    if not isinstance(raw, dict):
        raise DataError("The data file must contain a mapping")

    calendar_raw = raw.get("calendar")
    if not isinstance(calendar_raw, dict):
        raise DataError("calendar must be a mapping")

    calendar_context = "calendar"
    calendar = CalendarDetails(
        name=require_non_empty_string(
            calendar_raw.get("name"), "name", calendar_context
        ),
        description=require_non_empty_string(
            calendar_raw.get("description"), "description", calendar_context
        ),
        public_url=validate_https_url(
            calendar_raw.get("public_url"), "public_url", calendar_context
        ).rstrip("/")
        + "/",
    )

    events_raw = raw.get("conferences")
    if not isinstance(events_raw, list):
        raise DataError("conferences must be a list")

    conferences: list[Conference] = []
    seen_ids: set[str] = set()
    for index, event_raw in enumerate(events_raw, start=1):
        context = f"conference #{index}"
        if not isinstance(event_raw, dict):
            raise DataError(f"{context} must be a mapping")

        fields = set(event_raw)
        missing = REQUIRED_EVENT_FIELDS - fields
        unknown = fields - REQUIRED_EVENT_FIELDS - OPTIONAL_EVENT_FIELDS
        if missing:
            raise DataError(f"{context} is missing: {', '.join(sorted(missing))}")
        if unknown:
            raise DataError(
                f"{context} has unknown fields: {', '.join(sorted(unknown))}"
            )

        event_id = require_non_empty_string(event_raw["id"], "id", context)
        context = f"conference {event_id!r}"
        if not ID_PATTERN.fullmatch(event_id):
            raise DataError(
                f"{context}: id must contain lowercase letters, numbers and hyphens"
            )
        if event_id in seen_ids:
            raise DataError(f"{context}: duplicate id")
        seen_ids.add(event_id)

        start_date = parse_iso_date(event_raw["start_date"], "start_date", context)
        end_date = parse_iso_date(event_raw["end_date"], "end_date", context)
        if end_date < start_date:
            raise DataError(f"{context}: end_date cannot be before start_date")

        event_format = require_non_empty_string(event_raw["format"], "format", context)
        if event_format not in ALLOWED_FORMATS:
            allowed = ", ".join(sorted(ALLOWED_FORMATS))
            raise DataError(f"{context}: format must be one of {allowed}")

        status = require_non_empty_string(
            event_raw["status"], "status", context
        ).lower()
        if status not in ALLOWED_STATUSES:
            allowed = ", ".join(sorted(ALLOWED_STATUSES))
            raise DataError(f"{context}: status must be one of {allowed}")

        sequence = event_raw["sequence"]
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            raise DataError(f"{context}: sequence must be a non-negative integer")

        optional_values: dict[str, str | None] = {}
        for field in OPTIONAL_EVENT_FIELDS:
            value = event_raw.get(field)
            optional_values[field] = (
                require_non_empty_string(value, field, context)
                if value is not None
                else None
            )

        conferences.append(
            Conference(
                id=event_id,
                name=require_non_empty_string(event_raw["name"], "name", context),
                start_date=start_date,
                end_date=end_date,
                location=require_non_empty_string(
                    event_raw["location"], "location", context
                ),
                format=event_format,
                url=validate_https_url(event_raw["url"], "url", context),
                description=require_non_empty_string(
                    event_raw["description"], "description", context
                ),
                status=status,
                sequence=sequence,
                last_verified=parse_iso_date(
                    event_raw["last_verified"], "last_verified", context
                ),
                language=optional_values["language"],
                organizer=optional_values["organizer"],
            )
        )

    return calendar, sorted(
        conferences, key=lambda event: (event.start_date, event.name.casefold())
    )


def format_date_range(start: date, end: date) -> str:
    if start == end:
        return f"{start.day} {start.strftime('%B')} {start.year}"
    if start.year == end.year and start.month == end.month:
        return f"{start.day}–{end.day} {start.strftime('%B')} {start.year}"
    if start.year == end.year:
        return (
            f"{start.day} {start.strftime('%B')} – "
            f"{end.day} {end.strftime('%B')} {start.year}"
        )
    return (
        f"{start.day} {start.strftime('%B')} {start.year} – "
        f"{end.day} {end.strftime('%B')} {end.year}"
    )


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def event_display_name(event: Conference) -> str:
    linked_name = f"[{markdown_escape(event.name)}]({event.url})"
    if event.status == "cancelled":
        return f"~~{linked_name}~~ (cancelled)"
    if event.status == "tentative":
        return f"{linked_name} (tentative)"
    return linked_name


def render_markdown(calendar: CalendarDetails, conferences: list[Conference]) -> str:
    rows = []
    for event in conferences:
        rows.append(
            "| "
            + " | ".join(
                [
                    format_date_range(event.start_date, event.end_date),
                    event_display_name(event),
                    markdown_escape(event.format),
                    markdown_escape(event.location),
                    markdown_escape(event.language or "Not specified"),
                    f"[Add]({CALENDAR_DIRECTORY.name}/{event.event_feed_url})",
                ]
            )
            + " |"
        )

    if not rows:
        rows.append("| No events listed |  |  |  |  |  |")

    return "\n".join(
        [
            "<!-- Generated by .github/scripts/generate_conferences.py. Edit data/conferences.yml instead. -->",
            "",
            "# Accessibility conferences and events",
            "",
            (
                "This table and its calendar files are generated from "
                "[`data/conferences.yml`](data/conferences.yml)."
            ),
            "",
            "## Subscribe to the calendar",
            "",
            f"- [Open the calendar page to subscribe]({calendar.public_url})",
            f"- [Download the complete ICS calendar]({calendar.feed_url})",
            f"- Subscription URL: `{calendar.feed_url}`",
            "",
            (
                "Calendar applications decide how frequently subscriptions are refreshed. "
                "The individual Add links below are one-time downloads and do not receive "
                "later updates."
            ),
            "",
            "## Events",
            "",
            "| Date | Event | Format | Location | Language | Calendar |",
            "| --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
            "## Suggest an event or correction",
            "",
            (
                "You do not need to edit repository files. Use the guided issue forms to "
                "[suggest a conference or event]"
                f"({ADDITION_FORM_URL}) or [report a correction]({CORRECTION_FORM_URL}). "
                "Maintainers will review the official source before changing the calendar."
            ),
            "",
            (
                "Technical contributors can read "
                "[the conference data guide](data/README.md) before opening a pull request."
            ),
            "",
        ]
    )


def ics_escape(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
    )


def fold_ics_line(line: str) -> str:
    """Fold an iCalendar content line at 75 UTF-8 octets."""
    chunks: list[str] = []
    current = ""
    byte_limit = 75
    for character in line:
        candidate = current + character
        if current and len(candidate.encode("utf-8")) > byte_limit:
            chunks.append(current)
            current = character
            byte_limit = 74
        else:
            current = candidate
    chunks.append(current)
    return "\r\n ".join(chunks)


def ics_timestamp(value: date) -> str:
    timestamp = datetime.combine(value, datetime.min.time(), tzinfo=timezone.utc)
    return timestamp.strftime("%Y%m%dT%H%M%SZ")


def event_ics_lines(event: Conference) -> list[str]:
    description_parts = [event.description]
    if event.organizer:
        description_parts.append(f"Organizer: {event.organizer}")
    if event.language:
        description_parts.append(f"Language: {event.language}")

    return [
        "BEGIN:VEVENT",
        f"UID:{event.id}@{UID_DOMAIN}",
        f"DTSTAMP:{ics_timestamp(event.last_verified)}",
        f"LAST-MODIFIED:{ics_timestamp(event.last_verified)}",
        f"SEQUENCE:{event.sequence}",
        f"DTSTART;VALUE=DATE:{event.start_date.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{(event.end_date + timedelta(days=1)).strftime('%Y%m%d')}",
        f"SUMMARY:{ics_escape(event.name)}",
        f"DESCRIPTION:{ics_escape(chr(10).join(description_parts))}",
        f"LOCATION:{ics_escape(event.location)}",
        f"URL:{event.url}",
        f"STATUS:{event.status.upper()}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT",
    ]


def render_ics(calendar: CalendarDetails, conferences: list[Conference]) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Nordic Accessibility Community Group//Conference Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{ics_escape(calendar.name)}",
        f"X-WR-CALDESC:{ics_escape(calendar.description)}",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
        "X-PUBLISHED-TTL:PT12H",
    ]
    for event in conferences:
        lines.extend(event_ics_lines(event))
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold_ics_line(line) for line in lines) + "\r\n"


def html_event_name(event: Conference) -> str:
    name = html.escape(event.name)
    if event.status == "cancelled":
        name = f'<s>{name}</s> <span class="status">Cancelled</span>'
    elif event.status == "tentative":
        name = f'{name} <span class="status">Tentative</span>'
    return name


def render_html(calendar: CalendarDetails, conferences: list[Conference]) -> str:
    rows = []
    for event in conferences:
        language = html.escape(event.language or "Not specified")
        rows.append(
            f"""          <tr>
            <td><time datetime="{event.start_date.isoformat()}">{html.escape(format_date_range(event.start_date, event.end_date))}</time></td>
            <td>
              <a href="{html.escape(event.url, quote=True)}">{html_event_name(event)}</a>
              <p>{html.escape(event.description)}</p>
            </td>
            <td>{html.escape(event.format)}</td>
            <td>{html.escape(event.location)}</td>
            <td>{language}</td>
            <td><a href="{html.escape(event.event_feed_url, quote=True)}">Add event</a></td>
          </tr>"""
        )

    if not rows:
        rows.append(
            '          <tr><td colspan="6">No events are currently listed.</td></tr>'
        )

    calendar_name = html.escape(calendar.name)
    calendar_description = html.escape(calendar.description)
    feed_url = html.escape(calendar.feed_url, quote=True)
    webcal_url = html.escape(calendar.webcal_url, quote=True)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{calendar_description}">
  <title>{calendar_name}</title>
  <style>
    :root {{
      color-scheme: light dark;
      --background: #f7f6f1;
      --surface: #ffffff;
      --text: #17221d;
      --muted: #4b5b53;
      --accent: #075c46;
      --accent-hover: #043f30;
      --border: #cbd4cf;
      --focus: #ffbf47;
      --radius: 0.75rem;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--background);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 1rem;
      line-height: 1.6;
    }}

    a {{ color: var(--accent); text-underline-offset: 0.18em; }}
    a:hover {{ color: var(--accent-hover); }}
    a:focus-visible, input:focus-visible {{ outline: 0.25rem solid var(--focus); outline-offset: 0.2rem; }}

    header, main, footer {{ width: min(76rem, calc(100% - 2rem)); margin-inline: auto; }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding-block: 1.25rem;
    }}

    header a {{ font-weight: 700; }}

    main {{ padding-block: clamp(2rem, 6vw, 5rem); }}
    h1 {{ max-width: 18ch; margin: 0; font-size: clamp(2.4rem, 7vw, 5rem); line-height: 1.02; letter-spacing: -0.035em; }}
    h2 {{ margin-top: 0; font-size: clamp(1.6rem, 4vw, 2.2rem); line-height: 1.15; }}
    .intro {{ max-width: 48rem; margin: 1.5rem 0 3rem; color: var(--muted); font-size: 1.2rem; }}

    section {{ margin-block: 3rem; }}
    .panel {{ padding: clamp(1.25rem, 4vw, 2rem); border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin-block: 1.5rem; }}
    .button {{
      display: inline-block;
      padding: 0.7rem 1rem;
      border: 2px solid var(--accent);
      border-radius: 0.4rem;
      font-weight: 700;
      text-decoration: none;
    }}
    .button.primary {{ background: var(--accent); color: #ffffff; }}
    .button.primary:hover {{ background: var(--accent-hover); border-color: var(--accent-hover); color: #ffffff; }}

    label {{ display: block; margin-bottom: 0.35rem; font-weight: 700; }}
    input {{
      width: 100%;
      padding: 0.7rem;
      border: 1px solid var(--border);
      border-radius: 0.3rem;
      background: var(--background);
      color: var(--text);
      font: inherit;
    }}

    .table-wrap {{ overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 1rem; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }}
    th {{ background: color-mix(in srgb, var(--surface), var(--accent) 8%); }}
    td p {{ min-width: 18rem; margin: 0.35rem 0 0; color: var(--muted); }}
    tr:last-child td {{ border-bottom: 0; }}
    .status {{ display: inline-block; margin-left: 0.35rem; font-size: 0.9rem; font-weight: 700; }}

    footer {{ padding-block: 2rem; border-top: 1px solid var(--border); color: var(--muted); }}

    @media (max-width: 40rem) {{
      header {{ align-items: flex-start; flex-direction: column; }}
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --background: #111814;
        --surface: #18231d;
        --text: #f2f6f3;
        --muted: #c2cec7;
        --accent: #7ee0bd;
        --accent-hover: #a3efd3;
        --border: #42564b;
      }}
      .button.primary {{ color: #102019; }}
      .button.primary:hover {{ color: #102019; }}
    }}
  </style>
</head>
<body>
  <header>
    <a href="{REPOSITORY_URL}">Nordic Accessibility Community Group</a>
    <a href="{REPOSITORY_URL}/blob/main/conferences.md">View on GitHub</a>
  </header>
  <main>
    <h1>Accessibility conferences and events</h1>
    <p class="intro">{calendar_description}</p>

    <section class="panel" aria-labelledby="subscribe-heading">
      <h2 id="subscribe-heading">Subscribe to the calendar</h2>
      <p>Subscribe once to receive additions, corrections and cancellations when your calendar application refreshes the feed.</p>
      <div class="actions">
        <a class="button primary" href="{webcal_url}">Subscribe in a calendar app</a>
        <a class="button" href="{feed_url}" download>Download complete ICS calendar</a>
      </div>
      <label for="subscription-url">Subscription URL</label>
      <input id="subscription-url" type="url" readonly value="{feed_url}" onclick="this.select()">
      <p>For Google Calendar, copy the subscription URL and add it using <strong>Other calendars</strong>, then <strong>From URL</strong>. Calendar applications control how frequently subscriptions refresh.</p>
    </section>

    <section aria-labelledby="events-heading">
      <h2 id="events-heading">Events</h2>
      <div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable conference table">
        <table>
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Event</th>
              <th scope="col">Format</th>
              <th scope="col">Location</th>
              <th scope="col">Language</th>
              <th scope="col">Calendar</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel" aria-labelledby="suggest-heading">
      <h2 id="suggest-heading">Suggest an event or correction</h2>
      <p>You do not need to know Git or edit data files. A guided form collects the information maintainers need to review the official source.</p>
      <div class="actions">
        <a class="button primary" href="{ADDITION_FORM_URL}">Suggest an event</a>
        <a class="button" href="{CORRECTION_FORM_URL}">Report a correction</a>
      </div>
    </section>
  </main>
  <footer>
    <p>Calendar data is maintained in the <a href="{REPOSITORY_URL}">EN 301 549 resources and EAA monitoring repository</a>.</p>
  </footer>
</body>
</html>
"""


def expected_outputs(
    calendar: CalendarDetails, conferences: list[Conference]
) -> dict[Path, str]:
    outputs = {
        MARKDOWN_FILE: render_markdown(calendar, conferences),
        FEED_FILE: render_ics(calendar, conferences),
        PAGE_FILE: render_html(calendar, conferences),
    }
    for event in conferences:
        outputs[EVENT_DIRECTORY / f"{event.id}.ics"] = render_ics(calendar, [event])
    return outputs


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="")

    expected_event_files = {path for path in outputs if path.parent == EVENT_DIRECTORY}
    if EVENT_DIRECTORY.exists():
        for path in EVENT_DIRECTORY.glob("*.ics"):
            if path not in expected_event_files:
                path.unlink()


def check_outputs(outputs: dict[Path, str]) -> list[Path]:
    stale: list[Path] = []
    for path, expected in outputs.items():
        try:
            with path.open("r", encoding="utf-8", newline="") as generated_file:
                actual = generated_file.read()
        except OSError:
            stale.append(path)
            continue
        if actual != expected:
            stale.append(path)

    expected_event_files = {path for path in outputs if path.parent == EVENT_DIRECTORY}
    if EVENT_DIRECTORY.exists():
        stale.extend(
            path
            for path in EVENT_DIRECTORY.glob("*.ics")
            if path not in expected_event_files
        )
    return sorted(set(stale))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated files do not match the conference data",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        calendar, conferences = load_data()
    except DataError as error:
        print(f"Conference data error: {error}", file=sys.stderr)
        return 1

    outputs = expected_outputs(calendar, conferences)
    if arguments.check:
        stale = check_outputs(outputs)
        if stale:
            print("Generated conference files are out of date:", file=sys.stderr)
            for path in stale:
                print(f"- {path.relative_to(ROOT)}", file=sys.stderr)
            print(
                "Run python3 .github/scripts/generate_conferences.py and commit the results.",
                file=sys.stderr,
            )
            return 1
        print(f"Conference data and {len(outputs)} generated files are up to date.")
        return 0

    write_outputs(outputs)
    print(f"Generated {len(outputs)} files for {len(conferences)} conferences.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
