import pandas as pd
from rapidfuzz import fuzz

def load_data(invoice_path, payment_path):
    """
    Load invoice and payment data from CSV files.
    """
    invoices = pd.read_csv(invoice_path)
    payments = pd.read_csv(payment_path)

    # Strip whitespace and standardize names

    invoices['customer_name'] = invoices['customer_name'].str.strip().str.lower()
    payments['customer_name'] = payments['customer_name'].str.strip().str.lower()

    return invoices, payments

# Match payments to invoices using fuzzy name + amount
def reconcile(invoices, payments):
    matches = []
    unmatched_invoices = invoices.copy()
    unmatched_payments = payments.copy()

    for _, payment in payments.iterrows():
        best_score = 0
        best_match = None

        for _, invoice in unmatched_invoices.iterrows():
            name_score = fuzz.token_sort_ratio(payment['customer_name'], invoice['customer_name'])
            amount_match = abs(payment['amount_paid'] - invoice['amount_due']) < 0.01

            if name_score > 85 and amount_match:
                best_score = name_score
                best_match = invoice
                break  # Assume one-to-one match

        if best_match is not None:
            match_record = {
                'invoice_id': best_match['invoice_id'],
                'invoice_customer': best_match['customer_name'],
                'amount_due': best_match['amount_due'],
                'payment_id': payment['payment_id'],
                'payment_customer': payment['customer_name'],
                'amount_paid': payment['amount_paid'],
                'status': 'Matched'
            }
            matches.append(match_record)

            # Remove matched records
            unmatched_invoices = unmatched_invoices[unmatched_invoices['invoice_id'] != best_match['invoice_id']]
            unmatched_payments = unmatched_payments[unmatched_payments['payment_id'] != payment['payment_id']]
        else:
            matches.append({
                'invoice_id': None,
                'invoice_customer': None,
                'amount_due': None,
                'payment_id': payment['payment_id'],
                'payment_customer': payment['customer_name'],
                'amount_paid': payment['amount_paid'],
                'status': 'Unmatched Payment'
            })

    # Remaining unmatched invoices
    for _, invoice in unmatched_invoices.iterrows():
        matches.append({
            'invoice_id': invoice['invoice_id'],
            'invoice_customer': invoice['customer_name'],
            'amount_due': invoice['amount_due'],
            'payment_id': None,
            'payment_customer': None,
            'amount_paid': None,
            'status': 'Unpaid Invoice'
        })

    results = pd.DataFrame(matches)
    return results

# Summary stats for dashboard
def get_summary_stats(results):
    total_invoices = results['invoice_id'].nunique()
    total_matched = results[results['status'] == 'Matched'].shape[0]
    total_unmatched_payments = results[results['status'] == 'Unmatched Payment'].shape[0]
    total_unpaid_invoices = results[results['status'] == 'Unpaid Invoice'].shape[0]

    return {
        'Total Invoices': total_invoices,
        'Matched': total_matched,
        'Unmatched Payments': total_unmatched_payments,
        'Unpaid Invoices': total_unpaid_invoices
    }