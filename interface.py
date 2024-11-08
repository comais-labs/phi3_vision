import streamlit as st
import requests

st.title("Processador de Imagens com API")

# URL da API
API_URL = "http://localhost:8081/processar_imagem/"

def main():
    st.write("Faça upload de uma imagem para extrair dados")

    # Upload da imagem
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["png", "jpg", "jpeg"])
    prompt = st.text_input("Insira o o prompt")

    if uploaded_file is not None:
        # Exibe a imagem carregada
        st.image(uploaded_file, caption='Imagem Carregada', use_column_width=True)
        
        if st.button("Processar Imagem"):
            with st.spinner('Processando...'):
                try:
                    # Envia a imagem para a API
                    files = {'arquivo': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                             }
                    data= {'texto': prompt}

                    response = requests.post(API_URL, files=files, data=data)
                    print('Testando prompt', data['texto'])
                    response.raise_for_status()
                    
                    # Exibe a resposta
                    resposta = response.json()
                    st.success("Processamento concluído!")
                    st.write("**Resposta da API:**")
                    st.html(resposta.get("resposta", "Nenhuma resposta obtida."))
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro na requisição: {e}")
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()