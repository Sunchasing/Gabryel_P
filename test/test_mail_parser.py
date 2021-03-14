import pytest
from src.mail_parser import MailParser


mail_parser = MailParser()


@pytest.mark.parametrize('test_message, test_from, test_to, expected',
                         [(r'inside\r\n\r\n outside', 's', 'e', 'sid'), (r'\r\n\r\n outside13', 'yes', 'no', '  outside13'),
                          (r'\r\n\r\noutside', '12', '0', ' outside'), (r'\r\n\r\noutside', 'o', 'de', 'outsi')])
def test_strip_message(test_message, test_from, test_to, expected):
    assert mail_parser.strip_message(test_message, test_from, test_to) == expected


# @pytest.mark.parametrize('message',
#                          [('Address or Business Name: Anonymous Email Address: jd@yes.con Patient Name: Jane Doe '
#                            'Pickup Date & Time: 19:00 Job Type: Root Canal Return Date & Time: Never Notes: N/A  ')])
# def test_create_client_dictionary(message):
#
#     expected_dict = {'Address or Business Name:': 'Anonymous',
#                      'Email Address:': 'jd@yes.con',
#                      'Patient Name:': 'Jane Doe',
#                      'Pickup Date & Time:': '19:00',
#                      'Job Type:': 'Root Canal',
#                      'Return Date & Time:': 'Never',
#                      'Notes:': 'N/A'}
#     assert mail_parser.create_client_dictionary(message) == expected_dict
