
Explicação do projeto de Analise de dados sobre doenças

## Dados

O projeto utiliza o arquivo `DENGBR25.csv` que contém dados de notificações de dengue no Brasil.

**Importante**: O arquivo de dados não está versionado no Git devido ao seu tamanho (430 MB).

Para executar o projeto, você precisa:
1. Baixar o arquivo de dados da fonte oficial
2. Colocar o arquivo na pasta `data/` com o nome `DENGBR25.csv`

## Configuração do Ambiente

### Passo a Passo para Converter Código Python em Notebook

1. **Ative o ambiente virtual (.venv)**
   ```bash
   source .venv/bin/activate
   ```

2. **Instale o jupytext**
   ```bash
   pip install jupytext
   ```

3. **Converta o arquivo Python para Notebook**
   ```bash
   jupytext --to notebook code/analise.py
   ```
   
   Isso criará o arquivo `code/analise.ipynb`

4. **Sincronização automática (opcional)**
   
   Para manter o .py e .ipynb sincronizados automaticamente:
   ```bash
   jupytext --set-formats ipynb,py code/analise.ipynb
   ```
   
   Agora qualquer alteração em um arquivo será refletida no outro!

5. **Abra o notebook no VS Code**
   - O notebook já estará pronto para uso
   - Certifique-se de que o kernel selecionado usa o .venv

### Executar o Projeto

1. Ative o ambiente virtual:
   ```bash
   source .venv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o notebook ou o script Python:
   - **Notebook**: Abra `code/analise.ipynb` no VS Code
   - **Script**: `python code/analise.py`
