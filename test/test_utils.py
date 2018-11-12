from unittest import TestCase

from src.utils.parser import sanitize_blogpost, sentence_translator


class TestUtilities(TestCase):
    def test_sanitizer(self):
        """
        Ensures that the blog post sanitizer works as intended.
        """
        fake_post = 'Words! Mere words! \n\nHow terrible they were! ' \
                    'How clear\n, and vivid, ~and cruel! \"One could not ' \
                    'escape from them.\n And yet\n what a \'subtle magic there ' \
                    'was in them! They seemed .to be able :to give a plastic ' \
                    'form to\n\n formless things, and. to ;have a music \nof their ' \
                    'own as sweet as that\n of viol or of lute. Mere words! Was ' \
                    'there anything so real as words? Also here\'s a hyphenated-word.'
        expected_word_result = 'words mere words how terrible they were ' \
                               'how clear and vivid and cruel one could not ' \
                               'escape from them and yet what a subtle magic ' \
                               'there was in them they seemed to be able to give ' \
                               'a plastic form to formless things and to have a music ' \
                               'of their own as sweet as that of viol or of lute mere ' \
                               'words was there anything so real as words also heres a hyphenated-word'
        expected_sentence_result = 'words mere words how terrible they were how clear and vivid and cruel ' \
                                   'one could not escape from them and yet what a subtle magic there was in ' \
                                   'them they seemed to be able to give a plastic form to formless things and ' \
                                   'to have a music of their own as sweet as that of viol or of lute mere' \
                                   ' words was there anything so real as words also heres a hyphenated-word'

        self.assertEqual(sanitize_blogpost(fake_post), expected_word_result)
        self.assertEqual(sanitize_blogpost(
            fake_post, sentence_translator), expected_sentence_result)
