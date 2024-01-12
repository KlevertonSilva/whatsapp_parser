from whatsapp_parser.whats_app_parser import WhatsAppParser
from utils import Utils
from io import BytesIO
import matplotlib.pyplot as plt
import streamlit as st
import tempfile
import os

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

language = st.sidebar.selectbox('Language', ('English 🇺🇸', 'Português 🇧🇷'))
texts = Utils.read_language_files(language)
st.sidebar.markdown(texts['warning'])
uploaded_file = st.sidebar.file_uploader(texts['select_file'], type=["txt"])

if not uploaded_file:
    st.image('wpp_logo.png', width=80)
    st.markdown(texts['markdown'])
    st.info(texts['info'])

if uploaded_file is not None:
    # Save the content of the uploaded file to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file_path = temp_file.name
    temp_file.close()

    chat = WhatsAppParser(temp_file_path)

    # Clean up the temporary file
    os.remove(temp_file_path)

    # File was uploaded
    if chat:
        st.markdown(f"""#### {texts['welcome']['group' if chat.group_chat else 'chat']} \n _{chat._folder_name.split('_')[2] if chat.group_chat else texts['welcome']['and'].join(chat.users)}_""")

        col1, col2 = st.columns(2)

        # Date input for start_date in the first column
        start_date = col1.date_input(texts['start_date'], chat.chat_dataframe['date'].min(), max_value=chat.chat_dataframe['date'].max(),
                                     min_value=chat.chat_dataframe['date'].min()).strftime('%Y-%m-%d')

        # Date input for end_date in the second column
        end_date = col2.date_input(texts['end_date'], chat.chat_dataframe['date'].max(), max_value=chat.chat_dataframe['date'].max(),
                                   min_value=chat.chat_dataframe['date'].min()).strftime('%Y-%m-%d')

        # Displaying dataframe
        df_display = chat.display_dataframe(start_date=start_date,
                                            end_date=end_date,
                                            language=language)
        st.dataframe(df_display.set_index(texts['dataframe_columns']['timestamp']), height=200)

        # Button to reset dates in the third column
        if col1.button(texts['reset_date']):
            start_date = chat.chat_dataframe['date'].min().strftime('%Y-%m-%d')
            end_date = chat.chat_dataframe['date'].max().strftime('%Y-%m-%d')

        if start_date > end_date: st.warning(texts['date_conflict'], icon="⚠️")
        else:
            st.markdown(f"#### {texts['Wordcloud']}")
            plt.imshow(chat.generate_word_cloud(), interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()

            # Activity Heatmap
            fig6 = chat.generate_activity_heatmap(start_date=start_date, end_date=end_date, language=language).update_layout(height=400, width=1000)
            st.plotly_chart(fig6, theme="streamlit")

            # Number of messages per hour
            fig4 = chat.generate_graph_number_of_messages_per_hour(start_date=start_date, end_date=end_date, language=language)
            st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

            # Number of messages per day
            fig1 = chat.generate_graph_number_of_messages_per_day(start_date=start_date, end_date=end_date, language=language).update_layout(width=1000)
            st.plotly_chart(fig1, theme="streamlit")

            # Number from type of messages per user
            fig3 = chat.generate_graph_number_of_types_of_messages_per_user(start_date=start_date, end_date=end_date, language=language)
            st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

            # Number of messages per user
            fig5 = chat.generate_number_of_messages_per_user(start_date=start_date, end_date=end_date, language=language)
            st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

            # Number from type of messages
            fig2 = chat.generate_graph_number_of_types_of_messages(start_date=start_date, end_date=end_date, language=language)
            st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

            # Search word per person
            st.write(texts['count_word_occurrences_by_person']['title'])
            text_search = st.text_input(texts['count_word_occurrences_by_person']['sub_title'], texts['count_word_occurrences_by_person']['default'])
            df = chat.count_word_occurrences_by_person(text_search)
            df.columns = texts['count_word_occurrences_by_person']['columns']
            styler = df.style.bar(subset=texts['count_word_occurrences_by_person']['columns'][1],
                                  align='mid',
                                  color=chat.hex['main_wpp_7'])
            st.write(styler.to_html(), unsafe_allow_html=True)

            # Structure for excel download
            excel_buffer = BytesIO()
            chat.chat_dataframe.to_excel(excel_buffer, index=False, engine='xlsxwriter')
            excel_buffer.seek(0)
            st.sidebar.download_button(
                label=texts['Download_excel_button'],
                data=excel_buffer.read(),
                file_name=chat.excel_file_name,
                key='download_button'
            )
