from whatsapp_parser.whats_app_parser import WhatsAppParser

chat = WhatsAppParser('chats/_chat.txt')
fig = chat.generate_activity_heatmap(save_as_file=True, language='Português 🇧🇷')
# fig = chat.generate_graph_number_of_types_of_messages(save_as_file=True)
# fig = chat.generate_graph_number_of_types_of_messages_per_user(save_as_file=True)
# fig = chat.generate_graph_number_of_messages_per_hour(save_as_file=True)
# fig = chat.generate_word_cloud(save_as_file=True)
# fig = chat.generate_number_of_messages_per_user(save_as_file=True)
# fig = chat.generate_activity_heatmap(save_as_file=True)
fig
