# E-Commerce-Analysis
## Project Background
This project aims to analyze an e-commerce public dataset to extract valuable insights into customer behavior, sales trends, and overall business performance. By applying data analysis techniques, we seek to address specific business questions to provide recommendations for optimization and growth. This project is a practical application of data science skills to real-world business scenarios, showcasing the power of data-driven decision-making.

## Dataset Attributes
The dataset comprises several tables, each containing information about a specific aspect of the e-commerce operations:

- Customers: Data on customers, including their unique IDs, locations, and demographics.
- Geolocation: Information about geographical locations, such as zip codes, cities, and states.
- Order Items: Details about items purchased in each order, quantities, prices, and shipping information.
- Order Payments: Data on payment methods, installments, and values for each order.
- Order Reviews: Customer feedback on orders, including review scores and comments.
- Orders: Comprehensive data on orders, including purchase timestamps, order statuses, and delivery details.
- Product Category: Translation of product category names into English.
- Products: Information about products, their categories, descriptions, dimensions, and weights.
- Sellers: Data on sellers, including their IDs, locations, and ratings.
These datasets are interconnected and provide a holistic view of the e-commerce business.

## Executive Summary
This analysis of an e-commerce public dataset reveals key insights into sales trends, customer behavior, and business performance. Sales, orders, and customer acquisition grew significantly from October 2016 to late 2017, likely driven by successful marketing strategies. However, a gradual decline in 2018 suggests potential challenges in customer engagement and market saturation.

While a weak negative correlation exists between delivery time and customer satisfaction, it's not a primary driver of customer sentiment. RFM analysis identified valuable customer segments based on recency, frequency, and monetary value, providing opportunities for targeted marketing efforts.

## Insight Deep-Dive
### Sales, Orders, and Customers:
The analysis reveals a significant growth trend in sales, orders, and customer acquisition from October 2016 to late 2017.
A peak in sales during November 2017 suggests the effectiveness of marketing campaigns during that period.
Fluctuations and a gradual decline in sales observed in 2018 indicate potential challenges such as customer engagement, market saturation, or reduced promotional activities.
### Average Sales per Customer:
A sharp drop in average sales per customer in December 2016 might be attributed to seasonality, operational disruptions, or decreased demand.
A rapid increase in January 2017 could be due to operational recovery or specific sales promotions.
Fluctuations in the latter half of the analysis period (July 2017 - August 2018) suggest a need for strategies to maintain growth momentum.
### Order Delivery Time and Customer Satisfaction:
A weak negative correlation between order delivery time and customer satisfaction suggests that longer delivery times may slightly affect customer satisfaction, but the relationship is not strong.
### RFM Analysis:
- Recency: Customers who recently transacted are highly engaged and valuable for retention efforts. Personalized marketing strategies can be applied to maintain their loyalty.
- Frequency: Customers with high transaction frequency are loyal and contribute significantly to business activity. Reward programs and exclusive offers can enhance their loyalty.
- Monetary: Customers with high monetary value are crucial for revenue generation. Personalized experiences and premium services can cater to their needs.
## Recommendations
Based on the insights derived from the analysis, the following recommendations are proposed:

- Customer Retention: Implement strategies to retain customers, especially those with high recency, frequency, and monetary value.
- Targeted Marketing: Develop targeted marketing campaigns based on customer segments identified through RFM analysis.
- Delivery Time Optimization: Explore options to optimize delivery times, considering the weak negative correlation with customer satisfaction.
- Product and Promotion Strategies: Introduce new products, services, and promotions to address market saturation and maintain growth momentum.
- Customer Engagement: Implement initiatives to improve customer engagement and address potential decline in sales.
- Operational Efficiency: Continuously monitor and improve operational efficiency to ensure timely order fulfillment and enhance customer satisfaction.
- Data-Driven Decision-Making: Leverage data insights for continuous improvement and strategic planning.
By implementing these recommendations, the e-commerce business can enhance customer satisfaction, optimize operations, and drive sustainable growth.

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```
