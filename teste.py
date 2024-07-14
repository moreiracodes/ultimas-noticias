from datetime import *

prazo = timedelta(days=2)

agora = datetime.now()

print(f"hoje: {agora}")
print(f"prazo: {prazo}")

calc = agora - prazo

print(f"calc: {calc}")

data_noticia = datetime.fromisoformat('2019-12-04')

print(f"data_noticia: {data_noticia}")

if (data_noticia > calc):
    print(True)
else:
    print(False)
