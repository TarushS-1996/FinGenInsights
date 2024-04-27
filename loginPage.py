import streamlit as st
import json
from streamlit_option_menu import option_menu

default_users = {
    'admin': 'admin'
}

loginStatus = False

def loginpage():
    global loginStatus  # Declare loginStatus as a global variable
    
    if not loginStatus:  # Check if the user is not logged in
        with st.container():
            selected = option_menu(menu_title=None, options=['Login', 'Sign up'],
                                   icons=['chat-left-text-fill', 'lightbulb-fill'],
                                   orientation='horizontal', key="login_option_menu")

        if selected == 'Login':
            st.title('Login Page')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            if st.button('Login'):
                if username in default_users and password == default_users[username]:
                    st.success('Logged in')
                    loginStatus = True
                else:
                    st.error('Invalid username or password')
                    loginStatus = False

                return loginStatus

        elif selected == 'Sign up':
            st.title('Sign Up Page')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            if st.button('Sign up'):
                default_users[username] = password
                with open('users.json', 'w') as f:
                    json.dump(default_users, f)
                st.success('Account created successfully')
    else:
        st.success('You are already logged in')

    return loginStatus
            
    
if __name__ == '__main__':
    loginpage()