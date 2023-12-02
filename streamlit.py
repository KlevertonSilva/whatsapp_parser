from whatsapp_parser.whats_app_parser import WhatsAppParser
from utils import Utils
import streamlit as st
import tempfile
import os

language = st.sidebar.selectbox('Language', ('English 🇺🇸', 'Português 🇧🇷'))
texts = Utils.read_language_files(language)
uploaded_file = st.sidebar.file_uploader(texts['select_file'], type=["txt"])

if not uploaded_file:
    st.markdown(texts['markdown'])

if uploaded_file is not None:
    # Save the content of the uploaded file to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file_path = temp_file.name
    temp_file.close()

    chat = WhatsAppParser(temp_file_path)

    # Clean up the temporary file
    os.remove(temp_file_path)

    if chat:
        col1, col2 = st.columns(2)

        # Date input for start_date in the first column
        start_date = col1.date_input(texts['start_date'], chat.chat_dataframe['date'].min(), max_value=chat.chat_dataframe['date'].max(),
                                     min_value=chat.chat_dataframe['date'].min()).strftime('%Y-%m-%d')

        # Date input for end_date in the second column
        end_date = col2.date_input(texts['end_date'], chat.chat_dataframe['date'].max(), max_value=chat.chat_dataframe['date'].max(),
                                   min_value=chat.chat_dataframe['date'].min()).strftime('%Y-%m-%d')

        # Button to reset dates in the third column
        if col1.button(texts['reset_date']):
            start_date = chat.chat_dataframe['date'].min().strftime('%Y-%m-%d')
            end_date = chat.chat_dataframe['date'].max().strftime('%Y-%m-%d')

        if start_date > end_date:
            st.warning(texts['date_conflict'], icon="⚠️")
        else:
            fig1 = chat.generate_graph_number_of_messages_per_day(start_date=start_date,
                                                                  end_date=end_date,
                                                                  language=language).update_layout(width=1000)
            st.plotly_chart(fig1, theme="streamlit")

            fig2 = chat.generate_graph_number_of_types_of_messages(start_date=start_date,
                                                                   end_date=end_date,
                                                                   language=language)
            st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

            fig3 = chat.generate_graph_number_of_types_of_messages_per_user(start_date=start_date,
                                                                            end_date=end_date,
                                                                            language=language)
            st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

            fig4 = chat.generate_graph_number_of_messages_per_hour(start_date=start_date,
                                                                   end_date=end_date,
                                                                   language=language)
            st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

            fig5 = chat.generate_number_of_messages_per_user(start_date=start_date,
                                                             end_date=end_date,
                                                             language=language)
            st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

            fig6 = chat.generate_activity_heatmap(start_date=start_date,
                                                  end_date=end_date,
                                                  language=language).update_layout(height=400, width=1000)
            st.plotly_chart(fig6, theme="streamlit")

            # fig7 = chat.generate_word_cloud(save_as_file=False)
            # st.image(fig7)
