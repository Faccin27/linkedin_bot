# LinkedIn Automation

## Descrição
Este projeto é uma ferramenta automatizada para conexões no LinkedIn, utilizando Selenium para interagir com a plataforma. Ele permite realizar login, pesquisar por palavras-chave e enviar solicitações de conexão automaticamente.

## Funcionalidades
- Login automático no LinkedIn
- Pesquisa de perfis com base em um termo definido
- Rolar a página automaticamente para carregar mais resultados
- Enviar solicitações de conexão
- Fechamento automático do navegador ao final da execução

## Requisitos
- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome
- Bibliotecas Python:
  - `selenium`
  - `python-dotenv`

## Instalação
1. Clone o repositório:
   ```sh
   git clone https://github.com/Faccin27/linkedin_bot
   cd linkedin_bot
   ```

2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais:
   ```ini
   LINKEDIN_EMAIL=seuemail@example.com
   LINKEDIN_PASSWORD=suasenha
   ```

4. Execute o script:
   ```sh
   python main.py
   ```

## Uso
- O script irá abrir o LinkedIn, fazer login e iniciar a pesquisa com o termo especificado.
- Ele irá rolar a página e enviar solicitações de conexão automaticamente.
- Caso ocorra algum erro, ele será registrado no log.

## Contribuição
Sinta-se à vontade para contribuir enviando pull requests ou relatando problemas na aba de issues.

## Licença
Este projeto está licenciado sob a MIT License.

