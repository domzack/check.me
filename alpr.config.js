module.exports = {
    apps: [
        {
            name: "192.168.7.56",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.56:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.57",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.57:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.58",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.58:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.59",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.59:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.60",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.60:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.61",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.61:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.66",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.66:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.67",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.67:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.68",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.68:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.69",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.69:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.70",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.70:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.71",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.71:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.72",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.72:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.73",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.73:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.74",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.74:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.75",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.75:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        }, {
            name: "192.168.7.76",
            script: "zplate.py",
            interpreter: "python3",
            args: "rtsp://brtronic:iMo_brc_m79@192.168.7.76:554/Streaming/Channels/101/ --outputstream 'http://127.0.0.1:3031/pyzplate'",
            autorestart: true,  // Reinicia automaticamente se o processo falhar
            restart_delay: 5000, // Aguarda 5 segundos antes de tentar um novo reinício
            watch: false,  // Evita reinícios desnecessários ao alterar arquivos
            max_memory_restart: "500M",  // Reinicia se ultrapassar 500MB de memória
            log_date_format: "YYYY-D-MM HH:mm:ss",  // Define o formato da data nos logs
            time: true,  // Habilita timestamp nos logs
            output: "./logs/out.log",  // Define o arquivo de saída padrão
            error: "./logs/err.log"  // Define o arquivo de erro padrão
        },
    ]
};