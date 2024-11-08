from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
import torch
import psutil
import asyncio
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    text: str
    

# Carrega o modelo e o processador
model_id = "microsoft/Phi-3-vision-128k-instruct"

modelo = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="cuda",
    trust_remote_code=True,
    torch_dtype="auto",
    _attn_implementation='flash_attention_2'
)

processador = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

# Limite de requisições simultâneas
sem = asyncio.Semaphore(2) 

def checar_recursos():
    # Checar memória RAM disponível
    mem = psutil.virtual_memory()
    if mem.available < 500 * 1024 * 1024:  # Menos de 500MB disponíveis
        return False

    # Checar memória GPU disponível
    if torch.cuda.is_available():
        memoria_disponivel, _ = torch.cuda.mem_get_info() # retorna uma tupla com a memória disponível e a memória total em bytes
        if memoria_disponivel < 1000 * 1024 * 1024:  # Menos de 1GB disponíveis
            return False
    else:
        return False  # Se não há GPU disponível, retorna False

    return True


@app.post("/processar_imagem/")
async def processar_imagem(arquivo: UploadFile = File(None), texto: str = Form(None)):   
  
    print('texto--->', texto)
    async with sem:
        if not checar_recursos():
            raise HTTPException(
                status_code=503,
                detail="Recursos insuficientes para processar a requisição no momento. Por favor, tente novamente mais tarde."
            )

        try:
            # Abre a imagem enviada
            imagem = Image.open(arquivo.file).convert("RGB")
            print('valor:', texto)
            

            if not texto: 
                mensagens = [ 
                    {"role": "user", "content": "<|image_1|>\n"}, 
                    {"role": "user", "content": "Please extract only the raw text contained in the provided image,\
                    without adding comments, interpretations, or additional information. "}, 
                    {"role": "user", "content": " traduza para o português Brasil."}, 
                ]
            else:    
                mensagens = [ 
                    {"role": "user", "content": "<|image_1|>\n"}, 
                    {"role": "user", "content": texto}, 
                    {"role": "user", "content": " traduza para o português Brasil."}, 
                ]
            
            prompt = processador.tokenizer.apply_chat_template(
                mensagens,
                tokenize=False,
                add_generation_prompt=True
            )

            entradas = processador(
                prompt,
                images=[imagem],
                return_tensors="pt"
            ).to("cuda:0") 

            argumentos_geracao = { 
                "max_new_tokens": 500, 
                "temperature": 0.0, 
                "do_sample": False, 
            } 

            ids_gerados = modelo.generate(
                **entradas,
                eos_token_id=processador.tokenizer.eos_token_id,
                **argumentos_geracao
            ) 

            # Remove os tokens de entrada 
            ids_gerados = ids_gerados[:, entradas['input_ids'].shape[1]:]
            resposta = processador.batch_decode(
                ids_gerados,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False
            )[0] 
            
            return JSONResponse(content={"resposta": resposta})

        except RuntimeError as e:
            if 'CUDA out of memory' in str(e):
                raise HTTPException(
                    status_code=503,
                    detail="Memória GPU insuficiente para processar a requisição. Por favor, tente novamente mais tarde."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Erro interno do servidor. Por favor, tente novamente mais tarde."
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    