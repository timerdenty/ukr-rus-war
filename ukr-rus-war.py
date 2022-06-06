
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt




st.title('Українсько-російська війна. Статистика втрат росії')

st.markdown("""
На основі офіційних джерел Генерального штабу ЗСУ

**Джерело:** [Офіційна сторінка збройних сил України](https://www.zsu.gov.ua/All_news/ua).
""")


columns = ["Дата", "Літаки",  "Гелікоптери", "Танки", "БТРи",
           "Польова артилерія", "РСЗВ", "Паливні цистерни",
           "Безпілотники", "Кораблі", "ППО", "Спецтехніка техника",
           "Балістичні ракети", "Крилаті ракети", "Військові авто"]

df_selected = pd.read_csv('russia_losses_equipment.csv')
df_selected = df_selected.fillna(0)
df_selected["Військові авто"] = df_selected["military auto"] + df_selected["vehicles and fuel tanks"]
df_selected = df_selected.drop("military auto",  axis=1)
df_selected = df_selected.drop("vehicles and fuel tanks",  axis=1)
df_selected = df_selected.drop("day",  axis=1)
df_selected['date'] = pd.to_datetime(df_selected['date'])
# df_selected = df_selected.set_index('date')
df_selected.columns = columns
df_selected = df_selected.astype({"Військові авто":"int",
                                  "Балістичні ракети":"int",
                                  "Спецтехніка техника":"int",
                                  "Крилаті ракети":"int",
                                  "Паливні цистерни":"int"})

columns_selected = columns[1:]
date_selected = df_selected['Дата']

# Sidebar - обираємо вид зброї
selected_pos = st.sidebar.multiselect('Вид зброї', columns_selected, columns_selected)

df_selected_armor = df_selected[selected_pos]

# Опис датафрейму
st.write(
    'Опис даних: ' + str(df_selected_armor.shape[0]) + ' строк та ' + str(df_selected.shape[1]) + ' колонок.')


st.dataframe(df_selected_armor)


def filedownload(df):
    csv = df_selected_armor.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="df_selected_armor.csv">Скачати результат у форматі CSV</a>'
    return href


st.markdown(filedownload(df_selected_armor), unsafe_allow_html=True)



# Plot multiple lines
fig, ax = plt.subplots(figsize=(10, 10 * 0.618))

plt.plot(date_selected, df_selected_armor, marker='', linewidth=1, alpha=0.9)

# Add legend
plt.legend(df_selected_armor)

# Add titles
plt.title("Втрати військової техники росії", fontsize=20)
plt.xlabel("Час")
plt.ylabel("Втрати")

st.set_option('deprecation.showPyplotGlobalUse', False)

# Show the graph
st.pyplot(plt.show())


