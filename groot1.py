import cv2
from openalpr import Alpr
import numpy as np
import logging
from onvif import ONVIFCamera
from datetime import datetime
import threading
from queue import Queue

# import time
import requests
import base64

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("alpr_log.log"), logging.StreamHandler()],
)

color_green = (0, 255, 0)
color_red = (0, 0, 255)
color_blue = (255, 0, 0)
color_black = (0, 0, 0)
color_white = (255, 255, 255)
fonte = cv2.FONT_HERSHEY_SIMPLEX
font_size_plate = 0.7

running = True
comando_var = None

threads = {}  # Dicionário para monitorar threads ativas
lock = threading.Lock()  # Controle de acesso às threads


def post_screenshot(url, imagen, dados_adicionais):
    _, buffer = cv2.imencode(".jpg", imagen)
    body = {"image": base64.b64encode(buffer).decode("utf-8"), "data": dados_adicionais}
    # Fazer a requisição POST
    resposta = requests.post(url, json=body)
    # Retornar a resposta (pode incluir o status ou os dados retornados)
    return resposta.json()


def obter_rtsp_url(host, porta, usuario, senha):
    try:
        camera = ONVIFCamera(host, porta, usuario, senha, "/etc/onvif/wsdl/")
        media_service = camera.create_media_service()
        profiles = media_service.GetProfiles()
        profile = profiles[0]  # Seleciona o primeiro perfil
        stream_uri = media_service.GetStreamUri(
            {
                "StreamSetup": {"Stream": "RTP-Unicast", "Transport": "RTSP"},
                "ProfileToken": profile.token,
            }
        )
        rtsp_url = stream_uri.Uri.replace("rtsp://", f"rtsp://{usuario}:{senha}@")
        return rtsp_url, None
    except Exception as e:
        return None, e


def adicionar_data_hora(imagem):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    altura, largura, _ = imagem.shape
    (largura_texto, altura_texto), _ = cv2.getTextSize(
        f"ZPLATE - {data_hora}", fonte, font_size_plate, 1
    )
    x_inicio = largura - largura_texto - 10
    y_inicio = 0
    x_fim = largura
    y_fim = y_inicio + altura_texto + 10
    cv2.rectangle(
        imagem, (x_inicio, y_inicio), (x_fim, y_fim), color_black, thickness=-1
    )
    cv2.putText(
        imagem,
        data_hora,
        (x_inicio + 5, y_inicio + altura_texto + 5),
        fonte,
        font_size_plate,
        color_white,
        1,
    )
    return imagem


def comprimir_salvar(path_to_save, image, taxa):
    cv2.imwrite(path_to_save, image, [cv2.IMWRITE_JPEG_QUALITY, taxa])


def capture_frames(cap, frame_queue):
    while True:
        ret, frame = cap.read()
        if ret:
            if frame_queue.full():
                frame_queue.get()
            frame_queue.put(frame)


def AlprStart(region):
    try:
        config_file = "/etc/openalpr/openalpr.conf"
        runtime_data = "/usr/share/openalpr/runtime_data"
        alpr = Alpr(region, config_file, runtime_data)
        alpr.set_default_region(region)
        alpr.set_detect_region(True)
        alpr.set_top_n(10)
        if not alpr.is_loaded():
            logging.error(f"Erro ao carregar o OpenALPR: {region}")
            exit(1)
        # logging.info(f"OpenALPR carregado para região: {region}")
        return alpr
    except Exception as e:
        logging.error(f"AlprStart: {e}")
        exit(1)


def StreamStart(rtsp_url):
    # logging.info(f"Iniciando stream RTSP")
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cap.isOpened():
        logging.error(f"Falha ao conectar ao stream RTSP")
        return False, None
    # logging.info("Stream RTSP iniciado com sucesso.")
    return True, cap


def extract_results(results):
    resultset = {}
    try:
        for resultado in results["results"]:
            region = resultado["region"]
            coordinates = resultado["coordinates"]
            candidates = resultado["candidates"]
            confidence = resultado["confidence"]
            plate = resultado["plate"]
            pontos = [(coord["x"], coord["y"]) for coord in coordinates]
            pontos = np.array(pontos, dtype=np.int32)
            resultset = {
                "region": region,
                "plate": plate,
                "pontos": pontos,
                "candidates": candidates,
                "confidence": confidence,
            }
        return resultset
    except Exception as e:
        logging.error(f"extract_results: {e}")
        return {}


def recortar_regiao(imagem, alpr_results):
    x_min, x_max, y_min, y_max = roi(alpr_results["pontos"])
    margem = 400
    x_min = max(x_min - margem, 0)
    y_min = max(y_min - margem, 0)
    x_max = min(x_max + 200, imagem.shape[1])
    y_max = min(y_max + 200, imagem.shape[0])
    cropped_image = imagem[y_min:y_max, x_min:x_max]
    return cropped_image


