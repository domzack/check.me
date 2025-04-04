import argparse
from datetime import datetime
from queue import Queue
import threading
import numpy as np
import openalpr

import sys

sys.path.append("/home/")
from domzack.groot1 import (
    AlprStart,
    StreamStart,
    adicionar_data_hora,
    capture_frames,
    comprimir_salvar,
    desenha_candidatas,
    desenha_placa,
    enviar_imagem_e_json,
    extract_results,
    liberar_recursos,
    post_screenshot,
    recortar_regiao,
)


def t_processar_rtsp_alpr(rtsp_url, output):
    t_running = True
    cap = None
    alpr_eu = None
    alpr_us = None
    camera_ip = rtsp_url.split("@")[1].split(":")[0]

    try:
        ret, cap = StreamStart(rtsp_url)
        if ret is None or t_running is False:
            print(f"Falha ao obter Stream: {rtsp_url}")
            t_running = False

        if t_running:
            frame_queue = Queue(maxsize=1)
            threading.Thread(
                target=capture_frames, args=(cap, frame_queue), daemon=True
            ).start()
            alpr_eu = AlprStart("eu")
            alpr_us = AlprStart("us")
            alpr_list = [alpr_eu, alpr_us]

        while t_running:
            if not frame_queue.empty():
                frame = frame_queue.get()
                frame_cp = adicionar_data_hora(frame.copy())
                np_image = np.array(frame)

                result_set = []
                for alpr_instance in alpr_list:
                    results_alpr = alpr_instance.recognize_ndarray(np_image)
                    results_alpr = extract_results(results_alpr)
                    results_alpr["camera_ip"] = camera_ip
                    results_alpr["timestamp"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if len(results_alpr) != 0:
                        try:
                            region = results_alpr["region"]
                            plate = results_alpr["plate"]
                            candidates = results_alpr["candidates"]
                            img_plate = desenha_placa(frame.copy(), results_alpr)
                            img_plate = recortar_regiao(img_plate, results_alpr)
                            img_plate = desenha_candidatas(img_plate, results_alpr)
                            img_plate = adicionar_data_hora(img_plate)

                            dados_adicionais = {
                                "camera_ip": results_alpr["camera_ip"],
                                "timestamp": results_alpr["timestamp"],
                                "plate": plate,
                                "region": region,
                                "confidence": f"{int(round(results_alpr['confidence'], 2))}%",
                                "candidates": [
                                    {
                                        "plate": c["plate"],
                                        "confidence": f"{int(round(c['confidence'], 2))}%",
                                    }
                                    for c in candidates
                                ],
                            }
                            enviar_imagem_e_json(output, img_plate, dados_adicionais)
                            result_set.append(results_alpr)
                        except Exception as e:
                            continue

                if not result_set or len(result_set) == 0:
                    dados_adicionais = {
                        "camera_ip": camera_ip,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "message": "No plates detected",
                    }
                    enviar_imagem_e_json(output, frame_cp, dados_adicionais)

        print(f"Thread '{camera_ip}' foi encerrada: {e}")
        liberar_recursos(cap, [alpr_eu, alpr_us])

    except Exception as e:
        print(f"Thread '{camera_ip}' foi encerrada: {e}")
        liberar_recursos(cap, [alpr_eu, alpr_us])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Leitura de placas utilizando OpenALPR."
    )
    parser.add_argument("rtsp_url", help="rtsp://usuario:senha@ip:porta/caminho")
    parser.add_argument(
        "--outputstream",
        help="Output Stream",
        type=str,
        default="http://127.0.0.1/post/plate",
    )

    args = parser.parse_args()
    print("iniciando...")
    t_processar_rtsp_alpr(args.rtsp_url, args.outputstream)

    # python3 zplate.py rtsp://brtronic:iMo_brc_m79@192.168.7.66:554/Streaming/Channels/101/
