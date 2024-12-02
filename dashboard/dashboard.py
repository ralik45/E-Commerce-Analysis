import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Introduction
st.title("E-Commerce Data Analysis Dashboard")
st.write("Explore insights from the e-commerce dataset.")

# Corrected file paths
orders_items_payments_path = "C:/Users/HP Elitebook 830 G5/Desktop/Barra/Projects/E-Commerce-Analysis/dashboard/orders_items_payments.csv"
orders_path = "C:/Users/HP Elitebook 830 G5/Desktop/Barra/Projects/E-Commerce-Analysis/dashboard/rfm_df.csv"
order_reviews_path = "C:/Users/HP Elitebook 830 G5/Desktop/Barra/Projects/E-Commerce-Analysis/dashboard/order_delivery_satisfaction_df.csv"

try:
    # Read datasets
    orders_items_payments = pd.read_csv(orders_items_payments_path)
    orders_df = pd.read_csv(orders_path)
    order_reviews_df = pd.read_csv(order_reviews_path)
    
    # Monthly Sales Analysis
    st.subheader("Monthly Sales Analysis")
    monthly_sales = orders_items_payments.groupby('order_month')['payment_value'].sum()
    st.line_chart(monthly_sales)

    # Monthly Orders
    st.subheader("Monthly Orders Analysis")
    monthly_orders = orders_items_payments.groupby('order_month')['order_id'].count()
    st.line_chart(monthly_orders)
    
    # Monthly Customers
    st.subheader("Monthly Customers Analysis")
    monthly_customers = orders_items_payments.groupby('order_month')['customer_id'].count()
    st.line_chart(monthly_customers)
    
    st.markdown("### Total Sales, Orders, and Customers")
    st.markdown("3 Chart ini memberikan pandangan yang jelas mengenai monthly sales, Orders, dan Customers selama ini, menunjukkan growth yang signifikan dari oktober 2016 sampai akhir 2017. Peningkatan di sales, lebih tepatnya pada puncak november 2017, ini mungkin menunjukkan suksesnya strategi marketing yang mendorong pelanggan untuk beli. Namun, fluktuasi pasca-puncak dan penurunan bertahap pada tahun 2018 menyoroti tantangan potensial, seperti berkurangnya keterlibatan pelanggan, kejenuhan pasar, atau berkurangnya upaya promosi. Hal ini menekankan pentingnya mempertahankan momentum melalui strategi inovatif, kampanye tepat waktu, atau peningkatan produk.")
    st.markdown("Sebagai kesimpulan, meskipun tren kenaikan secara keseluruhan mencerminkan keberadaan pasar yang kuat dan potensi pertumbuhan, pola penurunan pada tahun 2018 menandakan perlunya tindakan segera untuk mengatasi stagnasi penjualan. Bisnis harus memanfaatkan wawasan dari periode puncak untuk mengidentifikasi apa yang disukai pelanggan sambil mengatasi kesenjangan dalam kinerja. Dengan demikian, mereka dapat membangun ketahanan jangka panjang, memanfaatkan peluang pertumbuhan, dan mempertahankan lintasan penjualan yang stabil.")

    # Average Sales per Customer
    st.subheader("Average Spending per Customer")
    sales_per_customer = (
        orders_items_payments.groupby(['order_month', 'customer_id'])['payment_value'].sum().reset_index()
    )
    sales_per_customer_per_month = sales_per_customer.groupby('order_month').agg(
    avg_sales_per_customer=('payment_value', 'mean')
    )
    st.line_chart(sales_per_customer_per_month)
    
    st.markdown("### Average Spending per Customer")
    st.markdown("Grafik di atas menunjukkan rata-rata penjualan per pelanggan per bulan dalam rentang waktu tertentu, dimulai dari Oktober 2016 hingga Agustus 2018. Pada awal periode, terlihat adanya penurunan tajam pada bulan Desember 2016, yang menunjukkan nilai rata-rata penjualan per pelanggan sangat rendah dibandingkan bulan sebelumnya. Penurunan ini dapat disebabkan oleh faktor musiman, gangguan dalam operasi bisnis, atau penurunan permintaan. Setelah titik terendah ini, terdapat peningkatan tajam di bulan Januari 2017, yang mungkin disebabkan oleh pulihnya operasional atau promosi penjualan khusus di awal tahun. Setelah Januari 2017, rata-rata penjualan per pelanggan cenderung stabil dengan fluktuasi kecil hingga pertengahan 2017.")
    st.markdown("Pada pertengahan hingga akhir periode, sekitar bulan Juli 2017 hingga Agustus 2018, grafik menunjukkan adanya pola fluktuasi yang lebih teratur tetapi tetap berada dalam kisaran yang lebih tinggi dibandingkan awal 2017. Peningkatan rata-rata penjualan per pelanggan di beberapa bulan seperti Juni 2017 hingga September 2017 dapat mencerminkan peluncuran produk baru atau keberhasilan kampanye pemasaran. Namun, tren mulai menurun perlahan setelah puncak tersebut hingga Agustus 2018, menunjukkan perlunya strategi baru untuk menjaga momentum pertumbuhan. Secara keseluruhan, grafik ini memberikan wawasan penting tentang perilaku pelanggan dan efektivitas strategi pemasaran pada periode tersebut, serta mengindikasikan perlunya analisis lebih lanjut terhadap faktor-faktor penyebab penurunan dan peningkatan penjualan pada periode tertentu.")

    # Correlation Analysis
    st.subheader("Correlation: Delivery Time vs Customer Satisfaction")
    if 'delivery_time' in order_reviews_df:
        plt.figure(figsize=(10, 5))
        sns.scatterplot(data=order_reviews_df, x='delivery_time', y='review_score')
        st.pyplot(plt)

    st.markdown("### Korelasi Antara Order Delivery Time dan Customer Satisfaction")
    st.markdown("Korelasi antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan sebesar -0.3336852815284544 menunjukkan adanya korelasi negatif yang lemah antara kedua variabel tersebut. Nilai korelasi negatif menunjukkan bahwa ada kecenderungan bahwa semakin lama waktu pengiriman pesanan, tingkat kepuasan pelanggan cenderung menurun. Namun, penting untuk diingat bahwa korelasi sebesar -0.3336852815284544 itu cukup lemah, yang berarti hubungan antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan tidak terlalu kuat.")
    st.markdown("Dalam konteks ini, sementara ada korelasi negatif yang lemah antara waktu pengiriman pesanan dan tingkat kepuasan pelanggan, tidak dapat disimpulkan bahwa waktu pengiriman secara langsung menyebabkan penurunan tingkat kepuasan pelanggan. Hal ini hanya menunjukkan bahwa ada hubungan yang lemah antara kedua variabel tersebut.")
    
    # RFM Analysis
    st.subheader("RFM Analysis")

    # Ensure the 'order_purchase_timestamp' column is in datetime format
    orders_items_payments['order_purchase_timestamp'] = pd.to_datetime(
        orders_items_payments['order_purchase_timestamp']
    )

    # Filter data for the last month
    one_month_ago = orders_items_payments['order_purchase_timestamp'].max() - pd.DateOffset(months=1)
    rfm_df_filtered = orders_items_payments[orders_items_payments['order_purchase_timestamp'] >= one_month_ago]

    # Calculate Frequency, Monetary, and Recency
    rfm = rfm_df_filtered.groupby('customer_id').agg(
        frequency=('order_id', 'count'),  # Count of orders
        monetary=('payment_value', 'sum'),  # Sum of payment values
        recency=('order_purchase_timestamp', 'max')  # Maximum order date
    )

    # Convert recency to days
    rfm['recency'] = (rfm_df_filtered['order_purchase_timestamp'].max() - rfm['recency']).dt.days

    # Sort data for plotting
    rfm_frequency = rfm.sort_values(by='frequency', ascending=False).head(5)
    rfm_monetary = rfm.sort_values(by='monetary', ascending=False).head(5)
    rfm_recency = rfm.sort_values(by='recency', ascending=True).head(5)

    # Create bar charts
    st.markdown("### Customers by Frequency")
    fig, ax = plt.subplots()
    sns.barplot(x=rfm_frequency.index, y=rfm_frequency['frequency'], palette="Blues_d", ax=ax)
    ax.set_xlabel("Customer ID")
    ax.set_ylabel("Frequency")
    ax.set_title("Top 5 Customers by Frequency")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
    
    st.markdown("Frequency mengukur seberapa sering pelanggan melakukan transaksi. Pada grafik 'By Frequency,' terlihat bahwa beberapa pelanggan memiliki frekuensi transaksi yang sangat tinggi, dengan puncaknya lebih dari 25 transaksi, sedangkan pelanggan lain memiliki frekuensi yang lebih rendah (antara 10 hingga 15 transaksi).")
    st.markdown("Pelanggan dengan frekuensi tinggi adalah pelanggan setia yang terus memberikan kontribusi besar terhadap aktivitas bisnis. Mereka adalah pelanggan yang paling loyal dan cenderung stabil dalam memberikan pendapatan.")
    st.markdown("""
                **Kesimpulan:**
                - Pelanggan dengan frekuensi tinggi perlu dipertahankan melalui program loyalitas, seperti diskon eksklusif atau akses ke produk premium.
                - Pelanggan dengan frekuensi rendah dapat diidentifikasi sebagai peluang untuk ditingkatkan, misalnya dengan memberikan insentif agar mereka lebih sering bertransaksi.
                """)
    st.markdown("""
                **Rekomendasi:**
                - Gunakan reward points untuk pelanggan dengan frekuensi tinggi untuk memperkuat loyalitas.
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
    
    st.markdown("Monetary menunjukkan seberapa besar pendapatan yang dihasilkan dari masing-masing pelanggan. Pada grafik 'By Monetary,' terlihat bahwa beberapa pelanggan menyumbang pendapatan yang sangat tinggi (mencapai lebih dari 30.000 unit mata uang), sementara pelanggan lainnya memberikan kontribusi yang lebih kecil.")
    st.markdown("Pelanggan dengan monetary tinggi merupakan aset yang sangat berharga bagi bisnis. Mereka termasuk dalam kategori 'big spender' yang berkontribusi signifikan terhadap total pendapatan perusahaan. Sebaliknya, pelanggan dengan monetary rendah tetap penting, tetapi mungkin memerlukan pendekatan berbeda untuk meningkatkan kontribusi mereka.")
    st.markdown("""
                **Kesimpulan:**
                - Pelanggan dengan monetary tinggi adalah prioritas utama untuk diberikan pengalaman personalisasi atau layanan premium.
                - Pelanggan dengan monetary rendah perlu didorong untuk melakukan pembelian yang lebih besar melalui promosi, bundling produk, atau insentif pembelian.
                """)
    st.markdown("""
                **Rekomendasi:**
                - Berikan pelanggan dengan monetary tinggi penawaran eksklusif seperti early access ke produk baru, bonus belanja, atau layanan prioritas.
                - Tawarkan pelanggan dengan monetary rendah promosi bundling atau diskon khusus untuk mendorong peningkatan nilai transaksi mereka.
                """)

    st.markdown("### Customers by Recency")
    fig, ax = plt.subplots()
    sns.barplot(x=rfm_recency.index, y=rfm_recency['recency'], palette="Reds_d", ax=ax)
    ax.set_xlabel("Customer ID")
    ax.set_ylabel("Recency (Days)")
    ax.set_title("Top 5 Customers by Recency (Most Recent First)")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
    st.markdown("Recency mengukur seberapa baru pelanggan terakhir kali melakukan transaksi. Dalam grafik 'By Recency', data kosong menunjukkan bahwa pelanggan yang tercantum telah melakukan transaksi pada hari yang sama dengan waktu analisis ini. Dengan kata lain, mereka adalah pelanggan yang paling aktif dan baru saja berinteraksi dengan bisnis Anda.")
    st.markdown("Nilai recency yang sangat kecil (atau nol) menunjukkan bahwa pelanggan tersebut sangat terlibat dan memiliki hubungan aktif dengan bisnis. Pelanggan ini merupakan target yang ideal untuk mempertahankan loyalitas mereka melalui strategi pemasaran personalisasi.")
    st.markdown("""
                **Kesimpulan:**
                - Pelanggan ini sedang aktif bertransaksi.
                - Mereka dapat dimasukkan ke dalam kategori pelanggan dengan tingkat urgensi tinggi untuk diberi perhatian, seperti memberikan penawaran khusus setelah transaksi mereka.
                """)
    st.markdown("""
                **Rekomendasi:**
                - Kirimkan ucapan terima kasih atau penawaran langsung untuk pembelian berikutnya guna memperkuat loyalitas.
                - Gunakan strategi cross-selling atau up-selling dengan produk yang relevan.
                """)
    
except FileNotFoundError:
    st.error("One or more data files could not be found. Please check the file paths.")
