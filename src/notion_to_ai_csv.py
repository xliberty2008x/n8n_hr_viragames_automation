import argparse
import csv
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from dotenv import load_dotenv


NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


@dataclass
class PageData:
    page_id: str
    url: str
    title: str
    last_edited_time: Optional[str]
    properties: Dict[str, Any]
    content_text: str


def load_config(env_path: str = "config/config.env", require_openai: bool = True) -> Tuple[str, Optional[str]]:
    load_dotenv(env_path)
    notion_token = os.getenv("NOTION_API")
    openai_key = os.getenv("OPEN_API_KEY")
    if not notion_token:
        raise RuntimeError("NOTION_API is not set in config/config.env")
    if require_openai and not openai_key:
        raise RuntimeError("OPEN_API_KEY is not set in config/config.env")
    return notion_token, openai_key


def extract_database_id(database_url_or_id: str) -> str:
    candidate = database_url_or_id.strip()
    # If it's a URL, pull the 32-hex ID segment
    if candidate.startswith("http://") or candidate.startswith("https://"):
        # Notion URLs often contain a 32-hex id either in path before ?v= or as a trailing segment
        m = re.search(r"([0-9a-fA-F]{32})", candidate)
        if not m:
            # Try dashed UUID
            m2 = re.search(r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})", candidate)
            if not m2:
                raise ValueError("Unable to extract database ID from URL")
            raw = m2.group(1).replace("-", "")
        else:
            raw = m.group(1)
    else:
        raw = re.sub(r"[^0-9a-fA-F]", "", candidate)
        if len(raw) not in (32,):
            # Maybe it's already dashed UUID
            dashed = re.match(r"^[0-9a-fA-F\-]{36}$", candidate)
            if dashed:
                raw = candidate.replace("-", "")
            else:
                raise ValueError("Invalid Notion database ID")

    # Insert dashes 8-4-4-4-12
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"


def notion_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def query_database_all(token: str, database_id: str) -> Iterable[Dict[str, Any]]:
    url = f"{NOTION_API_BASE}/databases/{database_id}/query"
    payload: Dict[str, Any] = {"page_size": 100}
    while True:
        resp = requests.post(url, headers=notion_headers(token), data=json.dumps(payload))
        resp.raise_for_status()
        data = resp.json()
        for result in data.get("results", []):
            yield result
        next_cursor = data.get("next_cursor")
        has_more = data.get("has_more")
        if not has_more or not next_cursor:
            break
        payload["start_cursor"] = next_cursor


def get_block_children_all(token: str, block_id: str) -> List[Dict[str, Any]]:
    children: List[Dict[str, Any]] = []
    url = f"{NOTION_API_BASE}/blocks/{block_id}/children"
    params = {"page_size": 100}
    while True:
        resp = requests.get(url, headers=notion_headers(token), params=params)
        resp.raise_for_status()
        data = resp.json()
        children.extend(data.get("results", []))
        next_cursor = data.get("next_cursor")
        has_more = data.get("has_more")
        if not has_more or not next_cursor:
            break
        params["start_cursor"] = next_cursor
    return children


