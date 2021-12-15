import asyncio, aiohttp, os, logging, secrets, random, base64
from tasksio import TaskPool


logging.basicConfig(
	level=logging.INFO,
	format='\t\u001b[38;5;87m[\u001b[38;5;231m%(asctime)s\u001b[38;5;87m]\u001b[38;5;231m -> \u001b[38;5;87m%(message)s',
	datefmt=f'%I:%M:%S',
)


class TokenEditor(object):

	def __init__(self, Token = list()):
		self.Tokens = Token
		with open('Data - Libraries/Proxies.txt', encoding='utf-8') as f:
			self.Proxies = [i.strip() for i in f]
		for line in open('Data - Libraries/Tokens.txt'):
			self.Tokens.append(line.replace('\n', ''))
		self.Red = '\u001b[31m'
		self.Cyan = '\u001b[38;5;87m'
		self.Proxy = f'http://{random.choice(self.Proxies)}'
		self.Reset = '\u001b[38;5;231m'
		self.Green = '\u001b[32;1m'
		self.Clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
		self.MenuColor = '\u001b[38;5;87m'
		


	def Banner(self) -> str:
		Banner = f'''{self.MenuColor}
	     ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗    ███████╗██████╗ ██╗████████╗ ██████╗ ██████╗ 
	     ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ██╔════╝██╔══██╗██║╚══██╔══╝██╔═══██╗██╔══██╗
		██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║    █████╗  ██║  ██║██║   ██║   ██║   ██║██████╔╝
		██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║    ██╔══╝  ██║  ██║██║   ██║   ██║   ██║██╔══██╗
		██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║    ███████╗██████╔╝██║   ██║   ╚██████╔╝██║  ██║
		╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝    ╚══════╝╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
	   '''
		return Banner

	def headers(self, Token: str) -> str:
		headers = {
			'Authorization': Token,
			'accept': '*/*',
			'accept-language': 'en-US',
			'connection': 'keep-alive',
			'cookie': f'__cfduid = {secrets.token_hex(43)}; __dcfduid={secrets.token_hex(32)}; locale=en-US',
			'DNT': '1',
			'origin': 'https://discord.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'referer': 'https://discord.com/channels/@me',
			'TE': 'Trailers',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
			'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
		}
		return headers

	async def BioChanger(self, Bio: str, Token: str) -> str:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.patch('https://discord.com/api/v9/users/@me', headers = self.headers(Token), json = {'bio': Bio}, proxy=self.Proxy) as response:
					if response.status in (200, 201, 204, 500):
						logging.info(f'{self.Green}[Success]{self.Reset} Changed bio for {Token[:20]}***************')
					else:
						logging.info(f'{self.Red}[Failed]{self.Reset} Could not change bio for {Token[:20]}************** | {await response.text()}')

		except Exception as exception:
			logging.error(f'{self.Red}[Failed]{self.Reset} There was an error running the {TokenEditor.BioChanger.__name__} function, retrying | {exception}')
			await TokenEditor.BioChanger(self, Bio = Bio, Token = Token)

	async def AvatarChanger(self, Token: str):
		try:
			async with aiohttp.ClientSession() as session:
				payload = base64.b64encode(open('Data - Libraries/Image.png', 'rb').read()).decode('utf-8')
				async with session.patch('https://discord.com/api/v9/users/@me', headers = self.headers(Token), json = {'avatar': f'data:image/png;base64,{payload}'}) as response:
					if response.status in (200, 201, 204, 500):
						logging.info(f'{self.Green}[Success]{self.Reset} Changed avatar for {Token[:20]}***************')
					else:
						logging.info(f'{self.Red}[Failed]{self.Reset} Could not change avatar for {Token[:20]}************** | {await response.text()}')

		except Exception as exception:
			logging.error(f'{self.Red}[Failed]{self.Reset} There was an error running the {TokenEditor.AvatarChanger.__name__} function, retrying | {exception}')
			await TokenEditor.AvatarChanger(self, Token = Token)


	async def ChangePassword(self, Password: str, NewPassword: str, Token: str) -> str:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.patch('https://discord.com/api/v9/users/@me', headers = self.headers(Token), json = {'password': Password, 'new_password': NewPassword,}, proxy = self.Proxy) as response:
					if response.status in (200, 201, 204, 500):
						open('Data - Libraries/NewTokens.txt', 'w').write(f'{(await response.json())["token"]}\n')
						logging.info(f'{self.Green}[Success]{self.Reset} Changed password for {Token[:20]}***************, Saved new token in [NewTokens.txt]')
					else:
						logging.info(f'{self.Red}[Failed]{self.Reset} Could not change password for {Token[:20]}************** | {await response.text()}')

		except Exception as exception:
			logging.error(f'{self.Red}[Failed]{self.Reset} There was an error running the {TokenEditor.ChangePassword.__name__} function, retrying | {exception}')
			await TokenEditor.ChangePassword(self, Password = Password, NewPassword = NewPassword, Token = Token)


	async def ChangeUsername(self, Username: str, Password: str, Token: str) -> str:
		try:
			async with aiohttp.ClientSession() as session:
				async with session.patch('https://discord.com/api/v9/users/@me', headers = self.headers(Token), json = {'username': Username, 'password': Password}, proxy = self.Proxy) as response:
					if response.status in (200, 201, 204, 500):
						logging.info(f'{self.Green}[Success]{self.Reset} Changed username for {Token[:20]}***************')
					else:
						logging.info(f'{self.Red}[Failed]{self.Reset} Could not change username for {Token[:20]}************** | {await response.text()}')

		except Exception as exception:
			logging.error(f'{self.Red}[Failed]{self.Reset} There was an error running the {TokenEditor.ChangeUsername.__name__} function, retrying | {exception}')
			await self.ChangeUsername(self, Username = Username, Password = Password, Token = Token)



	async def ScrapeProxy(self):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all') as response:
					open('Data - Libraries/Proxies.txt', 'w').write(await response.text())
					logging.info(f'{self.Green}[Success]{self.Reset} Scraped proxies.')

		except Exception as exception:
			logging.error(f'{self.Red}[Failed]{self.Reset} There was a error running the {TokenEditor.ScrapeProxy.__name__} function | {exception}')
 
	async def start(self):
		(TokenEditor().Clear(), print(TokenEditor.Banner(self)))
		(
		logging.info(f'{self.Reset}Loaded {len(self.Tokens)} tokens'),
		logging.info(f'{self.Reset}Loaded {len(self.Proxies)} proxies\n\n'),
		logging.info(f'[1] {self.Reset}-> {self.Cyan}Change Tokens Username'),
		logging.info(f'[2] {self.Reset}-> {self.Cyan}Change Tokens Password'),
		logging.info(f'[3] {self.Reset}-> {self.Cyan}Change Tokens Avatar'),
		logging.info(f'[4] {self.Reset}-> {self.Cyan}Change About Me'),
		logging.info(f'[5] {self.Reset}-> {self.Cyan}Scrape Proxies'),
		logging.info(f'[6] {self.Reset}-> {self.Cyan}Info'),
		)
		Selection = input(f'\n\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Selection:{self.Cyan} ')

		if Selection == '1':
			print('\n')
			NewUsername = input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} New Username:{self.Cyan} ')
			CurrentPassword = input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Current Password:{self.Cyan} ')
			Threads = int(input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Threads:{self.Cyan} '))
			async with TaskPool(Threads) as pool:
				for Token in self.Tokens:
					await pool.put(self.ChangeUsername(NewUsername, CurrentPassword, Token))
			(logging.info('Completed the task, returning to menu...'), await asyncio.sleep(2), await TokenEditor().start())
			
		
		elif Selection == '2':
			print('\n')
			CurrentPassword = input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Current Password:{self.Cyan} ')
			NewPassword = input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} New Password:{self.Cyan} ')
			Threads = int(input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Threads:{self.Cyan} '))
			async with TaskPool(Threads) as pool:
				for Token in self.Tokens:
					await pool.put(self.ChangePassword(CurrentPassword, NewPassword, Token))
			(logging.info('Completed the task, returning to menu...'), await asyncio.sleep(2), await TokenEditor().start())

		elif Selection == '3':
			print('\n')
			Threads = int(input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Threads:{self.Cyan} '))
			async with TaskPool(Threads) as pool:
				for Token in self.Tokens:
					await pool.put(self.AvatarChanger(Token)) 
			(logging.info('Completed the task, returning to menu...'), await asyncio.sleep(2), await TokenEditor().start())

		elif Selection == '4':
			print('\n')
			Bio = input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} New AboutMe:{self.Cyan} ')
			Threads = int(input(f'\t{self.Cyan}[{self.Reset}?{self.Cyan}]{self.Reset} Threads:{self.Cyan} '))
			async with TaskPool(Threads) as pool:
				for Token in self.Tokens:
					await pool.put(self.BioChanger(Bio, Token))
			(logging.info('Completed the task, returning to menu...'), await asyncio.sleep(2), await TokenEditor().start())

		elif Selection == '5':
			print('\n')
			await TokenEditor().ScrapeProxy()
			(logging.info('Completed the task, returning to menu...'), await asyncio.sleep(2), await TokenEditor().start())

		elif Selection == '6':
			print('''\n
		This Tool is Developed by both Aced & Scripted.

		Aced: trey'#4184 [918338445515059221] (https://github.com/trey1337)
		Scripted: https://solo.to/scripted
				''')
			(logging.info('Completed the task, returning to menu...'), await asyncio.sleep(2), await TokenEditor().start())

		else:
			(logging.error('Invalid choice - Returning to Menu'), await asyncio.sleep(2), await TokenEditor().start())

if __name__ == '__main__':
	try: asyncio.run(TokenEditor().start())
	except Exception as exception: (logging.error(f'There was a critical error, Could not run the file | {exception}'), input(), exit(0),)
