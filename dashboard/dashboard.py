import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Introduction
st.title("E-Commerce Data Analysis Dashboard")
st.markdown("""
            ## Project Background
            This project aims to analyze an e-commerce public dataset to extract valuable insights into customer behavior, sales trends, and overall business performance. By applying data analysis techniques, we seek to address specific business questions to provide recommendations for optimization and growth. This project is a practical application of data science skills to real-world business scenarios, showcasing the power of data-driven decision-making.

            ## Dataset Overview
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
            """)

# Load datasets
orders_items_payments_path = "https://raw.githubusercontent.com/ralik45/E-Commerce-Analysis/refs/heads/main/dashboard/orders_items_payments.csv"
orders_path = "https://raw.githubusercontent.com/ralik45/E-Commerce-Analysis/refs/heads/main/dashboard/rfm_df.csv"
avg_popularity_products_path = "https://raw.githubusercontent.com/ralik45/E-Commerce-Analysis/refs/heads/main/dashboard/avg_popularity_product.csv"
order_reviews_path = "https://raw.githubusercontent.com/ralik45/E-Commerce-Analysis/refs/heads/main/dashboard/order_delivery_satisfaction_df.csv"

try:
    orders_items_payments = pd.read_csv(orders_items_payments_path)
    orders_df = pd.read_csv(orders_path)
    avg_popularity_products = pd.read_csv(avg_popularity_products_path)
    order_reviews_df = pd.read_csv(order_reviews_path)

    def unified_filter(dataframes):
        """
        Create a unified filter for year and month, applied to multiple dataframes.
        """
        # Ensure datetime format
        for df in dataframes:
            df['order_month'] = pd.to_datetime(df['order_month'])
            df['year'] = df['order_month'].dt.year
            df['month'] = df['order_month'].dt.month_name()

        # Sidebar filters
        st.sidebar.header("Apply Filters")
        available_years = sorted(dataframes[0]['year'].unique())
        selected_years = st.sidebar.multiselect(
            "Select Years",
            options=available_years,
            default=available_years,
        )
        available_months = sorted(dataframes[0]['month'].unique(), key=lambda x: pd.to_datetime(x, format='%B').month)
        selected_months = st.sidebar.multiselect(
            "Select Months",
            options=available_months,
            default=available_months,
        )

        # Apply filters
        filtered_dataframes = [
            df[(df['year'].isin(selected_years)) & (df['month'].isin(selected_months))]
            for df in dataframes
        ]
        return filtered_dataframes

    def sales_dashboard(filtered_df):
        """
        Sales Dashboard: Displays sales trends, orders, and customer behavior.
        """
        st.title("Sales Dashboard")

        # 1. Monthly Sales Analysis
        st.subheader("Monthly Sales Analysis")
        monthly_sales = filtered_df.groupby('order_month')['payment_value'].sum()
        st.line_chart(monthly_sales)
        st.markdown("Chart ini menunjukkan data penjualan dari Oktober 2016 hingga Agustus 2018, yang mencerminkan tren kenaikan signifikan secara keseluruhan. Titik terendah terjadi pada Desember 2016 dengan nilai 19.62, sementara puncaknya tercapai pada November 2017 dengan nilai 1,548,547.86. Setelah kenaikan tajam dari awal 2017 hingga akhir 2017, tren mengalami sedikit fluktuasi namun tetap berada pada kisaran tinggi hingga pertengahan 2018. Secara keseluruhan, data ini memperlihatkan pola pertumbuhan positif dengan kenaikan drastis pada tahun 2017 dan stabilisasi pada tingkat yang lebih tinggi selama 2018.")

        # 2. Monthly Orders Analysis
        st.subheader("Monthly Orders Analysis")
        monthly_orders = filtered_df.groupby('order_month')['order_id'].count()
        st.line_chart(monthly_orders)
        st.markdown("Chart ini memperlihatkan jumlah pesanan bulanan dari Oktober 2016 hingga Agustus 2018, menunjukkan pertumbuhan signifikan secara keseluruhan. Titik terendah terjadi pada Desember 2016 dengan 1 pesanan, sementara puncaknya tercapai pada November 2017 dengan 8.812 pesanan. Dari awal 2017, jumlah pesanan meningkat secara konsisten hingga mencapai puncak di akhir tahun, kemudian stabil di kisaran tinggi sepanjang 2018 meskipun sedikit menurun dari puncaknya. Secara keseluruhan, tren pesanan menunjukkan peningkatan yang kuat pada tahun 2017, diikuti oleh stabilisasi pada tingkat yang relatif tinggi di tahun 2018.")

        # 3. Monthly Customers Analysis
        st.subheader("Monthly Customers Analysis")
        monthly_customers = filtered_df.groupby('order_month')['customer_id'].nunique()
        st.line_chart(monthly_customers)
        st.markdown("Chart ini memperlihatkan jumlah pelanggan bulanan dari Oktober 2016 hingga Agustus 2018, menunjukkan tren pertumbuhan yang signifikan secara keseluruhan. Jumlah pelanggan terendah tercatat pada Desember 2016 dengan 1 pelanggan, sementara puncaknya terjadi pada November 2017 dengan 7.288 pelanggan. Dari awal 2017, jumlah pelanggan meningkat tajam hingga akhir tahun 2017, diikuti oleh stabilisasi pada tingkat tinggi sepanjang tahun 2018 dengan sedikit penurunan setelah puncaknya. Secara keseluruhan, data ini menunjukkan pertumbuhan pesat selama 2017, yang kemudian berlanjut dengan konsistensi pada tingkat yang tinggi sepanjang 2018.")
        
        # 4. Dashboard Insights
        st.sidebar.header("Dashboard Insights")
        st.sidebar.metric("Total Sales", f"${monthly_sales.sum():,.2f}")
        st.sidebar.metric("Total Orders", monthly_orders.sum())
        st.sidebar.metric("Total Unique Customers", monthly_customers.sum())
        
        # 5. Average Sales per Customer
        st.subheader("Average Spending per Customer")
        sales_per_customer = (
            filtered_df.groupby(['order_month', 'customer_id'])['payment_value'].sum().reset_index()
        )
        sales_per_customer_per_month = sales_per_customer.groupby('order_month').agg(
            avg_sales_per_customer=('payment_value', 'mean')
        )
        st.line_chart(sales_per_customer_per_month)
        st.markdown("Chart ini menunjukkan rata-rata penjualan per pelanggan per bulan dari Oktober 2016 hingga Agustus 2018. Rata-rata penjualan tertinggi tercatat pada Oktober 2016 sebesar 233.01, sementara titik terendahnya terjadi pada Desember 2016 dengan 19.62. Setelah fluktuasi awal, rata-rata penjualan per pelanggan stabil pada kisaran 180-240 di tahun-tahun berikutnya, dengan sedikit peningkatan di beberapa bulan seperti September 2017 (240.08) dan Mei 2018 (219.39). Secara keseluruhan, tren menunjukkan penurunan tajam setelah Oktober 2016, diikuti dengan stabilisasi pada tingkat menengah hingga akhir periode.")

    def rfm_dashboard(filtered_rfm):
        """
        RFM Dashboard: Displays customer segmentation based on Recency, Frequency, and Monetary metrics.
        """
        st.title("RFM Dashboard")

        # Filtered RFM Data based on unified filter
        st.subheader("RFM Analysis")

        # Ensure the 'order_purchase_timestamp' column is in datetime format
        filtered_rfm['order_purchase_timestamp'] = pd.to_datetime(
            filtered_rfm['order_purchase_timestamp']
        )

        # Filter data for the last month
        one_month_ago = filtered_rfm['order_purchase_timestamp'].max() - pd.DateOffset(months=1)
        rfm_df_filtered = filtered_rfm[filtered_rfm['order_purchase_timestamp'] >= one_month_ago]

        # Calculate Frequency, Monetary, and Recency
        rfm = rfm_df_filtered.groupby('customer_id').agg(
            frequency=('order_id', 'count'),  # Count of orders
            monetary=('payment_value', 'sum'),  # Sum of payment values
            recency=('order_purchase_timestamp', 'max')  # Maximum order date
        )

        # Convert recency to days
        rfm['recency'] = (
            rfm_df_filtered['order_purchase_timestamp'].max() - rfm['recency']
        ).dt.days

        # Sort data for plotting
        rfm_frequency = rfm.sort_values(by='frequency', ascending=False).head(5)
        rfm_monetary = rfm.sort_values(by='monetary', ascending=False).head(5)
        rfm_recency = rfm.sort_values(by='recency', ascending=True).head(5)

        # Create bar charts
        st.markdown("### Customers by Recency")
        fig, ax = plt.subplots()
        sns.barplot(x=rfm_recency.index, y=rfm_recency['recency'], palette="Reds_d", ax=ax)
        ax.set_xlabel("Customer ID")
        ax.set_ylabel("Recency (Days)")
        ax.set_title("Top 5 Customers by Recency (Most Recent First)")
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)
        st.markdown("""
                    Recency mengukur seberapa baru pelanggan terakhir kali melakukan transaksi. Dalam grafik "By Recency", data kosong menunjukkan bahwa pelanggan yang tercantum telah melakukan **transaksi pada hari yang sama** dengan waktu analisis ini. Dengan kata lain, mereka adalah pelanggan yang **paling aktif** dan baru saja berinteraksi dengan bisnis Anda.

                    Nilai recency yang sangat kecil (atau nol) menunjukkan bahwa pelanggan tersebut sangat terlibat dan memiliki hubungan aktif dengan bisnis. Pelanggan ini merupakan target yang ideal untuk mempertahankan loyalitas mereka melalui strategi pemasaran personalisasi.

                    **Kesimpulan untuk Recency:**
                    - Pelanggan ini sedang aktif bertransaksi.
                    - Mereka dapat dimasukkan ke dalam kategori pelanggan dengan tingkat urgensi tinggi untuk diberi perhatian, seperti memberikan penawaran khusus setelah transaksi mereka.

                    **Rekomendasi:**
                    - Kirimkan **ucapan terima kasih** atau penawaran langsung untuk pembelian berikutnya guna memperkuat loyalitas.
                    - Gunakan strategi **cross-selling** atau **up-selling** dengan produk yang relevan.
                    """)
        
        st.markdown("### Customers by Frequency")
        fig, ax = plt.subplots()
        sns.barplot(x=rfm_frequency.index, y=rfm_frequency['frequency'], palette="Blues_d", ax=ax)
        ax.set_xlabel("Customer ID")
        ax.set_ylabel("Frequency")
        ax.set_title("Top 5 Customers by Frequency")
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)
        st.markdown("""
                    Frequency mengukur seberapa sering pelanggan melakukan transaksi. Pada grafik "By Frequency," terlihat bahwa beberapa pelanggan memiliki frekuensi transaksi yang sangat tinggi, dengan puncaknya lebih dari 25 transaksi, sedangkan pelanggan lain memiliki frekuensi yang lebih rendah (antara 10 hingga 15 transaksi).

                    Pelanggan dengan frekuensi tinggi adalah pelanggan setia yang terus memberikan kontribusi besar terhadap aktivitas bisnis. Mereka adalah pelanggan **yang paling loyal** dan cenderung stabil dalam memberikan pendapatan.

                    **Kesimpulan untuk Frequency:**
                    - Pelanggan dengan frekuensi tinggi perlu dipertahankan melalui program loyalitas, seperti diskon eksklusif atau akses ke produk premium.
                    - Pelanggan dengan frekuensi rendah dapat diidentifikasi sebagai peluang untuk ditingkatkan, misalnya dengan memberikan insentif agar mereka lebih sering bertransaksi.

                    **Rekomendasi:**
                    - Gunakan **reward points** untuk pelanggan dengan frekuensi tinggi untuk memperkuat loyalitas.
                    - Lakukan kampanye pemasaran bertarget kepada pelanggan dengan frekuensi rendah untuk meningkatkan engagement mereka.
                    """)
        
        st.markdown("### Customers by Monetary Value")
        fig, ax = plt.subplots()
        sns.barplot(x=rfm_monetary.index, y=rfm_monetary['monetary'], palette="Greens_d", ax=ax)
        ax.set_xlabel("Customer ID")
        ax.set_ylabel("Monetary Value")
        ax.set_title("Top 5 Customers by Monetary Value")
        ax.tick_params(axis='x', rotation=90)
        st.pyplot(fig)
        st.markdown("""
                    Monetary menunjukkan seberapa besar pendapatan yang dihasilkan dari masing-masing pelanggan. Pada grafik "By Monetary," terlihat bahwa beberapa pelanggan menyumbang pendapatan yang sangat tinggi (mencapai lebih dari 30.000 unit mata uang), sementara pelanggan lainnya memberikan kontribusi yang lebih kecil.

                    Pelanggan dengan monetary tinggi merupakan aset yang sangat berharga bagi bisnis. Mereka termasuk dalam kategori **"big spender"** yang berkontribusi signifikan terhadap total pendapatan perusahaan. Sebaliknya, pelanggan dengan monetary rendah tetap penting, tetapi mungkin memerlukan pendekatan berbeda untuk meningkatkan kontribusi mereka.

                    **Kesimpulan untuk Monetary:**
                    - Pelanggan dengan monetary tinggi adalah prioritas utama untuk diberikan **pengalaman personalisasi** atau layanan premium.
                    - Pelanggan dengan monetary rendah perlu didorong untuk melakukan pembelian yang lebih besar melalui promosi, bundling produk, atau insentif pembelian.

                    **Rekomendasi:**
                    - Berikan pelanggan dengan monetary tinggi **penawaran eksklusif** seperti early access ke produk baru, bonus belanja, atau layanan prioritas.
                    - Tawarkan pelanggan dengan monetary rendah **promosi bundling** atau diskon khusus untuk mendorong peningkatan nilai transaksi mereka.
                    """)

    def product_popularity_analysis():
        """
        Analyze and display product popularity insights.
        """
        st.title("Product Popularity Analysis")

        # Average Product Price per Category (Top 10)
        st.subheader("Average Product Price per Category (Top 10)")
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x='price',
            y='product_category_name_english',
            data=avg_popularity_products.sort_values(by='price', ascending=False).head(10),
            palette='viridis',
            ax=ax1
        )
        ax1.set_xlabel("Average Price")
        ax1.set_ylabel("Product Category")
        ax1.set_title("Average Product Price per Category (Top 10)")
        st.pyplot(fig1)
        st.markdown("""
                    Chart ini menggambarkan harga produk rata-rata di berbagai kategori menunjukkan variasi yang signifikan. "Komputer" muncul sebagai kategori dengan harga produk rata-rata tertinggi, melebihi 1100. Diikuti oleh "Peralatan Kecil, Oven Rumah Tangga, dan Kopi", "Peralatan Rumah Tangga 2", "Industri Pertanian dan Perdagangan", dan "Pendingin Udara" dengan harga rata-rata berkisar antara 700 dan 1000. Di sisi lain, kategori seperti "Bunga", "Keamanan dan Pengawasan", "Perlengkapan Pesta", "Tas Fashion", "Makanan Minuman", dan "Popok dan Kebersihan" memiliki harga produk rata-rata yang relatif lebih rendah, yaitu di bawah 200. Kisaran harga rata-rata yang luas ini menyoroti keberagaman dalam penawaran produk dan strategi penetapan harga di berbagai kategori dalam platform e-commerce.
                    """)
        
        # Product Category Popularity (Top 10)
        st.subheader("Product Category Popularity (Top 10)")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x='product_id',
            y='product_category_name_english',
            data=avg_popularity_products.sort_values(by='product_id', ascending=False).head(10),
            palette='viridis',
            ax=ax2
        )
        ax2.set_xlabel("Number of Products Sold")
        ax2.set_ylabel("Product Category")
        ax2.set_title("Product Category Popularity (Top 10)")
        st.pyplot(fig2)
        st.markdown("""
                    Chart ini menyajikan wawasan mengenai popularitas kategori produk berdasarkan jumlah produk yang terjual. "Bed Bath Table" memimpin popularitas dengan hampir 12.000 produk terjual, diikuti oleh "Health Beauty" dengan sekitar 10.000 produk dan "Sports Leisure" yang melampaui 9.000. "Furniture Decor", "Computers Accessories", "Housewares", dan "Watches and Accessories" juga termasuk kategori populer, masing-masing dengan lebih dari 6.000 produk terjual. Di sisi lain, kategori seperti "Arts and Craftmanship", "La Cuisine", "cds dvds musics", dan "Fashion Childrens Clothes" tampaknya kurang populer dengan angka penjualan yang jauh lebih rendah. Temuan ini menunjukkan preferensi pelanggan dan pola permintaan di berbagai kategori produk, yang memberikan informasi berharga untuk manajemen inventaris dan strategi pemasaran.
                    """)

    def correlation_analysis():
        """
        Analyze and display the correlation between delivery time and customer satisfaction.
        """
        st.title("Correlation Analysis")

        if 'delivery_time' in order_reviews_df:
            st.subheader("Delivery Time vs Customer Satisfaction")
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=order_reviews_df, x='delivery_time', y='review_score')
            st.pyplot(plt)
        st.markdown("Korelasi antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan sebesar -0.3336852815284544 menunjukkan adanya korelasi negatif yang lemah antara kedua variabel tersebut. Nilai korelasi negatif menunjukkan bahwa ada kecenderungan bahwa semakin lama waktu pengiriman pesanan, tingkat kepuasan pelanggan cenderung menurun. Namun, penting untuk diingat bahwa korelasi sebesar -0.3336852815284544 itu cukup lemah, yang berarti hubungan antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan tidak terlalu kuat.")
        st.markdown("Dalam konteks ini, sementara ada korelasi negatif yang lemah antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan, tidak dapat disimpulkan bahwa waktu pengiriman secara langsung menyebabkan penurunan tingkat kepuasan pelanggan. Hal ini hanya menunjukkan bahwa ada hubungan yang lemah antara kedua variabel tersebut.")


    # Apply the unified filter
    filtered_orders_items_payments, filtered_orders_df = unified_filter([orders_items_payments, orders_df])

    # Display dashboards
    sales_dashboard(filtered_orders_items_payments)
    product_popularity_analysis()
    correlation_analysis()
    rfm_dashboard(filtered_orders_items_payments)

except FileNotFoundError:
    st.error("One or more data files could not be found. Please check the file paths.")
