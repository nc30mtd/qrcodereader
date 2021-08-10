import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

# python3 -m pip install opencv-python
# python3 -m pip install pyzbar
# https://qiita.com/PoodleMaster/items/0afbce4be7e442e75be6

DEVICE_ID = 0
font = cv2.FONT_HERSHEY_SIMPLEX

# QRコードデコード
def detect_and_read_opencv(frame):
    # QRCodeDetectorインスタンス生成
    qrd = cv2.QRCodeDetector()

    retval, decoded_info, points, straight_qrcode = qrd.detectAndDecodeMulti(frame)

    if retval:
        points = points.astype(np.int32)

        for dec_inf, point in zip(decoded_info, points):
            if dec_inf == '':
                continue

            # QRコード座標取得
            x = point[0][0]
            y = point[0][1]

            # QRコードデータ
            print('dec:', dec_inf)
            frame = cv2.putText(frame, dec_inf, (x, y - 6), FONT, .3, (0, 0, 255), 1, cv2.LINE_AA)

            # バウンディングボックス
            frame = cv2.polylines(frame, [point], True, (0, 255, 0), 1, cv2.LINE_AA)

def detect_and_read_pyzbar(frame):
    # デコード
    value = decode(frame, symbols=[ZBarSymbol.QRCODE])

    retarray = []

    if value:
        for qrcode in value:
            # QRコード座標
            x, y, w, h = qrcode.rect

            # QRコードデータ
            dec_inf = qrcode.data.decode('utf-8')
            retarray.append(dec_inf)
            frame = cv2.putText(frame, dec_inf, (x, y-6), font, .3, (255, 0, 0), 1, cv2.LINE_AA)

            # バウンディングボックス
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
    return retarray

if __name__ == '__main__':
    # VideoCapture オブジェクトを取得します
    capture = cv2.VideoCapture(DEVICE_ID)

    while(True):
        ret, frame = capture.read()

        #detect_and_read_opencv(frame)
        ret = detect_and_read_pyzbar(frame)

        print(ret)

        cv2.imshow('title', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()