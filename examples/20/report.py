"""Deterministic offline report, Python 3.10+. No third-party packages."""
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


def build(path):
    clean, errors, seen, duplicates = [], [], {}, 0
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        required = {'order_id', 'occurred_at', 'amount', 'currency', 'source'}
        if set(reader.fieldnames or []) != required:
            raise ValueError('欄位不符合資料契約')
        for number, row in enumerate(reader, 2):
            try:
                if None in row or any(not str(row[k] or '').strip() for k in required):
                    raise ValueError('缺值或欄位數錯誤')
                row = {k: v.strip() for k, v in row.items()}
                dt = datetime.fromisoformat(row['occurred_at'].replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    raise ValueError('時間缺少時區')
                amount = Decimal(row['amount'])
                if not amount.is_finite() or amount < 0 or amount != amount.quantize(Decimal('0.01')):
                    raise ValueError('金額必須非負且至多兩位小數')
                if row['currency'] != 'TWD':
                    raise ValueError('本報告只接受TWD')
                normalized = {**row, 'occurred_at': dt.astimezone(timezone.utc).isoformat(), 'amount': format(amount, '.2f')}
                key = (row['source'], row['order_id'])
                if key in seen:
                    if seen[key] != normalized:
                        raise ValueError('同一訂單鍵內容衝突')
                    duplicates += 1
                    continue
                seen[key] = normalized
                clean.append(normalized)
            except (ValueError, InvalidOperation) as exc:
                errors.append({'line': number, 'reason': str(exc), 'row': row})
    total = sum((Decimal(r['amount']) for r in clean), Decimal('0'))
    return {'input_rows': len(clean) + duplicates + len(errors), 'accepted': len(clean),
            'duplicates': duplicates, 'rejected': len(errors), 'total_TWD': str(total),
            'rows': clean, 'errors': errors, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=Path(__file__).parent / 'orders.csv')
    ap.add_argument('--out', type=Path, default=Path('report-output'))
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    report = build(args.input)
    if not args.dry_run:
        args.out.mkdir(parents=True, exist_ok=True)
        # Rebuild each batch; never append totals. Same input means same bytes.
        for name, value in [('report.json', report), ('errors.json', report['errors']),
                            ('state.json', {'source_sha256': report['source_sha256'], 'status': 'completed'})]:
            tmp = args.out / (name + '.tmp')
            tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            tmp.replace(args.out / name)
    print(json.dumps({k: report[k] for k in ['input_rows', 'accepted', 'duplicates', 'rejected', 'total_TWD']}))

if __name__ == '__main__':
    main()
