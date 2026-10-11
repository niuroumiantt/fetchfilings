"""Microsoft FY2025 cash additions to PP&E, consolidated company scope."""
from helpers import html, candidate, date


def extract(data, source, original, sampled_at):
    p = html(data)
    if 'Year Ended June 30, 2025 2024 2023' not in p.text or '(In millions)' not in p.text:
        raise ValueError('financial period/scale changed')
    rows = [r for r in p.rows if r and r[0] == 'Additions to property and equipment']
    if len(rows) != 1:
        raise ValueError('cash flow row missing or ambiguous')
    row = rows[0]
    numbers = [c for c in row[1:] if c]
    if len(numbers) != 3 or not numbers[0].startswith('(') or not numbers[0].endswith(')'):
        raise ValueError('cash flow year/value schema changed')
    value = -float(numbers[0][1:-1].replace(',', ''))
    result = candidate('company', 'Microsoft Corporation', {'CIK': '0000789019', 'ticker': 'MSFT'},
        'finance.cashflow.additions_to_ppe', value, 'USD million',
        'Microsoft consolidated; FY2025 ended June 30; cash flow investing outflow; excludes noncash lease additions; not individual campus capex',
        'reported', 'Consolidated statements of cash flows; Additions to property and equipment; FY2025 column',
        numbers[0], 'Year Ended June 30, 2025 2024 2023 | In millions USD | ' + ' | '.join(row),
        date('2025-06-30', 'day', 'fiscal year end, not expenditure on this day'))
    result.update(period_start='2024-07-01', period_end='2025-06-30')
    return [result]
