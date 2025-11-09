import pandas as pd
import numpy as np

n = 250

firearms = ['9mm Pistol', 'Revolver', 'Hunting Rifle', 'Bow', 'Shotgun', 'Shorty', 'El Diablo', 'Flamethrower', 'Ninguna']
craftables = ['Health Kit', 'Molotov Cocktail', 'Nail Bomb', 'Shiv', 'Smoke Bomb', 'Ninguno']
melee = ['2x4', 'Baseball Bat', 'Hatchet', 'Lead Pipe', 'Machete', 'Switchblade', 'Ninguna']

# Facciones (inmune es raro)
facciones = ['Firefly', 'Civil', 'Cazador', 'Militar', 'Inmune']
probs_facciones = [0.25, 0.35, 0.2, 0.19, 0.01]

data = {
    'Edad': np.random.randint(15, 60, n),
    'Genero': np.random.choice(['Masculino', 'Femenino'], n),
    'Faccion': np.random.choice(facciones, p=probs_facciones, size=n),
    'ExperienciaCombate': np.random.randint(1, 11, n),
    'HabilidadSigilo': np.random.randint(1, 11, n),
    'Salud': np.random.randint(30, 101, n),
    'ArmaFuego': np.random.choice(firearms, n),
    'ArmaCuerpoCuerpo': np.random.choice(melee, n),
    'ItemCreable': np.random.choice(craftables, n),
    'NivelInfeccionZona': np.random.randint(0, 11, n),
    'CondicionesClimaticas': np.random.choice(['Seco', 'Húmedo', 'Lluvioso'], n),
    'NivelEstrés': np.random.randint(0, 11, n),
    'TieneCompañero': np.random.choice([0, 1], n)
}

df = pd.DataFrame(data)

def calcular_supervivencia_realista(row):
    # Factores base (normalizados a 0-1)
    salud_score = row['Salud'] / 100
    sigilo_score = row['HabilidadSigilo'] / 10
    combate_score = row['ExperienciaCombate'] / 10
    estres_score = 1 - (row['NivelEstrés'] / 10)  # menos estrés = mejor
    companero_score = 1 if row['TieneCompañero'] == 1 else 0
    armas_score = 0
    if row['ArmaFuego'] != 'Ninguna': armas_score += 0.5
    if row['ArmaCuerpoCuerpo'] != 'Ninguna': armas_score += 0.5

    # Zona de infección
    zona = row['NivelInfeccionZona']
    if zona <= 2:
        zona_mod = 1.2  # zona segura
    elif zona <= 5:
        zona_mod = 1.0  # neutral
    elif zona <= 8:
        zona_mod = 0.8  # peligrosa
    else:
        zona_mod = 0.6  # infestada

    # Facción Inmune: ignora parte del efecto negativo de la zona
    if row['Faccion'] == 'Inmune':
        zona_mod = min(zona_mod + 0.3, 1.2)  # beneficio extra

    # Ponderaciones
    score = (
        salud_score * 25 +
        sigilo_score * 15 +
        combate_score * 15 +
        armas_score * 10 +
        estres_score * 10 +
        companero_score * 5
    ) * zona_mod

    # Límite de 100
    if score > 100:
        score = 100

    # Convertir en etiqueta binaria
    return 1 if score >= 50 else 0

df['Superviviente'] = df.apply(calcular_supervivencia_realista, axis=1)
df.head(20)