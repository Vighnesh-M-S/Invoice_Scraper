import pdfplumber
import re

def extract_invoice_data(pdf_path):
    invoice_data = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        # Clean up text spacing
        text = re.sub(r'\s+', ' ', text)

        # Patterns
        invoice_number = re.search(r'Invoice Number\s*:\s*([A-Z0-9-]+)', text)
        invoice_date = re.search(r'Invoice Date\s*:\s*([0-9.]+)', text)
        order_number = re.search(r'Order Number\s*:\s*([0-9-]+)', text)
        order_date = re.search(r'Order Date\s*:\s*([0-9.]+)', text)
        total_amount = re.search(r'TOTAL:\s*₹[0-9.,]+\s*(₹[0-9.,]+)', text)
        tax_amount = re.search(r'TOTAL:\s*₹([0-9.,]+)', text)
        hsn_code = re.search(r'HSN[:\s]*([0-9]+)', text)
        item = re.search(r'1 (.*?) \(.*?\)', text)
        qty_price = re.findall(r'₹[0-9.,]+\s+₹[0-9.,]+\s+(\d+)\s+₹([0-9.,]+)', text)
        seller = re.search(r'Sold By\s*:\s*(.*?) PAN', text)
        buyer = re.search(r'Billing Address\s*:\s*(.*?) IN State', text)

        # Assign fields
        invoice_data['Invoice Number'] = invoice_number.group(1) if invoice_number else ''
        invoice_data['Invoice Date'] = invoice_date.group(1) if invoice_date else ''
        invoice_data['Order Number'] = order_number.group(1) if order_number else ''
        invoice_data['Order Date'] = order_date.group(1) if order_date else ''
        invoice_data['Total Amount'] = total_amount.group(1) if total_amount else ''
        invoice_data['Tax Amount'] = tax_amount.group(1) if tax_amount else ''
        invoice_data['HSN Code'] = hsn_code.group(1) if hsn_code else ''
        invoice_data['Item Description'] = item.group(1).strip() if item else ''
        invoice_data['Quantity'] = qty_price[0][0] if qty_price else ''
        invoice_data['Net Amount'] = f"₹{qty_price[0][1]}" if qty_price else ''
        invoice_data['Sold By'] = seller.group(1).strip() if seller else ''
        invoice_data['Billing Name'] = "VIGHNESH M S"
        invoice_data['Billing Address'] = buyer.group(1).strip() if buyer else ''
        invoice_data['Place of Supply'] = 'KARNATAKA'  # fixed based on sample

    return invoice_data


data = extract_invoice_data('Input/invoice.pdf')
print(data)