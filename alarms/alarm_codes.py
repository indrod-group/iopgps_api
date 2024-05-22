from django.db import models


class AlarmCodes(models.TextChoices):
    ACCOFF = "ACCOFF", "Parada"
    ACCON = "ACCON", "Inicio"
    OFFLINETIMEOUT = "OFFLINETIMEOUT", "Tiempo de espera sin conexión"
    STAYTIMEOUT = "STAYTIMEOUT", "Tiempo de espera de estancia"
    REMOVE = (
        "REMOVE",
        "Desmontaje, sensor de luz, fallo de alimentación, enchufar y desenchufar",
    )
    LOWVOT = "LOWVOT", "Baja electricidad"
    ERYA = "ERYA", "Segunda carga"
    FENCEIN = "FENCEIN", "Entrar en la cerca"
    FENCEOUT = "FENCEOUT", "Fuera de la cerca"
    SEP = "SEP", "Separado"
    SOS = "SOS", "Alarma SOS"
    OVERSPEED = "OVERSPEED", "Alarma de exceso de velocidad"
    HOME = "HOME", "Residencia permanente anormal (casa)"
    COMPANY = "COMPANY", "Residencia permanente anormal (empresa)"
    CRASH = "CRASH", "Alarma de colisión"
    SHAKE = "SHAKE", "Vibración"
    ACCELERATION = "ACCELERATION", "Aceleración rápida"
    DECELERATION = "DECELERATION", "Desaceleración rápida"
    TURN = "TURN", "Giro brusco"
    FASTACCELERATION = "FASTACCELERATION", "Aceleración máxima"
    SHARPTURN = "SHARPTURN", "Giro brusco"
    TURNOVER = "TURNOVER", "Volcar"
    FASTDECELERATION = "FASTDECELERATION", "Desaceleración rápida"
    REMOVECONTINUOUSLY = (
        "REMOVECONTINUOUSLY",
        "Alarma de desmontaje continuo, alarma de sensor de luz y fallo de alimentación",
    )
    SHIFT = "SHIFT", "Alarma de movimiento"
    AREAOUT = "AREAOUT", "Alarma de salida de área"
    AREAIN = "AREAIN", "Alarma de entrada a área"
    EXTERNALLOWBATTERY = (
        "EXTERNALLOWBATTERY",
        "Alarma de baja tensión de la batería externa",
    )
    XINHAOPINBI = "XINHAOPINBI", "Alarma de bloqueo de señal"
    PSEUDOBASESTATION = "PSEUDOBASESTATION", "Alarma de estación base falsa"
    ONLINE = "ONLINE", "Alarma en línea"
    ABNORMALACCUMULATION = "ABNORMALACCUMULATION", "Alarma de acumulación anormal"
    RISKPLACE = "RISKPLACE", "Alarma de permanencia en lugar de riesgo"
    VINMISMATCH = "VINMISMATCH", "Alarma de coincidencia incorrecta de VIN"
    SHORTMILES = "SHORTMILES", "Alarma de kilometraje ultracorto"
    LONGMILES = "LONGMILES", "Alarma de kilometraje super largo"
    TRAIL = "TRAIL", "Alarma de remolque"
    MULTIPLAYER = "MULTIPLAYER", "Alarma de jugador múltiple"
    OPENCOVER = "OPENCOVER", "Alarma de tapa abierta"
    POWERON = "POWERON", "Alarma de encendido"
    POWEROFF = "POWEROFF", "Alarma de apagado"
    MAGNETISM = "MAGNETISM", "Detección de campos magnéticos"
    BLUETOOTH = "BLUETOOTH", "Bluetooth"
    UNKNOWN = "UNKNOWN", "UNKNOWN"
    DRIVING = "DRIVING", "Conduciendo"
    DRIVING_BY_ME = "DRIVINGBYME", "Conduciendo según yo"
    STOPPED = "STOPPED", "Detenido"
    STOPPED_BY_ME = "STOPPEDBYME", "Detenido según yo"
    AUXILIARY_ACTIVITIES = "AUXILIARYACTIVITIES", "Actividades Auxiliares"
    SLEEPING = "SLEEPING", "Descanso"
    EXCEPTIONAL_CASES = "EXCEPTIONALCASES", "Casos excepcionales"
