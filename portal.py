import asyncio
from bs4 import BeautifulSoup
from playwright_stealth import stealth_async
from playwright.async_api import async_playwright

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
        self.browser = await self.playwright.firefox.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        await stealth_async(self.page)

    async def playwright_finish(self) -> None:
        # Finaliza a sessão do playwright
        await self.context.close()
        await self.playwright.stop()
        await self.browser.close()

    async def _coleta_gastos(self) -> list | None:
        # Acesso à página principal
        await self.page.goto("https://www.portaltransparencia.gov.br/")
        await self.page.wait_for_timeout(5000)

        # Clicando no botão Despesas e Receitas
        await self.page.locator("button[id=\"despesas-card\"]").click()
        await self.page.wait_for_timeout(3000)

        #Exemplo de função javascript (Acesso ao botao "consultar")
        await self.page.evaluate('document.querySelector("#despesas-links > li:nth-child(2) > a").click()')
        await self.page.wait_for_timeout(3000)

        await self.page.get_by_role("link", name="Pela classificação contábil da despesa").click()
        await self.page.wait_for_timeout(3000)

        # Abre a lista de débitos em 50 linhas
        await self.page.locator("select[name=\"lista_length\"]").select_option(value="50")
        html = await self.page.content()

        #Utilizando a biblioteca bs4 para organizar o conteúdo em html trazido da página
        soup = BeautifulSoup(html, "html.parser")

        #Ainda com o Beautifulsoup também é possível percorrer os elementos da página
        div = soup.find("div", {"class":"dataTables_wrapper form-inline dt-bootstrap no-footer"})
        tabela = div.find("table", {"class":"dataTable no-footer"}).find("tbody")
        linhas = tabela.find_all("tr")

        await self._varredura_tabela(linhas)
    
    async def _varredura_tabela(self, linhas: list) -> list | None:
        #Aqui crio um dicionario para receber os dados da página e os coloco dentro de uma lista
        for linha in linhas[1:]:
            coluna = linha.find_all("td")
            dados = {
                "origem": coluna[2].text,
                "destino": coluna[3].text,
                "mes_ano": coluna[1].text,
                "valor_total": coluna[17].text
            }
            self.debitos.append(dados)
       
        return print(self.debitos)
    
async def main() -> None:
    transparencia = Transparencia()
    await transparencia.playwright_start()
    await transparencia._coleta_gastos()
    await transparencia.playwright_finish()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
