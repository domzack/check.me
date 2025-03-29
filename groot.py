import threading
import time
import queue

# Variáveis globais
running = True  # Controla o loop principal
threads = {}  # Dicionário para monitorar threads ativas
lock = threading.Lock()  # Controle de acesso às threads
command_queue = queue.Queue()  # Fila para enviar comandos do monitor ao main


# Monitor de comandos (executado em uma thread separada)
def monitor_comandos():
    global running
    while running:
        comando = input("Digite um comando: ").strip().lower()
        if comando == "sair":
            command_queue.put("sair")  # Envia o comando para a fila
        elif comando.startswith("iniciar "):
            _, nome = comando.split(" ", 1)
            command_queue.put(f"iniciar {nome}")  # Inicia uma nova thread
        elif comando.startswith("parar "):
            _, nome = comando.split(" ", 1)
            command_queue.put(f"parar {nome}")  # Para uma thread específica
        elif comando.startswith("remover "):
            _, nome = comando.split(" ", 1)
            command_queue.put(f"remover {nome}")  # Remove uma thread específica
        elif comando == "listar":
            command_queue.put("listar")  # Lista threads ativas
        else:
            print(f"Comando '{comando}' não reconhecido.")


# Função exemplo para uma thread
def tarefa(nome):
    try:
        while True:
            print(f"Thread '{nome}' está rodando...")
            time.sleep(2)
    except Exception as e:
        print(f"Thread '{nome}' foi encerrada: {e}")


# Monitoramento e gerenciamento de threads no bloco principal
def monitorar_threads():
    global threads
    with lock:
        for nome, thread in list(threads.items()):
            if not thread.is_alive():  # Se a thread foi encerrada
                print(f"Thread '{nome}' foi encerrada.")
                threads.pop(nome)  # Remove do dicionário
                # Ação planejada: reiniciar ou apenas registrar
                reiniciar = (
                    input(f"Deseja reiniciar a thread '{nome}'? (s/n): ")
                    .strip()
                    .lower()
                )
                if reiniciar == "s":
                    iniciar_thread(nome)


# Função para iniciar uma nova thread
def iniciar_thread(nome):
    global threads
    with lock:
        if nome in threads:
            print(f"Thread '{nome}' já está ativa.")
        else:
            print(f"Iniciando thread '{nome}'...")
            nova_thread = threading.Thread(target=tarefa, args=(nome,), daemon=True)
            threads[nome] = nova_thread
            nova_thread.start()


# Função para parar uma thread (simulado por Exception)
def parar_thread(nome):
    global threads
    with lock:
        if nome in threads and threads[nome].is_alive():
            print(f"Parando thread '{nome}'...")
            # Aqui você pode usar algum mecanismo de sinal para encerrar a thread com segurança.
            # Atualmente, a thread será simplesmente marcada como encerrada.
        else:
            print(f"Thread '{nome}' não está ativa.")


# Função para listar threads ativas
def listar_threads():
    global threads
    with lock:
        print("Threads ativas:")
        for nome, thread in threads.items():
            status = "ativo" if thread.is_alive() else "encerrado"
            print(f" - {nome}: {status}")


# Bloco principal
if __name__ == "__main__":
    # Inicia o monitor de comandos em uma thread separada
    threading.Thread(target=monitor_comandos, daemon=True).start()

    try:
        while running:
            # Processa comandos da fila
            while not command_queue.empty():
                comando = command_queue.get()
                if comando == "sair":
                    running = False
                elif comando.startswith("iniciar "):
                    _, nome = comando.split(" ", 1)
                    iniciar_thread(nome)
                elif comando.startswith("parar "):
                    _, nome = comando.split(" ", 1)
                    parar_thread(nome)
                elif comando.startswith("remover "):
                    _, nome = comando.split(" ", 1)
                    parar_thread(nome)
                    with lock:
                        threads.pop(nome, None)
                        print(f"Thread '{nome}' removida.")
                elif comando == "listar":
                    listar_threads()

            # Monitorar threads encerradas
            monitorar_threads()

            # Aguarda brevemente antes de continuar no loop principal
            time.sleep(1)

    except KeyboardInterrupt:
        print("Programa encerrado manualmente.")

    finally:
        print("Encerrando todas as threads...")
        running = False
        time.sleep(2)