def roi(pontos):
    if pontos is not None and len(pontos) > 0:
        x_min = min(ponto[0] for ponto in pontos)  # Ponto horizontal esquerdo
        x_max = max(ponto[0] for ponto in pontos)  # Ponto horizontal direito
        y_min = min(ponto[1] for ponto in pontos)  # Ponto vertical superior
        y_max = max(ponto[1] for ponto in pontos)  # Ponto vertical inferior
        return x_min, x_max, y_min, y_max  # retorna coordenadas roi alpr_results
    else:
        logging.error("Erro: Não foi possível determinar os pontos de recorte.")
        return None, None, None, None


def desenha_placa(imagem, alpr_results):
    img_cp = imagem.copy()
    plate = alpr_results["plate"]
    pontos = alpr_results["pontos"]
    region = alpr_results["region"]
    x_min, x_max, y_min, y_max = roi(pontos)
    cv2.polylines(img_cp, [pontos], isClosed=True, color=color_green, thickness=2)
    (largura_texto, altura_texto), _ = cv2.getTextSize(
        f"  {plate}  ", fonte, font_size_plate, 1
    )
    x_inicio = x_min
    y_inicio = y_min
    x_fim = x_inicio + largura_texto + 10
    y_fim = y_inicio - altura_texto - 10
    cv2.rectangle(
        img_cp, (x_inicio, y_inicio), (x_fim, y_fim), color_black, thickness=-1
    )
    cv2.putText(
        img_cp,
        f"  {plate}  ",
        (x_inicio + 5, y_inicio - 5),
        fonte,
        font_size_plate,
        color_white,
        1,
    )
    return img_cp


def desenha_candidatas(imagem, alpr_results):
    img_cp = imagem.copy()
    candidates = alpr_results["candidates"]
    region = alpr_results["region"]
    candidates = [
        {
            "plate": candidate["plate"],
            "confidence": f"{float(candidate['confidence']) * 1:.2f}%",
        }
        for candidate in candidates
    ]

    try:
        altura_box = 0
        largura_box = 0
        offset_text = 0
        for candidate in candidates:
            text = f"10. {candidate['plate']} ({candidate['confidence']})"
            (largura_texto, altura_texto), _ = cv2.getTextSize(
                text, fonte, font_size_plate, 1
            )
            largura_box = max(largura_box, largura_texto)
            altura_box += altura_texto + 10
            offset_text = altura_texto
        x_inicio = 10
        y_inicio = 10
        x_fim = x_inicio + largura_box + 20
        y_fim = altura_box + 20
        cv2.rectangle(
            img_cp, (x_inicio, y_inicio), (x_fim, y_fim), color_black, thickness=-1
        )
        y_offset = y_inicio + 20
        posicao = 0
        for candidate in candidates:
            posicao += 1
            text = f"{posicao}. {candidate['plate']} ({candidate['confidence']})"
            cv2.putText(
                img_cp,
                text,
                (x_inicio + 10, y_offset + 2),
                fonte,
                font_size_plate,
                color_white,
                1,
            )
            y_offset = y_offset + (offset_text + 10)
    except Exception as e:
        logging.error(f"Erro ao desenhar candidatas: {e}")
    return img_cp


def monitorar_comandos():
    global running, comando_var
    while running:
        comando = input("groot_cmd$ running... \n").strip().lower()
        # print('')
        if comando == "sair":
            logging.info("Encerrando o programa...")
            running = False
        elif comando.startswith("set "):
            try:
                _, valor = comando.split(" ", 1)
                comando_var = valor
                logging.info(f"Valor de 'comando_var' alterado para: {comando_var}")
            except ValueError:
                logging.error("Comando inválido. Use: set <valor>")
        else:
            logging.info(f"Comando '{comando}' não reconhecido.")


def liberar_recursos(cap, alpr_instances):
    if cap is not None:
        cap.release()
        logging.info("Conexão RTSP encerrada.")
    for alpr in alpr_instances:
        if alpr is not None:
            alpr.unload()
            logging.info(f"Instância OpenALPR liberada: {alpr.get_default_region()}")
    logging.info("Todos os recursos foram liberados com sucesso.")


def monitorar_threads():
    global threads
    with lock:
        for camera_ip, thread in list(threads.items()):
            if not thread.is_alive():  # Se a thread foi encerrada
                # logging.error(f"CCTV '{camera_ip}' foi encerrada.")
                # threads.pop(camera_ip)  # Remove do dicionário
                # Ação planejada: reiniciar ou apenas registrar
                # reiniciar = input(f"Deseja reiniciar CCTV '{camera_ip}'? (s/n): ")
                # logging.info(f"REINICIAR: {reiniciar}")
                # if reiniciar == "s":
                #     print(f"Reiniciar CCTV '{camera_ip}' Sim")
                #     continue
                # else:
                #     print(f"Reiniciar CCTV '{camera_ip}' Nao")
                continue


