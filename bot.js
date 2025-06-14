const express = require('express');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const puppeteer = require('puppeteer');
const qrcodeTerminal = require('qrcode-terminal');
const qrImage = require('qrcode');
const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// === CONFIGURAÇÕES ===
const caminhoExcel = './leads fulltimeexperience.xlsx';
const caminhoImagem = './img2.jpg';
const mensagemBase = `{nome}

🌟 Tenho um convite especial pra você 🌟

No dia 18/06 às 19hs, Empresários e Empreendedores estarão reunidos no 2° Fulltime Networking Experience em Caraguatatuba-SP.

Uma noite exclusiva de conexões estratégicas, negócios e crescimento.

Venha fazer parte desse ambiente.

🎯 Vagas limitadas!
Garanta a sua participação gratuita agora mesmo clicando no link abaixo.

🔗 https://fulltimenetworking.com.br/experience

abs.
Cássio Moreira`;

// Função para ler Excel
function lerContatos(caminhoArquivo) {
    if (!fs.existsSync(caminhoArquivo)) {
        console.error("❌ Arquivo Excel não encontrado.");
        process.exit(1);
    }

    const workbook = XLSX.readFile(caminhoArquivo);
    const primeiraPlanilha = workbook.SheetNames[0];
    const dados = XLSX.utils.sheet_to_json(workbook.Sheets[primeiraPlanilha]);

    if (dados.length === 0) {
        console.error("❌ Planilha vazia.");
        process.exit(1);
    }

    return dados;
}

// Função para normalizar telefone
function formatarTelefone(telefoneBruto) {
    let telefone = telefoneBruto.toString().replace(/\D/g, '');

    if (telefone.startsWith('+')) {
        telefone = telefone.replace(/^\+/, '');
    }

    if (telefone.startsWith('55')) {
        telefone = telefone.replace(/^55+/, '55');
    } else if (telefone.startsWith('0')) {
        telefone = telefone.replace(/^0+/, '');
        telefone = '55' + telefone;
    } else if (telefone.length === 11 || telefone.length === 10) {
        telefone = '55' + telefone;
    } else {
        telefone = '55' + telefone;
    }

    return telefone;
}

// === INICIALIZA WHATSAPP ===

const app = express();
app.use(express.json());

let currentQrCode = null;

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        executablePath: puppeteer.executablePath(),
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--no-user-data-dir'
        ]
    }
});

let isReady = false;

client.once('ready', async () => {
    isReady = true;
    console.log('✅ Client is ready!');

    await iniciarEnvio();
});

async function iniciarEnvio() {
    const contatos = lerContatos(caminhoExcel);
    const media = MessageMedia.fromFilePath(caminhoImagem);

    for (const contato of contatos) {
        const nome = contato.Nome;
        const telefone = formatarTelefone(contato.Telefone);
        const mensagem = mensagemBase.replace('{nome}', nome);

        try {
            await client.sendMessage(`${telefone}@c.us`, media, { caption: mensagem });
            console.log(`✅ Mensagem enviada para ${nome} - ${telefone}`);
        } catch (err) {
            console.error(`❌ Erro ao enviar para ${nome}: ${err}`);
        }

        await esperar(3000);
    }

    console.log("🚀 Todos os envios foram concluídos.");

    perguntarReenvio();
}

// Função que pergunta se deseja reenviar
function perguntarReenvio() {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question('Deseja reenviar para todos novamente? (s/n): ', async (resposta) => {
        rl.close();

        if (resposta.toLowerCase() === 's') {
            console.log('🔄 Reenviando para todos...');
            await iniciarEnvio();
        } else {
            console.log('✅ Processo finalizado.');
            process.exit(0);
        }
    });
}

// QR Code no terminal
client.on('qr', (qr) => {
    currentQrCode = qr;
    console.log('📲 QR RECEIVED');
    qrcodeTerminal.generate(qr, { small: true });
});

// Evento de autenticação
client.on('authenticated', () => {
    console.log('🔐 Client authenticated');
    currentQrCode = null;
});

// Evento de desconexão
client.on('disconnected', (reason) => {
    console.warn('⚠️ Client disconnected:', reason);
    isReady = false;
});

client.initialize();

// Exibe o QR Code via navegador
app.get('/qrcode', async (req, res) => {
    if (!currentQrCode) {
        return res.send('QR Code ainda não gerado ou já expirado. Aguarde ou reinicie a conexão.');
    }

    try {
        const qrDataURL = await qrImage.toDataURL(currentQrCode);
        res.send(`
            <html>
                <head><title>QR Code WhatsApp</title></head>
                <body style="text-align: center; font-family: sans-serif;">
                    <h2>Escaneie o QR Code abaixo para conectar ao WhatsApp</h2>
                    <img src="${qrDataURL}" alt="QR Code" />
                    <p style="margin-top: 20px; color: gray;">Atualize esta página se o QR expirar.</p>
                </body>
            </html>
        `);
    } catch (error) {
        res.status(500).send('Erro ao gerar o QR Code.');
    }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`🚀 Bot rodando na porta ${PORT}`));

// Função delay
function esperar(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
