import time
from bitcoin import get_bitcoin_price
from bot import send_line_notification

threshold_price = 0#50000  # 設定您的閾值
check_interval = 0#60 * 60  # 檢查間隔，這裡設為每小時檢查一次

while True:
    price = get_bitcoin_price()
    price = float(price.replace(',', '').replace('$', ''))  # 根據實際情況調整，去除價格中的符號和逗號
    print(f'Bitcoin price is {price}')
    if price > threshold_price:
        print(f'Bitcoin price is above {threshold_price}: current price is {price}')
        send_line_notification(f'Bitcoin price is above {threshold_price}: current price is {price}')
    elif price < threshold_price:
        print(f'Bitcoin price is below {threshold_price}: current price is {price}')
        send_line_notification(f'Bitcoin price is below {threshold_price}: current price is {price}')

    time.sleep(check_interval)
