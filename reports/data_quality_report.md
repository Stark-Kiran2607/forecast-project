#FORESIGHT - Data Quality Report

- message=sales : shape =500,000 rows, 16 columns from sale.csv
- message=sku : shape =5,000 rows, 7 columns from sku.csv
- message=calendar : shape =1,765 rows, 10 columns from calendar.csv
- message=inventory : shape =26,408 rows, 6 columns from inventory.csv
- sales: normalized sku_id (4->5 digit) and store_id (3->2 digit)
- sales: aggregated 500,000 transactions into 167,973 (date, sku_id) rows
- calendar: extended by 61 rows to cover sales through 2025-12-31
- calendar: no holiday indicator in source - added 'is_holiday' defaulted to False
- calendar: no promo_event column - promo signal comes from sales-level discount_promo_id instead
- sku_master: catalog has 5,000 SKUs; filtered to 250 active (sold) SKUs
- inventory: point-in-time snapshot, not a dated time series - risk scoring will use stock_on_hand, safety_stock, reorder_point
- inventory_position: aggregated to 4,495 SKU-level rows
- master_dataset: 167,973 rows, 24 columns