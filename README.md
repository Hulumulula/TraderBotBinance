# TraderBotBinance
TraderBotBinance - это тестовый бот,  
создающий ордера и выводящий их в консоль.
* Используется версия `Python=3.10`

### Настройка проекта:
Создайте папку под проект и перейдите в неё  
Клонируйте этот git-репозиторий  
```bash
git clone https://github.com/Hulumulula/
```  
Создайте виртуальное окружение и перейдите в него    
Установите пакеты из requierments.txt  
```bash
pip install -r requierments.txt
```  
Создайте рядом с `main.py` файл  
`.env` по подобию `.env-example`  
Перейдите по ссылке `https://testnet.binance.vision/`  
И создайте себе ключи, которые по аналогии нужно добавить  
в файл `.env`

### Запуск проекта:
Для запуска проекта используйте команду:  
```bash
python main.py
```  
Для запуска тестов используйте команду:  
```bash
python -m unittest tests.py
```  
