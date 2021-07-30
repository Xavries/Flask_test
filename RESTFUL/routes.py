from resource import User_details, Post_get_put, User_Login, User_Signup

def initialize_routes(api):
    api.add_resource(User_details, '/users')
    api.add_resource(User_Signup, '/signup')
    api.add_resource(User_Login, '/login')
    api.add_resource(Post_get_put, '/posts')
