#!/usr/bin/env python3
"""
Automation script to parse call center metrics from data.txt
and update the embedded dashboard data inside index.html.

Usage:
    python3 update_dashboard.py
"""

import os
import re
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'data.txt')
HTML_FILE = os.path.join(SCRIPT_DIR, 'index.html')

def parse_data(text):
    days = []
    current_day = None
    current_section = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # Match date header like *18/11/26* or *18.11.26* or *18-11-2026*
        m_date = re.match(r'^\*(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})\*$', line)
        if m_date:
            current_day = {
                'date': m_date.group(1),
                'metrics': {},
                'bookings': []
            }
            days.append(current_day)
            current_section = None
            continue

        # Match section header like *MRI SCAN*, *CONFIRMED MRI BOOKINGS*
        m_sec = re.match(r'^\*([^*]+)\*$', line)
        if m_sec:
            current_section = m_sec.group(1).strip()
            continue

        if not current_day or not current_section:
            continue

        sec_upper = current_section.upper()

        # Handle confirmed bookings section
        if 'CONFIRMED' in sec_upper and 'BOOKING' in sec_upper:
            # Matches: 1. NAME - PHONE - DATE - TIME  or  - NAME - PHONE - ...
            m_item = re.match(r'^(?:\d+[.)]|-|\*)\s*(.*)$', line)
            if m_item:
                parts = [p.strip() for p in m_item.group(1).split('-')]
                if len(parts) >= 2:
                    modality = 'MRI' if 'MRI' in sec_upper else ('CT' if 'CT' in sec_upper else ('Ultrasound' if 'ULTRA' in sec_upper or 'USG' in sec_upper else 'Scan'))
                    booking = {
                        'name': parts[0],
                        'phone': parts[1],
                        'date': parts[2] if len(parts) > 2 else '',
                        'time': ' - '.join(parts[3:]) if len(parts) > 3 else '',
                        'modality': modality,
                        'logged_date': current_day['date']
                    }
                    current_day['bookings'].append(booking)
        else:
            # Handle metric key-value lines: e.g. BOOKINGS TAKEN FOR TODAY : 12
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip()
                v = v.strip()

                # Requirement: exclude unconfirmed enquiry info
                if 'YET TO CONFIRM' in k.upper():
                    continue

                val = int(v) if v.isdigit() else v
                if current_section not in current_day['metrics']:
                    current_day['metrics'][current_section] = {}
                current_day['metrics'][current_section][k] = val

    return days

def update_index_html(days):
    if not os.path.exists(HTML_FILE):
        print(f"Error: {HTML_FILE} not found.")
        return False

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    data_json = json.dumps(days, indent=2, ensure_ascii=False)
    tag_pattern = r'<script type="application/json" id="dashboard-data">([\s\S]*?)</script>'

    new_block = f'<script type="application/json" id="dashboard-data">\n{data_json}\n</script>'

    if re.search(tag_pattern, html):
        updated_html = re.sub(tag_pattern, new_block, html)
    else:
        # Insert before study-data
        target = '<script type="text/markdown" id="study-data">'
        if target in html:
            updated_html = html.replace(target, new_block + '\n\n' + target)
        else:
            # Fallback: insert before closing body
            updated_html = html.replace('</body>', new_block + '\n</body>')

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    return True

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        text = f.read()

    days = parse_data(text)
    if not days:
        print("Warning: No daily records parsed from data.txt.")
        return

    success = update_index_html(days)
    if success:
        total_bookings = sum(len(d['bookings']) for d in days)
        dates = [d['date'] for d in days]
        print(f"✓ Successfully updated {HTML_FILE}")
        print(f"  - Total days logged: {len(days)} ({', '.join(dates)})")
        print(f"  - Confirmed bookings logged: {total_bookings}")

if __name__ == '__main__':
    main()
