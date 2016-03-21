def hash_password(password):
    return password


def render_login_template(handler, wrong_user, wrong_password):
    template = handler.environment.get_template('login.html')
    temp_dict = dict(handler.texts['en'])
    vars = {}
    vars['wrong_user'] = 1 if wrong_user else 0
    vars['wrong_password'] = 1 if wrong_password else 0
    temp_dict['vars'] = vars
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def render_signup_template(handler, user_already_exists, passwords_are_not_same):
    template = handler.environment.get_template('signup.html')
    temp_dict = dict(handler.texts['en'])
    vars = {}
    vars['user_already_exists'] = 1 if user_already_exists else 0
    vars['passwords_are_not_same'] = 1 if passwords_are_not_same else 0
    temp_dict['vars'] = vars
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
