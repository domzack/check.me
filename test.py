import cv2
from openalpr import Alpr
import time

# Configuração do OpenALPR
# Substitua 'us' ou 'eu' pela região correta da sua câmera (ex.: 'br' para Brasil)
alpr = Alpr("br", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Erro ao carregar o OpenALPR")
    exit(1)

# Configurações opcionais do OpenALPR (ajuste conforme necessário)
alpr.set_top_n(10)  # Número máximo de resultados por frame
alpr.set_default_region("br")  # Região padrão para placas

# URL do stream RTSP da câmera IP
# Substitua pelo endereço RTSP da sua câmera (ex.: rtsp://usuario:senha@IP:porta/caminho)
rtsp_url = "rtsp://admin:12345@192.168.1.100:554/stream1"

# Conexão com o stream RTSP
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Erro ao conectar ao stream RTSP")
    exit(1)

print("Conectado ao stream RTSP com sucesso!")

# Loop para capturar e processar frames em tempo real
while True:
    ret, frame = cap.read()  # Lê o próximo frame
    if not ret:
        print("Falha ao capturar frame. Tentando reconectar...")
        cap.release()
        cap = cv2.VideoCapture(rtsp_url)  # Tenta reconectar
        time.sleep(1)  # Pequena pausa antes de tentar novamente
        continue

    # Converte o frame para formato que o OpenALPR aceita (JPEG em memória)
    ret, encoded_image = cv2.imencode(".jpg", frame)
    if not ret:
        print("Erro ao codificar o frame")
        continue

    # Processa o frame com OpenALPR
    results = alpr.recognize_array(encoded_image.tobytes())

    # Verifica se há placas detectadas
    if results["results"]:
        for plate in results["results"]:
            plate_number = plate["plate"]
            confidence = plate["confidence"]
            print(f"Placa detectada: {plate_number} - Confiança: {confidence:.2f}%")

            # Opcional: Desenhar um retângulo ao redor da placa no frame
            coordinates = plate["coordinates"]
            x1, y1 = coordinates[0]["x"], coordinates[0]["y"]
            x2, y2 = coordinates[2]["x"], coordinates[2]["y"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{plate_number} ({confidence:.2f}%)", 
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Exibe o frame processado em uma janela
    cv2.imshow("Stream RTSP com OpenALPR", frame)

    # Sai do loop ao pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
alpr.unload()
print("Programa encerrado.")