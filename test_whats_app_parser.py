import unittest
from whatsapp_parser.whats_app_parser import WhatsAppParser


class TestWhatsAppParser(unittest.TestCase):

    def test_txt_file_to_list(self):
        whatsapp_parser = WhatsAppParser('chats/_chat_test.txt')
        result = whatsapp_parser._txt_file_to_list('chats/_chat_test.txt')
        expected_result = [
            '[01/01/2000, 01:00:00] User 1: \u200eAs mensagens e as chamadas são protegidas com a criptografia de ponta a ponta e ficam somente entre você e os participantes desta conversa. Nem mesmo o WhatsApp pode ler ou ouvi-las.',
            '[01/01/2000, 02:00:00] User 1: Oi',
            '[01/01/2000, 04:00:00] User 1: Tudo bom?',
            '[01/01/2000, 05:00:00] User 2: Oi',
            '[01/01/2000, 06:00:00] User 2: Tudo otimo, e com você?'
        ]
        self.assertEqual(result, expected_result)

    def test_organize_data_in_dict(self):
        whatsapp_parser = WhatsAppParser('chats/_chat_test.txt')
        result = whatsapp_parser._organize_data_in_dict()
        expected_result = {
            'timestamp':
                ['01/01/2000 02:00:00', '01/01/2000 04:00:00', '01/01/2000 05:00:00', '01/01/2000 06:00:00'],
            'who_sended':
                ['User 1', 'User 1', 'User 2', 'User 2'],
            'message':
                ['Oi', 'Tudo bom?', 'Oi', 'Tudo otimo, e com você?'],
            'message_type':
                ['Text', 'Text', 'Text', 'Text']
        }
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
