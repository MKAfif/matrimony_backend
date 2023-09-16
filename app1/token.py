# from rest_framework_simplejwt.tokens import RefreshToken


# def get_token(user):
#     refresh = RefreshToken.for_user(user)
#     refresh['id'] = user.id

#     return{
#         'refresh' : str(refresh),
#         'access'  : str(refresh.access_token),
#     }


from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user, user_type):

    refresh = RefreshToken.for_user(user)
    if user_type == 'admin':
        refresh['user_type'] = 'admin'
    elif user_type == 'member':
        refresh['user_type'] = 'member'
    else:
        refresh['user_type'] = 'regular'  


    refresh['id'] = user.id

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




# from rest_framework_simplejwt.tokens import RefreshToken

# def get_token(user, user_type):
#     refresh = RefreshToken.for_user(user)

#     if user_type == 'admin':
#         refresh['user_type'] = 'admin'
#         refresh_token_name = 'admintoken'
#     elif user_type == 'member':
#         refresh['user_type'] = 'member'
#         refresh_token_name = 'membertoken'
#     else:
#         refresh['user_type'] = 'regular'
#         refresh_token_name = 'usertoken'

#     refresh['id'] = user.id

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#         'refresh_token_name': refresh_token_name
#     }
