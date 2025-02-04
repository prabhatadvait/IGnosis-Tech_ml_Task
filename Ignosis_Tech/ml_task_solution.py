
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

transaction_data = pd.read_csv('transaction_data.csv')
purchase_behaviour = pd.read_csv('purchase_behaviour.csv')

print(transaction_data.isnull().sum())
print(purchase_behaviour.isnull().sum())

print(transaction_data.duplicated().sum())
print(purchase_behaviour.duplicated().sum())

transaction_data['DATE'] = pd.to_datetime(transaction_data['DATE'], errors='coerce')

transaction_data.drop_duplicates(inplace=True)
purchase_behaviour.drop_duplicates(inplace=True)

merged_data = pd.merge(transaction_data, purchase_behaviour, on='LYLTY_CARD_NBR', how='inner')

print(purchase_behaviour.columns)

customer_spend = merged_data.groupby('LYLTY_CARD_NBR')['TOT_SALES'].sum().reset_index()

customer_data = pd.merge(customer_spend, purchase_behaviour, on='LYLTY_CARD_NBR', how='left')

segmentation = customer_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).agg({
    'TOT_SALES': 'sum',
    'LYLTY_CARD_NBR': 'count'
}).reset_index()

print(segmentation.head())

top_customers = customer_spend.sort_values(by='TOT_SALES', ascending=False).head(3)
print(top_customers)

product_revenue = merged_data.groupby('PROD_NAME')['TOT_SALES'].sum().reset_index()

top_products = product_revenue.sort_values(by='TOT_SALES', ascending=False).head(3)
print(top_products)

plt.figure(figsize=(10, 6))
sns.barplot(data=segmentation, x='PREMIUM_CUSTOMER', y='TOT_SALES', hue='LIFESTAGE')
plt.title('Customer Segmentation by Premium Customer and Lifestyle')
plt.xlabel('Premium Customer')
plt.ylabel('Total Spend')
plt.show()

plt.figure(figsize=(8, 5))
sns.barplot(data=top_products, x='PROD_NAME', y='TOT_SALES')
plt.title('Top 3 Most Profitable Products')
plt.xlabel('Product Name')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.show()