def iniciar_thread(camera_ip, porta, usuario, senha):
    global threads
    with lock:
        if camera_ip in threads:
            logging.error(f"CCTV '{camera_ip}' já está ativa.")
        else:
            logging.info(f"Iniciando CCTV '{camera_ip}'...")
            nova_thread = threading.Thread(
                target=t_processar_rtsp_alpr,
                args=(camera_ip, porta, usuario, senha),
                daemon=True,
            )
            threads[camera_ip] = nova_thread
            nova_thread.start()


def t_processar_rtsp_alpr(camera_ip, porta, usuario, senha):
    try:
        rtsp_url, err = obter_rtsp_url(camera_ip, porta, usuario, senha)
        if err is not None:
            logging.error(f"Erro ao obter_rtsp_url '{camera_ip}': {err}")
            exit(1)
        ret, cap = StreamStart(rtsp_url)
        if ret is None:
            logging.info(f"Falha ao obter Stream: {camera_ip}")
            exit(1)
        frame_queue = Queue(maxsize=1)
        threading.Thread(
            target=capture_frames, args=(cap, frame_queue), daemon=True
        ).start()

        alpr_eu = AlprStart("eu")
        alpr_us = AlprStart("us")

        alpr_list = [alpr_eu, alpr_us]

        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()
                frame_cp = adicionar_data_hora(frame.copy())
                comprimir_salvar(f"screenshot/{camera_ip}.jpg", frame_cp, 25)
                np_image = np.array(frame)

                result_set = []
                for alpr_instance in alpr_list:
                    results_alpr = alpr_instance.recognize_ndarray(np_image)
                    results_alpr = extract_results(results_alpr)

                    # cv2.imwrite('plates/X_screenshot.jpg', frame)

                    if results_alpr:
                        result_set.append(results_alpr)

                    if results_alpr:
                        region = results_alpr["region"]
                        plate = results_alpr["plate"]
                        img_plate = desenha_placa(frame.copy(), results_alpr)
                        img_plate = recortar_regiao(img_plate, results_alpr)
                        img_plate = desenha_candidatas(img_plate, results_alpr)
                        img_plate = adicionar_data_hora(img_plate)

                        # cv2.imwrite(f"plates/{plate}_{region}_{camera_ip}.jpg", img_plate)

                        comprimir_salvar(
                            f"plates/{plate}_{region}_{camera_ip}.jpg", img_plate, 25
                        )

                # if result_set:
                # print('----------- >')
                # print(result_set)
                # print('----------- <')

            continue

    except Exception as e:
        print(f"Thread '{camera_ip}' foi encerrada: {e}")
        liberar_recursos(cap, [alpr_eu, alpr_us])


camera_ip = "192.168.7.66"
porta = 80
usuario = "zplate"
senha = "iMo_brc_m79_brsul"

camera_list = [
    {"name": "BALBIO_INT_OLFAR", "host": "192.168.7.56"},
    {"name": "BALBIO_EXT_OLFAR", "host": "192.168.7.57"},
    {"name": "BALBIO_INT_ENERGIR", "host": "192.168.7.58"},
    {"name": "BALBIO_EXT_ENERGIR", "host": "192.168.7.59"},
    {"name": "BALMAT_EXT_SILO", "host": "192.168.7.60"},
    {"name": "BALMAT_INT_TI", "host": "192.168.7.61"},
    {"name": "BALMAT_1", "host": "192.168.7.66"},
    {"name": "BALMAT_INT_TOMBA", "host": "192.168.7.67"},
    {"name": "ALMOX_ENTRADA", "host": "192.168.7.68"},
    {"name": "ALMOX_SAIDA", "host": "192.168.7.69"},
    {"name": "PORTARIA_1", "host": "192.168.7.70"},
    {"name": "PORTARIA_ESTACIONAMENTO", "host": "192.168.7.71"},
    {"name": "FATURISTA_1", "host": "192.168.7.72"},
    {"name": "FATURISTA_2", "host": "192.168.7.73"},
    {"name": "PORTARIA_BIO_ENTRADA", "host": "192.168.7.74"},
    {"name": "PORTARIA_BIO_SAIDA", "host": "192.168.7.75"},
    {"name": "PORTARIA_BIO_VESTUARIO", "host": "192.168.7.76"},
]

if __name__ == "__main__":

    logging.info("I m Groot!")
    threading.Thread(target=monitorar_comandos, daemon=True).start()

    for camera in camera_list:
        iniciar_thread(camera["host"], porta, usuario, senha)
        # time.sleep(1)

    try:
        while running:
            monitorar_threads()
            continue
    except KeyboardInterrupt:
        logging.error("Programa interrompido manualmente.")
    finally:
        logging.info("Programa encerrado.")
