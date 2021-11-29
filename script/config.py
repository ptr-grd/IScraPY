
# === Описание === #
# Файл конфигурации. Необходим для настройки скрипта.
# Включает в себя два раздела: пользовательский и технический.
# Можно изменять пользовательский, технический - не рекомендуется.

# ===== Раздел 1: Пользовательский ===== #

# Данные для авторизации
USER = "login"
PASSWORD = "password"

# Настройки работы скрипта
BACKGROUND_MODE = False			# Фоновый режим работы (без отображения браузера)
FAKE_USER_AGENT = True			# Режим фейкового юзер-агента

# ===== Раздел 2: Технический ===== #

# Полный путь до драйвера Chrome
path_driver = "C:\\Папка1\\Папка2\\chromedriver.exe"

# Список всех элементов сайта для взаимодействия
elements = {
	'auth_btn': '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button',
	'user_login': '//*[@id="loginForm"]/div/div[1]/div/label/input',
	'user_password': '//*[@id="loginForm"]/div/div[2]/div/label/input',
	'login_link': '//*[@id="loginForm"]/div/div[3]/button',
	'dialog_window': '//*[@id="react-root"]/section/main/div/div/div/div/button',
	'scroll': '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div',
	'load_comm_btn': '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/li/div/button',
	'load_nested_comm_btn': '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/ul[1]/li/ul/li/div/button'
}
