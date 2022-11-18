import asyncio
from bs4 import BeautifulSoup
from playwright_stealth import stealth_async
from playwright.async_api import Playwright, async_playwright


async def run(playwright: Playwright) -> None:

    #Inicializa o playwright
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    #Utilizando a biblioteca playwright_stealth acessar a pagina em modo anonimo
    await stealth_async(page)

    await page.goto("https://www.portaltransparencia.gov.br/")

    await page.locator('button >> nth=6').click()
    await page.wait_for_timeout(3000)

    #Exemplo de função javascript (Acesso ao botao "consultar")
    await page.evaluate('document.querySelector("#despesas-links > li:nth-child(2) > a").click()')
    await page.wait_for_timeout(3000)

    await page.get_by_role("link", name="Pela classificação contábil da despesa").click()
    await page.wait_for_timeout(3000)

    html = await page.content()

    #Utilizando a biblioteca bs4 para organizar o conteúdo em html trazido da página
    soup = BeautifulSoup(html, "html.parser")

    #Ainda com o Beautifulsoup também é possível percorrer os elementos da página
    div = soup.find("div", {"class":"dataTables_wrapper form-inline dt-bootstrap no-footer"})
    tabela = div.find("table", {"class":"dataTable no-footer"}).find("tbody")
    linhas = tabela.find_all("tr")
    linhas.pop(0)

    lista_dados = []

    #Aqui crio um dicionario para receber os dados da página e os coloco dentro de uma lista
    for linha in linhas:
        td = linha.find_all("td")
        dados = {
            "origem": td[2].text,
            "destino": td[3].text,
            "mes/ano": td[1].text,
            "valor_total": td[17].text
        }
        print(dados)
        lista_dados.append(dados)
    
   
    #Finaliza a sessão do playwright
    await context.close()
    await browser.close()

    return lista_dados


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
