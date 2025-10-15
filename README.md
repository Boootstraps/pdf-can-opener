# pdf-can-opener

Recover forgotten PDF passwords when the password is in DDMMYYYY format and you know the date range.

## Installation

Install [uv](https://github.com/astral-sh/uv):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:
```bash
uv pip install pikepdf tqdm
```

Or using a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install pikepdf tqdm
```

## Usage
```bash
python main.py   
```

**Examples:**
```bash
python main.py document.pdf 01/01/2020 31/12/2024
python main.py invoice.pdf 2023-06-01 2023-06-30
```

**Supported date formats:** DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY

## Output
```
Attempting to crack PDF: document.pdf
Date range: 01/01/2020 to 31/12/2023
Testing 1461 possible passwords...

Cracking: 45%|████████████▌             | 658/1461 [00:12<00:15, 52.3pwd/s]

✓ SUCCESS! Password found: 15032022
```

## Limitations

- Only works for DDMMYYYY format passwords
- Cannot crack non-date-based passwords
- Tests user password only (not owner password)