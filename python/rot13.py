import webapp2
import cgi

rot_form = """
            <form method='post'>
                ROT 13!
                <br>
                <textarea name="text"
                    rows="10" cols="50">%(input)s</textarea>
                <br>
                <input type="submit">
            </form>
            """

class Rot13(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(rot_form % { 'input' : ''})

    def post(self):
        user_text = self.request.get('text')
        user_text = cypher(user_text)
        self.response.out.write(rot_form % { 'input' : user_text })


def cypher(text):
    for i in range(len(text)):
        if text[i].isalpha():
            text = text[:i] + get_char(text[i]) + text[i+1:]
    return text

def get_char(char):
    val = ord(char) + 13
    if char.islower():
        if val > ord('z'):
            val -= (ord('z') - ord('a') + 1)
    else:
        if val > ord('Z'):
            val -= (ord('Z') - ord('A') + 1)
    return chr(val)