def rich_text_to_plain(rich_text: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    for r in rich_text or []:
        text = r.get("plain_text")
        if text:
            parts.append(text)
    return "".join(parts)


def block_to_text_lines(block: Dict[str, Any], token: str, depth: int = 0) -> List[str]:
    indent = "  " * depth
    lines: List[str] = []
    block_type = block.get("type")
    obj = block.get(block_type, {}) if isinstance(block.get(block_type), dict) else {}

    # Extract main line
    if "rich_text" in obj:
        text = rich_text_to_plain(obj.get("rich_text", []))
        if text:
            lines.append(f"{indent}{text}")
    elif block_type in ("heading_1", "heading_2", "heading_3") and "rich_text" in obj:
        text = rich_text_to_plain(obj.get("rich_text", []))
        if text:
            lines.append(f"{indent}{text}")

    # Append special content types
    if block_type == "to_do" and obj.get("rich_text"):
        text = rich_text_to_plain(obj.get("rich_text", []))
        checked = obj.get("checked")
        prefix = "[x]" if checked else "[ ]"
        lines.append(f"{indent}{prefix} {text}")

    if block.get("has_children"):
        # Fetch children of this block and recurse
        child_blocks = get_block_children_all(token, block.get("id"))
        for cb in child_blocks:
            lines.extend(block_to_text_lines(cb, token, depth=depth + 1))

    return lines


def parse_property_value(prop: Dict[str, Any]) -> Any:
    p_type = prop.get("type")
    val = prop.get(p_type)
    if p_type == "title":
        return rich_text_to_plain(val or [])
    if p_type == "rich_text":
        return rich_text_to_plain(val or [])
    if p_type == "select":
        return (val or {}).get("name") if val else None
    if p_type == "multi_select":
        return [v.get("name") for v in (val or [])]
    if p_type == "date":
        if not val:
            return None
        return {"start": val.get("start"), "end": val.get("end"), "time_zone": val.get("time_zone")}
    if p_type == "people":
        return [p.get("name") or p.get("person", {}).get("email") for p in (val or [])]
    if p_type == "email":
        return val
    if p_type == "url":
        return val
    if p_type == "checkbox":
        return bool(val)
    if p_type == "number":
        return val
    if p_type == "files":
        return [f.get("name") for f in (val or [])]
    if p_type == "relation":
        return [r.get("id") for r in (val or [])]
    if p_type == "created_by":
        return (val or {}).get("name")
    if p_type == "created_time":
        return val
    if p_type == "last_edited_by":
        return (val or {}).get("name")
    if p_type == "last_edited_time":
        return val
    return val


def assemble_page(token: str, page_obj: Dict[str, Any]) -> PageData:
    page_id = page_obj.get("id")
    url = page_obj.get("url")
    last_edited_time = page_obj.get("last_edited_time")
    properties_obj = page_obj.get("properties", {})

    properties: Dict[str, Any] = {}
    title = "Untitled"
    for name, p in properties_obj.items():
        parsed = parse_property_value(p)
        properties[name] = parsed
        if p.get("type") == "title":
            maybe_title = parsed or "Untitled"
            if isinstance(maybe_title, str) and maybe_title.strip():
                title = maybe_title.strip()

    # Pull content text from child blocks
    lines: List[str] = []
    for line in block_to_text_lines({"id": page_id, "type": "page", "has_children": True}, token):
        lines.append(line)
    content_text = "\n".join([l for l in lines if l])

    return PageData(
        page_id=page_id,
        url=url,
        title=title,
        last_edited_time=last_edited_time,
        properties=properties,
        content_text=content_text,
    )


def call_openai_for_summary(openai_key: str, page: PageData, model: str = "gpt-4o", max_retries: int = 3, retry_delay: float = 2.0) -> Dict[str, Any]:
    # Lazy import to avoid dependency unless used
    from openai import OpenAI

    client = OpenAI(api_key=openai_key)
    system_prompt = (
        "You are a senior project management assistant. Analyze a Notion task object "
        "containing properties and extracted page content and return a STRICT JSON object only, "
        "no prose. Required keys: task_name, status, assignee, responsible, priority, team, "
        "dates {start, due, end}, achievement_summary (2-3 sentences), key_points (array of 3-7 bullets), "
        "completion_status (integer 0-100), next_steps (one short sentence). Rules: 1) Prefer explicit property "
        "values over guesses; 2) If a value is missing use empty string or [] (not null); 3) Map emails or names from "
        "assignee/responsible arrays to string (single value if one, else join by '; '); 4) Derive summary ONLY from "
        "description/content; 5) Do not include markdown or code fences; 6) Ensure valid JSON."
    )

    user_payload = {
        "id": page.page_id,
        "url": page.url,
        "title": page.title,
        "last_edited_time": page.last_edited_time,
        "properties": page.properties,
        "content": page.content_text,
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Try to salvage JSON
                m = re.search(r"\{[\s\S]*\}", content)
                if m:
                    return json.loads(m.group(0))
                raise
        except Exception as e:  # noqa: BLE001
            if attempt >= max_retries:
                return {"error": str(e)}
            time.sleep(retry_delay * attempt)


def flatten_summary_for_csv(summary: Dict[str, Any], page: PageData) -> Dict[str, Any]:
    dates = summary.get("dates") or {}
    to_str = lambda v: v if isinstance(v, str) else (
        "; ".join(v) if isinstance(v, list) else ("" if v is None else str(v))
    )
    return {
        "Task Name": summary.get("task_name") or page.title or "Untitled",
        "Status": to_str(summary.get("status", "")),
        "Assignee": to_str(summary.get("assignee", "")),
        "Responsible": to_str(summary.get("responsible", "")),
        "Priority": to_str(summary.get("priority", "")),
        "Team": to_str(summary.get("team", "")),
        "Start Date": to_str(dates.get("start", "")),
        "Due Date": to_str(dates.get("due", "")),
        "End Date": to_str(dates.get("end", "")),
        "Achievement Summary": to_str(summary.get("achievement_summary", "")),
        "Key Points": to_str(summary.get("key_points", [])),
        "Completion %": summary.get("completion_status", ""),
        "Next Steps": to_str(summary.get("next_steps", "")),
        "URL": page.url,
        "Last Edited": page.last_edited_time or "",
        "Page ID": page.page_id,
    }


def write_csv(rows: List[Dict[str, Any]], out_path: str) -> None:
    if not rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            pass
        return
    # Build union of all keys to ensure we don't drop columns across items
    seen: OrderedDict[str, None] = OrderedDict()
    for row in rows:
        for k in row.keys():
            if k not in seen:
                seen[k] = None
    fieldnames = list(seen.keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def flatten_page_for_csv(page: PageData) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "Page ID": page.page_id,
        "URL": page.url,
        "Title": page.title,
        "Last Edited": page.last_edited_time or "",
        "Content": page.content_text,
    }

    for name, value in page.properties.items():
        if isinstance(value, dict) and set(value.keys()) & {"start", "end", "time_zone"}:
            # Date-like
            row[f"{name} Start"] = value.get("start", "")
            row[f"{name} End"] = value.get("end", "")
            if value.get("time_zone"):
                row[f"{name} Time Zone"] = value.get("time_zone", "")
            continue
        if isinstance(value, list):
            row[name] = "; ".join([str(v) for v in value])
            continue
        row[name] = "" if value is None else str(value)
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Notion DB pages to CSV (with optional AI summaries)")
    parser.add_argument("database", help="Notion database URL or ID")
    parser.add_argument("--out", dest="out", default="notion_task_summaries.csv", help="Output CSV path")
    parser.add_argument("--model", dest="model", default="gpt-4o", help="OpenAI model (default: gpt-4o)")
    parser.add_argument("--sleep", dest="sleep", type=float, default=0.0, help="Sleep seconds between pages")
    parser.add_argument("--no-ai", dest="no_ai", action="store_true", help="Do not call AI, just assemble properties + content to CSV")

    args = parser.parse_args()

    try:
        notion_token, openai_key = load_config(require_openai=not args.no_ai)
    except Exception as e:  # noqa: BLE001
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        database_id = extract_database_id(args.database)
    except Exception as e:  # noqa: BLE001
        print(f"Invalid database input: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Querying Notion database: {database_id}")
    pages_raw = list(query_database_all(notion_token, database_id))
    print(f"Found {len(pages_raw)} pages")

    pages: List[PageData] = []
    for i, p in enumerate(pages_raw, start=1):
        try:
            page = assemble_page(notion_token, p)
            pages.append(page)
        except Exception as e:  # noqa: BLE001
            print(f"Failed assembling page {p.get('id')}: {e}", file=sys.stderr)
        if args.sleep:
            time.sleep(args.sleep)

    rows: List[Dict[str, Any]] = []
    if args.no_ai:
        print("Assembling pages without AI...")
        for idx, page in enumerate(pages, start=1):
            print(f"[{idx}/{len(pages)}] {page.title}")
            rows.append(flatten_page_for_csv(page))
            if args.sleep:
                time.sleep(args.sleep)
    else:
        print("Calling OpenAI for summaries...")
        for idx, page in enumerate(pages, start=1):
            print(f"[{idx}/{len(pages)}] {page.title}")
            summary = call_openai_for_summary(openai_key, page, model=args.model)
            row = flatten_summary_for_csv(summary, page)
            rows.append(row)
            if args.sleep:
                time.sleep(args.sleep)

    write_csv(rows, args.out)
    print(f"Wrote CSV: {args.out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()


