# Technical instructions

## Create and activate Python virtual environment
```bash
    python -m venv venv
    .\venv\Scripts\Activate
```
## Activar permisos para inicia el entorno, solo sino lo 
´´´bash
    Set-ExecutionPolicy RemoteSigned
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
´´´
## Install dependencies
Create file *requirements.txt*

```bash
    pip install -r requirements.txt
```

## Run FastAPI

```bash
    uvicorn app.main:app --reload
```

## Run streamlit project

```bash
    streamlit run app.py 
```

# Utilities
## Steps to remove virtual environment
```bash
    deactivate
    rm -rf venv
```

## Steps to remove files uploaded to github with gitignore
```bash
    git rm --cached -r .
```

## Steps to create a new branch 
```bash
    git checkout -b feature/"name of the branch"
```#   F i n a l _ P r o y e c t  
 g i t  
 i n i t  
 g i t  
 a d d  
 - A  
 g i t  
 c o m m i t  
 - m  
 f i r s t   c o m m i t  
 g i t  
 b r a n c h  
 - M  
 m a i n  
 g i t  
 r e m o t e  
 a d d  
 o r i g i n  
 h t t p s : / / g i t h u b . c o m / j u a n p a b l o 1 3 9 9 / F i n a l _ P r o y e c t . g i t  
 g i t  
 p u s h  
 - u  
 o r i g i n  
 m a i n  
 #   F i n a l _ P r o y e c t  
 