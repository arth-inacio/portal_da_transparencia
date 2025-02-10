
   <h1 align="center">Fazendo consulta de despesas públicas com o Playwright</h1>
   
   <h2 align="left">Objetivos</h2>
   <ul>
       <li>Esse projeto tem a intenção de apresentar a utilização da biblioteca Playwright de forma simples.</li>
       <li>O script faz a extração de despesas públicas diretamente do site do <a href="https://portaldatransparencia.gov.br/" target="_blank">Portal da Transparência</a> por classificação contábil de forma automatizada, gerando um dataframe e um arquivo .csv com os dados das despesas.</li>
       <li>Projeto utilizado para a apresentação-resumo do artigo no evento SELITEC Internacional.</li>
   </ul>
   
   <h2 align="left">Tecnologias Utilizadas</h2>
   <ul>
       <li>Python 3.10.11</li>
       <li>Playwright (Async) 1.28</li>
       <li>BeautifulSoup4 4.11.1</li>
       <li>Pandas</li>
       <li>As bibliotecas restantes se encontram no arquivo <code>requirements.txt</code> e podem ser instaladas através do comando:<br>
           <code>pip install -r requirements.txt</code>
       </li>
   </ul>
   
   <h2 align="left">Estrutura do Projeto</h2>
   <ul>
       <li><code>portal.py</code>: Script principal que realiza a extração dos dados.</li>
       <li><code>requirements.txt</code>: Lista de dependências do projeto.</li>
       <li><code>saida.PNG</code>: Imagem de exemplo da saída gerada pelo script.</li>
   </ul>
   
   <h2 align="left">Como Executar o Projeto</h2>
   <ol>
       <li><strong>Clonar o repositório:</strong>
           <pre><code>git clone https://github.com/arth-inacio/portal_da_transparencia.git
cd portal_da_transparencia</code></pre>
        </li>
        <li><strong>Instalar as dependências:</strong>
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li><strong>Instalar o Playwright:</strong>
            <pre><code>playwright install</code></pre>
        </li>
        <li><strong>Executar o script:</strong>
            <pre><code>python portal.py</code></pre>
        </li>
    </ol>
    
   <h2 align="left">Personalização</h2>
   <p>Para modificar os parâmetros de extração, como a classificação contábil ou o período das despesas, edite as variáveis correspondentes no início do arquivo <code>portal.py</code>. Certifique-se de que os valores correspondam aos disponíveis no Portal da Transparência.</p>
   <br>
   <p>Para visualizar as interações com a página, mude a flag na função de inicialização do playwright para headless="False".</p>

   <h2 align="left">Contribuição</h2>
   <p>Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias ou correções.</p>
   
   <h2 align="left">Licença</h2>
   <p>Este projeto está licenciado sob a licença MIT. Consulte o arquivo <code>LICENSE</code> para mais informações.</p>
   
   <p>Para mais detalhes, visite o repositório no GitHub: <a href="https://github.com/arth-inacio/portal_da_transparencia" target="_blank">arth-inacio/portal_da_transparencia</a></p>
