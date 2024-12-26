# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# Данные для двигателя CHPA 1.4 TSI
rpm = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
torque_chpa = [150, 250, 250, 250, 250, 250, 230, 210, 190]  # Примерные значения
speed_chpa = [27.2, 40.8, 54.4, 68.0, 81.6, 95.2, 108.8, 122.4, 136.0]  # Примерные значения

# Данные для двигателя CDAB 1.8 TSI
torque_cdab = [180, 250, 250, 250, 250, 250, 250, 250, 230]  # Примерные значения
speed_cdab = [21.3, 31.9, 42.6, 53.2, 63.9, 74.5, 85.2, 95.8, 106.5]  # Примерные значения

fig, ax1 = plt.subplots(figsize=(10, 6))

# Первая ось Y для крутящего момента
ax1.plot(rpm, torque_chpa, marker='o', linestyle='-', color='b', label='Крутящий момент CHPA')
ax1.plot(rpm, torque_cdab, marker='o', linestyle='--', color='b', label='Крутящий момент CDAB')
ax1.set_xlabel('Обороты (об/мин)')
ax1.set_ylabel('Крутящий момент (Н·м)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Вторая ось Y для скорости
# ax2 = ax1.twinx()
# ax2.plot(rpm, speed_chpa, marker='o', linestyle='-', color='r', label='Скорость CHPA')
# ax2.plot(rpm, speed_cdab, marker='o', linestyle='--', color='r', label='Скорость CDAB')
# ax2.set_ylabel('Скорость (км/ч)', color='r')
# ax2.tick_params(axis='y', labelcolor='r')

# Заголовок и легенда
plt.title('Зависимость крутящего момента и скорости от оборотов двигателя для CHPA и CDAB')
fig.tight_layout()
plt.show()