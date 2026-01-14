import socket
import time

# 設定
HOST = '192.168.11.34'  # 配信PCのIPアドレス
PORT = 2101              # ポート番号
RECEIVE_TIMEOUT = 10     # 受信時間（秒）
BUFFER_SIZE = 4096       # 受信バッファサイズ


def main():
    print(f"[INFO] {HOST}:{PORT} に接続します")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect((HOST, PORT))
            print("[INFO] 接続成功")
        except Exception as e:
            print(f"[ERROR] 接続失敗: {e}")
            return

        start_time = time.time()
        loop_count = 0
        total_bytes = 0
        while True:
            loop_count += 1
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            try:
                data = s.recv(BUFFER_SIZE)
                if not data:
                    print(f"[INFO] データ受信終了 (ループ:{loop_count}, 経過:{int(time.time()-start_time)}秒, 総バイト数:{total_bytes})")
                    break
                total_bytes += len(data)
                print(f"[DATA][{now}] 受信バイト数:{len(data)} 累計:{total_bytes} ループ:{loop_count}")
                print(f"  {data}")
            except socket.timeout:
                print(f"[WARN][{now}] タイムアウト、再試行 (ループ:{loop_count}, 経過:{int(time.time()-start_time)}秒, 総バイト数:{total_bytes})")
                continue
            except Exception as e:
                print(f"[ERROR][{now}] 受信エラー: {e} (ループ:{loop_count}, 経過:{int(time.time()-start_time)}秒, 総バイト数:{total_bytes})")
                break
            if time.time() - start_time > RECEIVE_TIMEOUT:
                print(f"[INFO][{now}] {RECEIVE_TIMEOUT}秒経過したので終了します (ループ:{loop_count}, 総バイト数:{total_bytes})")
                break

if __name__ == "__main__":
    main()
