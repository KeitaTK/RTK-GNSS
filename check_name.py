import serial

# --- 設定 ---
PORT = 'COM6'  # ← ここをu-centerで確認した番号に書き換えてください
BAUD = 115200

def main():
    print(f"--- {PORT} に直接接続します ---")
    try:
        # シリアルポートを開く
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            print("接続成功！座標を探しています...")
            
            while True:
                line = ser.readline().decode('ascii', errors='ignore')
                
                # $GNGGA という文字が含まれていたら表示
                if "$GNGGA" in line:
                    parts = line.split(',')
                    if len(parts) > 6 and parts[2]:
                        lat = parts[2] # 緯度
                        lon = parts[4] # 経度
                        print(f"【現在地】緯度: {lat} / 経度: {lon}")
                    else:
                        print("測位中（まだ衛星を捕捉していません）...")
                        
    except Exception as e:
        print(f"エラー: {e}")
        print("※u-centerが接続中の場合は、一度u-centerを閉じてから実行してください")

if __name__ == "__main__":
    main()