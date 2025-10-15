#!/usr/bin/env python3
"""
PDF Password Brute Force for Date Format (DDMMYYYY)
"""

import pikepdf
from datetime import datetime, timedelta
from tqdm import tqdm
import sys


def generate_date_passwords(start_date: str, end_date: str):
    """
    Generate all dates between start_date and end_date in DDMMYYYY format.

    Args:
        start_date: Date string in format 'DD/MM/YYYY' or 'YYYY-MM-DD'
        end_date: Date string in format 'DD/MM/YYYY' or 'YYYY-MM-DD'
    """
    # Parse dates
    for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
        try:
            start = datetime.strptime(start_date, fmt)
            end = datetime.strptime(end_date, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Could not parse dates. Use format DD/MM/YYYY or YYYY-MM-DD")

    current = start
    while current <= end:
        yield current.strftime('%d%m%Y')
        current += timedelta(days=1)


def count_days(start_date: str, end_date: str) -> int:
    """Count total days in the range for progress bar."""
    for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
        try:
            start = datetime.strptime(start_date, fmt)
            end = datetime.strptime(end_date, fmt)
            return (end - start).days + 1
        except ValueError:
            continue
    return 0


def crack_pdf_password(pdf_path: str, start_date: str, end_date: str):
    """
    Attempt to open a PDF with passwords in DDMMYYYY format.

    Args:
        pdf_path: Path to the password-protected PDF
        start_date: Start of date range
        end_date: End of date range
    """
    print(f"Attempting to crack PDF: {pdf_path}")
    print(f"Date range: {start_date} to {end_date}")

    total = count_days(start_date, end_date)
    print(f"Testing {total} possible passwords...\n")

    with tqdm(total=total, desc="Cracking", unit="pwd") as pbar:
        for password in generate_date_passwords(start_date, end_date):
            try:
                with pikepdf.open(pdf_path, password=password):
                    pbar.close()
                    print(f"\n✓ SUCCESS! Password found: {password}")
                    return password
            except pikepdf.PasswordError:
                pbar.update(1)
                continue
            except Exception as e:
                pbar.write(f"Error with password {password}: {e}")
                pbar.update(1)
                continue

    print(f"\n✗ Password not found. Tried all {total} combinations.")
    return None


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <pdf_file> <start_date> <end_date>")
        print("Example: python main.py document.pdf 01/01/2020 31/12/2023")
        sys.exit(1)

    pdf_file = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]

    password = crack_pdf_password(pdf_file, start, end)

    if password:
        print(f"\nSUCCESS! Password found: {password}")