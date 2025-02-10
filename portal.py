import re
import asyncio
import csv
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError

class Transparencia:
    def __init__(self) -> None:
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.debitos = []
    
    async def playwright_start(self) -> None:
        # Método que Inicializa o playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def playwright_finish(self) -> None:
        # Finaliza a sessão do playwright
        await self.context.close()
        await self.playwright.stop()
        await self.browser.close()

    async def _coleta_gastos(self) -> None:
        # Acesso à página principal
        await self.page.goto("https://portaldatransparencia.gov.br/despesas/lista-consultas")
        await self.page.wait_for_load_state("networkidle")
        await self.page.wait_for_timeout(5000)

        # Seleciona a opção de consulta por classificação contábil
        await self.page.get_by_role("link", name="Classificação Contábil").click()
        await self.page.wait_for_load_state("domcontentloaded")
        await self.page.wait_for_timeout(5000)

        # Seleciona a opção de paginação completa para podemos utilizar a maior parte dos dados da tabela
        await self.page.get_by_role("button", name="Paginação completa").click()
        await self.page.wait_for_timeout(3000)
    
        # Abre a lista de débitos em 50 linhas
        await self.page.locator("select[name=\"lista_length\"]").select_option(value="30")
        await self.page.wait_for_load_state("networkidle")
        
        html = await self.page.content()
        
        # Usando regex para coletar o total de páginas
        total_paginas = re.search(r"Página\s\d\sde\s(.*?)<", html, re.S).group(1)
        total_paginas = total_paginas.replace(".", "")

        for _ in range(1, int(total_paginas)):
            #Utilizando a biblioteca bs4 para organizar o conteúdo em html trazido da página
            soup = BeautifulSoup(html, "html.parser")

            #Ainda com o Beautifulsoup também é possível percorrer os elementos da página
            tabela = soup.find("table", {"id": "lista"}).find("tbody")
            linhas = tabela.find_all("tr")

            # Aqui é feita a varredura de todos os débitos pagina a pagina
            await self._varredura_tabela(linhas)
            try:
                await self.page.get_by_role("button", name="").click()
                await self.page.wait_for_timeout(1500)
            except TimeoutError:
                pass

        await self._salvar_csv()
        await self._estruturar_csv()
       
    async def _varredura_tabela(self, linhas: list) -> list | None:
        #Aqui crio um dicionario para receber os dados da página e os coloco dentro de uma lista
        for linha in linhas[1:]:
            coluna = linha.find_all("td")
            dados = {
                "origem": coluna[2].text,
                "destino": coluna[3].text,
                "mes_ano": coluna[1].text,
                "valor_total": coluna[18].text
            }
            self.debitos.append(dados)
    
    async def _salvar_csv(self) -> None:
        # Cria um arquivo .csv estruturado com as colunas de descricao
        with open('debitos.csv', 'w', encoding='utf-8') as file:
            campos = ['origem', 'destino', 'mes_ano', 'valor_total']
            escritor = csv.DictWriter(file, fieldnames=campos)
            escritor.writeheader()
            for deb in self.debitos:
                escritor.writerow(deb)

    async def _estruturar_csv(self) -> None:
        # Aqui é utilizado o pandas para criar um dataframe e assim inserir os dados coletados
        df = pd.DataFrame(self.debitos)
        print(df)
        df.to_csv('debitos.csv', index=False, encoding='utf-8')

async def main() -> None:
    transparencia = Transparencia()
    await transparencia.playwright_start()
    try:
        await transparencia._coleta_gastos()
    except TimeoutError:
        raise TimeoutError("Não foi possivel fazer a coleta dos dados no momento, tente novamente mais tarde!")
    await transparencia.playwright_finish()

if __name__ == "__main__":
    asyncio.run(main())