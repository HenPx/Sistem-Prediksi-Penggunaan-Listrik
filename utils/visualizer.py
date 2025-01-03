import plotly.graph_objs as go
import streamlit as st

# Visualize forecast using Plotly
def visualize_forecast(model, forecast, df_prophet, periods):
    st.subheader('Hasil Prediksi')

    # Determine the cutoff date for actual vs. future predictions
    cutoff_date = df_prophet['ds'].max()

    # Plot the forecast
    fig = go.Figure()

    # Add actual data (Bintik Hitam)
    fig.add_trace(go.Scatter(
        x=df_prophet['ds'], 
        y=df_prophet['y'], 
        mode='markers', 
        name='Actual Data (Bintik Hitam)',
        marker=dict(color='grey', size=3)
    ))

    # Add forecast data up to the cutoff date (in blue)
    fig.add_trace(go.Scatter(
        x=forecast[forecast['ds'] <= cutoff_date]['ds'], 
        y=forecast[forecast['ds'] <= cutoff_date]['yhat'], 
        mode='lines', 
        name='Historical Forecast',
        line=dict(color='blue'),
        legendgroup='group1'
    ))

    # Add upper bound and lower bound for historical data (in blue)
    fig.add_trace(go.Scatter(
        x=forecast[forecast['ds'] <= cutoff_date]['ds'], 
        y=forecast[forecast['ds'] <= cutoff_date]['yhat_upper'], 
        mode='lines', 
        line=dict(color='lightblue'),
        showlegend=False,
        legendgroup='group1'
    ))

    fig.add_trace(go.Scatter(
        x=forecast[forecast['ds'] <= cutoff_date]['ds'], 
        y=forecast[forecast['ds'] <= cutoff_date]['yhat_lower'], 
        mode='lines', 
        line=dict(color='lightblue'),
        fill='tonexty',
        showlegend=False,
        legendgroup='group1'
    ))

    # Future Forecast: Different colors based on yhat value
    future_forecast = forecast[forecast['ds'] > cutoff_date]
    
    # Green lines
    fig.add_trace(go.Scatter(
        x=future_forecast[future_forecast['yhat'] < 10000]['ds'], 
        y=future_forecast[future_forecast['yhat'] < 10000]['yhat'], 
        mode='lines', 
        name='Future Forecast < 10,000',
        line=dict(color='green'),
        legendgroup='group2'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast[future_forecast['yhat'] < 10000]['ds'], 
        y=future_forecast[future_forecast['yhat'] < 10000]['yhat_upper'], 
        mode='lines', 
        line=dict(color='lightgreen'),
        showlegend=False,
        legendgroup='group2'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast[future_forecast['yhat'] < 10000]['ds'], 
        y=future_forecast[future_forecast['yhat'] < 10000]['yhat_lower'], 
        mode='lines', 
        line=dict(color='lightgreen'),
        fill='tonexty',
        showlegend=False,
        legendgroup='group2'
    ))

    # Yellow lines
    fig.add_trace(go.Scatter(
        x=future_forecast[(future_forecast['yhat'] >= 10000) & (future_forecast['yhat'] <= 14000)]['ds'], 
        y=future_forecast[(future_forecast['yhat'] >= 10000) & (future_forecast['yhat'] <= 14000)]['yhat'], 
        mode='lines', 
        name='Future Forecast 10,000 - 14,000',
        line=dict(color='#FFB82B'),
        legendgroup='group3'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast[(future_forecast['yhat'] >= 10000) & (future_forecast['yhat'] <= 14000)]['ds'], 
        y=future_forecast[(future_forecast['yhat'] >= 10000) & (future_forecast['yhat'] <= 14000)]['yhat_upper'], 
        mode='lines', 
        line=dict(color='#FFCF60'),
        showlegend=False,
        legendgroup='group3'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast[(future_forecast['yhat'] >= 10000) & (future_forecast['yhat'] <= 14000)]['ds'], 
        y=future_forecast[(future_forecast['yhat'] >= 10000) & (future_forecast['yhat'] <= 14000)]['yhat_lower'], 
        mode='lines', 
        line=dict(color='#FFCF60'),
        fill='tonexty',
        showlegend=False,
        legendgroup='group3'
    ))

    # Red lines
    fig.add_trace(go.Scatter(
        x=future_forecast[future_forecast['yhat'] > 14000]['ds'], 
        y=future_forecast[future_forecast['yhat'] > 14000]['yhat'], 
        mode='lines', 
        name='Future Forecast > 14,000',
        line=dict(color='red'),
        legendgroup='group4'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast[future_forecast['yhat'] > 14000]['ds'], 
        y=future_forecast[future_forecast['yhat'] > 14000]['yhat_upper'], 
        mode='lines', 
        line=dict(color='lightcoral'),
        showlegend=False,
        legendgroup='group4'
    ))
    fig.add_trace(go.Scatter(
        x=future_forecast[future_forecast['yhat'] > 14000]['ds'], 
        y=future_forecast[future_forecast['yhat'] > 14000]['yhat_lower'], 
        mode='lines', 
        line=dict(color='lightcoral'),
        fill='tonexty',
        showlegend=False,
        legendgroup='group4'
    ))

    # Update layout
    fig.update_layout(
        title='Prediksi Penggunaan Listrik dengan Algoritma Prophet',
        xaxis_title='Date',
        yaxis_title='BP',
        legend_title='Legend',
        hovermode='x'
    )

    # Show the plot
    st.plotly_chart(fig)

    
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods))
    
    # Komponen Prediksi dengan Plotly
    st.subheader('Komponen Prediksi')

    # Plot komponen tren dengan upper dan lower bound
    fig_trend = go.Figure()

    # Garis utama untuk trend
    fig_trend.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['trend'],
        mode='lines', name='Trend', line=dict(color='blue')
    ))

    # Garis untuk upper bound
    fig_trend.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['trend_upper'],
        mode='lines', name='Upper Bound', line=dict(color='lightblue'),
        fill=None
    ))

    # Garis untuk lower bound
    fig_trend.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['trend_lower'],
        mode='lines', name='Lower Bound', line=dict(color='lightblue'),
        fill='tonexty', fillcolor='rgba(173, 216, 230, 0.3)'  # Mengisi area antara upper dan lower bound
    ))

    fig_trend.update_layout(title='Komponen Tren dengan Upper & Lower Bound (batas atas dan batas bawah)', 
                            xaxis_title='Tanggal', 
                            yaxis_title='Nilai Tren',
                            xaxis=dict(showgrid=True, gridcolor='LightGray', gridwidth=0.5),  # Menambahkan grid di sumbu X
                            yaxis=dict(showgrid=True, gridcolor='LightGray', gridwidth=0.5) )
    st.plotly_chart(fig_trend, use_container_width=True)

    # Plot komponen musiman mingguan (jika ada)
    if 'weekly' in forecast.columns:
        fig_weekly = go.Figure()
        fig_weekly.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['weekly'],
            mode='lines', name='Musiman Mingguan', line=dict(color='orange')
        ))

        # Upper bound musiman mingguan
        if 'weekly_upper' in forecast.columns and 'weekly_lower' in forecast.columns:
            fig_weekly.add_trace(go.Scatter(
                x=forecast['ds'], y=forecast['weekly_upper'],
                mode='lines', name='Upper Bound', line=dict(color='lightorange'),
                fill=None
            ))

            fig_weekly.add_trace(go.Scatter(
                x=forecast['ds'], y=forecast['weekly_lower'],
                mode='lines', name='Lower Bound', line=dict(color='lightorange'),
                fill='tonexty', fillcolor='rgba(255, 165, 0, 0.3)'  # Mengisi area antara upper dan lower bound
            ))

        fig_weekly.update_layout(title='Komponen Musiman Mingguan dengan Upper & Lower Bound (batas atas dan batas bawah)', 
                                xaxis_title='Tanggal', 
                                yaxis_title='Nilai Musiman Mingguan')
        st.plotly_chart(fig_weekly, use_container_width=True)

    # Plot komponen musiman tahunan (jika ada)
    if 'yearly' in forecast.columns:
        fig_yearly = go.Figure()
        fig_yearly.add_trace(go.Scatter(
            x=forecast['ds'], y=forecast['yearly'],
            mode='lines', name='Musiman Tahunan', line=dict(color='green')
        ))


        fig_yearly.update_layout(title='Komponen Musiman Tahunan dengan Upper & Lower Bound (batas atas dan batas bawah)', 
                                xaxis_title='Tanggal', 
                                yaxis_title='Nilai Musiman Tahunan')
        st.plotly_chart(fig_yearly, use_container_width=True)

