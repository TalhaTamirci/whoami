"""Arena oyun modülleri — bu paketteki her modül otomatik yüklenir.

Bir oyun modülü import edildiğinde @register_game decorator'ı ile
kendini arena.GAME_REGISTRY'ye kaydeder.
"""
import importlib
import pkgutil

for _mod in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{_mod.name}")
