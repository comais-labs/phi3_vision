# Sistema de Processamento de Imagens e Texto com Modelo Multimodal Phi-3

Este repositório contém um sistema que processa imagens e texto utilizando o modelo multimodal **Phi-3** da Microsoft. O sistema é dividido em dois componentes principais:

- **Backend**: Uma API implementada em **FastAPI** para realizar o processamento de imagens e texto.
- **Frontend**: Uma interface gráfica desenvolvida em **Streamlit** para interação com o usuário.

---

## Estrutura do Repositório

```
.
├── interface.py           # Arquivo para rodar a interface gráfica (Streamlit)
├── main.py                # Arquivo que implementa a API (FastAPI)
├── README.md              # Documentação do projeto
└── requirements.txt       # Dependências do projeto
```

---

## Requisitos

### Instalações Necessárias

1. **Python 3.8+**
2. Instale as dependências com:
   ```bash
   pip install -r requirements.txt
   ```

   Principais pacotes:
   - **FastAPI**: Framework para a API backend.
   - **Streamlit**: Framework para a interface gráfica.
   - **Transformers**: Para carregar o modelo Phi-3.
   - **Pillow**: Para manipulação de imagens.
   - **Requests**: Para comunicação entre o frontend e a API.
   - **Psutil**: Para monitoramento de recursos do sistema.
   - **uvicorn**: Para rodar aplicações web escritas com frameworks como FastAPI

---

## Configuração do Sistema

### Backend (API)
1. Certifique-se de que a porta 8081 está disponível no seu sistema.
2. Inicie a API executando:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8081
   ```

   O servidor FastAPI será iniciado em `http://localhost:8081`.

### Frontend (Interface)
1. Certifique-se de que o backend está rodando antes de iniciar o frontend.
2. Inicie a interface executando:
   ```bash
   streamlit run interface.py
   ```

   A interface será iniciada no navegador padrão em `http://localhost:8501`.

---

## Funcionamento do Sistema

### Backend (API)
O arquivo `main.py` implementa uma API para:
- Processar imagens enviadas pelo frontend.
- Extrair texto da imagem com base em prompts fornecidos.
- Traduzir o texto extraído para português.

#### Endpoints

- **POST `/processar_imagem/`**
  - Recebe uma imagem e um texto opcional como prompt.
  - Retorna o texto processado e traduzido.

### Frontend (Interface)
O arquivo `interface.py` implementa uma interface gráfica para:
- Fazer upload de imagens.
- Fornecer um prompt opcional para direcionar o processamento.
- Enviar os dados para a API e exibir o resultado na tela.

---

## Exemplos de Uso

### Prompt Padrão

Caso nenhum prompt seja fornecido, o sistema extrai o texto da imagem e traduz para o português.

### Prompt Personalizado

Insira prompts como:
- `"Extraia o texto e forneça um resumo."`
- `"Traduza o texto para espanhol e resuma-o."`

### Fluxo de Trabalho

1. Faça upload de uma imagem através da interface.
2. Insira um prompt (opcional).
3. Clique no botão "Processar Imagem".
4. Visualize o texto processado e traduzido.

---

## Tratamento de Erros

- **Erro de Requisição**: Caso a API não esteja disponível, a interface exibirá uma mensagem apropriada.
- **Erro de Memória**: O backend verifica a disponibilidade de memória RAM e GPU antes de processar a requisição.

---

## Estrutura do Projeto

```
.
├── interface.py           # Frontend em Streamlit
├── main.py                # Backend em FastAPI
├── README.md              # Documentação do projeto
```

---

## Observações

- Atualize o arquivo `interface.py` caso o backend rode em uma URL ou porta diferente:
  ```python
  API_URL = "http://<seu_endereco>:<sua_porta>/processar_imagem/"
  ```
- O sistema é otimizado para GPUs com suporte CUDA. Caso contrário, ele utilizará a CPU, mas pode haver impacto no desempenho.

---

## Referências

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Modelo Phi-3 Vision - Microsoft](https://huggingface.co/microsoft/Phi-3-vision-128k-instruct)