def plot_forecast_with_capacity(forecast, total_capacity):
            fig = go.Figure()

            # Pisahkan data prediksi yang melebihi kapasitas dan yang tidak
            below_capacity = forecast['yhat'].where(forecast['yhat'] <= total_capacity, total_capacity)
            above_capacity = forecast['yhat'].where(forecast['yhat'] > total_capacity)

            # Plot prediksi beban puncak yang di bawah atau sama dengan kapasitas (warna biru)
            fig.add_trace(go.Scatter(
                x=forecast['ds'], 
                y=below_capacity,
                mode='lines', 
                name='Prediksi Beban Puncak (Di Bawah Kapasitas)',
                line=dict(color='blue')
            ))

            # Plot prediksi beban puncak yang melebihi kapasitas (warna merah)
            fig.add_trace(go.Scatter(
                x=forecast['ds'], 
                y=above_capacity,
                mode='lines', 
                name='Prediksi Beban Puncak (Melebihi Kapasitas)',
                line=dict(color='red')
            ))

            # Plot garis batas kapasitas listrik (garis putus-putus merah)
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=[total_capacity] * len(forecast),
                mode='lines',
                name='Kapasitas Maksimum Listrik',
                line=dict(color='red', dash='dash')
            ))

            # Menyusun layout
            fig.update_layout(title='Prediksi Beban Puncak vs Kapasitas Listrik',
                            xaxis_title='Tanggal',
                            yaxis_title='Beban Puncak (kW)',
                            showlegend=True)

            # Tampilkan plot
            st.plotly_chart(fig, use_container_width=True)

            # Filter prediksi yang melebihi kapasitas
            exceeding_capacity = forecast[forecast['yhat'] > total_capacity]

            # Tampilkan data yang melebihi kapasitas jika ada
            if not exceeding_capacity.empty:
                st.subheader("Prediksi yang Melebihi Kapasitas Listrik")
                st.write("Prediksi yang melebihi kapasitas listrik membantu mengidentifikasi potensi risiko kelebihan beban pada sistem energi. Dengan menganalisis data historis dan pola penggunaan, kita dapat memperkirakan momen-momen ketika konsumsi listrik diperkirakan akan melampaui batas kapasitas yang aman.")
                st.dataframe(exceeding_capacity[['ds', 'yhat']])
            else:
                st.write("Tidak ada prediksi yang melebihi kapasitas listrik.")

