import cv2
from ultralytics import YOLO
from imutils.video import VideoStream
import time
import serial
import os
import sparepart

def main():
    ser_arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1) 
    model = YOLO('/home/otics/on/project_pt_otics_ai_hla/best_25_01_2024_100_ym.pt')
    rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"
    vidio_streaming = VideoStream(rtsp_url).start()
    previous_input = None
    sum_hla = 0
    condition_take_picture = 0
    data_time = ''
    data_date = ''
    date_time = ''
    print("Running....")
    while True:
        try:
            time.sleep(0.1)
            frame = vidio_streaming.read()
            results = model(frame)
            annotated_frame = results[0].plot(line_width=1, labels=True, conf=False)
            result = results[0]
            input_hla = 0
            output_serial = ser_arduino.readline()
            get_source_datetime = output_serial.decode().strip()
            get_datetime = get_source_datetime.split(';')
            if(get_datetime[0] == "on_time"):
                data_time = get_datetime[3]
                data_date = get_datetime[1]
                date_time = data_date + "_" + data_time
            nama_file_excel = f"/home/otics/on/project_pt_otics_ai_hla/runs/laporan_project_hla_{data_date}.xlsx"
            print(data_date)
            print(data_time)
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                if class_id == "hla":
                    input_hla += 1
            if input_hla == 0:
                previous_input = None
            else:
                if previous_input is None or input_hla > previous_input:
                    sum_hla += 1
                    previous_input = input_hla

            laporan_data = [
                data_time, 'HLA', input_hla, "-", sum_hla,
            ]

            if(input_hla == 192):
                ser_arduino.write(b"1")
                if(condition_take_picture <= 2):
                    save_dir = os.path.join("/home/otics/on/project_pt_otics_ai_hla/runs/hasil_deteksi_kamera_hla/", data_date)
                    file_name = os.path.join(save_dir, f"HLA_{date_time}.png")
                    os.makedirs(save_dir, exist_ok=True)
                    cv2.imwrite(file_name, annotated_frame)
                    condition_take_picture = condition_take_picture + 1
                    sparepart.make_report(nama_file_excel, laporan_data)
            if(input_hla > 192):
                if(condition_take_picture <= 2):
                    save_dir = os.path.join("/home/otics/on/project_pt_otics_ai_hla/runs/hasil_deteksi_kamera_hla/", data_date)
                    file_name = os.path.join(save_dir, f"HLA_{date_time}.png")
                    os.makedirs(save_dir, exist_ok=True)
                    cv2.imwrite(file_name, annotated_frame)
                    condition_take_picture = condition_take_picture + 1
                    sparepart.make_report(nama_file_excel, laporan_data)
            if(sum_hla < 192):
                condition_take_picture = 0 

            text ="Unit :" + str(input_hla) + " Pcs"
            text_position = (10, 10)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text, text_position, text_font_scale, text_font_thickness, box_size)

            
            resize_frame = cv2.resize(annotated_frame, (1280, 720))           
            cv2.imshow("Hasil Deteksi Part HLA", resize_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        except ValueError:
            print("Ada Error, Hubungi Member TPS.")
if __name__ == "__main__":
    main()