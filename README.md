# Markdown PDF Django

Este projeto é uma aplicação Django que permite converter arquivos Markdown em PDFs formatados para trabalhos acadêmicos, utilizando um conversor customizado com suporte a CSS e fórmulas matemáticas.

## Funcionalidades

- Upload de arquivos Markdown (.md) via formulário web
- Conversão automática para PDF com estilo ABNT (ou customizável via CSS)
- Download imediato do PDF gerado
- Suporte a fórmulas matemáticas (MathJax)

## Estrutura do Projeto

```bash
apps/
  converter/
    backend/
      conversor.py   # Função principal de conversão
    templates/
      converter/
        upload.html  # Formulário de upload
    views.py         # View para upload/conversão
    urls.py          # Rotas do app
core/
  settings.py        # Configurações do Django
  urls.py            # Rotas principais do projeto
manage.py            # Utilitário Django
Makefile             # Comando para rodar o servidor
```

## Como executar

1. **Clone o repositório e acesse a pasta:**

   ```bash
   git clone <repo-url>
   cd markdown-pdf-django
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   # ou, se usar pyproject.toml:
   pip install -e .
   ```

4. **Aplique as migrações do Django:**

   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor na porta 8081:**

   ```bash
   make start
   # ou
   python manage.py runserver 0.0.0.0:8081
   ```

6. **Acesse a aplicação:**
   Abra o navegador em [http://localhost:8081/converter/](http://localhost:8081/converter/)

7. **Utilize:**
   - Faça upload de um arquivo Markdown (e opcionalmente um CSS)
   - Baixe o PDF gerado

## Observações

- O projeto está em modo de desenvolvimento (`DEBUG=True`). Não use em produção sem ajustes de segurança.
- O CSS padrão segue o estilo ABNT, mas pode ser customizado.
- Para fórmulas matemáticas, use sintaxe LaTeX no Markdown.

## Licença

MIT