def plot_stacked_chart(data):
    # Resampling data
    weekly_data = data['BP'].resample('W').mean()
    monthly_data = data['BP'].resample('ME').mean()
    yearly_data = data['BP'].resample('YE').mean()

    # Membuat figure baru
    fig = go.Figure()

    # Menambahkan trace untuk rata-rata mingguan
    fig.add_trace(go.Scatter(x=weekly_data.index, y=weekly_data, mode='lines', name='Rata-rata Mingguan'))

    # Menambahkan trace untuk rata-rata bulanan
    fig.add_trace(go.Scatter(x=monthly_data.index, y=monthly_data, mode='lines', name='Rata-rata Bulanan'))

    # Menambahkan trace untuk rata-rata tahunan
    fig.add_trace(go.Scatter(x=yearly_data.index, y=yearly_data, mode='lines', name='Rata-rata Tahunan'))

    # Menyusun layout
    fig.update_layout(title='Perbandingan Rata-rata Beban Puncak (Mingguan, Bulanan, Tahunan)',
                      xaxis_title='Tanggal',
                      yaxis_title='Beban Puncak',
                      showlegend=True)

    # Menampilkan chart
    st.plotly_chart(fig, use_container_width=True)
    
# Fungsi untuk menumpukkan data berdasarkan tahun
def plot_data_per_year(data):
    st.write("_Silahkan klik tanggal pada bagian keterangan untuk menyeleksi analisis data dari tahun-tahun tertentu sesuai dengan yang Anda inginkan._")
    data['Year'] = data.index.year
    years = data['Year'].unique()
    
    fig = go.Figure()
    
    for year in years:
        yearly_data = data[data['Year'] == year]['BP'].resample('D').mean()
        fig.add_trace(go.Scatter(x=yearly_data.index.dayofyear, 
                                y=yearly_data, 
                                mode='lines', 
                                name=str(year)))
    
    fig.update_layout(title='Data Beban Puncak per Tahun',
                    xaxis_title='Hari ke-',
                    yaxis_title='Beban Puncak',
                    showlegend=True)
    return fig